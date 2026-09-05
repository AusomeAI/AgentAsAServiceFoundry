# Doc 51 §1.2: ONE Container Apps deployment — the Harness is one
# deployable, never split into microservices, however many internal
# modules it has in code (harness/run_manager.py, policy_engine.py,
# verifier.py, saga.py, tool_gateway.py, memory_manager.py,
# escalation_manager.py, telemetry_emitter.py are all one process).

variable "tenant_id" {
  type = string
}

variable "ai_platform" {
  description = "The full module.ai_platform object (Doc 60 §5.3.2's excerpt) — this module reads its outputs (project id, content safety endpoint) rather than re-deriving them."
  type        = any
}

variable "data" {
  description = "The full module.data object — Cosmos/Storage/SQL ids this Container App connects to."
  type        = any
}

variable "connector_types" {
  type        = list(string)
  description = <<-EOT
    The UNION of connector types every enabled agent's Tool Gateway needs
    (Doc 60 §5.3.2 local.required_connectors) — drives which connector
    credentials this Container App's Key Vault references are configured
    for. NOT hardcoded; grows only when an enabled blueprint's
    requirements.connector_types introduces a new type.
  EOT
}

variable "deploy_approval_ui" {
  type        = bool
  description = "Doc 56 §2 — provision the Escalation Review queue's backing resources only if an enabled agent can reach R3 (Doc 60 §5.3.2 local.needs_r3_approval_flow)."
}
