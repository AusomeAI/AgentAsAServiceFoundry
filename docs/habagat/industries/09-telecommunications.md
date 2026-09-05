# Document 09 — Telecommunications

> 13 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Telcos have the highest transaction volumes in the catalogue and the thinnest margins per transaction. This makes them the **best proving ground for agent unit economics** — and the most punishing if the cost model is wrong.
- Two agents dominate the business case: **TEL-01 Customer Care & Order Support** (contact cost is the single largest opex line after network) and **TEL-06 Network Fault Diagnosis** (drives both cost and the churn-causing experience).
- Telcos are also *selling* AI to their own enterprise customers. Habagat should treat them as a **channel partner opportunity**, not only an end customer — a telco with 5,000 enterprise accounts is a distribution asset.
- The recurring failure mode in telco automation is **order-fall-out**: complex product catalogues and legacy stacks mean a large share of orders fail mid-flight. An agent that resolves fall-out is worth more than one that takes orders.

---

### TEL-01 — Customer Care, Billing & Order Support
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Enormous contact volumes on billing, plan changes, service faults and device issues; complex catalogues make accurate answers hard even for trained agents.
**Trigger** — Customer contacts via app, chat, IVR, or store.
**Workflow** — 1) Authenticate to the assurance level required by the requested action. 2) Classify intent, detecting the common multi-intent contact ("my bill is wrong and my data isn't working"). 3) Assemble account truth: plan, add-ons, contract term and end date, device, billing history, usage, and open orders and faults. 4) For billing, decompose the bill into base charges, usage overage, one-off charges, pro-rations from mid-cycle changes, and promotions that expired — **pro-ration and expired promotions cause most billing contacts** and are the hardest for humans to explain. 5) For service issues, run diagnostics against the network and device, and hand to TEL-06 where a network fault is indicated. 6) Execute within policy: plan changes, add-on activation, bill adjustments within threshold, SIM actions, and appointment booking. 7) Detect churn risk from contract position, sentiment and behaviour, and route to retention where value justifies it. 8) For sales intent, check eligibility and present accurate, complete pricing including contract implications.
**Systems** — CRM, billing/BSS, order management, network diagnostics, device management, retention systems.
**Outcome & KPIs** — Containment/auto-resolution rate; cost per contact; repeat contacts within 7 days; CSAT; adjustment leakage; churn saves.
**Human gate** — Retention offers above threshold, complaints, contract disputes, and vulnerability indicators.

### TEL-02 — Order Fall-Out Management
**A5 · L3 · B3 · Order-to-cash**
**Pain** — A significant share of orders fail somewhere between sale and activation — address validation, port-in mismatch, credit check, network provisioning, appointment failure. Each failure is a manual investigation across systems, and the customer is left waiting.
**Trigger** — Order fails at any stage in the fulfilment chain.
**Workflow** — 1) Detect the failure and identify the failing step and system precisely. 2) Diagnose the true cause, which is frequently upstream of where the failure surfaced: bad address data, mismatched port-in details, catalogue configuration error, stock unavailability, or a downstream system timeout. 3) Classify as auto-recoverable, data-fixable, or blocked. 4) **Auto-recover where safe**: retry transient failures, correct address formats against the authoritative address database, resolve catalogue configuration conflicts using the ordering rules. 5) For data mismatches requiring customer input (port-in account number, ID verification), generate a specific, plain-language request rather than a generic "there was a problem". 6) For blocked orders, assemble the case for the fall-out team with the diagnosis and recommended action. 7) Keep the customer informed with accurate expectations at every state change. 8) Report fall-out causes upstream — the compounding win, because most fall-out is caused by a fixable defect in ordering or catalogue.
**Systems** — Order management, BSS/OSS, provisioning, inventory, address database, number portability systems, CRM.
**Outcome & KPIs** — Fall-out rate; auto-recovery rate; order cycle time; orders cancelled due to fall-out; repeat fall-out causes eliminated.
**Human gate** — Credit decisions, identity verification failures and fraud-flagged orders.

