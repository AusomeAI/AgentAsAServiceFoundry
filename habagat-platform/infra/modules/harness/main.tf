resource "azurerm_resource_group" "compute" {
  name     = "rg-${var.tenant_id}-compute"
  location = data.azurerm_resource_group.network.location
}

data "azurerm_resource_group" "network" {
  name = "rg-${var.tenant_id}-network"
}

resource "azurerm_container_app_environment" "harness" {
  name                = "cae-${var.tenant_id}"
  resource_group_name = azurerm_resource_group.compute.name
  location            = azurerm_resource_group.compute.location
}

# The Harness — ONE Container App, per Doc 51 §1.2. Its internal modules
# (Run Manager, Policy Engine, Verifier, Saga Coordinator, Tool Gateway,
# Memory Manager, Escalation Manager, Telemetry Emitter — habagat-platform/
# harness/*.py) all run inside this one revision; connector_types and
# deploy_approval_ui only change this container's CONFIG (env vars / which
# credentials it's granted), never spawn a second deployable.
resource "azurerm_container_app" "harness" {
  name                         = "ca-${var.tenant_id}-harness"
  container_app_environment_id = azurerm_container_app_environment.harness.id
  resource_group_name          = azurerm_resource_group.compute.name
  revision_mode                = "Single"

  template {
    container {
      name   = "harness"
      image  = "habagatacr.azurecr.io/harness:latest" # pinned to a signed digest by the Provisioning Engine at deploy time, not by this file
      cpu    = 1.0
      memory = "2Gi"

      env {
        name  = "COSMOS_ACCOUNT_ID"
        value = var.data.cosmos_account_id
      }
      env {
        name  = "STORAGE_ACCOUNT_ID"
        value = var.data.storage_account_id
      }
      env {
        name  = "AI_FOUNDRY_PROJECT_ID"
        value = var.ai_platform.id
      }
      env {
        name  = "ENABLED_CONNECTOR_TYPES"
        value = join(",", var.connector_types)
      }
      env {
        name  = "APPROVAL_UI_ENABLED"
        value = tostring(var.deploy_approval_ui)
      }

      # Doc 58 §7 / Doc 60's "every service gets a health-check endpoint
      # the IaC's Container Apps configuration expects" — see
      # harness/health.py for the endpoint this probes.
      liveness_probe {
        transport = "HTTP"
        path      = "/healthz"
        port      = 8080
      }
    }
  }

  ingress {
    external_enabled = false # private endpoint only, Doc 32 §2.1's deny-public rule
    target_port      = 8080
  }
}

# Doc 56 §2 backing resources — only provisioned when an enabled agent can
# actually reach R3 (Doc 60 §5.3.2), never unconditionally.
resource "azurerm_servicebus_namespace" "approval_queue" {
  count               = var.deploy_approval_ui ? 1 : 0
  name                = "sb-${var.tenant_id}-approvals"
  resource_group_name = azurerm_resource_group.compute.name
  location            = azurerm_resource_group.compute.location
  sku                 = "Standard"
}

output "id" {
  value = azurerm_container_app.harness.id
}

output "fqdn" {
  value = "${var.tenant_id}.harness.habagat.dev" # the internal DNS name infra/modules/agent-instance/main.tf calls
}
