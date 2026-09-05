resource "azurerm_resource_group" "data" {
  name     = "rg-${var.tenant_id}-data"
  location = data.azurerm_resource_group.landing_zone_region.location
}

# Region is inherited implicitly by referencing the VNet's own resource
# group location rather than re-declaring a region variable here — keeps
# this module's surface minimal per Doc 60 §5.3.1's "config, not code" rule.
data "azurerm_resource_group" "landing_zone_region" {
  name = "rg-${var.tenant_id}-network"
}

resource "azurerm_storage_account" "documents" {
  name                            = "st${replace(var.tenant_id, "-", "")}"
  resource_group_name             = azurerm_resource_group.data.name
  location                        = azurerm_resource_group.data.location
  account_tier                    = "Standard"
  account_replication_type        = "ZRS"
  is_hns_enabled                  = true # ADLS Gen2
  public_network_access_enabled   = false

  customer_managed_key {
    key_vault_key_id = var.cmk
  }
}

# Doc 52 §3.1/§3.2: Run state, checkpoints, memory — per-tenant Cosmos
# account. See MIGRATION_RUNBOOK.md in this module directory for the
# runbook Doc 59 ADR-12 flags as a prerequisite before production data
# accumulates (Doc 60 §7 item 3 — authored here, not deferred further).
resource "azurerm_cosmosdb_account" "run_state" {
  name                          = "cosmos-${var.tenant_id}"
  resource_group_name           = azurerm_resource_group.data.name
  location                      = azurerm_resource_group.data.location
  offer_type                    = "Standard"
  kind                          = "GlobalDocumentDB"
  public_network_access_enabled = false

  consistency_policy {
    consistency_level = "Session" # Doc 52 §2's per-run consistency needs, not strong global consistency
  }

  geo_location {
    location          = azurerm_resource_group.data.location
    failover_priority = 0
  }
}

resource "azurerm_mssql_server" "reporting" {
  name                         = "sql-${var.tenant_id}"
  resource_group_name          = azurerm_resource_group.data.name
  location                     = azurerm_resource_group.data.location
  version                      = "12.0"
  public_network_access_enabled = false
}

resource "azurerm_mssql_database" "reporting" {
  name      = "db-${var.tenant_id}-reporting"
  server_id = azurerm_mssql_server.reporting.id
  sku_name  = "S1"
}

output "storage_account_id" {
  value = azurerm_storage_account.documents.id
}

output "cosmos_account_id" {
  value = azurerm_cosmosdb_account.run_state.id
}

output "sql_database_id" {
  value = azurerm_mssql_database.reporting.id
}
