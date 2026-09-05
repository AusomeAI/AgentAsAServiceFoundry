# Document 35 — Azure & Microsoft Services Catalogue

> Every Microsoft service Habagat depends on, what it is used for, why it was chosen, and what the alternative would be.
> This document exists so that an architect can build the platform and a CFO can model its cost.

---

## Executive take

- Habagat is deliberately **deep on Azure, not portable across clouds**. Depth buys speed, an enterprise-credible security story, and Microsoft co-sell. Portability is preserved only at the **agent specification layer**, not the infrastructure layer.
- The critical dependency is **Azure AI Foundry** — hub, project, Agent Service, model catalogue, evaluations and content safety. It is the reason the platform can be small.
- The second critical dependency is **Microsoft Entra ID**, which is what makes entitlement-aware retrieval and act-on-behalf-of possible. Without it, most of the security architecture would have to be rebuilt.
- Being a Microsoft-native ISV is a **go-to-market decision as much as a technical one**: Azure Marketplace transactability, MACC drawdown and co-sell change the enterprise sales motion materially.

---

## 1. Core AI platform

| Service | Use in Habagat | Why this, and not the alternative |
|---|---|---|
| **Azure AI Foundry (hub + project)** | The per-tenant AI workspace: model deployments, agents, evaluations, tracing, content safety, connections | Gives an enterprise-governed, region-pinned, network-isolated AI workspace out of the box. Building the equivalent would consume the platform team for a year |
| **Foundry Agent Service** | The agent runtime: threads, tool calling, the model loop | Managed agent loop with enterprise controls. Habagat wraps it with the harness rather than replacing it — buy the inference, build the trust |
| **Azure OpenAI in Foundry** | Frontier and mid-tier reasoning models | Enterprise terms (no training on customer data), regional deployment, PTU capacity, and Azure's compliance envelope |
| **Foundry Model Catalogue** | Access to open-weight and third-party models for specialised and cost-optimised tasks | Model diversity without leaving the tenant's compliance boundary |
| **Azure AI Content Safety (+ Prompt Shields)** | Input and output filtering; jailbreak and injection detection | Native integration; a detective layer over the structural controls |
| **Foundry Evaluations** | Executes the eval corpus; built-in and custom graders | Habagat owns the corpus and graders; Foundry runs them. Building a runner is undifferentiated work |
| **Azure AI Search** | Grounding index: hybrid search, semantic ranking, **ACL security trimming** | Security trimming with Entra group membership is the deciding feature. Standalone vector databases do not have it, and post-filtering leaks |
| **Azure AI Document Intelligence** | Structured extraction from invoices, forms, contracts, IDs, receipts | Pre-built models for the highest-volume document types in the catalogue; custom models for the rest |
| **Azure AI Speech** | Transcription and voice channels | Contact-centre and field use cases (TEL, TRV, HC) |
| **Azure AI Vision** | Image and video analysis | Manufacturing quality, media archive, agriculture, construction |
| **Azure AI Translator** | Multilingual service delivery | Essential in travel, telecom, public sector and NGO use cases |

---

## 2. Compute and integration

| Service | Use | Notes |
|---|---|---|
| **Azure Container Apps** | Hosts the Habagat Harness | KEDA scaling on queue depth; scale-to-zero for low-volume tenants; VNet integration; simpler to operate than AKS at Habagat's scale |
| **Azure Kubernetes Service** | Reserved for the largest tenants and specialised workloads | Only where Container Apps limits genuinely bind. Do not start here |
| **Azure Functions** | Trigger adapters, scheduled runs, lightweight tools | Consumption or Flex Consumption for cost efficiency |
| **Durable Functions** | Long-running sagas with human gates spanning hours or days | Durable state, replay semantics, timers — exactly the primitive needed for L2 approval workflows |
| **Azure API Management** | Ingress authentication, rate limiting, and the tool egress control point | The single choke point for both inbound and outbound; also where per-tenant quotas are enforced |
| **Azure Logic Apps** | Pre-built connectors to hundreds of SaaS systems | Fastest path to a connector for a long-tail system; not for high-volume paths |
| **Azure Event Grid / Service Bus** | Event triggers and run queueing | Service Bus where ordering and sessions matter; Event Grid for fan-out |
| **Azure Arc** | Agent execution on-premises or at the edge | Essential for manufacturing, mining and utilities where data cannot leave site |

---

## 3. Data and state

| Service | Use | Notes |
|---|---|---|
| **Azure Cosmos DB** | Run state, checkpoints, agent memory, session continuity | Low-latency, multi-region, serverless option for smaller tenants; TTL for automatic retention enforcement |
| **Azure Storage (ADLS Gen2)** | Documents, artefacts, trace archives, evaluation corpora | Lifecycle management for retention; CMK; private endpoints |
| **Azure SQL Database** | Structured domain data where relational semantics are needed | Preferred over Cosmos for anything requiring joins and transactions |
| **Microsoft Fabric** | Analytics, the customer's data platform, cross-agent reporting | Where the customer already uses Fabric, it becomes the grounding source for structured data |
| **Azure Cache for Redis** | Response caching, session cache, rate-limit counters | A meaningful COGS lever — caching identical retrievals and prompt prefixes materially reduces inference cost |

---

## 4. Identity, security and governance

