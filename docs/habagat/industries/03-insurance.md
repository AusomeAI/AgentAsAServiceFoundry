# Document 03 — Insurance

> 14 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Insurance is a **document-and-judgement industry with a P&L that responds instantly to cycle time and leakage**. Two points of claims leakage is often larger than the entire IT budget.
- The three agents that move the combined ratio most: **INS-04 Claims FNOL & Triage**, **INS-06 Claims Leakage Detection**, **INS-02 Submission Intake & Clearance**. Underwriters and adjusters do not need help writing; they need the file assembled.
- Underwriting appetite and claims denial stay human (L2). Everything upstream and downstream of those two decisions is automatable.
- Insurers buy on **loss ratio, expense ratio and cycle time** — Habagat should price against measured leakage reduction, which is the most credible ROI story in any vertical.

---

### INS-01 — Broker & Customer Enquiry Handling
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Service teams handle high volumes of policy, cover, endorsement and document requests; brokers wait days for answers that exist in the policy document.
**Trigger** — Email, broker portal message, or call.
**Workflow** — 1) Identify the policy and the enquirer's authority to receive information. 2) Classify intent: cover question, document request, mid-term adjustment, renewal query, claim status. 3) For cover questions, retrieve the **actual policy wording, schedule and endorsements for that specific policy version** — never a generic product summary; the endorsements are where the answer lives. 4) Determine whether the question can be answered factually from the wording or requires an underwriting judgement. 5) Generate a cited answer quoting the operative clause. 6) For document requests, produce and dispatch through the approved channel. 7) For adjustments, price within the auto-rateable envelope or route to underwriting. 8) Log to the policy file.
**Systems** — Policy admin, document management, rating engine, broker portal, CRM.
**Outcome & KPIs** — Response time; auto-answer rate; clause-citation accuracy; broker satisfaction; escalation precision.
**Human gate** — Any statement about whether a claim would be covered — that is a coverage opinion and must be human.

### INS-02 — Submission Intake, Clearance & Triage
**A2 · L3 · B2 · Demand creation**
**Pain** — Commercial insurers receive submissions as email + spreadsheet + PDF in a thousand formats. Underwriters spend hours on data entry before deciding whether they even want the risk. Low quote-to-bind ratios follow directly.
**Trigger** — Broker submission arrives by email or portal.
**Workflow** — 1) Classify the submission and identify the line of business and broker. 2) Extract the risk data: insured entity, operations, locations, values, limits, deductibles, loss history, current programme structure. 3) **Clearance** — check whether this risk is already in-house via another broker; a genuine commercial control that is done badly and manually today. 4) Appetite screening against the underwriting appetite matrix: class, geography, size, hazard, and current portfolio concentration. 5) Fast decline with a clear, respectful reason where out of appetite — the highest-value output, because it returns underwriter time to winnable business. 6) For in-appetite risks, enrich: property characteristics, catastrophe exposure, financial health, sanctions screening, adverse media, prior loss experience. 7) Generate the risk summary and completeness report, naming exactly what is missing and drafting the broker request. 8) Prioritise the underwriter's queue by expected value, not arrival order.
**Systems** — Underwriting workbench, policy admin, clearance database, catastrophe models, external data, document intelligence.
**Outcome & KPIs** — Submissions processed per underwriter; time-to-quote; quote-to-bind ratio; declination speed; data-capture accuracy; clearance conflicts detected.
**Human gate** — All appetite exceptions and all quotations.

