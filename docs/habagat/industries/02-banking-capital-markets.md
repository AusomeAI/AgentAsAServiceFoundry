# Document 02 — Banking & Capital Markets

> 15 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Banking has the highest density of *documented, verifiable, high-volume judgement work* of any industry — which is exactly the agent-fit profile. It is Habagat's highest-ACV vertical.
- The binding constraint is not capability, it is **evidence**: every agent decision must be explainable to a regulator (SR 11-7 / model risk management, FCA Consumer Duty, EU AI Act credit-scoring classification). Habagat's Trust Layer is the product here, not the model.
- Highest-value entry points: **BFS-03 Onboarding/KYC**, **BFS-06 Credit Memo Preparation**, **BFS-09 AML Alert Investigation** — all three have brutal cost baselines and unambiguous quality measures.
- Credit decisioning and AML disposition stay at L2 permanently. That is a feature: the bank's regulator will demand it, and the agent still removes 70–80% of the labour.

---

### BFS-01 — Retail Customer Service & Dispute Intake
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Contact centres handle enormous volumes of balance, transaction, card and dispute queries; regulated complaint handling has strict clocks that manual processes routinely breach.
**Trigger** — Customer contacts via app chat, IVR, or secure message.
**Workflow** — 1) Authenticate customer to the required assurance level for the intent requested. 2) Classify intent, detecting **complaint** and **vulnerability** markers separately from the topic. 3) Assemble account context: balances, recent transactions, card status, product terms, prior contacts. 4) For a disputed transaction, walk the regulated dispute script: merchant, date, amount, cardholder-present, prior attempts to resolve with merchant. 5) Auto-classify dispute reason code against scheme rules (Visa/Mastercard), which determines evidence requirements and timelines. 6) Provisional credit decision within policy thresholds; raise the chargeback case in the disputes system. 7) If the contact meets the regulatory definition of a **complaint**, start the statutory clock, log it, and route to the complaints team — never resolve it silently. 8) Send confirmation with the customer's rights, timescales and case reference.
**Systems** — Core banking, card management, disputes platform, CRM, complaints register, IVR/chat.
**Outcome & KPIs** — Containment rate; dispute cases raised correctly first time; complaint-clock breaches (must be zero); AHT; CSAT; vulnerability detection recall.
**Human gate** — All complaints, all vulnerability flags, provisional credit above threshold, and any account restriction.

### BFS-02 — Product & Pricing Enquiry Advisor
**A4 · L1 · B3 · Demand creation**
**Pain** — Frontline staff give inconsistent product information; in advised markets this is a regulated-advice risk.
**Trigger** — Customer or banker asks about a product, rate or eligibility.
**Workflow** — 1) Classify enquiry as **information** vs **advice** — the regulatory boundary, resolved first and deterministically. 2) Retrieve current product terms, rates and eligibility from the authoritative product master (never from marketing PDFs). 3) Assemble the customer's eligibility signals from held data only. 4) Generate a factual comparison with representative examples and mandated risk warnings. 5) Insert jurisdiction-required disclosures automatically. 6) Where the question crosses into advice, stop and route to a qualified adviser, telling the customer why. 7) Log the interaction to the suitability record.
**Systems** — Product master, pricing engine, CRM, disclosure library, adviser routing.
**Outcome & KPIs** — Information accuracy vs product master; disclosure inclusion rate (100% required); adviser-referral precision; conversion; complaint rate.
**Human gate** — Any personal recommendation. The agent is architecturally prevented from making suitability statements.

### BFS-03 — Client Onboarding, KYC & CDD
**A2 · L2 · B4 · Risk-to-assurance**
**Pain** — Corporate onboarding takes 30–90 days, dominated by document chasing, ownership-structure unpicking and screening adjudication. Abandonment is high and the cost per file runs into thousands.
**Trigger** — New client application or periodic KYC refresh due.
**Workflow** — 1) Determine required due-diligence level from customer type, jurisdiction, products and risk model. 2) Generate the precise document request list — and only that list; over-requesting is the main driver of abandonment. 3) Ingest documents; verify authenticity, validity dates and consistency across documents. 4) Extract and reconstruct the **ownership and control structure**, walking through holding companies and trusts to identify ultimate beneficial owners at the applicable threshold. 5) Screen all identified parties against sanctions, PEP and adverse-media lists; deduplicate and pre-adjudicate obvious false positives with reasoning. 6) Build the risk rating from the model's factors, with each factor's contribution shown. 7) Identify gaps and chase the client with specific, plain-language requests. 8) Assemble the complete CDD file with the analyst's checklist pre-populated and every source cited. 9) Analyst reviews and decides.
**Systems** — Onboarding platform, KYC utility, screening engine, company registries, document intelligence, case management.
**Outcome & KPIs** — Time-to-onboard; abandonment rate; cost per file; UBO identification accuracy; screening false-positive reduction; QA/audit defect rate.
**Human gate** — Every onboarding approval and every risk rating is human-signed. True sanctions matches escalate immediately to the MLRO.

