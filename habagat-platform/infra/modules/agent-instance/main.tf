# Doc 60 §5.3.2: intentionally tiny and generic — this module has NO
# knowledge of "invoice-ap" or any other specific blueprint, which is
# precisely what makes it work unchanged for blueprint #26 next year. It
# calls the Fleet Manager's own provisioning API (Doc 55 §2, Doc 53 §1.2)
# rather than modeling AgentInstance as first-class Terraform state,
# because AgentInstance lifecycle (promotion, autonomy ramp, Doc 33 §1.4)
# is a governed APPLICATION process, not an infrastructure process —
# Terraform creates the binding; the Fleet Manager and Agent Review Board
# govern what happens to it after that.
#
# Doc 60 §5.3.4 row 2: this module provisions ZERO new Azure resources
# with network reach — it only calls the already-provisioned Harness's own
# internal API, over the network path modules/landing-zone already
# established. Adding an agent never widens the isolation boundary.

resource "http" "register_agent_instance" {
  url    = "https://${var.tenant_id}.harness.habagat.dev/internal/v1/instances"
  method = "POST"
  request_headers = {
    Content-Type = "application/json"
  }
  request_body = jsonencode({
    blueprint_ref = var.blueprint_ref
    autonomy      = var.autonomy # a REQUEST, clamped server-side — see variables.tf
    status        = "shadow"     # Doc 52 §1.2 — every instance starts in shadow, never "live"
  })
}

# Connector types are provisioned ONCE per tenant by modules/harness
# (main.tf's local.required_connectors); this resource only creates the
# CONFIG BINDING from this specific agent to those already-existing
# connector deployments.
resource "http" "bind_connectors" {
  for_each = toset(var.requirements.connector_types)

  url    = "https://${var.tenant_id}.harness.habagat.dev/internal/v1/instances/${jsondecode(http.register_agent_instance.response_body).instance_id}/connectors"
  method = "POST"
  request_headers = {
    Content-Type = "application/json"
  }
  request_body = jsonencode({ connector_type = each.value })
}

# Doc 60 §5.3.4 row 4: removing an agent from enabled_agents (this module
# instance simply disappearing from `for_each` in infra/tenant/main.tf on
# the next apply) must call disable, never leave the instance silently
# orphaned and still running.
#
# GAP RECORDED (see BUILD_LOG.md): the standard hashicorp/http provider's
# `http` resource does not expose a first-class "run this request on
# destroy" hook in the way this module's create-time resources use POST —
# a fully faithful implementation needs either a provisioner with
# `when = destroy` calling a small script (curl to the DELETE endpoint) or
# a purpose-built Habagat Terraform provider action. This build takes the
# conservative, explicit path — a `null_resource` with a destroy-time
# `local-exec` provisioner — rather than inventing a resource shape the
# `http` provider doesn't support, per the task instruction to record
# rather than paper over a gap.
resource "null_resource" "disable_on_removal" {
  triggers = {
    instance_id = jsondecode(http.register_agent_instance.response_body).instance_id
    tenant_id   = var.tenant_id
  }

  provisioner "local-exec" {
    when    = destroy
    command = "curl -sf -X DELETE https://${self.triggers.tenant_id}.harness.habagat.dev/internal/v1/instances/${self.triggers.instance_id}"
  }
}

output "instance_id" {
  value = jsondecode(http.register_agent_instance.response_body).instance_id
}