### INS-03 — Underwriting Risk Assessment & Pricing Support
**A4 · L2 · B4 · Demand creation**
**Pain** — Underwriters must synthesise loss history, exposure data, external risk signals and portfolio context under time pressure, with inconsistent depth across the team.
**Trigger** — Submission cleared and in appetite.
**Workflow** — 1) Assemble the complete risk picture from submission, enrichment and internal history. 2) Analyse loss history: frequency, severity, trend, causation patterns, and whether the insured's controls have changed since the losses. 3) Retrieve comparable risks from the book with their pricing and subsequent loss experience — the underwriter's most valuable and least accessible reference. 4) Run the technical rating model and decompose the price into its drivers. 5) Portfolio impact: concentration by geography, peril, industry and cat aggregation; capital consumption. 6) Recommend terms — limits, deductibles, sub-limits, exclusions, warranties and risk-improvement conditions — grounded in the wording library. 7) Draft the underwriting rationale to file standard, which also satisfies audit and reinsurer review. 8) Underwriter decides, prices and quotes.
**Systems** — Rating engine, underwriting workbench, cat models, portfolio analytics, wording library, external risk data.
**Outcome & KPIs** — Underwriter throughput; pricing-consistency dispersion; rationale completeness; hit ratio; subsequent loss ratio on agent-supported vs baseline risks.
**Human gate** — **Pricing, terms and binding are always human.** Agent output is decision support with a documented rationale trail.

### INS-04 — First Notice of Loss (FNOL) & Claims Triage
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — FNOL quality determines the entire claim's cost. Poor intake means missed information, wrong routing, late investigation and inflated settlement.
**Trigger** — Claim reported by phone, app, portal, broker or telematics event.
**Workflow** — 1) Identify the policy and verify it was in force at the date of loss — the first and most consequential check. 2) Conduct structured intake adapted to the loss type; ask only the questions that matter for this peril, and ask them in the order that preserves the claimant's account. 3) Detect and respond to distress, injury or vulnerability immediately, with a human handoff and an appropriate tone. 4) Preliminary coverage assessment against the policy terms: is the peril insured, are exclusions potentially engaged, what is the deductible and limit? Present as *indicative*, never as a decision. 5) Complexity and reserve triage: fast-track, standard, complex or potential-litigation — routing to the right adjuster skill level at intake is worth more than any downstream optimisation. 6) Early fraud indicator scoring from the intake pattern, prior claims and network links. 7) Immediate service orchestration: assign the adjuster, instruct the surveyor/loss adjuster, arrange emergency mitigation, book the hire car, and set the initial reserve within policy bands. 8) Confirm to the claimant what happens next and by when.
**Systems** — Claims platform, policy admin, telephony/app, supplier network, fraud engine, reserving rules.
**Outcome & KPIs** — FNOL completeness; correct routing at first assignment; time to first contact; **claim cycle time and average cost by segment**; early fraud referral rate; claimant NPS.
**Human gate** — Coverage decisions, injury claims, fatalities, and any vulnerability indicator route immediately to a human.

### INS-05 — Claims Document Processing & Validation
**A2 · L3 · B3 · Issue-to-resolution**
**Pain** — Claims files accumulate invoices, estimates, reports, receipts and medical records; adjusters read them serially and inconsistently.
**Trigger** — Document received into the claim file.
**Workflow** — 1) Classify the document and attach it to the correct claim and event. 2) Extract structured content appropriate to type: repair estimate line items, invoice values, medical findings, adjuster report conclusions. 3) Validate internal consistency: does the estimate match the damage described, does the invoice match the approved estimate, do dates align with the loss date? 4) Cross-check against the policy: are the claimed items covered, within sub-limits, and above the deductible? 5) Benchmark costs against the insurer's own rates and market data; flag material deviations with specifics ("labour hours 40% above regional norm for this repair type"). 6) Detect duplicate submissions and previously-paid items. 7) Update the claim record and adjust the reserve recommendation. 8) Present the adjuster with a summary of what changed and what needs a decision.
**Systems** — Claims platform, document intelligence, estimating platforms (Audatex/Xactimate), medical coding, supplier rate tables.
**Outcome & KPIs** — Documents auto-processed; adjuster reading time saved; cost deviations detected; duplicate payments prevented; reserve accuracy.
**Human gate** — All payment authorisations; all medical-evidence interpretation affecting liability or quantum.

