# Habagat — Technical Roadmap & Scaling Milestones

> Owner: CTO · Status: Board draft v1.0 · Horizon: 8 quarters (FY26 Q1 → FY27 Q4), with FY28 shape
> Dates, headcounts and tenant counts are **illustrative assumptions** tied to the plan in docs 02 and 04. Exit criteria are normative: a quarter is not complete until they are met, and slipping a quarter is preferable to declaring one done that is not.

## Executive take

- **The MVP is not an agent. It is the Agent Factory v1** — the machinery that turns a customer use case into an isolated, evaluated, deployable agent. If we ship two impressive agents and no factory, we have built a consultancy.
- **Eight quarters, four phases:** Prove (Q1–Q2) → Repeat (Q3–Q4) → Industrialize (Q5–Q6) → Compound (Q7–Q8). Each phase has one dominant constraint, and building ahead of the constraint is the main way we would waste the seed round.
- **The scaling breakpoints are known in advance**: at 5 tenants, manual release breaks; at 25, quota and drift break; at 100, human review economics and eval-corpus maintenance break. Each has a named capability that must exist *before* we cross it.
- **We deliberately do not build in v1:** multi-region, self-serve onboarding, a marketplace, fine-tuning, real-time cost attribution, PTU, mobile, or an agent-builder UI for customers. Every one of these is a plausible-sounding way to arrive at Q4 with no factory.
- **The two hard exit criteria for the seed period** are: 3 tenants live on 2 archetypes with eval gates enforced, and a platform patch reaching 100% of the fleet in under 7 days without manual intervention.

---

## 1. The MVP: Agent Factory v1

### 1.1 Definition

**Agent Factory v1 is complete when a new customer, matching an existing archetype, can go from signed contract to a production agent in ≤6 weeks with ≤2 pod-weeks of engineering effort, using only golden paths, with an eval gate enforced at every promotion.**

That single sentence is the definition of done. It decomposes into six shipped components:

| # | Component | v1 scope | Explicitly out of v1 scope |
|---|---|---|---|
| 1 | **Agent Spec + compiler** | YAML spec; compiles to Foundry Agent Service; schema validation; risk classification of tools (R0–R3) enforced at compile time | Second compiler target (stub only, hardened later); visual editor |
| 2 | **Blueprint catalog** | 2 archetypes fully parameterized (document extraction + validation; document generation with review) | Marketplace, third-party blueprints, variant inheritance |
| 3 | **Tenant module (Isolation Fabric v1)** | Terraform module provisioning a complete single-region tenant: Foundry project, model deployments, AI Search, Storage, Cosmos, Key Vault, Log Analytics, private endpoints, managed identities; ≤4 hours automated | Multi-region, sovereign cloud, CMK (Q3), subscription vending automation (Q3) |
| 4 | **Eval harness + first corpus** | Suite runner, LLM judges with human-agreement calibration, regression baselines, CI gate, scorecard on PRs; ≥150 labeled cases per archetype | Automated eval-case generation, corpus productization |
| 5 | **Deterministic policy engine** | Rule bundles, preconditions, R3 approval enforcement, spend limits, compile-time rejection of unsafe specs | Customer-authored policies, policy simulation UI |
| 6 | **Review Console + lineage** | HITL queue, evidence panel, correction capture (which feeds the corpus), per-run lineage record | Rich analytics, customer-configurable workflows, mobile |

Plus the minimum control plane: fleet inventory, run/token/cost metering (daily granularity), and basic dashboards.

### 1.2 Deliberately NOT in v1 — and why