### BFS-04 — Periodic KYC Refresh at Scale
**A2 · L3 · B3 · Risk-to-assurance**
**Pain** — Banks must periodically refresh millions of customer files; most refreshes find nothing changed, but the labour is spent anyway.
**Trigger** — Refresh due date, or an event-driven trigger (address change, ownership change, adverse media hit, transaction-behaviour shift).
**Workflow** — 1) Pull the existing file and determine what actually requires re-verification versus what remains valid. 2) Check external sources for changes: registry filings, sanctions/PEP status, adverse media, directorship changes. 3) Compare declared vs. observed activity: does actual transaction behaviour still match the stated purpose of the relationship? This is the check that finds real risk. 4) **No-change path (majority):** auto-refresh with evidence and full audit trail at L3. 5) **Change path:** generate a targeted outreach requesting only the changed items. 6) Material change → re-rate risk and route to an analyst. 7) Update the file, the next-review date and the audit record.
**Systems** — KYC platform, core banking, transaction monitoring, external registries, screening, outreach channels.
**Outcome & KPIs** — % refreshed without human touch; backlog reduction; overdue-refresh count (regulatory metric); material changes detected; cost per refresh.
**Human gate** — Any risk-rating increase, any new adverse finding, and all high-risk customers.

### BFS-05 — AML Transaction Monitoring Alert Triage
**A1 · L2 · B4 · Risk-to-assurance**
**Pain** — 90–95% of transaction-monitoring alerts are false positives. Investigators spend their careers writing the same "no suspicion" narratives.
**Trigger** — Monitoring system generates an alert.
**Workflow** — 1) Retrieve the alert, the triggering rule and the transactions involved. 2) Rebuild the customer picture: KYC profile, expected activity, occupation/business type, relationship history, prior alerts and dispositions. 3) Analyse the transaction pattern in context — counterparties, geographies, structuring signatures, timing, round-amount patterns, and network links to other customers. 4) Test the benign hypotheses explicitly: is this a property purchase, a bonus, a documented business flow, a known seasonal pattern? 5) Corroborate against internal evidence (documents held, prior enquiries) and permitted external sources. 6) Produce a recommended disposition with a **complete, regulator-quality narrative** citing every piece of evidence. 7) Clear-false-positive cases arrive at the investigator pre-written for one-click confirmation; suspicious cases arrive with the case fully built for escalation to SAR/STR drafting. 8) Feed disposition outcomes back into threshold tuning.
**Systems** — TM system (Actimize/Verafin/Quantexa), core banking, KYC, case management, network analytics, external data.
**Outcome & KPIs** — Investigator time per alert; % alerts auto-narrated and confirmed; **SAR quality and conversion**; false-negative rate under sampling; backlog age; regulatory findings.
**Human gate** — **Every disposition is human-confirmed. SAR/STR filing is always human.** The agent proposes, the MLRO decides — a permanent L2 ceiling by regulatory design.

### BFS-06 — Commercial Credit Memo Preparation
**A3 · L2 · B4 · Order-to-cash**
**Pain** — Relationship managers and credit analysts spend 15–30 hours preparing a credit paper: spreading financials, writing industry context, modelling covenants, assembling the committee pack.
**Trigger** — New facility request, annual review, or amendment request.
**Workflow** — 1) Assemble the borrower file: financial statements, tax filings, existing facilities, security, covenant history, account conduct. 2) **Spread the financials** into the bank's standard template, normalising for accounting policy differences and one-offs, with every adjustment shown and justified. 3) Compute the bank's ratio set and trend analysis; compare against the industry peer set. 4) Analyse account conduct: excesses, returned items, seasonality, concentration of receivables. 5) Generate the industry and market context section from approved research sources. 6) Model the proposal against policy: leverage, DSCR, LTV, tenor, and the bank's risk-appetite statement — flagging every policy exception explicitly. 7) Stress-test against prescribed scenarios (rate shock, revenue decline, margin compression). 8) Draft the full credit memo including the recommendation structure, conditions precedent, covenants and monitoring requirements. 9) Analyst reviews, forms the credit judgement, and signs.
**Systems** — Loan origination, credit-risk engine, financial spreading, core banking, collateral system, market data, document intelligence.
**Outcome & KPIs** — Hours per credit paper; time from request to committee; spreading accuracy vs analyst rework; policy-exception detection rate; committee first-pass approval rate.
**Human gate** — The credit decision is always human and committee-governed. The agent never assigns a risk grade as final; it proposes with evidence.