### INS-06 — Claims Leakage & Settlement Assurance
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Leakage — paying more than the policy and the facts require — typically runs 2–5% of claims spend. It is caused by missed recovery rights, unapplied deductibles, out-of-scope items, and inconsistent settlement practice, not by fraud.
**Trigger** — Claim reaches settlement recommendation, or continuous portfolio scan.
**Workflow** — 1) Re-derive the entitlement independently from policy terms, verified facts and the applicable jurisdiction's rules. 2) Compare against the proposed settlement and itemise every difference. 3) Test the standard leakage categories systematically: deductible application, sub-limits, betterment, depreciation, VAT/tax treatment, salvage value, **subrogation and recovery rights**, contribution from other policies, and scope creep beyond the damage. 4) Benchmark against comparable settled claims for the same peril, severity and region. 5) Check that all mandatory investigation steps were completed before settlement. 6) Produce a leakage report per claim with quantified findings and a recommended action. 7) Aggregate to identify systemic patterns by adjuster, supplier, region and peril — where the real money is. 8) Feed findings into supplier management and adjuster coaching.
**Systems** — Claims platform, policy admin, payment records, supplier data, benchmark analytics, recovery/subrogation system.
**Outcome & KPIs** — **Leakage identified and prevented ($)**; subrogation recovery rate; settlement dispersion for like claims; average claim cost trend; supplier cost variance.
**Human gate** — Settlement decisions remain with the adjuster; the agent's findings are advisory but tracked to disposition so patterns are visible.

### INS-07 — Fraud Detection & Investigation Support
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Fraud investigation units are small and swamped. Referrals are inconsistent; organised fraud rings are invisible from a single-claim view.
**Trigger** — Fraud score threshold at FNOL or during the claim lifecycle; or a network-level detection.
**Workflow** — 1) Score the claim against known fraud indicators for that peril, with the contributing factors made explicit. 2) **Network analysis:** link the claim to others through people, addresses, phones, bank accounts, vehicles, suppliers and repairers — organised fraud is a graph problem, not a claim problem. 3) Timeline reconstruction across all evidence, looking for inconsistencies between statements, documents and external data. 4) External corroboration within legal limits: prior claims databases, public records, permitted open-source checks. 5) Assess alternative innocent explanations explicitly, and weight them fairly — this discipline is what keeps referral precision acceptable. 6) Build the investigator's case file: indicators, evidence, network map, and specific recommended investigation steps. 7) Feed confirmed outcomes back into detection tuning.
**Systems** — Fraud analytics, claims platform, industry fraud databases, graph analytics, public records, case management.
**Outcome & KPIs** — Referral precision; fraud identified ($); investigation cycle time; false-accusation rate (critical guardrail); network rings detected.
**Human gate** — **All fraud determinations are human.** No claim is ever declined, delayed or referred to law enforcement on agent output alone. Bias monitoring across protected characteristics is mandatory and reported.

### INS-08 — Subrogation & Recovery Identification
**A6 · L3 · B2 · Order-to-cash**
**Pain** — Recovery rights are missed at scale because identifying them requires reading the file carefully at the moment of settlement, and adjusters are measured on closing claims.
**Trigger** — Claim settled or reserved above threshold; or a portfolio sweep of closed claims.
**Workflow** — 1) Analyse the loss facts to identify potentially liable third parties: other drivers, contractors, product manufacturers, property owners, other insurers. 2) Assess the legal basis and the strength of the recovery case under the applicable jurisdiction. 3) Check limitation periods and flag anything approaching expiry — pure, immediate, recoverable money. 4) Quantify the recoverable amount including the insured's deductible. 5) Assemble the recovery pack: evidence, liability analysis, quantum, and the demand letter draft. 6) Route to the recovery team or the appointed panel with a priority score by expected value. 7) Track recovery progress and outcomes; report realised recovery rate by category.
**Systems** — Claims platform, document store, legal panel management, recovery ledger.
**Outcome & KPIs** — Recovery opportunities identified; recovery rate as % of paid claims; time-barred losses (target zero); average recovery cycle; net recovery after cost.
**Human gate** — Legal proceedings and settlement of recovery claims are human/legal decisions.