| Not built | Why not | When it earns its place |
|---|---|---|
| Multi-region tenants | Zero customers need it at 3 tenants; it doubles the Fabric's complexity | When a signed contract requires it (Q5 at earliest) |
| Self-serve customer onboarding portal | We do not yet know what onboarding *is*; automating an undiscovered process is the classic seed-stage waste | Q6, after 10 tenants have taught us the pattern |
| Customer-facing agent builder | Sells a story, creates support load, and undermines the "evaluated agent" claim | Not in this 3-year plan |
| Fine-tuning pipeline | Anti-default by policy (doc 04 §3); no measured need yet | Only with a CTO-approved eval-backed case |
| PTU / reserved capacity | Break-even is ~300k runs/month; no tenant is close | Per-tenant, when the volume or a latency SKU justifies it |
| Real-time cost attribution | Daily is sufficient to catch drift; real-time is a streaming pipeline we do not need | Q7, when margin management gets fine-grained |
| Marketplace / partner-delivered agents | Requires blueprints stable enough to hand to others | FY28 |
| Multi-agent orchestration frameworks | Two archetypes do not need it; deterministic Workflow Kernel is sufficient and safer | Q5, evaluated against Foundry connected agents |
| Mobile / rich end-user apps | Teams and Outlook are the delivery surfaces our buyers already use | Not planned |
| Our own vector database, model hosting, or auth | Hold ring (doc 01 §4) | Never |

---

## 2. Quarter-by-quarter roadmap

### Phase 1 — Prove (Q1–Q2). Dominant constraint: *does the thing work at all, in a customer's boundary?*

#### Q1 — "First tenant, first evidence"
| | |
|---|---|
| **Theme** | Stand up one real tenant and one real agent, with an eval that can fail |
| **Epics** | E1 Tenant module v0.5 (single region, private endpoints, managed identities, Key Vault) · E2 Agent Spec v0 + Foundry compiler · E3 Archetype #1 (document extraction + validation) for design partner #1 · E4 Eval harness v0 with 150 labeled cases and judge calibration · E5 CI skeleton with the eval gate wired in from day one |
| **Exit criteria** | Design partner #1 running in **their** subscription, shadow mode, ≥1,000 runs · Eval suite demonstrably fails a seeded-bad build · Tenant provisioning ≤1 day (manual steps documented, not yet eliminated) · Judge–human agreement κ ≥ 0.70 |
| **Capability unlocked** | We can make an evidence-backed accuracy claim to a prospect |
| **Team** | 8 engineers |

#### Q2 — "Second tenant proves the blueprint"
| | |
|---|---|
| **Theme** | The second customer must cost materially less than the first |
| **Epics** | E6 Blueprint extraction: turn customer #1's agent into a parameterized blueprint · E7 Deterministic policy engine v1 with R0–R3 classification and compile-time enforcement · E8 Review Console v1 + lineage store · E9 Design partner #2 on the same archetype · E10 Tenant module v1, ≤4 hours automated · E11 Control-plane fleet inventory + daily metering |
| **Exit criteria** | Customer #2 live using **≥60% blueprint reuse**, delivered in ≤6 pod-weeks (vs. ~16 for #1) · Zero manual steps in tenant provisioning · No prompts or code in either tenant repo (CI-enforced) · Lineage record for 100% of runs · Cost per run measured and within 150% of model |
| **Capability unlocked** | Repeatability is demonstrated, not asserted — the core investor claim |
| **Team** | 10–12 |

### Phase 2 — Repeat (Q3–Q4). Dominant constraint: *release management across a fleet.*

#### Q3 — "Rings and trust"
| | |
|---|---|
| **Theme** | Stop deploying by hand; start being auditable |
| **Epics** | E12 Ring-based fleet release (R0→R3) with automated halt criteria · E13 Drift detection (nightly reconciliation) · E14 Archetype #2 (document generation with expert review) · E15 CMK support + subscription vending automation · E16 SOC 2 Type I evidence automation · E17 Adversarial/prompt-injection suite in CI · E18 Autonomy ramp mechanism (review % as a config flip) |
| **Exit criteria** | 5 tenants live · A platform change reaches 100% of fleet via rings with **zero manual tenant touches** · Drift report green across the fleet for 14 consecutive days · SOC 2 Type I achieved · Design partner #1 at ≤30% human review with accuracy holding |
| **Capability unlocked** | We can sell to a security-reviewed enterprise and operate more than a handful of tenants |
| **Team** | 12–14 |

