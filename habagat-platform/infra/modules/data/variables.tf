# Doc 32 §2.1's rg-<c>-data: Storage (ADLS Gen2), Cosmos DB, Azure SQL.
# SHARED per tenant — Doc 60 §5.3.1 requirement 3 again: run state and
# documents for every enabled agent live in these same per-tenant
# accounts, never a database per agent.

variable "tenant_id" {
  type = string
}

variable "vnet_id" {
  type = string
}

variable "cmk" {
  type        = string
  description = "Customer-managed key ID from modules/landing-zone, for CMK encryption (Doc 32 §2.1: 'Storage... CMK-encrypted')."
}