### BFS-07 — Covenant & Portfolio Monitoring
**A6 · L3 · B3 · Risk-to-assurance**
**Pain** — Covenant testing depends on borrowers submitting information on time and analysts checking it. Breaches are found late; early-warning signals are anecdotal.
**Trigger** — Covenant test date, financial-information receipt, or a continuous early-warning signal.
**Workflow** — 1) Track information-covenant deadlines per facility and chase borrowers automatically before the due date. 2) On receipt, extract the financials and compute each covenant exactly as defined in the facility agreement — definitions differ per deal and this is where manual testing fails. 3) Compare against thresholds; compute headroom and trend. 4) Continuously monitor early-warning indicators: account conduct deterioration, filings, adverse media, sector stress, payment behaviour with other creditors where visible. 5) Compose a portfolio-level view: which exposures are trending toward breach, and what the aggregate sector concentration looks like. 6) On breach or near-breach, assemble the case file with history, security position and options. 7) Route to the relationship team and, where thresholds require, to watchlist/credit risk.
**Systems** — Loan servicing, covenant register, financial spreading, market/news data, credit-risk analytics, CRM.
**Outcome & KPIs** — Covenant tests completed on time; breaches detected at or before test date; information-covenant compliance rate; early-warning lead time; watchlist migration accuracy.
**Human gate** — Waiver decisions, watchlist migration and impairment triggers are human credit decisions.

### BFS-08 — Regulatory Reporting Assembly & Assurance
**A8 · L2 · B4 · Record-to-report**
**Pain** — Regulatory reporting (COREP/FINREP, Call Reports, liquidity, large exposures) consumes enormous effort with high error and resubmission risk.
**Trigger** — Reporting-period end or an ad-hoc regulatory data request.
**Workflow** — 1) Orchestrate the reporting calendar with data-source readiness checks. 2) Ingest source data; validate against schema, referential integrity and prior-period continuity before anything is computed. 3) Apply the regulatory calculation rules, keeping full lineage from every reported figure back to source records. 4) Run the regulator's own validation rules plus the bank's internal reasonableness checks. 5) **Explain every material period-on-period movement** — the question the regulator always asks and the one that takes teams days to answer. 6) Flag anomalies with a diagnosis (data issue vs genuine business movement). 7) Assemble the submission pack with sign-off evidence and lineage documentation. 8) Post-submission, monitor regulator queries and map them to prepared lineage.
**Systems** — Regulatory reporting platform (AxiomSL/Vermeg), data warehouse, GL, risk systems, lineage/metadata catalogue.
**Outcome & KPIs** — On-time submission; validation failures pre-submission; resubmissions (target zero); hours per return; time to answer a regulator query; lineage completeness.
**Human gate** — All submissions are human-attested by the accountable executive; this is personally attestable in most regimes.

### BFS-09 — Trade Surveillance & Market-Abuse Review
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Surveillance alerts (spoofing, layering, insider patterns, front-running) require correlating trades, orders, communications and market data. Most alerts are noise; the review is expensive and inconsistent.
**Trigger** — Surveillance alert on trading or communications data.
**Workflow** — 1) Reconstruct the complete order and trade lifecycle around the alert, including cancels and amendments. 2) Rebuild the market context: prevailing prices, depth, volatility, news events at the relevant timestamps. 3) Correlate with communications (e-comms and voice transcripts) under strict access controls and legal-basis constraints. 4) Assess trader context: mandate, typical behaviour, position, client orders held. 5) Test alternative explanations — legitimate hedging, client facilitation, algorithmic behaviour, market-making obligations. 6) Produce a reasoned recommendation with a full evidence timeline. 7) Escalate genuine concerns to compliance with a case file ready for regulator-facing use.
**Systems** — Surveillance platform, OMS/EMS, market data, communications archive, HR/mandate data, case management.
**Outcome & KPIs** — Review time per alert; false-positive reduction; escalation precision; case-file completeness; regulatory examination outcomes.
**Human gate** — All escalations and all closures on significant alert types are compliance-officer decisions. Communications access is legally gated and logged.

