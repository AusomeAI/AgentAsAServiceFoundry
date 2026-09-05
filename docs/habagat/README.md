# Habagat — Agent as a Service

> **A complete research and planning corpus for an AI startup building vertical AI agents for enterprise workflows and operating them as a service inside each customer's own isolated Azure tenant.**

---

## What this is

A fresh, first-principles study of where AI agents can transform enterprise work, plus the full technical, operational and commercial plan to build a company that delivers it.

| | |
|---|---|
| **Use cases catalogued** | **284** — 20 cross-industry + 264 across 20 industries |
| **Agent archetypes identified** | 8 reusable engineering patterns explaining ~90% of them |
| **Industries covered** | 20 |
| **Delivery model** | Agent as a Service — single-tenant, one isolated Azure tenant/subscription per customer |
| **Platform** | Microsoft Azure AI Foundry + Azure |
| **Documents** | 40 |

Every use case is specified as a closed loop — **trigger → workflow → systems → outcome → KPIs → human gate** — so it can be lifted directly into a delivery backlog.

---

## Read in this order

### Start here
| Doc | Title | Why |
|---|---|---|
| [00](00-research-method-and-taxonomy.md) | **Research Method, Agent Taxonomy & Notation** | The method, the 8 archetypes, the autonomy ladder (L0–L4), blast-radius classes (B1–B4), and the notation every use case uses. **Read this first.** |
| [41](business/41-investor-narrative.md) | **Investor Narrative** | The story, the evidence, the honest risks |

### The research — what agents should do
| Doc | Title | Use cases |
|---|---|---|
| [01](01-cross-industry-use-cases.md) | **Cross-Industry Use Cases** — the horizontal product line | 20 |
| [02](industries/02-banking-capital-markets.md) | Banking & Capital Markets | 15 |
| [03](industries/03-insurance.md) | Insurance | 14 |
| [04](industries/04-healthcare-providers.md) | Healthcare Providers | 15 |
| [05](industries/05-life-sciences-pharma.md) | Life Sciences & Pharmaceuticals | 14 |
| [06](industries/06-retail-ecommerce.md) | Retail & E-Commerce | 14 |
| [07](industries/07-manufacturing-industrial.md) | Manufacturing & Industrial | 14 |
| [08](industries/08-energy-utilities.md) | Energy & Utilities | 14 |
| [09](industries/09-telecommunications.md) | Telecommunications | 13 |
| [10](industries/10-transportation-logistics.md) | Transportation & Logistics | 13 |
| [11](industries/11-public-sector-government.md) | Public Sector & Government | 14 |
| [12](industries/12-education.md) | Education | 13 |
| [13](industries/13-professional-services.md) | Professional Services | 13 |
| [14](industries/14-real-estate-construction.md) | Real Estate & Construction | 13 |
| [15](industries/15-travel-hospitality.md) | Travel, Hospitality & Leisure | 12 |
| [16](industries/16-media-entertainment.md) | Media, Entertainment & Publishing | 12 |
| [17](industries/17-agriculture-food.md) | Agriculture & Food Production | 12 |
| [18](industries/18-technology-software.md) | Technology & Software | 13 |
| [19](industries/19-mining-natural-resources.md) | Mining, Metals & Natural Resources | 12 |
| [20](industries/20-automotive-mobility.md) | Automotive & Mobility | 12 |
| [21](industries/21-nonprofit-social-impact.md) | Nonprofit, NGO & Social Impact | 12 |

### The platform — how to build and run it
| Doc | Title | Covers |
|---|---|---|
| [30](platform/30-reference-architecture.md) | **Reference Architecture** | The two-plane model, the isolation boundary, Agent Blueprints, run lifecycle, multi-agent patterns, ADRs |
| [31](platform/31-orchestrator-harness.md) | **The Habagat Harness** | The seven runtime subsystems, policy envelopes, compensation, prompt-injection defence, build-vs-buy |
| [32](platform/32-azure-landing-zone.md) | **Per-Tenant Azure Landing Zone** | Three deployment models, resource topology, provisioning pipeline, connectivity, cost model, onboarding runbook |
| [33](platform/33-governance-and-management.md) | **Governance & Fleet Management** | AI governance bodies, the prohibited list, autonomy promotion gates, ring rollout, drift, incidents |
| [34](platform/34-security-and-compliance.md) | **Security & Compliance** | Threat model, identity architecture, agent-specific controls, certification roadmap, the isolation evidence pack |
| [35](platform/35-azure-services-catalogue.md) | **Azure Services Catalogue** | Every Microsoft dependency, why chosen, and the dependency risks |
| [36](platform/36-evaluation-and-quality.md) | **Evaluation & the Trust Layer** | The corpus that is the moat: how it is built, run, and used to gate everything |

### CTO technical strategy
Produced by a dedicated **CTO Agent**.

