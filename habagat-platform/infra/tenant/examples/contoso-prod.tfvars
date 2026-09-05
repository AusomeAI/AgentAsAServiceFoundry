# A customer's own tenant.tfvars — this is ALL that changes to add an
# agent, including a future one that doesn't exist today. Doc 60 §5.3.3,
# reproduced verbatim as the worked example.

tenant_id          = "contoso-prod"
deployment_model   = "B"
primary_region     = "swedencentral"
compliance_profile = "iso27001-gdpr"

enabled_agents = [
  { blueprint_ref = "enterprise-knowledge@2.1.0", autonomy = "L2" },
  { blueprint_ref = "invoice-ap@4.2.0",            autonomy = "L2" },
  { blueprint_ref = "support-triage@3.0.1",        autonomy = "L2" },
  # Adding a brand-new blueprint next year is exactly this one line —
  # no module code changes, no new .tf file, no re-plan of shared resources
  # unless the new agent needs a model tier or connector type the tenant
  # doesn't already have (in which case `terraform plan` shows exactly and
  # only that incremental resource, per local.required_model_tiers'
  # distinct() union in registry_lookup.tf):
  # { blueprint_ref = "contract-negotiation@1.0.0", autonomy = "L1" },
]
