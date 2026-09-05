variable "tenant_id" {
  type = string
}

variable "blueprint_ref" {
  type        = string
  description = "e.g. \"invoice-ap@4.2.0\" (Doc 53 §4.1 metadata.blueprint format)."
}

variable "autonomy" {
  type        = string
  description = "The tenant's REQUESTED starting autonomy level. Clamped server-side to requirements.max_autonomy_permitted by the Fleet Manager — this module never writes autonomy directly to any datastore (Doc 60 §5.3.4 row 1)."
}

variable "harness_id" {
  type = string
}

variable "requirements" {
  type        = any
  description = "The decoded Blueprint Registry requirements object for this blueprint_ref (Doc 60 §5.3.2's registry_lookup.tf output)."
}