#### Q4 — "Cost becomes a first-class citizen"
| | |
|---|---|
| **Theme** | Know, and then reduce, the cost of every run |
| **Epics** | E19 Cost engine: cost per successful run per agent per tenant, with anomaly detection · E20 Cascade routing v1 (small/mid/frontier) + prompt caching · E21 Batch endpoints for eligible workloads · E22 Model deprecation runbook + certified fallback for every agent · E23 Archetype #3 · E24 Shadow evaluation on live traffic · E25 Second compiler target (portable) — first full quarterly eval run |
| **Exit criteria** | 8 tenants · Cost per successful run down ≥25% from Q2 baseline on archetype #1 · Every GA agent has a certified fallback model that passed the gate at ≥97% of primary · Portable target passes the full eval suite (evidence for diligence Q13) · Gross margin ≥50% |
| **Capability unlocked** | Margin is managed rather than discovered at month-end; the vendor-lock hedge is real |
| **Team** | 14–16 |

### Phase 3 — Industrialize (Q5–Q6). Dominant constraint: *quota, drift and eval maintenance at 25 tenants.*

#### Q5 — "Fleet at scale"
| | |
|---|---|
| **Theme** | Systems that assume N is large |
| **Epics** | E26 Fleet quota ledger + headroom SLOs + graceful degradation chain · E27 Automated drift remediation (auto-generated Terraform PRs) · E28 Multi-region tenant topology (first customer-driven) · E29 Trust Layer GA: audit export, decision lineage API, DSR execution runbook · E30 Archetypes #4–#6 · E31 First internal agents: Support Triage, Eval Case Drafter (doc 02 §8) · E32 Multi-agent composition decision — Foundry connected agents vs. Workflow Kernel, resolved with an ADR |
| **Exit criteria** | 15–20 tenants · Zero quota-caused incidents in the quarter · ≥60% of drift findings auto-remediated by PR · Tenants per pod ≥4 · Customer-facing audit export demonstrated to a real auditor |
| **Capability unlocked** | The fleet operates without a linear increase in toil |
| **Team** | 20–24 |

#### Q6 — "Corpus as a product"
| | |
|---|---|
| **Theme** | Make the moat measurable |
| **Epics** | E33 Corpus platform: per-vertical suites, versioning, coverage metrics against the failure taxonomy, contribution pipeline from production corrections · E34 Eval-case drafting agent in production (target 3× corpus growth at constant SME headcount) · E35 SOC 2 Type II + ISO 27001 readiness · E36 Onboarding accelerators (intake → tenant design assistant) · E37 Archetypes #7–#9 · E38 `nano` tenant tier (fixed floor −40%) |
| **Exit criteria** | 25 tenants · Corpus coverage ≥85% of named failure classes per active archetype · Blueprint reuse ratio ≥70% on new deals · Time-to-first-value ≤6 weeks median · SOC 2 Type II fieldwork underway · Gross margin ≥60% |
| **Capability unlocked** | The evaluation corpus becomes a defensible asset we can describe quantitatively to investors |
| **Team** | 26–30 |

### Phase 4 — Compound (Q7–Q8). Dominant constraint: *unit economics and organizational leverage.*

#### Q7 — "Margin engineering"
| | |
|---|---|
| **Theme** | Convert corpus and scale into COGS advantage |
| **Epics** | E39 Distillation pipeline: student model for one high-volume step, trained on our own traces · E40 Tool-result and retrieval caching with correct invalidation · E41 Expert-review acceleration for archetype C (pre-filled evidence, diffable drafts) · E42 Real-time cost attribution · E43 Drift Remediation and Cost Anomaly agents in production · E44 Archetypes #10–#12 · E45 First PTU deployment for the highest-volume tenant, as a priced SKU |
| **Exit criteria** | 40 tenants · Distilled model in production beating the mid tier on cost per successful run with no quality regression · Expert-review minutes per run down ≥30% on archetype C · Tenants per pod ≥6 · Gross margin ≥65% |
| **Capability unlocked** | COGS reduction becomes an engineering program with a repeatable playbook |
| **Team** | 32–40 |