### INS-09 — Policy Servicing & Mid-Term Adjustments
**A5 · L3 · B3 · Order-to-cash**
**Pain** — Endorsements, address changes, vehicle swaps and cover changes are high-volume, low-value transactions that still consume service capacity and generate errors.
**Trigger** — Customer or broker requests a change.
**Workflow** — 1) Authenticate and confirm authority to instruct. 2) Interpret the requested change and identify every policy element affected — the failure mode is changing one field and missing the dependent ones. 3) Check underwriting acceptability: is the changed risk still within auto-acceptance rules? 4) Rate the change and compute the premium adjustment including any fees, with a clear breakdown. 5) Check for **material-fact implications**: a change that reveals a previously undisclosed circumstance must be routed to underwriting, not processed. 6) Execute the endorsement in the policy system with the correct effective date. 7) Generate and issue the endorsement documents and updated schedule. 8) Handle the payment or refund per policy.
**Systems** — Policy admin, rating engine, document generation, payments, broker portal.
**Outcome & KPIs** — Straight-through endorsement rate; processing time; error/rework rate; premium-leakage on adjustments; customer effort score.
**Human gate** — Material-fact issues, risk-profile changes beyond auto-acceptance, and cancellations.

### INS-10 — Renewal Preparation & Retention
**A3 · L2 · B3 · Order-to-cash**
**Pain** — Renewals are worked in date order rather than value order; underwriters re-underwrite from scratch; at-risk accounts are identified after they leave.
**Trigger** — Renewal date approaching (per line-of-business lead time).
**Workflow** — 1) Assemble the renewal picture: exposure changes, claims experience, payment behaviour, service history, and any mid-term changes. 2) Re-rate technically and compare against the expiring premium; decompose the rate change into exposure, experience and rate-level effects so it can be *explained to the customer*. 3) Predict retention risk from experience, price movement, market conditions and service events. 4) Recommend a strategy per account: renew as-is, re-term, re-price, restructure, or non-renew — with the technical justification. 5) Assemble the broker/customer renewal pack with the story of the year. 6) For at-risk valuable accounts, generate a specific retention plan and brief the account handler in advance. 7) Track renewal outcomes and calibrate the retention model.
**Systems** — Policy admin, claims history, rating engine, CRM, market data, document generation.
**Outcome & KPIs** — Retention rate by segment; renewal cycle time; rate adequacy achieved; at-risk accounts saved; underwriter hours per renewal.
**Human gate** — Non-renewal decisions, material rate increases and all quoted terms.

### INS-11 — Regulatory & Conduct Compliance Monitoring
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Conduct regimes require insurers to evidence fair value, appropriate distribution and good customer outcomes continuously — obligations most insurers meet with periodic manual reviews.
**Trigger** — Continuous monitoring, product-review cycle, or a conduct-metric breach.
**Workflow** — 1) Monitor outcome metrics by product and customer segment: claims acceptance rates, complaint rates, cancellation rates, claims ratios, and time-to-settle. 2) Test **fair value**: is the price paid proportionate to the benefits delivered, by segment and distribution channel? Where it is not, identify which segment and which channel. 3) Detect disparate outcomes across customer groups, including vulnerable-customer cohorts. 4) Test distribution: are products reaching the defined target market, and are commissions consistent with fair value? 5) Review sales and claims communications for clarity and compliance with mandated content. 6) Produce the product-governance report with findings and quantified affected populations. 7) Track remediation to closure.
**Systems** — Policy admin, claims, complaints, distribution/commission data, product governance repository, BI.
**Outcome & KPIs** — Products with current fair-value assessment; outcome disparities identified; remediation cycle time; complaints trend; regulatory findings.
**Human gate** — Fair-value conclusions and product interventions are governance-committee decisions.