### BFS-10 — Client Reporting & Wealth Review Preparation
**A3 · L1 · B2 · Issue-to-resolution**
**Pain** — Advisers spend hours per client assembling performance reports and review packs, so review frequency is rationed and smaller clients are under-served.
**Trigger** — Scheduled review, quarter-end, or client request.
**Workflow** — 1) Assemble portfolio data: holdings, performance, attribution, fees, cash flows, tax position. 2) Compute performance against the mandate benchmark with attribution by asset class, security and currency. 3) Compare current allocation against the client's target and mandate; identify drift and rebalancing needs. 4) Cross-check suitability: does the portfolio still match the recorded risk profile, objectives and constraints? Flag divergence. 5) Retrieve the house market view and relate it to this specific portfolio. 6) Draft the review pack in the client's language and preferred detail level, with all mandated disclosures. 7) Prepare the adviser's briefing: what changed, what to discuss, what needs client consent, and what regulatory items are due.
**Systems** — Portfolio management, custody, CRM, market data, suitability records, document generation.
**Outcome & KPIs** — Adviser hours per review; review frequency achieved; suitability-drift detection; client engagement; disclosure completeness.
**Human gate** — The adviser owns every recommendation. No investment advice is generated or communicated by the agent.

### BFS-11 — Payments Exception & Investigation Handling
**A5 · L3 · B3 · Order-to-cash**
**Pain** — Failed, returned and misdirected payments generate manual investigations across correspondent banks with slow, template-driven messaging.
**Trigger** — Payment fails validation, is returned, or a customer raises a trace request.
**Workflow** — 1) Classify the failure: format, sanctions hit, insufficient funds, beneficiary detail mismatch, correspondent rejection, or duplicate. 2) Retrieve the full payment chain and messaging history. 3) For repairable technical failures (formatting, missing routing data), determine the correct value from reference data and repair within a strictly bounded, logged policy. 4) For sanctions holds, assemble the evidence pack for the sanctions team — never release. 5) For investigations, generate the correct interbank enquiry message to the right party and track responses against SLA. 6) Keep the customer proactively informed with an accurate expected resolution. 7) Recurrent-cause analysis: report which corridors, formats or clients generate repeated failures.
**Systems** — Payment engine, SWIFT/ISO 20022 messaging, sanctions screening, reference data, CRM, case management.
**Outcome & KPIs** — Auto-repair rate; investigation cycle time; customer contacts per exception; repeat-failure reduction; SLA attainment.
**Human gate** — Sanctions holds, any change to beneficiary bank details, and any payment release are human decisions without exception.

### BFS-12 — Mortgage & Consumer Loan Origination Support
**A2 · L2 · B4 · Order-to-cash**
**Pain** — Mortgage processing involves dozens of documents, verification steps and conditions; underwriters spend most of their time on document chasing rather than credit judgement.
**Trigger** — Application submitted.
**Workflow** — 1) Generate the document checklist based on applicant type, product and jurisdiction. 2) Ingest and classify documents; verify completeness, currency and internal consistency (do the payslips agree with the bank statements and the tax return?). 3) Compute verified income under the lender's specific policy for each income type — the genuinely difficult part for self-employed and variable-income applicants. 4) Analyse bank statements for undisclosed commitments, gambling patterns, irregular deposits and affordability signals. 5) Compute affordability and stress-tested serviceability per policy. 6) Validate the property and valuation inputs against the LTV policy. 7) Assemble the underwriting file with every policy rule evaluated, exceptions flagged, and conditions precedent listed. 8) Underwriter decides; the agent then tracks conditions to satisfaction through to completion.
**Systems** — LOS, credit bureau, open banking / statement analysis, valuation, document intelligence, core banking.
**Outcome & KPIs** — Time-to-decision; documents chased per file; underwriter hours per approval; condition-clearing cycle time; post-completion defect rate; fall-through rate.
**Human gate** — **Credit decisions are always human** — required by EU AI Act high-risk classification for creditworthiness and by fair-lending regimes. Adverse-action reasoning must be human-verifiable and disclosed.