#### Q8 — "Leverage"
| | |
|---|---|
| **Theme** | Grow customers faster than engineers |
| **Epics** | E46 Self-serve elements of onboarding (customer-side intake, data connection wizard, security-pack generation) · E47 Blueprint variant tooling so a pod can promote a variant without Platform · E48 Partner enablement: SI-delivered agents on our platform under our gates · E49 EU AI Act high-risk conformity tooling (technical documentation generation, oversight evidence) · E50 ISO 42001 · E51 Archetypes #13–#15 |
| **Exit criteria** | 55–65 tenants · ≥30% of new agents delivered with a partner or with minimal Platform involvement · Tenants per pod ≥7 · Fleet currency ≥90% on current minor · Gross margin ≥68% · ISO 42001 certified |
| **Capability unlocked** | Growth is no longer gated on Habagat engineering capacity |
| **Team** | 40–50 |

### FY28 shape (Q9–Q12, directional)
Themes: **corpus-driven autonomy** (autonomy rate as the primary product roadmap), **sovereign/regulated deployments**, **partner-scaled delivery**, and **agent portfolio management** (customers running 5–15 agents each, with cross-agent orchestration). Targets: 100 tenants, 25 archetypes, ~80 engineers, ~72% gross margin, tenants per pod 8–10.

---

## 3. Scaling milestones: what breaks and what must exist first

### 1 → 5 tenants

| What breaks | Symptom | Must be built before crossing | Owner |
|---|---|---|---|
| Manual deployment | A prompt fix takes a day per tenant; someone forgets one | Ring release pipeline (R0→R3); `.habagat-lock` as source of truth | Isolation Fabric |
| Ad hoc tenant setup | Each tenant is subtly different; the first security questionnaire is unanswerable | Terraform tenant module, ≤4h automated, zero manual steps | Isolation Fabric |
| Informal on-call | The person who built it is the only one who can fix it, at 2am | Runbooks, SLOs, two-person rotation, paging | SRE |
| No corpus | Quality claims are anecdotes; the second customer re-litigates the first's findings | Eval harness + ≥150 cases per archetype + CI gate | Eval Engineering |
| Prompt forks | Customer-specific prompt edits land in tenant repos | Zero-snowflake rule enforced in CI; parameters instead of forks | Foundry Platform |

**Gate to cross:** platform change to 100% of fleet with no manual tenant touch.

### 5 → 25 tenants

| What breaks | Symptom | Must be built before crossing | Owner |
|---|---|---|---|
| Quota | A tenant 429s during month-end close; support has no visibility | Fleet quota ledger, ≥40% headroom SLO, graceful degradation chain (backoff → fallback model → queue → batch) | Isolation Fabric + Applied AI |
| Drift | Tenants diverge; upgrades fail unpredictably | Nightly reconciliation, auto-remediation PRs, drift as a P2 | Isolation Fabric |
| Release throughput | One release train cannot serve 25 tenants with different change windows | Rings + per-tenant `changePolicy` (windows, approvals) with an emergency-change right | Isolation Fabric |
| Cost visibility | Margin is discovered at month-end, per-company not per-agent | Cost engine: cost per successful run per agent per tenant, with anomaly detection | Control Plane |
| Model deprecations | A provider retires a version; 12 agents must be re-evaluated at once | Certified fallback per agent + deprecation runbook + ring-based model rollover | Applied AI |
| Support load | Every alert reaches a human | Support Triage agent; alert correlation with fleet telemetry | SRE + Internal Tools |
| Eval maintenance | Corpus grows faster than SMEs can curate it | Eval Case Drafter agent; corpus coverage metrics | Eval Engineering |
| Compliance evidence | Every enterprise deal triggers a bespoke evidence hunt | Automated evidence collection; SOC 2 Type I then Type II | Trust & Security |

**Gate to cross:** zero quota-caused incidents in a quarter; ≥60% of drift auto-remediated; tenants per pod ≥4.

### 25 → 100 tenants