### INS-12 — Reinsurance Administration & Recovery
**A5 · L2 · B3 · Record-to-report**
**Pain** — Reinsurance treaty application, cession calculation and recovery collection are complex, spreadsheet-driven and error-prone; recoveries are under-claimed.
**Trigger** — Policy bound (cession), claim reserved/paid (recovery), or a reporting period close.
**Workflow** — 1) Determine which treaties apply to a given policy or claim from the treaty terms, inception dates, class and territory definitions. 2) Compute cessions and retentions per treaty structure (quota share, surplus, XoL layers), including reinstatements. 3) On claims, identify every recovery available across treaties and facultative placements, including aggregate and clash covers. 4) Assemble the recovery claim with the required evidence per the treaty's notification and proof requirements. 5) Track notification deadlines — missing them forfeits recovery. 6) Reconcile reinsurer accounts, chase overdue balances, and age the recoverables. 7) Produce the reinsurance reporting for finance and regulatory returns.
**Systems** — Reinsurance system, policy admin, claims, GL, treaty documents, broker statements.
**Outcome & KPIs** — Recoveries identified and collected; recoverable ageing; notification-deadline compliance; reconciliation differences; manual effort per cycle.
**Human gate** — Treaty interpretation disputes and commercial negotiations with reinsurers.

### INS-13 — Actuarial Data Preparation & Reserving Support
**A3 · L1 · B3 · Record-to-report**
**Pain** — Actuaries spend the majority of a reserving cycle preparing and validating data rather than exercising actuarial judgement.
**Trigger** — Reserving cycle, or a quarterly monitoring run.
**Workflow** — 1) Extract and construct claims triangles by class, peril, cohort and development period. 2) Validate data integrity: continuity with prior periods, reclassifications, large-loss treatment, and currency handling. 3) **Explain every movement** between this cycle's data and the last — the actuary's first question, and days of work to answer manually. 4) Identify distortions: large losses, one-off events, changes in claims-handling practice or reserving philosophy that break the development assumptions. 5) Run standard methods and produce diagnostic exhibits. 6) Draft the data-quality and movement commentary for the reserving report. 7) Flag emerging trends worth actuarial attention.
**Systems** — Claims data warehouse, actuarial platform (ResQ/Arius), GL, exposure data.
**Outcome & KPIs** — Data-prep hours per cycle; data-quality issues found before analysis; movement-explanation completeness; cycle duration; restatement frequency.
**Human gate** — **All reserving judgements and selections are the actuary's**, with formal actuarial sign-off. The agent prepares and diagnoses only.

### INS-14 — Broker & Distribution Partner Management
**A6 · L2 · B2 · Demand creation**
**Pain** — Insurers manage thousands of intermediaries with little visibility into which are profitable, compliant and worth investing in.
**Trigger** — Scheduled partner review, or a performance/compliance signal.
**Workflow** — 1) Build the partner picture: submission volume and quality, hit ratio, premium, loss ratio, cancellation and complaint rates, commission cost. 2) Compute true partner profitability including servicing cost and claims experience, not just premium volume. 3) Detect quality and conduct signals: high early-cancellation rates, misrepresentation patterns, poor claims experience relative to declared risk. 4) Verify regulatory status: authorisation, licences, and required agreements in force. 5) Segment partners and recommend actions — invest, maintain, remediate, or exit — with the evidence. 6) Draft the partner review pack and the specific conversation points. 7) Monitor remediation and re-assess.
**Systems** — Policy admin, claims, commission systems, regulatory registers, CRM, BI.
**Outcome & KPIs** — Partner profitability visibility; loss ratio by partner; compliance exceptions; volume shift to profitable partners; review cycle time.
**Human gate** — Partner termination and commercial terms are relationship decisions.

---
## Regulatory notes for this vertical
| Regime | Impact on agent design |
|---|---|
| **EU AI Act** | Risk assessment and pricing in **life and health insurance** is high-risk: human oversight, documentation, and post-market monitoring required. |
| **Conduct regimes (Consumer Duty, IDD, TCF)** | Fair-value and target-market testing must be evidenced continuously; vulnerability detection must trigger human handling. |
| **Solvency II / IFRS 17** | Actuarial and reserving outputs require qualified sign-off; agents support but never conclude. |
| **Anti-discrimination law** | Rating and claims agents require continuous bias monitoring across protected characteristics, with proxy-variable analysis (postcode as a race proxy is the classic failure). |
