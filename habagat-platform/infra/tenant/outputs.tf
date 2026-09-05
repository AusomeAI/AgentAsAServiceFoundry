output "harness_fqdn" {
  value = module.harness.fqdn
}

output "agent_instance_ids" {
  value = { for k, m in module.agent_instance : k => m.instance_id }
}

output "required_model_tiers" {
  description = "Exposed for the Fleet Manager's fleet-coordinate reconciliation (Doc 55 §2.1) to compare against the module_version/blueprint_versions it tracks independently."
  value       = local.required_model_tiers
}
