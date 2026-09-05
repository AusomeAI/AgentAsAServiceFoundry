# Habagat — Technical Due Diligence Pack

> Owner: CTO · Status: v1.0 · Audience: technical investors, enterprise CISOs, procurement, auditors
> Answers are written to be defensible. Where a capability is aspirational rather than shipped, it is marked **[planned — target date]**. Do not remove those markers; candor is the point of this document.

## Executive take

- **The isolation story is the differentiator and it is architecturally enforced, not policy-enforced.** Each customer runs in their own Azure subscription with their own keys, network, identity and logs. Our control plane is structurally incapable of holding customer payloads, and we verify that with an automated canary test.
- **We answer "how do you know it works?" with evidence, not assertion.** Every agent ships with an eval report against the customer's own data, on the exact model version deployed, with a named accuracy gate and a documented failure taxonomy.
- **Our vendor concentration on Microsoft/Azure is real, deliberate, and hedged at the orchestration seam.** We can re-target the agent runtime in roughly one quarter; we keep the alternative compiler target alive with a quarterly eval run.
- **Liability for agent actions is managed by architecture first, contract second.** Irreversible actions require deterministic preconditions plus human approval or a compensating action, enforced at compile time. Insurance and contractual caps are the backstop, not the control.
- **The honest risks are: COGS drift, fleet entropy at scale, key-person concentration in the first 18 months, and platform capability compression.** They are named in §3 with the leading indicators we watch.

---

## 1. Question and answer

### Architecture and scalability

**Q1. How does a single-tenant architecture scale to 100+ customers without headcount scaling linearly?**

Three mechanisms, each with a measured metric.
1. **Agent Factory** — new agents are instantiated from parameterized blueprints; blueprint reuse ratio is tracked per deal. Target: ≥70% of a new agent derived from an existing blueprint by FY27.
2. **Isolation Fabric** — tenants are provisioned entirely by Terraform (target ≤4 hours automated, zero manual steps) and upgraded by ring-based fleet releases, not by per-customer projects.
3. **Dogfooded internal agents** — triage, drift remediation, eval-case drafting and onboarding design are increasingly performed by our own agents (doc 02 §8), targeting ≥25% operational toil reduction by FY28.

The metric that proves it is **tenants per pod: 3 (FY26) → 5–7 (FY27) → 8–10 (FY28)**. We report it to the board monthly. If it does not improve, the thesis is not working and we slow sales rather than add headcount.

**Q2. What actually breaks first as you scale?**

In order of expected occurrence: (a) quota exhaustion across many subscriptions — mitigated by the fleet quota ledger and headroom SLOs; (b) release throughput — mitigated by rings; (c) drift/snowflakes — mitigated by nightly reconciliation and the zero-snowflake rule; (d) eval-corpus maintenance cost as archetypes multiply — mitigated by corpus reuse across tenants of the same archetype and by the Eval Case Drafter agent. See doc 06 §3 for the per-milestone breakage analysis.

**Q3. What is the per-tenant infrastructure floor, and how does that affect margin on small customers?**

Illustrative ~$2,400/month fully loaded per tenant (orchestration/storage/telemetry ~$900, allocated fleet ops ~$1,500), targeting ~$1,400 by FY28 with the `nano` tier and automation. We recover it with a **platform/isolation fee** independent of usage (illustratively $3,500/month), so a low-volume tenant is never gross-margin negative. We will decline deals whose total contract value cannot clear the floor with margin — a stated qualification criterion, not a case-by-case judgment.

**Q4. What is your availability architecture and what SLA do you offer?**