| Doc | Title |
|---|---|
| [CTO 01](cto/01-cto-technical-strategy.md) | Three-year technical strategy, the moat, build/buy/partner, technology radar, architectural bets |
| [CTO 02](cto/02-engineering-org-and-operating-model.md) | Engineering org at 8 → 30 → 80, the Agent Pod, first ten hires, rituals, dogfooding |
| [CTO 03](cto/03-platform-engineering-and-sdlc.md) | Repo topology, the agent SDLC, CI/CD, eval-as-a-gate, ring-based fleet release |
| [CTO 04](cto/04-model-strategy-and-economics.md) | Model portfolio, routing, **worked unit economics**, COGS levers, capacity strategy |
| [CTO 05](cto/05-technical-due-diligence-pack.md) | 26 diligence questions answered, evidence table, honest failure analysis |
| [CTO 06](cto/06-technical-roadmap-and-milestones.md) | MVP definition, 8-quarter roadmap, what breaks at 1 → 5 → 25 → 100 tenants |

### Business
| Doc | Title |
|---|---|
| [40](business/40-business-model-and-gtm.md) | **Business Model & Go-to-Market** — pricing architecture, landing sequence, unit economics, competitive positioning |
| [41](business/41-investor-narrative.md) | **Investor Narrative** — the story, the four assets, the traction plan, the risks we raise ourselves |

### Application architecture
Produced by a dedicated **Software Architect Agent**, run from Doc 50's prompt.

| Doc | Title |
|---|---|
| [51](architecture/51-application-architecture-overview.md) | Application architecture overview — service decomposition, bounded contexts, C4 diagrams |
| [52](architecture/52-domain-model-and-data-design.md) | Domain model & data design — entities, aggregates, Cosmos/SQL/Search schemas |
| [53](architecture/53-api-and-interface-contracts.md) | API & interface contracts — Control Plane API, Tool Interface, Blueprint Spec JSON Schema |
| [54](architecture/54-harness-detailed-design.md) | Harness detailed design — the seven subsystems, the saga engine, the envelope algorithm |
| [55](architecture/55-control-plane-design.md) | Control plane design — Registry, Fleet Manager, Provisioning, Evaluation, Billing |
| [56](architecture/56-frontend-and-experience-architecture.md) | Frontend & experience architecture — the Console, the human-review screen, Teams integration |
| [57](architecture/57-integration-and-connector-framework.md) | Integration & connector framework — reference connectors, ingestion, deletion propagation |
| [58](architecture/58-non-functional-requirements-and-slos.md) | NFRs & SLOs — performance, scaling breakpoints, security traceability, cost enforcement |
| [59](architecture/59-architecture-decision-records.md) | Architecture decision records — ADR-09 through ADR-19 |

### Next artefacts
| Doc | Title |
|---|---|
| [50](agents/50-software-architect-agent-prompt.md) | **Software Architect Agent Prompt** — ready to run, produced the application architecture above |
| [60](agents/60-development-team-agent-prompts.md) | **Build Team Prompts** — UI/UX Designer + Software Engineer agent prompts that build the actual codebase, design artifacts, and the per-tenant Infra-as-Code |

---

## The four ideas that hold this together

**1. Eight archetypes, not 284 projects.** The catalogued use cases collapse into eight reusable engineering patterns. Habagat builds the archetype once and instantiates it per customer. This is the entire margin structure.

**2. Autonomy is earned, never assumed.** Every agent ships at L1 or L2 and is promoted on evidence — an evaluation corpus, shadow-mode agreement, a measured false-action rate, and a customer's documented decision. Demotion is automatic.

**3. Isolation is the product, not the overhead.** One Azure tenant per customer costs more and is harder to operate. It is also the reason Habagat can sell to a bank, a hospital and a government in the same quarter. The engineering investment goes into making that operable at fleet scale.

**4. The evaluation corpus is the moat.** Models are a commodity. A graded corpus proving a specific agent handles a specific enterprise workflow correctly — including its edge cases and its should-escalate cases — cannot be bought. It grows from human corrections and production incidents, and it compounds with every customer.

---

## Conventions used throughout

| Notation | Meaning |
|---|---|
| **A1–A8** | Agent archetype (Doc 00 §2) |
| **L0–L4** | Autonomy level — L0 assistive → L4 autonomous with post-hoc audit (Doc 00 §3) |
| **B1–B4** | Blast radius — B1 read-only → B4 irreversible/regulated/safety-relevant (Doc 00 §4) |
| **R0–R3** | Tool risk class — R0 read-only → R3 irreversible, human approval mandatory (Doc 31 §2.2) |
| **Human gate** | Where a person must intervene, and on what signal |

---

*All figures are illustrative and labelled as such, with the arithmetic shown so it can be substituted and challenged.*
