# Document 33 — Governance, Fleet Management & Operations

> How Habagat governs what its agents are permitted to do, and how a small team operates hundreds of isolated customer environments without them diverging into hundreds of bespoke systems.

---

## Executive take

- Two distinct governance problems, often conflated: **AI governance** (is this agent permitted to do this, and who says so?) and **fleet governance** (are 200 tenants running what we think they're running?). Both are existential; they need different machinery.
- The AI governance model is built on the **autonomy ladder and blast-radius classes** from Document 00, with a promotion gate that requires evidence. Autonomy is earned, never assumed, and the evidence is a document, not an opinion.
- Fleet governance rests on one rule: **no snowflakes**. Every tenant is a composition of versioned blueprints plus configuration. Drift is detected continuously and remediated, never accepted.
- The organisational structure that makes this work is the **Agent Review Board** on the AI side and the **Fleet Operations function** on the platform side. Both must exist before the tenth customer, not after the fiftieth.

---

## 1. AI governance model

### 1.1 Governance bodies

| Body | Composition | Cadence | Decides |
|---|---|---|---|
| **Agent Review Board (Habagat)** | CTO (chair), Head of AI Safety, Head of Delivery, Legal/Compliance, a domain lead | Weekly | Blueprint approval for release; autonomy ceiling per blueprint; risk classification; incident findings; blueprint retirement |
| **Customer AI Council** *(per customer)* | Customer business owner, risk/compliance, data protection, IT security + Habagat account technical lead | Monthly, then quarterly | Which agents run; autonomy level in *their* tenant; acceptable-use boundaries; incident response; escalation of concerns |
| **Habagat Safety Review** | Head of AI Safety + independent reviewer outside the delivery pod | Ad hoc, mandatory for any B4 or L4 proposal | Whether a high-consequence agent may proceed at all |

**The independence rule.** The person who signs off an agent's safety must not report to the person whose delivery date depends on it. This is a small structural decision that determines whether governance is real. It costs one salary and saves the company.

### 1.2 The agent risk classification

Every blueprint carries a risk class computed from four inputs, not assigned by judgement:

```
riskClass = f(blastRadius, autonomy, dataSensitivity, regulatoryCategory)
```

| Risk class | Trigger | Required before release |
|---|---|---|
| **Low** | B1–B2, L0–L2, non-sensitive data, unregulated | Standard eval gate; pod sign-off |
| **Medium** | B3, or L3, or sensitive personal data | Eval gate + Agent Review Board approval + documented human-gate design |
| **High** | B4, or L4, or special-category data, or a regulated decision domain | All of the above + independent Safety Review + customer AI Council approval + documented risk assessment |
| **Prohibited** | Practices banned under applicable law (e.g. EU AI Act Article 5: social scoring, emotion recognition in workplace/education, certain biometric categorisation) | **Not built. Not sold.** Maintained as an explicit refusal list |

### 1.3 The prohibited list

Habagat maintains a published list of things it will not build. This is a commercial asset as much as an ethical position: it is the first thing a serious enterprise buyer's risk function asks for, and having one already written is disproportionately persuasive.

- Social scoring or general-purpose behavioural scoring of individuals.
- Emotion inference used to make decisions about people in workplaces or education.
- Real-time remote biometric identification for law enforcement.
- Fully autonomous adverse decisions about individuals' rights, benefits, employment, credit or liberty.
- Covert manipulation, dark patterns, or agents that conceal that they are agents where disclosure is required.
- Undisclosed individual employee surveillance or performance scoring.
- Any agent whose failure mode is physical harm without an independent, non-AI safety control.

### 1.4 The autonomy promotion gate

Promotion from L2 to L3 is the most commercially significant event in an agent's life — it is where the customer's labour saving becomes real. It is therefore the most rigorously gated.

| Requirement | Evidence |
|---|---|
| Evaluation performance | ≥ threshold on the current corpus, on **the customer's own data**, not just the reference corpus |
| Shadow operation | ≥ 14 days running alongside the human process, with the disagreement rate measured and the disagreements analysed individually |
| False-action rate | Below the blueprint's stated SLO, with a lower confidence bound, not a point estimate |
| Escalation quality | Escalations were genuinely necessary; over-escalation is a failure mode too |
| Reversibility | Every automated write has a tested compensating action, and the rollback has actually been exercised |
| Human capacity | The review queue can still absorb the expected exception volume |
| Customer approval | Documented decision by the customer's AI Council with a named accountable owner |
| Rollback plan | A tested procedure to return to L2 within one hour |

**Demotion is automatic and unemotional.** Defined signals — a false-action rate breach, an eval regression, a customer incident, or a model or data change without re-evaluation — return the agent to L2 immediately, without a meeting. The meeting happens afterwards. Making demotion automatic is what makes promotion safe.

---

## 2. Fleet governance

### 2.1 The fleet management problem

At 100 tenants, the questions that must be answerable in seconds are:

1. Which blueprint version is each tenant running, of each agent?
2. Which tenants are on a version with a known defect?
3. Which tenants have drifted from their declared configuration?
4. Which tenants are failing their SLOs, and why?
5. Which tenants are approaching a cost or quota limit?
6. Which tenants have agents at an autonomy level their evidence no longer supports?
7. If a model is deprecated in 90 days, which tenants are affected and what is the migration path?

The **Fleet Manager** exists to answer these. It is a control-plane service holding an inventory of tenants, their deployed versions, their configuration hashes, their health, and their rollout ring assignment.

### 2.2 Ring-based rollout

Every blueprint and platform change moves through rings. No exceptions, including for "urgent" fixes — an urgent fix that breaks 200 tenants is worse than the defect it fixed.

| Ring | Population | Soak | Purpose |
|---|---|---|---|
| **R0** | Habagat's own internal tenant | 3 days | Dogfooding. Habagat runs its own operations on its own agents |
| **R1** | Design partners (3–5 tenants, contractually opted in) | 5 days | Real data, real workflows, tolerant customers |
| **R2** | Early adopters (~20% of fleet) | 7 days | Statistical confidence at scale |
| **R3** | General fleet | — | Remainder |

Advancement between rings requires: no SLO regression, no eval regression, no new error classes, and no unexplained cost movement. Advancement is a decision the Fleet Manager proposes with the evidence and a human confirms.

### 2.3 Drift detection and remediation

| Drift type | Detection | Response |
|---|---|---|
| **Infrastructure drift** | Terraform plan run continuously against every tenant | Auto-revert for non-breaking; ticket + human for breaking |
| **Configuration drift** | Config hash comparison against the declared state | Auto-revert; investigate why it changed |
| **Version drift** | Fleet inventory versus target version map | Scheduled upgrade into the appropriate ring |
| **Policy drift** | Azure Policy compliance state per tenant | Deny effects prevent most; remediation tasks for the rest |
| **Prompt/spec drift** | Spec hash verification at harness startup — a modified spec fails to load | Hard fail. This is the zero-snowflake rule enforced at runtime |
| **Eval drift** | Scheduled re-evaluation against the current corpus | Regression → automatic autonomy demotion + alert |
| **Data drift** | Input distribution monitoring against the corpus baseline | Investigate; the corpus may need extending, which is the usual cause |
| **Model drift** | Provider model version changes | Re-evaluate before adopting; pin versions explicitly and never float |

> **Model version pinning is non-negotiable.** A silently updated model is an unevaluated change to a system a customer relies on. Habagat pins model versions per blueprint per tenant, evaluates new versions in R0/R1, and migrates deliberately. A customer must never be surprised by a model upgrade.

### 2.4 Fleet SLOs

| Metric | Target | Consequence of breach |
|---|---|---|
| Agent-run success rate | ≥ 99.0% (excluding correct policy denials) | Page on-call |
| Harness availability | ≥ 99.9% per tenant | Incident |
| P95 run latency, interactive | ≤ 8s | Investigation |
| Time to detect a failing tenant | ≤ 5 min | Fleet observability defect |
| Configuration compliance | 100% of tenants matching declared state | Blocks all fleet rollouts |
| Eval currency | Every agent evaluated within 30 days | Automatic autonomy freeze |
| Isolation canary | 100% pass | **P1 incident, all rollouts halted** |

---

## 3. Change management

| Change type | Approval | Rollout | Customer notice |
|---|---|---|---|
| Blueprint patch (prompt refinement, bug fix, no behaviour change) | Pod lead | R0→R3 over ~10 days | Release notes |
| Blueprint minor (new capability, same contract) | Agent Review Board | R0→R3 over ~14 days | 7 days' notice |
| Blueprint major (contract or behaviour change) | Agent Review Board + customer AI Council | Per-tenant, scheduled | 30 days' notice, customer schedules |
| Model version change | Agent Review Board with eval evidence | R0→R3 with per-ring re-evaluation | 14 days' notice |
| Autonomy change | Customer AI Council | Per-tenant | Explicit customer decision |
| Platform/infrastructure | Platform lead | R0→R3 | Notice if customer-visible |
| **Security patch (critical)** | Security lead, expedited | Accelerated rings, minimum soak preserved | Post-hoc notification within 24h |
| **Emergency kill switch** | Any on-call engineer | Immediate | Immediate notification |

### 3.1 Kill switches

Three levels, all tested quarterly. A kill switch that has never been exercised does not work.

1. **Agent kill switch** — disable one agent in one tenant. Sub-second. Available to the customer through their console, which is a significant trust signal.
2. **Blueprint kill switch** — disable an agent across the entire fleet. Used when a defect is found in R2/R3.
3. **Fleet freeze** — halt all rollouts and all autonomous action fleet-wide, dropping every agent to L1. Reserved for a security incident or a systemic quality failure.

---

## 4. Customer-facing governance

What the customer sees and controls is itself a product surface, and a competitive one.

| Capability | Delivery |
|---|---|
| **Agent inventory** | Every agent running in their tenant, its version, autonomy level, and what it is permitted to do |
| **Run explorer** | Search and inspect any run: what it did, why, what it changed, what it cost |
| **Approval queue** | The human-gate workflow, with SLA visibility |
| **Policy control** | Adjust autonomy (downward without approval, upward with the gate), value limits, and operating hours |
| **Kill switch** | Immediate disable, self-service |
| **Audit export** | Complete, tamper-evident activity export for the customer's own auditors |
| **Cost and usage** | Runs, cost and value delivered per agent |
| **Model card per agent** | What it does, its limitations, its evaluation results, its known failure modes, its human oversight design |
| **Incident history** | What went wrong, what was done, what changed as a result |

> **The model card is the sleeper feature.** Enterprise risk functions increasingly require documentation of every AI system in operation. Producing it automatically, per agent, per version, converts a compliance obligation into a reason to buy — and it is the artefact that gets Habagat past the second-line risk review that kills most AI vendors.

---

## 5. Regulatory alignment

| Framework | Habagat's position |
|---|---|
| **EU AI Act** | Habagat is a **provider** of AI systems; customers are **deployers**. Habagat maintains technical documentation, risk management, data governance records, logging, transparency information and post-market monitoring per Article 9–15 for high-risk blueprints, and supplies deployers with what they need for their own obligations. The prohibited list (§1.3) implements Article 5. |
| **ISO/IEC 42001** | The governance model in this document is designed to be certifiable against the AI management system standard. Target certification in year two — it is becoming a procurement checkbox. |
| **NIST AI RMF** | Govern / Map / Measure / Manage maps directly onto the Agent Review Board, risk classification, evaluation, and fleet operations. |
| **ISO 27001 / SOC 2** | Baseline security certifications. Year one. Non-negotiable for enterprise sales. |
| **GDPR and equivalents** | Habagat is a **processor** in each customer tenant. DPAs, sub-processor transparency, data-subject rights support (including memory inspection and deletion), and DPIA support for high-risk deployments. |
| **Sector regimes** | Model risk management (SR 11-7), GxP validation, HIPAA BAA, DORA, and public-sector requirements are handled as **compliance profiles** applied to a tenant at provisioning time — not as bespoke work. |

---

## 6. Incident management

| Severity | Definition | Response | Customer notification |
|---|---|---|---|
| **SEV-1** | Isolation breach, data exposure, agent caused material harm, fleet-wide outage | Immediate page; fleet freeze considered; exec involved | Within 1 hour |
| **SEV-2** | Single-tenant outage, agent producing systematically wrong output, security vulnerability | Page on-call; blueprint kill switch considered | Within 4 hours |
| **SEV-3** | Degraded performance, elevated escalation rate, cost anomaly | Business hours | Next business day |
| **SEV-4** | Individual run failure, isolated defect | Ticket | Release notes |

**Agent-specific incident classes** that standard IT incident processes do not cover, and which need their own runbooks:

- **Wrong action taken** — the agent did something it should not have. Immediate: contain, compensate, quantify scope across all tenants running that blueprint version, and notify. The scope question is the urgent one.
- **Systematic quality degradation** — outputs drifting worse without an outage. Detected by eval monitoring, not by alerts.
- **Escalation queue collapse** — the human gate is overwhelmed, so work is silently not being done. Detected by queue-age SLOs.
- **Prompt injection success** — an agent followed instructions from untrusted content. Treated as a SEV-1 security incident regardless of whether harm resulted.
- **Isolation canary failure** — customer data found in the control plane. Automatic SEV-1, automatic fleet freeze on rollouts.

Every SEV-1 and SEV-2 produces a blameless post-incident review, a fleet-wide check for the same class of defect, and — where relevant — a new case in the evaluation corpus. **The eval corpus is where incidents go to become permanent immunity**; an incident that does not produce an eval case will happen again.