### TEL-03 — B2B Quote, Design & Contract Support
**A3 · L2 · B3 · Demand creation**
**Pain** — Enterprise connectivity quotes require site surveys, network reach checks, design and pricing across dozens of sites. Quote cycles of 2–6 weeks lose deals.
**Trigger** — Enterprise RFQ or opportunity with a site list.
**Workflow** — 1) Parse the site list and requirements: bandwidth, resilience, SLA, technology preference, and timing. 2) For each site, determine network reach and available access technologies from the inventory and third-party reach data — the step that dominates quote time. 3) Identify sites requiring build, and estimate build cost and lead time. 4) Design the solution: access, aggregation, resilience topology, and managed services, applying the standard design patterns. 5) Price it: recurring and one-off charges, third-party access costs, build contribution, and margin against the pricing framework. 6) Identify commercial risk: onerous SLA requirements, penalty exposure, long build lead times, and third-party dependencies. 7) Generate the proposal with the solution description, pricing and assumptions. 8) Track win/loss with the reasons and feed pricing and reach data back.
**Systems** — Network inventory, reach/serviceability databases, CPQ, design tools, third-party carrier portals, CRM.
**Outcome & KPIs** — Quote cycle time; sites quoted per day; win rate; margin realised vs quoted; build-cost estimate accuracy.
**Human gate** — Solution architects approve designs; commercial approval for pricing and non-standard terms.

### TEL-04 — Network Capacity Planning & Optimisation
**A6 · L2 · B3 · Plan-to-produce**
**Pain** — Capacity investment must anticipate traffic growth by cell, node and link. Over-build wastes capital; under-build causes congestion and churn in exactly the places customers notice.
**Trigger** — Planning cycle, or a utilisation threshold breach.
**Workflow** — 1) Analyse traffic by element, time and service, decomposing growth into subscriber growth, usage-per-subscriber growth, and traffic-mix shift. 2) Forecast utilisation by element with confidence bounds, incorporating known events (new housing developments, venue openings, competitor exits). 3) Identify elements approaching congestion and the timing, translating utilisation into **customer experience impact** — that translation is what makes the business case. 4) Evaluate options: parameter optimisation, spectrum re-farming, carrier addition, cell split, small cells, backhaul upgrade, or new site. 5) Model cost, lead time and experience improvement per option. 6) Prioritise investment by customers affected and revenue at risk. 7) Generate the capacity plan with the evidence. 8) Verify realised improvement after implementation and recalibrate.
**Systems** — Network performance management, traffic analytics, planning tools, GIS, inventory, customer experience data.
**Outcome & KPIs** — Congested-element hours; capex efficiency; forecast accuracy; experience improvement per investment; congestion-related complaints and churn.
**Human gate** — Network planners and RF engineers own all design decisions; capital allocation is governed.

### TEL-05 — Field Engineering Dispatch & Installation
**A5 · L3 · B3 · Issue-to-resolution**
**Pain** — Installation and repair visits are expensive; failed appointments (customer not home, wrong skills, missing equipment, work not actually needed) are common and destroy both cost and satisfaction.
**Trigger** — Order requiring installation, or a fault requiring a visit.
**Workflow** — 1) Determine whether a visit is genuinely required — remote diagnostics and configuration resolve a meaningful share of "faults", and the avoided visit is the largest saving available. 2) Determine job requirements: skills, equipment, expected duration, access needs, and whether third-party access (building owner, road opening permit, other operator) is required. 3) Verify prerequisites before booking, especially third-party dependencies, which are the top cause of aborted visits. 4) Offer appointments optimised for engineer routing and customer preference, with honest duration estimates. 5) Confirm and remind, and re-confirm shortly before to reduce not-at-home failures. 6) Brief the engineer with the diagnosis, site history, network configuration and safety information. 7) Support the engineer during the job with configuration, diagnostics and escalation. 8) Verify service is working before the job is closed, and capture as-built records. 9) Analyse abort and repeat-visit causes.
**Systems** — Field service management, OSS/provisioning, network diagnostics, inventory, appointment systems, mobile app.
**Outcome & KPIs** — Right-first-time rate; aborted visits; jobs per engineer per day; avoided dispatch rate; appointment adherence; repeat visits within 30 days.
**Human gate** — Safety-related work follows formal procedure; complex installations are engineer-designed.