| Service | Use | Notes |
|---|---|---|
| **Microsoft Entra ID** | All authentication; group membership drives ACL-trimmed retrieval; on-behalf-of flow | The foundation of the entitlement model. Non-substitutable |
| **Entra Privileged Identity Management** | Just-in-time, justified, time-limited Habagat access | Implements the zero-standing-access principle |
| **Entra Workload ID / Managed Identity** | Identity for every agent component and connector | No secrets in code or configuration |
| **Azure Key Vault (Premium/HSM)** | Secrets, certificates, customer-managed keys | Purge protection and soft delete mandatory |
| **Azure Policy** | Enforces the landing-zone baseline: region, private endpoints, encryption, tagging | **Deny effects, not audit effects** — misconfiguration should be impossible, not merely visible |
| **Microsoft Defender for Cloud** | Posture management and workload protection across the fleet | Secure score per tenant is a reportable customer-facing metric |
| **Microsoft Sentinel** | Security monitoring; the agent's own activity is a monitored data source | Habagat ships detection rules for agent-specific threats |
| **Microsoft Purview** | Data classification, sensitivity labels, lineage, DSPM for AI | Labels propagate into retrieval and output handling; supports data-subject rights |
| **Azure Lighthouse** | Scoped, auditable, revocable Habagat access into customer subscriptions | The mechanism that makes Model B operable at fleet scale |
| **Azure Confidential Computing** | Optional tier for the most sensitive workloads | Offered where a customer requires in-use protection; not the default |

---

## 5. Operations and delivery

| Service | Use | Notes |
|---|---|---|
| **Azure Monitor / Log Analytics** | Per-tenant observability workspace | Retention per customer policy; the largest controllable observability cost |
| **Application Insights** | Distributed tracing of agent runs, with OpenTelemetry | Span-level cost and token attribution |
| **Azure DevOps or GitHub Enterprise** | Source control, pipelines, artefacts, work tracking | GitHub preferred for the developer experience and Copilot integration |
| **GitHub Advanced Security** | Secret scanning, code scanning, dependency review | Supports the supply-chain controls in Document 34 |
| **Azure Container Registry** | Signed harness images, per-region replication | Content trust and signing enforced |
| **Azure Deployment Environments / Terraform** | Landing-zone provisioning | Terraform is primary; Bicep where the provider lags |
| **Azure Cost Management + Exports** | Per-tenant cost attribution and margin analysis | Feeds the unit-economics model directly |
| **Azure Chaos Studio** | Resilience testing of the harness and failover | Validates the DR claims rather than asserting them |

---

## 6. Microsoft 365 and business surfaces

| Service | Use | Notes |
|---|---|---|
| **Microsoft Graph** | Access to mail, files, calendar, Teams, users and groups | The most common trigger source and grounding source in enterprise deployments |
| **Microsoft Teams** | The primary human interface: agent chat, approval cards, escalation queues | Meets users where they already work — adoption is dramatically higher than a separate portal |
| **Microsoft 365 Copilot / declarative agents** | Optional surfacing of Habagat agents inside the Copilot experience | A distribution channel where the customer has M365 Copilot; Habagat agents appear where users already ask |
| **Power Platform** | Customer-built extensions and simple front ends | Where a customer wants to extend a Habagat agent themselves |
| **Dataverse** | Where the customer's business data already lives in Power Platform | A grounding source |

---

## 7. Go-to-market services

| Service | Use | Commercial impact |
|---|---|---|
| **Azure Marketplace** | Transactable private offers and standard listings | Customers can purchase against their **Microsoft Azure Consumption Commitment (MACC)**, which converts Habagat's price into pre-committed budget. This is frequently decisive in enterprise procurement and shortens deal cycles materially |
| **Microsoft co-sell (ISV Success / partner programmes)** | Joint selling with Microsoft field teams | Access to accounts Habagat could not reach alone; Microsoft sellers are incentivised on Azure consumption, which Habagat drives |
| **Microsoft AI Cloud Partner Program** | Designations and specialisations | Credibility signal in enterprise procurement; supports co-sell eligibility |
| **Microsoft for Startups** | Azure credits, technical support | Materially reduces early-stage infrastructure cost while the fleet is small |

> **Strategic note.** Habagat's single-tenant architecture drives significant Azure consumption *inside the customer's own subscription* (Model B). That makes Habagat unusually attractive to Microsoft's field organisation, because every Habagat deal grows the customer's Azure spend. This should be an explicit part of the partnership strategy, not an accident — it is the cheapest distribution available to a company of this size.

---

## 8. Service dependency risk

| Dependency | Risk | Mitigation |
|---|---|---|
| **Foundry Agent Service** | Product direction changes; feature deprecation | Provider-neutral agent spec; a second compiler target kept warm by a quarterly portability test |
| **Azure OpenAI models** | Deprecation, capacity, pricing changes | Multi-model routing; models pinned per blueprint; evaluation suite makes substitution measurable rather than risky |
| **Azure AI Search** | Cost at scale; feature limits | Index-design discipline; tiering; the retrieval interface is abstracted in the harness |
| **Entra ID** | Deep coupling to Microsoft identity | Accepted. This is the intentional core of the enterprise value proposition |
| **Single cloud** | No multi-cloud story | Accepted and stated openly. Portability exists at the spec layer; infrastructure portability is deliberately not a goal, because pursuing it would halve the platform's velocity for a benefit no customer has yet asked for |

**The honest position for investors:** Habagat is a Microsoft-native company. That is a deliberate concentration of risk in exchange for speed, security credibility, and a distribution channel. The hedge is the agent specification layer — real, tested quarterly, and the reason a provider change would be a quarter of work rather than a rebuild.