### BFS-13 — Complaints Handling & Root-Cause Analysis
**A1 · L2 · B4 · Issue-to-resolution**
**Pain** — Regulated complaint handling has strict timelines, mandated content and redress obligations; root-cause analysis rarely happens because handling consumes all capacity.
**Trigger** — Complaint received on any channel, or reclassified from a service contact.
**Workflow** — 1) Confirm complaint status, log it, and start the statutory clock. 2) Assemble the full case history across all systems and channels. 3) Identify the specific allegations and map each to the applicable rules, product terms and prior communications. 4) Determine whether the firm's conduct met its obligations, evidence by evidence. 5) Where fault is indicated, compute redress per the prescribed methodology, including interest and consequential loss. 6) Draft the response covering every allegation, the finding, the reasoning, the redress and the customer's escalation rights. 7) Aggregate across complaints to identify systemic root causes and quantify the affected population — the analysis regulators care about most. 8) Feed root causes into remediation programmes.
**Systems** — Complaints platform, core systems, communications archive, redress calculators, regulatory-rules library.
**Outcome & KPIs** — Timeline compliance (zero breaches); uphold-rate consistency; ombudsman overturn rate; redress accuracy; systemic issues identified; repeat complaints.
**Human gate** — Every complaint outcome and every redress payment is human-approved. Systemic-issue declarations are governance decisions.

### BFS-14 — Treasury, Liquidity & Cash Position Analysis
**A6 · L2 · B3 · Record-to-report**
**Pain** — Treasury teams manually assemble intraday liquidity positions across accounts, currencies and entities, then explain movements to management and regulators.
**Trigger** — Intraday schedule, day-start/day-end, or a liquidity-threshold breach.
**Workflow** — 1) Aggregate balances and expected flows across all accounts, entities and currencies. 2) Reconcile expected vs actual flows and investigate discrepancies to source. 3) Project the intraday and short-term position, incorporating known large flows and behavioural models. 4) Compute regulatory liquidity metrics and headroom against limits and buffers. 5) On threshold approach, diagnose the driver and propose specific funding or investment actions within policy. 6) Draft the treasury commentary explaining the position and its movement. 7) Run stress scenarios and report the impact on buffers.
**Systems** — TMS, core banking, nostro/correspondent feeds, market data, regulatory liquidity engine.
**Outcome & KPIs** — Position-assembly time; forecast accuracy; limit-breach lead time; unexplained variance; idle-cash reduction.
**Human gate** — All funding, investment and hedging execution is human. The agent analyses and proposes only.

### BFS-15 — Branch & Operations Process Assurance
**A8 · L3 · B2 · Risk-to-assurance**
**Pain** — First- and second-line assurance relies on small manual samples, so control failures are found late and coverage is thin.
**Trigger** — Continuous monitoring, or an assurance-cycle schedule.
**Workflow** — 1) Define the control population from process definitions and regulatory requirements. 2) Test controls continuously across the **full population rather than a sample** — the structural advantage of automation in assurance. 3) For each exception, gather the evidence and classify: control failure, data issue, or legitimate exception. 4) Trace failures to a location, a process and a cause. 5) Raise findings with owners, severity and remediation actions. 6) Track remediation to closure and re-test. 7) Report thematic trends to the risk committee with quantified exposure.
**Systems** — Core systems, GRC, workflow, document store, BI.
**Outcome & KPIs** — Population coverage vs prior sampling; findings raised and closed; time from failure to detection; repeat findings; audit reliance on first-line testing.
**Human gate** — Risk acceptance and finding closure require the accountable control owner's sign-off.

---
## Regulatory notes for this vertical
| Regime | Impact on agent design |
|---|---|
| **EU AI Act** | Creditworthiness assessment is **high-risk** — mandatory human oversight, logging, transparency, technical documentation, and post-market monitoring. Design at L2 permanently. |
| **SR 11-7 / model risk** | Every agent is a model: it needs documented development, independent validation, ongoing monitoring, and an owner. Habagat ships a model-documentation pack per agent. |
| **AML/CFT (FATF, BSA, 6AMLD)** | Automated *disposition* of alerts is not acceptable; automated *preparation* is. Habagat's boundary is the disposition. |
| **Consumer Duty / TCF** | Vulnerability detection must be a first-class agent capability with immediate human routing, not a sentiment score. |
| **DORA** | Habagat is a third-party ICT provider: exit plans, resilience testing, concentration reporting and register entries are contractual obligations. |
