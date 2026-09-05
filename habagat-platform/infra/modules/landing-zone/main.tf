# Doc 32 §2 landing zone topology: rg-<c>-network + rg-<c>-platform.
#
# Design rule enforced here (Doc 32 §2.1's closing paragraph): "no public
# endpoints on any data-plane service" — Key Vault below has
# public_network_access_enabled = false and is checked additionally by the
# deny-effect Azure Policy assignment in policy.tf, so a future edit that
# forgets this flag is still blocked at the policy layer, not just by this
# one resource's config (the same belt-and-braces pattern harness/verifier.py
# uses at the code layer).

resource "azurerm_resource_group" "network" {
  name     = "rg-${var.tenant_id}-network"
  location = var.region
}

resource "azurerm_resource_group" "platform" {
  name     = "rg-${var.tenant_id}-platform"
  location = var.region
}

resource "azurerm_virtual_network" "main" {
  name                = "vnet-${var.tenant_id}"
  resource_group_name = azurerm_resource_group.network.name
  location            = var.region
  address_space       = ["10.0.0.0/16"]
}

# One subnet per resource group's private-endpoint surface (Doc 32 §2's
# RGA/RGD/RGC/RGP each get private link into this VNet).
resource "azurerm_subnet" "ai" {
  name                 = "snet-ai"
  resource_group_name  = azurerm_resource_group.network.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "data" {
  name                 = "snet-data"
  resource_group_name  = azurerm_resource_group.network.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_subnet" "compute" {
  name                 = "snet-compute"
  resource_group_name  = azurerm_resource_group.network.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.3.0/24"]
}

resource "azurerm_private_dns_zone" "core" {
  for_each            = toset(["privatelink.vaultcore.azure.net", "privatelink.blob.core.windows.net", "privatelink.documents.azure.com"])
  name                = each.value
  resource_group_name = azurerm_resource_group.network.name
}

# Doc 32 §2.1's outbound-allowlist rule.
resource "azurerm_firewall" "egress" {
  name                = "fw-${var.tenant_id}"
  resource_group_name = azurerm_resource_group.network.name
  location            = var.region
  sku_name            = "AZFW_VNet"
  sku_tier            = "Standard"
}

# Doc 32 §2.1: HSM-backed Key Vault, purge protection on, per-tenant, never
# shared — holds connector secrets and the CMK the data module references.
resource "azurerm_key_vault" "main" {
  name                            = "kv-${substr(var.tenant_id, 0, 17)}" # Key Vault name length limit
  resource_group_name             = azurerm_resource_group.platform.name
  location                        = var.region
  sku_name                        = "premium" # HSM-backed
  purge_protection_enabled        = true
  public_network_access_enabled   = false
  enable_rbac_authorization       = true
}

resource "azurerm_key_vault_key" "cmk" {
  name         = "cmk-${var.tenant_id}"
  key_vault_id = azurerm_key_vault.main.id
  key_type     = "RSA-HSM"
  key_size     = 3072
  key_opts     = ["decrypt", "encrypt", "wrapKey", "unwrapKey"]
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = "law-${var.tenant_id}"
  resource_group_name = azurerm_resource_group.platform.name
  location            = var.region
  retention_in_days   = 90 # Doc 32 §2.1 "retained per customer policy" — 90 is the platform default
}

resource "azurerm_user_assigned_identity" "harness" {
  name                = "id-${var.tenant_id}-harness"
  resource_group_name = azurerm_resource_group.platform.name
  location            = var.region
}

output "vnet_id" {
  value = azurerm_virtual_network.main.id
}

output "subnet_ids" {
  value = {
    ai      = azurerm_subnet.ai.id
    data    = azurerm_subnet.data.id
    compute = azurerm_subnet.compute.id
  }
}

output "cmk_key_id" {
  value = azurerm_key_vault_key.cmk.id
}

output "key_vault_id" {
  value = azurerm_key_vault.main.id
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.main.id
}

output "harness_identity_id" {
  value = azurerm_user_assigned_identity.harness.id
}
