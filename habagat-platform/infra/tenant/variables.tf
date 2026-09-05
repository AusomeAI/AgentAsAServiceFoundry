# Doc 60 §5.3.2, reproduced verbatim — this is the specification, not a
# paraphrase of it.

variable "tenant_id" {
  type = string
}

variable "deployment_model" {
  type    = string # "A" | "B" | "C" — Doc 32 §1
  validation {
    condition     = contains(["A", "B", "C"], var.deployment_model)
    error_message = "deployment_model must be A, B, or C per Doc 32 §1."
  }
}

variable "primary_region" {
  type = string
}

variable "compliance_profile" {
  type = string # e.g. "iso27001-gdpr", "hipaa-baa" — Doc 32 §3.2
}

variable "enabled_agents" {
  description = <<-EOT
    The set of agents this tenant runs, by blueprint reference. This is the
    ENTIRE mechanism for "selectable today, extensible tomorrow" (Doc 60
    §5.3.1). Adding a NEW blueprint to this list — including one that did
    not exist when this module was last changed — requires NO change to
    any .tf file in this module. The module resolves each reference's
    actual infrastructure requirements from the Blueprint Registry at plan
    time (see registry_lookup.tf), not from a hardcoded map in this repo.
  EOT
  type = list(object({
    blueprint_ref = string # e.g. "invoice-ap@4.2.0" (Doc 53 §4.1 metadata.blueprint format)
    autonomy      = string # tenant's chosen starting level, <= the blueprint's maxPermitted
  }))
}

variable "registry_base_url" {
  type        = string
  default     = "https://registry.habagat.dev"
  description = "Overridable for non-production Blueprint Registry endpoints (e.g. a staging registry for a design-partner tenant) — never hardcoded elsewhere in this module."
}
