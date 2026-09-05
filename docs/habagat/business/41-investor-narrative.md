# Document 41 — Habagat Investor Narrative

> The story, the evidence and the ask. Written to be read by an investor and defended in diligence.
> Every claim here traces to a document in this corpus. Numbers are illustrative and labelled as such; the arithmetic is shown so it can be challenged.

---

## The one-paragraph version

Enterprises have spent two years discovering that the hard part of AI agents is not the model — it is operating them safely inside a regulated business. **Habagat builds vertical AI agents for specific enterprise workflows and operates them as a service inside each customer's own isolated Azure tenant.** We have catalogued 284 workflows across 20 industries where agents replace expensive, repetitive judgement work. We build each one once as an evaluated blueprint and instantiate it many times. Our defensibility is not model access — it is the evaluation corpus, the vertical domain blueprints, and the isolation fabric that lets us run hundreds of single-tenant deployments at close to multi-tenant cost.

---

## 1. The problem

Enterprise work is full of processes that are **triggered, multi-step, judgement-bearing, high-volume and verifiable** — precisely the profile that agents can now handle and that deterministic automation never could. RPA failed at these because they require interpretation. Humans do them because nothing else could.

The market has not been short of AI enthusiasm. It has been short of AI in production. The reasons are consistent across every enterprise we modelled:

1. **Nobody can prove the agent is right.** No evaluation corpus, so no basis for trusting it unattended.
2. **Nobody will accept the data risk.** Multi-tenant AI vendors fail the security review in regulated sectors.
3. **Nobody owns the operation.** A pilot ships; then it needs monitoring, improvement, incident response and governance, and no one is resourced for it.
4. **Regulation arrived before deployment did.** The EU AI Act and sector rules impose documentation and oversight obligations that a demo cannot satisfy.

Every one of these is an *operating* problem, not a *modelling* problem. That is the opening.

---

## 2. The solution

**Agent as a Service, single-tenant, on Azure AI Foundry.**

| | What Habagat does | Why it matters |
|---|---|---|
| **Build** | Vertical agent blueprints — versioned, evaluated, governed specifications for specific workflows | Built once, deployed many times. The margin structure |
| **Isolate** | One dedicated Azure tenant/subscription per customer. The control plane holds zero customer content, and this is continuously tested | Passes the security review that stops competitors. Isolation is the product |
| **Operate** | Habagat runs the fleet: deployment, monitoring, evaluation, incidents, improvement, governance | The customer buys an outcome with an SLA, not a toolkit and a hiring problem |
| **Prove** | An evaluation corpus per blueprint gates every release and every autonomy increase; model cards and evidence packs go to the customer | Converts "trust us" into documented evidence — which is what the risk function actually needs |

---

## 3. Why we win

Four assets. None of them is the model. All of them compound.

| Asset | What it is | Why it is hard to copy |
|---|---|---|
| **The Evaluation Corpus** | Graded cases per blueprint — happy path, edge, adversarial, and should-escalate — grown from human corrections and production incidents across every customer | Cannot be bought or synthesised. Requires production deployments across many enterprises over time. It is the single most valuable thing we own |
| **Vertical Blueprints** | 284 catalogued workflows, mapped to eight reusable archetypes, with domain grounding and regulatory constraints encoded | Requires domain expertise plus deployment experience. A generalist platform cannot produce it |
| **The Isolation Fabric** | The automation that provisions and operates hundreds of independent tenants without them becoming snowflakes | This is the operational moat. It is unglamorous, and it is the reason we can sell single-tenant profitably |
| **The Trust Layer** | Policy envelopes, deterministic verification, compensating actions, audit-grade tracing, model cards, governance apparatus | The part regulated buyers require and most vendors have not built |

**The honest answer to "isn't this a wrapper?"** A wrapper calls a model. Habagat computes an authorisation envelope before the model sees untrusted content, enforces deterministic rules the model cannot override, compensates partial multi-system writes, produces a regulator-grade trace of every action, and gates every autonomy increase on a versioned evaluation corpus. Remove the model and replace it with a different one — as our provider-neutral spec allows — and the product still exists. That is the test of whether the value is in the wrapper.

---

## 4. The market

| Layer | Sizing logic |
|---|---|
| **The work** | The 284 catalogued use cases represent workflows currently performed by salaried humans in essentially every mid-to-large enterprise |
| **Beachhead** | Financial services, insurance, healthcare administration and professional services — the four verticals with the highest density of documented, verifiable, high-volume judgement work and the greatest regulatory pressure that favours our architecture |
| **Expansion** | The remaining 16 industries in the catalogue, entered by building the vertical blueprint once and reusing it |
| **Wedge** | The 20 cross-industry agents (Document 01) sell into any company in any sector — the volume business that funds vertical depth |

**Bottom-up unit view (illustrative):** a Standard customer is ~$150,000 ARR growing to $400,000+ as agents are added. NRR above 130% means the installed base compounds without new logos. The catalogue exists precisely to make that expansion systematic rather than opportunistic.

---

## 5. Business model

| Component | Rationale |
|---|---|
| **Platform fee** (per tenant/month) | Covers the real fixed cost of an isolated environment. We state this openly — single-tenant has a floor, and pricing that ignores it loses money |
| **Agent subscription** (per agent/month) | Monetises the blueprint and its evaluation corpus — the intellectual property |
| **Agent-run fees** | Aligns price to value delivered |

