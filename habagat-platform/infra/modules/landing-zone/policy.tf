# Doc 32 §2.1: "This is checked by Azure Policy with a deny effect, so a
# misconfiguration cannot be deployed rather than being detected
# afterwards." Assigned once per tenant subscription, at landing-zone
# provisioning time — independent of which agents are enabled.

resource "azurerm_subscription_policy_assignment" "deny_public_network_access" {
  name                 = "deny-public-network-${var.tenant_id}"
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/deny-public-network-access" # built-in initiative alias
  subscription_id      = data.azurerm_subscription.current.id
  description          = "Doc 32 §2.1: Foundry, Search, Storage, Cosmos and Key Vault must be private-endpoint only."
  enforce              = true
}

data "azurerm_subscription" "current" {}
