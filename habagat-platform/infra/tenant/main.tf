terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.90" }
    http    = { source = "hashicorp/http", version = "~> 3.4" }
    null    = { source = "hashicorp/null", version = "~> 3.2" }
  }

  # Doc 32 §3.1: "State in a Habagat-controlled backend with per-tenant
  # isolation and locking." One state file per tenant, never shared —
  # backend config is supplied per-tenant at `terraform init` time
  # (-backend-config), not hardcoded here, since the key itself must vary
  # by tenant_id.
  backend "azurerm" {}
}

provider "azurerm" {
  features {}
}

module "landing_zone" {
  source              = "../modules/landing-zone" # Doc 32 §2.1: network, KV, identities, Log Analytics
  tenant_id           = var.tenant_id
  region              = var.primary_region
  compliance_profile  = var.compliance_profile
}

module "ai_platform" {
  source                  = "../modules/ai-platform" # Doc 32 §2.1: Foundry hub+project, model deployments
  tenant_id               = var.tenant_id
  region                  = var.primary_region
  model_tiers             = local.required_model_tiers # NOT hardcoded — derived in registry_lookup.tf
  deploy_search           = local.needs_search
  deploy_document_intel   = local.needs_document_intel
  vnet_id                 = module.landing_zone.vnet_id
}

module "data" {
  source     = "../modules/data" # Doc 32 §2.1: Cosmos, Storage, SQL — SHARED, not per-agent
  tenant_id  = var.tenant_id
  vnet_id    = module.landing_zone.vnet_id
  cmk        = module.landing_zone.cmk_key_id
}

module "harness" {
  source              = "../modules/harness" # Doc 51 §1.2: ONE Container Apps deployment
  tenant_id           = var.tenant_id
  ai_platform         = module.ai_platform
  data                = module.data
  connector_types     = local.required_connectors    # Tool Gateway loads only what's actually needed
  deploy_approval_ui  = local.needs_r3_approval_flow  # Doc 56 §2 — only provision the review queue's
                                                       # backing resources if an enabled agent can reach R3
}

# The agent-instance module is the ONLY thing that varies in COUNT with
# enabled_agents. It does NOT provision new infrastructure per agent — it
# writes the AgentInstance record (Doc 52 §1.2) into the already-provisioned
# Fleet Manager / Harness config, and configures the tenant-scoped bindings
# (which tools this agent may use, its starting autonomy, its policy
# overrides). This is the concrete Terraform expression of Doc 30 §4.2's
# "tenant binding may contain configuration... never prompts, code, or tool
# definitions."
module "agent_instance" {
  source   = "../modules/agent-instance"
  for_each = { for a in var.enabled_agents : a.blueprint_ref => a }

  tenant_id      = var.tenant_id
  blueprint_ref  = each.value.blueprint_ref
  autonomy       = each.value.autonomy
  harness_id     = module.harness.id
  requirements   = jsondecode(data.http.blueprint_requirements[each.key].response_body)
}
