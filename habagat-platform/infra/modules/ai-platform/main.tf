resource "azurerm_resource_group" "ai" {
  name     = "rg-${var.tenant_id}-ai"
  location = var.region
}

# One Foundry hub + project per tenant, never shared (Doc 32 §2.1).
resource "azurerm_ai_foundry" "hub" {
  name                = "aif-${var.tenant_id}"
  resource_group_name = azurerm_resource_group.ai.name
  location            = var.region
  public_network_access = "Disabled" # Doc 32 §2.1's deny-public-endpoints rule
}

resource "azurerm_ai_foundry_project" "main" {
  name             = "aifp-${var.tenant_id}"
  ai_foundry_id    = azurerm_ai_foundry.hub.id
  location         = var.region
}

# Model deployments — one per required tier, sized from the UNION computed
# in infra/tenant/registry_lookup.tf, never a fixed list. A tenant running
# only small-tier blueprints gets zero frontier-tier spend; adding a
# frontier-needing blueprint later adds exactly this one resource on the
# next `terraform apply` via `for_each`, with no module code change.
resource "azurerm_ai_foundry_model_deployment" "tier" {
  for_each             = toset(var.model_tiers)
  name                 = "model-${each.value}"
  ai_foundry_project_id = azurerm_ai_foundry_project.main.id
  model_tier           = each.value
}

# Doc 32 §2.1: per-tenant service, per-use-case indexes — provisioned once
# per tenant iff ANY enabled agent needs it (Doc 60 §5.3.2's
# local.needs_search), never once per agent.
resource "azurerm_search_service" "grounding" {
  count                          = var.deploy_search ? 1 : 0
  name                           = "srch-${var.tenant_id}"
  resource_group_name            = azurerm_resource_group.ai.name
  location                       = var.region
  sku                            = "standard"
  public_network_access_enabled  = false
}

resource "azurerm_cognitive_account" "document_intelligence" {
  count               = var.deploy_document_intel ? 1 : 0
  name                = "di-${var.tenant_id}"
  resource_group_name = azurerm_resource_group.ai.name
  location            = var.region
  kind                = "FormRecognizer"
  sku_name            = "S0"
  public_network_access_enabled = false
}

# Content Safety is always provisioned per tenant (Doc 32 §2.1 — input/
# output filtering applies to every agent unconditionally, unlike Search
# or Document Intelligence which are agent-driven).
resource "azurerm_cognitive_account" "content_safety" {
  name                = "cs-${var.tenant_id}"
  resource_group_name = azurerm_resource_group.ai.name
  location            = var.region
  kind                = "ContentSafety"
  sku_name            = "S0"
  public_network_access_enabled = false
}

output "id" {
  value = azurerm_ai_foundry_project.main.id
}

output "content_safety_endpoint" {
  value = azurerm_cognitive_account.content_safety.endpoint
}
