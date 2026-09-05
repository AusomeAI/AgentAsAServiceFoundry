# Doc 32 §2.1's rg-<c>-ai: Foundry hub+project, model deployments, Search,
# Document Intelligence, Content Safety. Doc 60 §5.3.1 requirement 3: this
# resource GROUP is shared across every enabled agent — what varies is the
# CONFIGURATION inside it (which model tiers, whether Search/DocIntel are
# needed at all), never a new stack per agent.

variable "tenant_id" {
  type = string
}

variable "region" {
  type = string
}

variable "model_tiers" {
  type        = list(string)
  description = <<-EOT
    The UNION of model tiers every enabled agent needs (small/mid/frontier),
    derived in infra/tenant/registry_lookup.tf from each blueprint's
    requirements.model_tiers_used — NOT hardcoded here. Adding a future
    blueprint that needs a tier this tenant doesn't already have shows up
    as exactly one incremental model deployment on `terraform plan`, per
    Doc 60 §5.3.2.
  EOT
}

variable "deploy_search" {
  type        = bool
  description = "Doc 60 §5.3.2 local.needs_search — true iff any enabled blueprint's requirements.requires_search_index is true."
}

variable "deploy_document_intel" {
  type        = bool
  description = "Doc 60 §5.3.2 local.needs_document_intel."
}

variable "vnet_id" {
  type = string
}