### TEL-06 — Network Fault Diagnosis & Service Assurance
**A6 · L3 · B3 · Issue-to-resolution**
**Pain** — Alarms cascade: one root fault generates hundreds of downstream alarms across layers. Correlating them and finding the true cause is expert work under pressure, and customer impact is invisible until customers call.
**Trigger** — Alarm raised, performance degradation detected, or a cluster of customer reports.
**Workflow** — 1) Correlate alarms across layers (transport, IP, radio, service) and topology into a single root-cause hypothesis rather than an alarm list. 2) Enrich with topology, recent changes, planned work, environmental data and power status — **recent change is the most common cause and the first thing to check**. 3) Determine customer and service impact: which customers, which services, which enterprise SLAs, and which critical customers. 4) Diagnose using the fault-domain playbook, running read-only diagnostics to confirm or refute the hypothesis. 5) Execute pre-authorised, reversible remediation where the diagnosis is confident: service restart, path reroute, parameter reset. 6) Where physical intervention is needed, generate the work order with the diagnosis and required parts. 7) Notify affected enterprise customers proactively against their SLA commitments. 8) Produce the incident record and, for major incidents, the post-incident review pack. 9) Feed recurring faults into problem management.
**Systems** — Fault/performance management, network inventory and topology, change management, ticketing, customer service inventory, orchestration.
**Outcome & KPIs** — MTTR; alarm-to-ticket compression ratio; root-cause accuracy; customer-impacting minutes; SLA breaches; proactive notification rate.
**Human gate** — Any change affecting live traffic beyond the pre-authorised reversible set requires network-operations authorisation. Major incidents are human-commanded.

### TEL-07 — Fraud, Revenue Assurance & Leakage
**A6 · L2 · B3 · Risk-to-assurance**
**Pain** — Revenue leakage (unbilled usage, rating errors, provisioning-billing mismatches) typically runs 1–3% of revenue; fraud (subscription fraud, SIM swap, IRSF, wangiri) is fast-moving and expensive.
**Trigger** — Continuous monitoring of usage, provisioning and billing data.
**Workflow** — 1) Reconcile the chain end to end: network usage records → mediation → rating → billing → payment, identifying volume and value discrepancies at each hop. 2) Diagnose leakage causes: unrated records, incorrect tariffs, services provisioned but not billed, and promotions never expiring. 3) Detect fraud patterns: usage inconsistent with the subscriber profile, international premium-rate patterns, velocity anomalies at activation, and **SIM-swap sequences that precede account takeover** — the highest-harm fraud in telco because it defeats bank SMS authentication. 4) Score and prioritise by value and confidence, with a strong bias against false positives on legitimate customers. 5) Execute protective actions within policy for high-confidence fraud: rate limits, barring of premium destinations, and verification challenges. 6) Assemble investigation cases with the evidence chain. 7) Quantify recovered and prevented leakage, and route systemic causes to the responsible system owner.
**Systems** — Mediation, rating/billing, network usage records, provisioning, fraud management, revenue assurance platform.
**Outcome & KPIs** — Leakage identified and recovered; fraud loss prevented; false-positive rate on customer actions; time to detect a new fraud pattern; systemic defects fixed.
**Human gate** — Account suspension, customer accusation, and law-enforcement referral are human decisions with legal oversight.

### TEL-08 — Churn Prediction & Retention Orchestration
**A7 · L2 · B3 · Order-to-cash**
**Pain** — Retention offers are made too late, to the wrong customers, at the wrong price — often to customers who were never going to leave, which is pure margin destruction.
**Trigger** — Churn-risk score change, contract-end approach, or a trigger event (complaint, outage, competitor promotion, roaming bill shock).
**Workflow** — 1) Score churn risk from behaviour, experience, contract position, competitive context and service events. 2) Identify the **cause** of risk, not just its level: price, experience, coverage, device age, competitor offer, or a specific bad event. The cause determines the intervention, and a discount aimed at a coverage problem is wasted. 3) Estimate customer lifetime value and the value at risk. 4) **Estimate offer incrementality** — would this customer have stayed anyway? This is the discipline that separates a retention programme from a margin leak, and it requires holdout testing. 5) Select the intervention: fix the underlying problem (often cheaper and more durable than a discount), device upgrade, plan optimisation, or targeted offer. 6) Execute through the right channel with the right timing. 7) For inbound cancellation attempts, brief the retention agent with the full picture and the authorised offer range. 8) Measure retention effect against holdouts continuously.
**Systems** — CDP/analytics, CRM, billing, network experience data, offer management, campaign execution.
**Outcome & KPIs** — Churn rate; **incremental retention vs holdout**; retention cost per save; margin retained; problem-fix vs discount ratio.
**Human gate** — Offer policy and discount authority are commercially governed; the agent operates within an approved offer matrix.

