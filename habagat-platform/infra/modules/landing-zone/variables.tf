# infra/modules/landing-zone — Doc 32 §2.1's rg-<c>-platform + rg-<c>-network
# resource groups: network, Key Vault, managed identities, Log Analytics.
# Shared per tenant, independent of which agents are enabled (Doc 60 §5.3.1
# requirement 3 — this module never varies with enabled_agents).

variable "tenant_id" {
  type        = string
  description = "Doc 52 §1.2 Tenant.id — used as the naming prefix for every resource this module creates."
}

variable "region" {
  type        = string
  description = "Doc 32 §3.2 tenant config's primary_region."
}

variable "compliance_profile" {
  type        = string
  description = "e.g. \"iso27001-gdpr\", \"hipaa-baa\" — Doc 32 §3.2. Drives which Azure Policy initiative (§below) is assigned."
}