| What breaks | Symptom | Must be built before crossing | Owner |
|---|---|---|---|
| Human review economics | Review headcount grows linearly with volume; margin caps at ~60% | Autonomy program: targeted fixes on top failure classes, review-UI acceleration, escalation-precision tuning | Pods + Eval Engineering |
| Pod capacity | Pods serve 5 tenants and stall; hiring goes linear | Self-serve golden paths, blueprint variant tooling, partner enablement | Foundry Platform |
| Fleet observability | 100 tenants × 10 agents = 1,000 SLO surfaces; dashboards become noise | Fleet-level health scoring, exception-based reporting, automated triage | SRE + Control Plane |
| Regional and sovereign spread | A model is unavailable in a customer's required region mid-deal | Model × region matrix checked at intake; multi-region topology; open-weight fallback path | Applied AI + Fabric |
| Corpus governance | Suites conflict across tenants of the same archetype; regressions become ambiguous | Corpus platform with versioning, ownership, coverage, and promotion rules | Eval Engineering |
| Incident blast radius perception | One customer's incident is read by the market as a fleet risk | Lineage-based forensics, rehearsed Erroneous Action runbook, customer comms templates, insurance | SRE + Trust |
| Billing and margin at scale | Per-run rating across 100 subscriptions with disputes | Real-time cost attribution, invoice reconciliation, customer-visible usage portal | Control Plane |
| Institutional knowledge | Onboarding an engineer takes a quarter | Golden-path docs, ADR corpus, internal Onboarding Architect Assistant | All |

**Gate to cross:** tenants per pod ≥7; fleet currency ≥90%; gross margin ≥68%; escalation rate on flagship archetypes ≤5%.

---

## 4. Roadmap summary

| Quarter | Theme | Tenants | Archetypes | Engineers | GM | Headline exit criterion |
|---|---|---|---|---|---|---|
| Q1 | First tenant, first evidence | 1 | 1 | 8 | — | Eval suite can fail a seeded-bad build |
| Q2 | Second tenant proves the blueprint | 2–3 | 2 | 10–12 | — | ≥60% blueprint reuse; zero manual provisioning steps |
| Q3 | Rings and trust | 5 | 2 | 12–14 | ~45% | Fleet-wide release, zero manual tenant touches; SOC 2 Type I |
| Q4 | Cost becomes first-class | 8 | 3 | 14–16 | ~50% | Cost/successful run −25%; portable target passes full evals |
| Q5 | Fleet at scale | 15–20 | 6 | 20–24 | ~55% | Zero quota incidents; ≥60% drift auto-remediated |
| Q6 | Corpus as a product | 25 | 9 | 26–30 | ~60% | Blueprint reuse ≥70%; corpus coverage ≥85% |
| Q7 | Margin engineering | 40 | 12 | 32–40 | ~65% | Distilled model in production; expert-review minutes −30% |
| Q8 | Leverage | 55–65 | 15 | 40–50 | ~68% | ≥30% of agents partner/self-delivered; ISO 42001 |

**Dependency chain that must not be reordered:** eval harness → blueprint extraction → ring releases → drift control → cost engine → autonomy program → distillation. Every later item's value depends on the earlier ones existing. The most common way this plan fails is pulling distillation or multi-region forward because a prospect asked, before drift control exists.

---

## Decisions required from the founder/board

1. **Ratify the MVP definition** ("contract to production in ≤6 weeks with ≤2 pod-weeks for a known archetype") as the seed-period success criterion, in preference to a customer-count or revenue milestone.
2. **Approve the v1 exclusion list** — in particular no multi-region, no self-serve portal, no fine-tuning, no customer-facing agent builder before Q5 — and back the CTO in declining prospect-driven exceptions.
3. **Approve the two archetypes for FY26** (document extraction + validation; document generation with expert review) and, with them, the two verticals that get pods first.
4. **Accept the gross-margin ramp (≈45% in Q3 rising to ≈68% by Q8)** and brief investors on it proactively rather than defending it later.
5. **Approve the R1 design-partner ring as a contractual construct** with 2–4 named partners in Q2, including the pricing/roadmap concessions that buys.
6. **Pre-commit to the scaling gates**: we do not sign past 5, 25 or 100 tenants until the named gate metrics are met. This is the single decision that most determines whether we are a software company or a services company at exit.
7. **Decide the FY27 compliance depth** — SOC 2 Type II + ISO 27001 is the floor; ISO 42001 and EU AI Act high-risk tooling are discretionary investments that open specific verticals. Choose now, because they drive hiring two quarters ahead.