### TEL-09 — Spectrum, Site & Infrastructure Asset Management
**A8 · L2 · B3 · Plan-to-produce**
**Pain** — Operators manage tens of thousands of sites with leases, permits, power contracts, structural constraints and regulatory obligations. Costs leak through unclaimed rate reductions, over-paid leases and unused capacity.
**Trigger** — Lease event, site change, audit cycle, or a regulatory obligation.
**Workflow** — 1) Maintain the site record: lease terms, rent review dates, break clauses, permits, structural capacity, power supply, and co-location tenants. 2) Reconcile lease payments against terms and detect overpayment, duplicate payment and unapplied rent reductions — a routine and material recovery. 3) Track obligations: permit renewals, structural inspections, EMF compliance, planning conditions, and access agreements. 4) Manage lease events proactively: rent reviews, breaks and renewals with market benchmarking and a negotiating position. 5) Assess site capacity for new equipment against structural and power limits before deployment commits. 6) Identify co-location and site-sharing revenue opportunities and rationalisation candidates. 7) Support regulatory coverage and rollout obligation reporting with evidence.
**Systems** — Site/lease management, asset register, network inventory, GIS, finance/AP, regulatory reporting.
**Outcome & KPIs** — Lease cost per site; overpayments recovered; obligations met on time; site capacity utilisation; co-location revenue; rollout obligation compliance.
**Human gate** — Lease negotiations and property decisions are commercial; structural assessments require qualified engineers.

### TEL-10 — Regulatory Compliance & Reporting
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Telcos face dense regulation: coverage and quality reporting, number portability, lawful intercept, emergency services, consumer protection, and data retention — each with its own evidence requirements.
**Trigger** — Reporting deadline, regulatory change, or a compliance event.
**Workflow** — 1) Maintain the obligations register mapped to systems, owners and evidence sources. 2) Assemble reporting data with lineage: coverage measurements, quality metrics, complaint statistics, porting performance, and outage reporting. 3) Validate against the regulator's definitions, which frequently differ from internal metrics. 4) Monitor compliance continuously against thresholds and alert before breach — for example, porting completion times and emergency-call performance. 5) Assess regulatory changes for impact on products, systems and processes. 6) Manage consumer-protection obligations: contract transparency, price-rise notification, and switching processes. 7) Generate submissions and manage regulator queries. 8) Track commitments and remediation.
**Systems** — Network performance data, BSS, complaint systems, porting systems, regulatory reporting tools, obligations register.
**Outcome & KPIs** — Submission timeliness and accuracy; compliance breaches; regulatory penalties; time to assess a regulatory change; obligation coverage.
**Human gate** — All regulatory submissions are attested by the accountable executive; lawful-intercept processes are strictly access-controlled and outside agent scope.

### TEL-11 — Digital Channel & Self-Service Optimisation
**A6 · L1 · B2 · Demand creation**
**Pain** — Self-service channels are built and then not improved; customers fail at specific journey steps and fall into expensive assisted channels, and nobody knows exactly where or why.
**Trigger** — Continuous journey analytics, or a release.
**Workflow** — 1) Reconstruct customer journeys across app, web, IVR and assisted channels, linking sessions to outcomes and subsequent contacts. 2) Identify failure points where customers abandon or escalate, quantified by volume and downstream cost. 3) Diagnose causes: usability, missing capability, unclear content, technical error, or a policy that forces escalation. 4) **Correlate digital failure with contact-centre volume** to price each defect — this converts UX findings into a funded backlog. 5) Recommend fixes with expected deflection and revenue impact. 6) Generate and test content improvements for the highest-volume failure points. 7) Monitor releases for regression in journey completion. 8) Report channel-shift progress against the target.
**Systems** — Digital analytics, session capture, CRM/contact data, app/web platforms, content management, A/B testing.
**Outcome & KPIs** — Journey completion rate; digital containment; contacts generated per digital failure; cost avoided; regression detection time.
**Human gate** — Product owners prioritise; UX and content changes go through normal release governance.