Per-tenant: 99.5% monthly for agent execution (99.9% during the customer's declared business hours), with the caveat that we inherit the availability of the underlying Azure AI services and state that dependency explicitly in the SLA. Control plane: 99.9%. Degradation path on model unavailability: retry with backoff → certified fallback model → queue → batch → surfaced error. Agent execution continues if the control plane is down; the control plane is not in the customer's request path by design. **[Multi-region active-passive for tenants who buy it — planned, FY27 Q1.]**

**Q5. How do you handle a customer with 10× the volume you designed for?**

Volume scaling is a quota and capacity question, not an architecture question, because the runtime is managed. The steps are: raise quota (lead-time item), evaluate PTU against the break-even (doc 04 §6.1 — roughly 300k runs/month), enable batch endpoints for non-interactive traffic, and re-check the cascade routing at the new mix. Human review capacity is usually the real constraint, and the contract includes volume bands so review staffing is renegotiated rather than silently overrun.

### Isolation and data handling

**Q6. Prove the isolation. What technically prevents customer A's data reaching customer B?**

There is no shared data plane; there is nothing to segregate. Concretely:
- Each customer has a **dedicated Azure subscription** (theirs or Habagat-managed within their tenant) with its own Foundry project, model deployments, AI Search index, storage, Cosmos DB, Key Vault and Log Analytics workspace.
- No Habagat service holds credentials that span customers for data-plane resources. Control-plane→tenant access uses per-tenant managed identities with least-privilege role assignments, and is used for provisioning and telemetry only.
- Network: private endpoints, no public data-plane ingress by default, customer-controlled VNet integration.
- Keys: Azure Key Vault per tenant; **customer-managed keys (CMK)** available, which gives the customer a technical kill switch over their own data.
- Identity: Entra ID; agents act with managed identities or on-behalf-of the requesting user, so the customer's own authorization model constrains what the agent can read.
- **Verification:** a scheduled red-team job plants unique canary strings in tenant data and alerts if any canary is ever observed in control-plane storage or logs. Results are available to customers on request.

**Q7. What data does the control plane hold?**

Metadata, configuration and telemetry only: tenant identifiers, resource inventory, versions, ring assignment, quota state, run counts, token counts, latency, cost, outcome codes, escalation reason codes, and eval scores. **No prompts, no completions, no documents, no customer records.** The ingestion schema rejects free-text payload fields at the boundary, and payload fields are stripped in the tenant before egress. This is architectural bet B7 (doc 01) and it is the claim we would least like to be wrong about, hence the canary verification in Q6.

**Q8. Where is data processed and stored, and can you guarantee residency?**

The tenant is deployed in the customer's required Azure region; data at rest never leaves it. Processing residency depends on model availability in that region — we check this at intake (doc 04 §6.3), and if the required model is unavailable we use a certified fallback available in-region, or we tell the customer before contracting rather than after. We do not silently process cross-region.

**Q9. Is customer data used to train models?**

No. Model training on customer data is contractually prohibited and technically not implemented — we have no training pipeline connected to tenant data. Data sent to Azure OpenAI/Foundry model endpoints is not used by Microsoft or the model providers to train models under Azure's terms, and abuse-monitoring opt-out is available for customers who require it. **What we do retain** is described in Q11.

**Q10. What is your retention and deletion posture, including the "right to be forgotten"?**

Retention is per-tenant configuration: thread/run data, lineage records, and review-queue artifacts each have configurable retention (default 400 days for lineage to cover an audit cycle; shorter on request). Deletion of a data subject is executed within the tenant across: source index, vector index, agent long-term memory (which stores the record's scope key for exactly this reason), lineage store, and review queue. Because everything is in one subscription, deletion is verifiable — we can produce a resource-by-resource attestation. Full tenant deletion is a Terraform destroy plus subscription cancellation, with a signed certificate of destruction.

**Q11. What IP do you retain from a customer engagement — specifically prompts and evals?**

The commercial position we take, and which we will defend in negotiation:
- **Customer owns:** their data, their outputs, their business-process definitions, and any customer-specific configuration parameters and integration code written exclusively for them.
- **Habagat owns:** the platform, the blueprints, the Agent Spec, the eval harness, the generic prompts, and — importantly — **the generalized failure taxonomies, eval schemas and de-identified test cases** derived from operating the service.
- **The line we hold:** we may retain de-identified, non-attributable eval cases that capture a *pattern* (e.g. "multi-currency VAT on a partially-received PO line"), never the customer's actual documents or identifiers. This is disclosed up front, is opt-outable for the most sensitive customers, and is worded so that a customer's competitor could not reconstruct anything customer-specific.
- Some customers will refuse this. We accept the refusal and price the engagement higher, because losing the corpus contribution costs us long-term margin.

**Q12. What about the customer's own fine-tuned models or embeddings?**

Any model fine-tuned on customer data is deployed in the customer's subscription and is contractually the customer's, with weights deleted on termination. Embeddings derived from customer data are customer data and live only in their tenant.

### Models, providers and lock-in

**Q13. What happens if OpenAI, Anthropic or Microsoft changes pricing or terms materially?**

Layered answer.
1. **Model swap is a config change, not a project.** Every agent declares a certified fallback that has already passed the eval gate at ≥97% of primary. Swapping a model fleet-wide is a ring release, measured in days.
2. **Runtime swap is a quarter.** Agents are authored as a provider-neutral Agent Spec compiled to a runtime target. We maintain a second target (self-hosted loop on Azure Container Apps) and run the full eval suite against it quarterly so it does not rot. This is real insurance we actually pay a premium on.
3. **Pricing exposure is bounded by margin structure.** Model inference is ~18% of COGS in our reference archetype (doc 04 §4.2). A 50% model price increase costs ~9pp of gross margin — painful, not existential. Compare with a business where tokens are 70% of COGS.
4. **Commercially**, we have Foundry access to multiple model families, and we maintain a direct-provider contractual fallback.

**Q14. Isn't a single-cloud (Azure) bet a serious concentration risk?**

Yes, and we take it deliberately for FY26–27, because the enterprise data gravity in Entra ID/M365/Fabric is the reason our sales cycle is short. We hedge structurally: Terraform rather than Bicep-first, container-first services with cross-cloud analogues, no proprietary PaaS in the control plane without a portable equivalent, and OpenTelemetry rather than a proprietary APM. The revisit trigger is explicit: **>20% of qualified pipeline blocked on a non-Azure requirement**. A move would take 3–4 quarters for the data plane; we would see it coming through the pipeline metric.

**Q15. If the frontier models get dramatically better, does your product become unnecessary?**

Better models make our agents cheaper and more accurate against the *same* eval corpus — we capture that as margin and as a stronger quality claim. What does not become unnecessary is: the isolated deployment, the evaluation evidence, the deterministic policy layer over irreversible actions, the integrations, the human-review operation, and the ongoing re-certification as the substrate moves. The honest version of the risk is the reverse — that the *platform vendor* packages those things (doc 01 risk R1) — and our answer there is vertical corpus depth and outcome accountability, which platform vendors structurally do not sell.

### Quality, safety and liability

**Q16. How do you know an agent works? What is your evidence standard?**

Every GA agent has an **audit pack**: signed Agent Spec, the eval report (with model version, suite version, per-failure-class breakdown, and confidence intervals), the failure taxonomy, the policy bundle, the data-flow diagram, the runbook, and the human-review design. Gates are absolute (e.g. task success ≥0.96, zero-tolerance events = 0) and relative (no regression >1.0pp vs. baseline). Judges are calibrated against human raters with a required agreement threshold (κ ≥ 0.75) and re-measured quarterly. Nothing reaches production without passing on the exact model version deployed.

**Q17. How do you handle hallucination, and who is liable if the agent is wrong?**

Controls, in order:
1. **Grounding** — retrieval-backed answers with a minimum groundedness score enforced per agent; below threshold the run escalates rather than answers.
2. **Structured outputs** — every model boundary validates against a schema; unparseable output is a failure, not a guess.
3. **Deterministic verification** — factual claims that can be checked against a system of record are checked in code, not by the model (three-way match, arithmetic, date/entity validation).
4. **Policy preconditions** — irreversible actions require deterministic conditions to be true regardless of what the model concluded.
5. **Human-in-the-loop by risk tier** — with an autonomy ramp (100% review → 30% → 10% sampled) gated on measured accuracy.
6. **Shadow evaluation in production** — a sample of live runs is independently scored; drift pages the owning pod.

On liability: the agent is a tool operating within a customer-approved process, with a customer-approved review design and documented accuracy characteristics. Contractually we take responsibility for the service performing to its specified accuracy gates and for defects in our software; the customer retains responsibility for the business decision and for staffing the review design they approved. Liability is capped (typically 12 months' fees, higher for a negotiated premium), with carve-outs for our gross negligence, breach of confidentiality and IP indemnity. We carry tech E&O/cyber insurance sized to the largest contract. **We do not accept uncapped liability for model output**, and we say so early in the sales cycle rather than at the redline.

**Q18. What if an agent takes an incorrect irreversible action — moves money, sends a customer communication, files something?**

Prevention first: irreversible actions are classified R3, and our compiler **rejects an agent spec containing an R3 tool that has neither a compensating action nor a human-approval requirement**. This is enforced in CI, not in a policy document.

Response second: "Erroneous Action" is a defined P1 incident class with a rehearsed runbook — freeze the agent, enumerate affected runs from the lineage store (every run records inputs, retrieved evidence, prompt digest, model version, tool calls, outputs and decision path), notify the customer within 1 hour, produce a reconciliation list, then debug. The lineage store is what makes remediation tractable and is a required capability before any R3 agent goes live.

**Q19. What about prompt injection and data-borne attacks?**

Threat model: untrusted content (invoices, emails, web pages, tool results) can carry instructions. Controls: adversarial suites run in CI on every PR (document-borne injection, tool-output poisoning, exfiltration attempts); Azure AI Content Safety prompt-shield on untrusted inputs; **capability-based defense** — the agent's tools and identity are least-privilege, so a successful injection cannot exceed the agent's own authority; deterministic policy preconditions that an injected instruction cannot satisfy; egress restrictions on tools that could exfiltrate; and separation of instruction context from data context in prompt construction. We treat "the model can be persuaded" as a given and design so that persuasion is not sufficient to cause harm.

### Compliance

**Q20. What is your compliance status and roadmap?**

| Framework | Status | Target |
|---|---|---|
| SOC 2 Type I | **[planned]** | FY26 Q3 |
| SOC 2 Type II | **[planned]** | FY27 Q2 |
| ISO/IEC 27001 | **[planned]** | FY27 Q3 |
| ISO/IEC 42001 (AI management systems) | **[planned]** | FY27 Q4 — a genuine differentiator for AI vendors and worth doing early |
| GDPR | Architecture supports it now: residency by tenant, DPA with subprocessor list, DSR execution runbook, DPIA support pack, data minimization by design | Continuous |
| HIPAA | Azure services used are HIPAA-eligible; BAA available; PHI-specific controls (redaction, restricted review pool, audit) | FY27 Q2, gated on entering a healthcare vertical |
| EU AI Act | Classification per agent (most of our back-office agents are limited-risk; some HR/credit/insurance use cases are high-risk). We maintain per-agent technical documentation, logging, human oversight design, and accuracy/robustness evidence — which is largely what our audit pack already is | High-risk conformity readiness FY27 Q4 |
| PCI-DSS | Out of scope by design — we do not process cardholder data; agents that touch payment systems do so via tokenized references | Maintain scope exclusion |

An important structural advantage: because each customer is in their own subscription with their own logs and keys, **many controls are evidenced per tenant rather than argued in the abstract**, which is a materially easier audit conversation than a shared-plane vendor has.

**Q21. Who are your subprocessors?**

Microsoft Azure (compute, storage, AI services) is the principal one; model providers are accessed through Azure. The control plane uses a small, published set (identity provider, error tracking, billing/invoicing). The list is contractual with change notification. Notably, because the data plane is in the customer's subscription, **our subprocessor exposure for customer data is dramatically narrower than a typical SaaS vendor's** — most of our SaaS tools never touch customer data at all.

### Business and organizational risk

**Q22. What is your key-person risk?**

Real and concentrated in the first 18 months — in the CTO and the first two engineers. Mitigations we can evidence: everything is in Git (specs, prompts, evals, IaC, runbooks); ADRs record why decisions were made, not just what; blameless incident reviews are written; no undocumented production access paths; a documented bus-factor register per system with a target of ≥2 named owners per critical component by end of FY26. Hire #10 (an engineering manager) and the staff-engineer hires in FY27 are explicitly de-risking moves. We will not claim this risk is eliminated before FY27.

**Q23. How much technical debt are you carrying, and how do you manage it?**

Deliberate debt as of v1: (a) the portable compiler target exists but is not production-hardened — we pay it down with quarterly eval runs against it; (b) the Review Console is functional rather than polished; (c) multi-region tenant topology is single-region today; (d) cost attribution is daily rather than real-time. Each is tracked as a named item with an owner and a trigger condition for paydown (e.g. multi-region is built before the first tenant contracts for it, not speculatively). We hold a standing allocation of ~15% of engineering capacity for platform debt and reliability work, protected from feature pressure.

**Q24. What is your disaster recovery and business continuity posture?**

Per-tenant: all state is in Azure services with geo-redundant storage where the customer's residency rules allow; RPO ≤1 hour, RTO ≤4 hours for a full tenant rebuild, achievable because **the tenant is reproducible from code** — Terraform modules plus the tenant repo plus the Agent Bundles rebuild it deterministically. We rehearse this quarterly by destroying and rebuilding a test tenant end to end and measuring the actual time. Control plane: geo-redundant, RPO ≤15 min, RTO ≤2 hours; and critically, **control-plane loss does not stop agents running** — it stops provisioning, billing aggregation and dashboards. Company continuity: source escrow available for enterprise contracts, and see Q25.

**Q25. What happens to the customer if Habagat fails or is acquired? What are their exit rights?**

This is the question single-tenancy answers best, and we lead with it.
- The customer's agents already run **in their own Azure subscription**. If we disappear, the deployed agents keep running — nothing of ours sits in their request path.
- On termination the customer receives: their tenant repository, their Terraform state and modules, their Agent Bundles (specs, prompts, tool definitions), their eval suites and results, their lineage/audit exports, and their data — in open formats, on a defined timetable (illustratively within 30 days).
- **Source escrow** for the platform components required to maintain their agents is available for enterprise contracts.
- A **transition assistance** clause (illustratively 90 days at agreed rates) is standard.
- Practical honesty: they would lose ongoing model-refresh re-certification, platform improvements and support. They would not lose the working system or their data. Very few AI vendors can say that, and it is worth a premium in enterprise negotiation.

**Q26. How do you avoid becoming a services company with software-company multiples?**

By measuring it. The gate metrics are: blueprint reuse ratio (≥70% by FY27), tenants per pod (8–10 by FY28), gross margin trajectory (58% → 72%), and the share of revenue from recurring per-run/platform fees versus one-time implementation (target: implementation ≤15% of revenue). If blueprint reuse stalls, we are a services company and should be valued as one — and we would rather see that in a metric than discover it in a fundraise.

---

## 2. Evidence we can produce on request

| Artifact | Available |
|---|---|
| Reference tenant architecture diagram with resource inventory and network topology | Now |
| Sample agent audit pack (spec, eval report, policy bundle, data-flow, runbook) | Now |
| Canary isolation test results (control plane payload exclusion) | Now |
| Fleet health report (currency, drift, ring distribution) | Now |
| Eval methodology paper incl. judge calibration and human-agreement measurement | Now |
| DR rebuild exercise report with measured RTO | Quarterly |
| Penetration test report | **[planned — FY26 Q4, annual thereafter]** |
| SOC 2 report | **[planned — Type I FY26 Q3]** |
| Subprocessor list, DPA, BAA templates | Now / on request |

---

## 3. What could go wrong — the honest section

Investors discount vendors who claim no risk. Here are the four we would bet on going wrong, in order of probability × impact.

**1. Fleet entropy makes marginal customer cost stop falling.** *Probability: moderate-high. Impact: existential to the valuation thesis.*
The mechanism is boring and therefore likely: a "small" exception for a big customer, a skipped upgrade, a hand-edited resource. At 25–40 tenants this compounds into a stalled release train and linear headcount. Our defenses (zero-snowflake rule, nightly drift detection, ring SLOs, tenants-per-pod as a board metric) are real, but they are **cultural as much as technical**, and culture bends under revenue pressure. The tell will be tenants-per-pod flattening while sales accelerates. If we see that, the correct response is to slow sales — and that is a hard board conversation we are pre-committing to now.

**2. Gross margin does not reach 70%.** *Probability: moderate. Impact: high.*
The path in doc 04 depends most on raising autonomy rates (escalation 8% → 4–5%). Autonomy is limited by the *tail* of the customer's process — the 5% of cases that are genuinely ambiguous even for a human. If the tail is fatter than modeled in our chosen verticals, we plateau at 60–65% margin and become a good business rather than a great one. Leading indicator: the escalation-rate curve flattening in the first two design partners at a level above 6%.

**3. Platform capability compression.** *Probability: moderate. Impact: high.*
Microsoft ships vertical agent templates; frontier models make the guardrail scaffolding look like overhead; a prospect asks "why not build this ourselves on Foundry?" in most first calls. Our defense is corpus depth and outcome accountability, but a well-funded fast-follower with the same thesis and better distribution is a real scenario. Leading indicators: win-rate decline in accounts with internal AI platform teams, and ACV compression at constant scope.

**4. A serious agent-caused incident at a customer.** *Probability: low per-agent, but rising with fleet size — at 100 agents, low-probability events become annual events. Impact: high, and reputationally asymmetric.*
Our controls (R3 classification, compile-time enforcement, autonomy ramps, lineage store, rehearsed runbook) are designed for this, but the residual risk is not zero and we should not pretend otherwise. The decisive factor in whether such an incident is survivable is **whether we can reconstruct exactly what happened within hours** — which is why lineage and the incident runbook are prerequisites to R3 capability rather than follow-ons.

**Lesser risks we watch:** model deprecation cadence outrunning our re-eval capacity; Azure regional capacity shortfalls in a growth market; key-person concentration through FY26; a design partner in the R1 ring being harmed by an early release and souring a reference; and eval-corpus quality degrading as we scale labeling (guarded by judge–human agreement re-measurement).

---

## Decisions required from the founder/board

1. **Ratify the IP position on eval derivatives** (Q11) — the right to retain de-identified failure patterns and eval schemas — and accept losing some deals or pricing higher when a customer refuses it. This is a moat decision, not a legal detail.
2. **Approve the liability posture**: capped at 12 months' fees with defined carve-outs, no uncapped liability for model output, and a defined premium for elevated caps. Sales must be trained to raise this early.
3. **Fund the compliance roadmap** (SOC 2 Type I FY26 Q3, Type II + ISO 27001 FY27, ISO 42001 FY27 Q4) with a dedicated compliance engineer from hire #9, and decide whether ISO 42001 is worth pulling forward as a differentiator.
4. **Approve source escrow and 90-day transition assistance as standard enterprise terms** — these convert our biggest perceived risk (startup viability) into a selling point.
5. **Pre-commit to the "slow sales if tenants-per-pod flattens" discipline**, so the decision is made now rather than in the quarter it is needed.
6. **Approve tech E&O / cyber insurance sized to the largest contract**, before the first R3-capable agent reaches GA.
7. **Decide the healthcare/HIPAA timing** — it gates a vertical but pulls compliance spend forward by roughly two quarters.
