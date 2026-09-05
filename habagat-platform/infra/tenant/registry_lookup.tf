# THIS FILE IS THE ANSWER TO "how do we support a future agent without
# rewriting Terraform." It queries the Blueprint Registry's public,
# read-only metadata API (Doc 53 §1.2 /v1/blueprints/{id}/versions/{id})
# for each enabled_agents entry and gets back a small, STANDARDIZED
# requirements object every blueprint — present or future — is compiled to
# produce (Doc 53 §4.1's schema fully determines this shape; the compiler,
# habagat-platform/compiler/, emits it as bundle metadata alongside the
# signed bundle itself, served by controlplane/registry/service.py's
# get_requirements()). Terraform never needs to know what a blueprint
# DOES — only what infrastructure category of thing it needs, and that
# vocabulary (model tiers, tool connector types, index requirements) is
# closed and small even as the number of blueprints grows without bound.

data "http" "blueprint_requirements" {
  for_each = { for a in var.enabled_agents : a.blueprint_ref => a }

  url = "${var.registry_base_url}/v1/blueprints/${split("@", each.key)[0]}/versions/${split("@", each.key)[1]}/requirements"
  # Returns, for ANY blueprint (shipped today or in the future), e.g.:
  # {
  #   "model_tiers_used": ["mid", "frontier"],
  #   "connector_types": ["microsoft-graph", "sap-s4"],
  #   "requires_search_index": true,
  #   "requires_document_intelligence": true,
  #   "max_autonomy_permitted": "L3",
  #   "risk_class_ceiling": "R3"          # drives whether human-approval UI must be provisioned
  # }

  request_headers = {
    Accept = "application/json"
  }
}

locals {
  # Union across every enabled agent — this is what actually sizes the
  # shared tenant infrastructure (Doc 32 §2.1's "per-tenant service").
  required_model_tiers   = distinct(flatten([for r in data.http.blueprint_requirements : jsondecode(r.response_body).model_tiers_used]))
  required_connectors    = distinct(flatten([for r in data.http.blueprint_requirements : jsondecode(r.response_body).connector_types]))
  needs_search           = anytrue([for r in data.http.blueprint_requirements : jsondecode(r.response_body).requires_search_index])
  needs_document_intel   = anytrue([for r in data.http.blueprint_requirements : jsondecode(r.response_body).requires_document_intelligence])
  needs_r3_approval_flow = anytrue([for r in data.http.blueprint_requirements : jsondecode(r.response_body).risk_class_ceiling == "R3"])
}