### TEL-12 — Wholesale & Interconnect Settlement
**A8 · L3 · B3 · Record-to-report**
**Pain** — Interconnect, roaming and wholesale settlement involves complex rate structures across many partners; disputes are common, slow and expensive, and errors persist for months.
**Trigger** — Settlement period, partner invoice received, or a dispute raised.
**Workflow** — 1) Rate traffic against the applicable agreement terms per partner, route and service, including tiered and committed-volume structures. 2) Reconcile own records against partner statements at the detail level, identifying volume, rate and routing discrepancies separately. 3) Diagnose discrepancy causes: record loss, routing differences, rate-table version mismatch, timing, or genuine disagreement on terms. 4) Generate dispute submissions with the evidence, and process incoming disputes with the same rigour. 5) Track dispute ageing and value, escalating on the ones that matter. 6) Verify agreement terms are correctly implemented in the rating configuration — a surprising proportion of leakage is a mis-keyed rate table. 7) Forecast settlement positions and support commercial negotiation with traffic and margin analysis.
**Systems** — Interconnect billing, mediation, partner agreements repository, dispute management, finance.
**Outcome & KPIs** — Settlement accuracy; dispute value and ageing; disputes resolved in own favour; rate-configuration defects found; settlement cycle time.
**Human gate** — Commercial negotiation and dispute settlement above threshold are human.

### TEL-13 — Security Operations for Network & Subscriber Protection
**A6 · L3 · B3 · Risk-to-assurance**
**Pain** — Telcos are both a target and a vector: signalling attacks, DDoS, subscriber-targeted fraud and scam traffic. Volumes make manual analysis impossible.
**Trigger** — Security alert, traffic anomaly, or an abuse report.
**Workflow** — 1) Detect anomalies across signalling (SS7/Diameter), IP traffic, and subscriber behaviour. 2) Correlate with threat intelligence and known attack signatures, and with the operator's own historical incidents. 3) Assess impact and scope: which subscribers, which services, which network elements, and whether this is targeted or broad. 4) For scam and nuisance traffic, identify source patterns and assess blocking options against the risk of blocking legitimate traffic — false positives here block real people's calls. 5) Execute pre-authorised mitigations: rate limiting, filtering, and blocking of confirmed malicious sources. 6) Protect subscribers: detect and warn on SIM-swap and account-takeover patterns, coordinating with TEL-07. 7) Assemble incident records and regulatory notifications where required. 8) Feed patterns into detection improvement and into industry intelligence sharing where permitted.
**Systems** — Signalling firewalls, DDoS mitigation, SIEM, subscriber data, threat intelligence, abuse-report channels.
**Outcome & KPIs** — Time to detect and mitigate; subscriber harm prevented; false-positive blocking rate; incident volume trend; regulatory notification compliance.
**Human gate** — Large-scale blocking, anything affecting emergency services, and lawful-intercept-adjacent matters are human-authorised. Subscriber content is never accessed.

---
## Regulatory notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Communications privacy (ePrivacy, CPNI, LI regimes)** | Communication content is out of scope entirely. Metadata use is tightly purpose-bound and jurisdictionally constrained. Lawful intercept systems are isolated from all agent access. |
| **Emergency services obligations** | No agent action may degrade emergency call handling; this is a hard constraint on any traffic-affecting automation. |
| **Consumer protection & switching** | Price-change notification, contract transparency and porting timelines are hard-deadline obligations that agents must enforce, not merely report. |
| **Net neutrality** | Traffic management recommendations must comply with applicable neutrality rules; the agent must not propose discriminatory handling. |