**The margin story, stated honestly.** Year-one gross margin on a new customer is around **48%**. It rises to **65–72%** as agents are promoted from L2 (human reviews every output) to L3 (agent acts within a policy envelope). In our cost model, **human review is roughly 50% of COGS and inference roughly 18%** — so the margin lever is autonomy, not tokens.

**This makes the key operating metric unusually clear: the L3 promotion rate across the fleet.** It is the number we manage the company by, and the number we would ask a board to hold us to.

---

## 6. Go-to-market

**Land narrow, prove hard, expand fast.**

1. **Paid 90-day pilot**, two horizontal agents, against a workflow with an existing measured baseline. We charge for pilots — free pilots have no sponsor and no urgency.
2. **Prove with the customer's own numbers**: cost per transaction, cycle time, error rate.
3. **Land** an annual contract at 3–6 agents.
4. **Expand** at 2–3 agents per quarter, using the customer's own process data to identify where the value is (use case X20).

**Distribution advantage:** because Habagat deploys into the customer's own Azure subscription, every deal grows that customer's Azure consumption. This aligns Microsoft's field organisation with our growth and makes co-sell genuinely productive rather than nominal. Marketplace transactability lets customers buy against committed Azure spend, which shortens procurement materially.

---

## 7. Traction plan — what we will prove, in order

| Milestone | Evidence produced | Why an investor should care |
|---|---|---|
| **First 3 design partners live** | Agents in production at L2; measured baselines | Proves the delivery model and the 10-day claim |
| **First L3 promotion** | Documented promotion gate: eval results, shadow-mode agreement, false-action rate | **The single most important early proof point — it is the margin thesis made real** |
| **Second customer on the same blueprint** | Delivery cost for customer two versus customer one | Proves the reuse economics; the number should fall by more than half |
| **10 tenants under fleet management** | Zero configuration drift; ring rollout executed; isolation canary clean | Proves the operational moat and that single-tenant scales |
| **SOC 2 Type II + ISO 27001** | Certifications | Unlocks enterprise pipeline; removes the largest procurement blocker |
| **First vertical blueprint deployed at three customers** | Blueprint economics and corpus growth | Proves the compounding-asset thesis |
| **NRR above 130% on the first cohort** | Cohort expansion data | Proves the business model |

---

## 8. The team we need

The first ten hires, in order, with the reasoning:

1. **Founding Platform Engineer** — the harness. Everything depends on it.
2. **Agent Engineer** — the first blueprints.
3. **Evaluation Engineer** — hired *early*, because the corpus is the moat and retrofitting it is far harder than building it in.
4. **Solutions Architect** — owns customer onboarding and the 10-day commitment.
5. **Infrastructure/SRE Engineer** — the isolation fabric and fleet operations.
6. **Domain SME (beachhead vertical)** — the vertical depth competitors lack.
7. **Enterprise Account Executive** — with regulated-industry credibility.
8. **Head of AI Safety & Governance** — reporting independently of delivery. This is a structural requirement, not a title.
9. **Second Agent Pod** (engineer + SME) — scales delivery.
10. **Customer Success Lead** — owns NRR, which owns the business model.

---

## 9. Risks we would raise ourselves

An investor will find these. Better that we name them first.

| Risk | Our position |
|---|---|
| **Autonomy may stall at L2** | This is the central risk to the margin thesis. It is why evaluation is funded before sales, and why the L3 promotion rate is the metric we report every board meeting |
| **Fleet entropy would kill the model** | Enforced from customer one by the zero-snowflake rule in CI. Cheap to prevent, impossible to reverse |
| **Microsoft could build this** | They build platforms; we build vertical depth, evaluation corpora and operations. We drive their consumption, which makes us worth more to them as a partner than as a target. We accept this risk consciously |
| **Single-tenant costs more** | It does. It is also why we can sell into regulated sectors at all. The platform fee covers the floor, and we do not sell below it |
| **Agent-caused harm** | Contained by blast-radius design, human gates and compensating actions; managed by insurance and contractual caps; never eliminated |
| **We are concentrated on Azure** | Deliberate. The hedge is at the specification layer, tested quarterly, and would make a provider change a quarter of work rather than a rebuild |

---

## 10. What this corpus contains

The research and planning behind this narrative, available in full for diligence:

| Documents | Content |
|---|---|
| **00–21** | Research method, agent taxonomy, 20 cross-industry use cases, and 264 industry use cases across 20 industries — each with trigger, workflow, systems, KPIs and human gates |
| **30–36** | Reference architecture, the harness, per-tenant Azure landing zone, governance and fleet management, security and compliance, Azure services, and the evaluation framework |
| **CTO 01–06** | Technical strategy, engineering org, platform SDLC, model strategy and unit economics, technical due diligence pack, and the eight-quarter roadmap |
| **40–41** | Business model, go-to-market, and this narrative |
| **50** | The Software Architect Agent prompt — how the application architecture is produced next |

> **The point of the corpus.** Habagat is not asking an investor to believe that agents are valuable. It is showing 284 specific workflows, the architecture to deliver them safely, the economics of doing so, and the honest arithmetic of where the margin comes from and what would have to be true for it to fail.
