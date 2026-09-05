# Document 04 — Healthcare Providers (Hospitals, Health Systems, Clinics)

> 15 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Healthcare's agent opportunity is overwhelmingly **administrative, not clinical**. Roughly 25–30% of US health-system spend is administrative; that is where the safe, large, fast ROI is.
- Clinical-adjacent agents (documentation, coding, triage support) are viable at L1–L2 with clinician-in-the-loop. **Anything that constitutes a diagnosis or a treatment decision is out of scope** — regulatory (FDA SaMD / EU MDR), ethical and commercial.
- The two agents that pay for everything else: **HC-04 Prior Authorisation** and **HC-08 Denial Management & Appeals**. Both attack pure administrative waste with hard, auditable dollar outcomes.
- PHI handling is the whole architecture conversation. Habagat's single-tenant model is not a differentiator here — it is the entry ticket, and it must come with a BAA, HIPAA-eligible services only, and no data leaving the customer's tenant.

---

### HC-01 — Patient Access, Scheduling & Referral Intake
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Call centres are the front door and the bottleneck: long waits, high abandonment, complex scheduling rules, and referrals lost in fax queues.
**Trigger** — Patient calls/messages for an appointment, or a referral arrives (fax, HIE, portal, e-referral).
**Workflow** — 1) Identify or register the patient with strict identity-matching rules (duplicate MRN creation is a patient-safety issue, not a data issue). 2) Determine the visit type and clinical urgency using approved triage protocols — **protocol-driven, not model-improvised**. 3) Apply scheduling rules: provider, modality, prep requirements, sequencing with other appointments, and location/travel constraints. 4) Verify insurance eligibility and benefits in real time; identify the patient's expected cost share. 5) Check whether prior authorisation will be required and initiate it (hands to HC-04). 6) Offer appointment options optimised for both patient preference and clinic utilisation. 7) Book, confirm, and send preparation instructions in the patient's language and literacy level. 8) Manage reminders, confirmations and rescheduling; proactively fill cancellations from the waitlist. 9) Any red-flag symptom in the intake conversation triggers an immediate protocol-defined escalation to a clinician.
**Systems** — EHR (Epic/Cerner/Meditech), scheduling, eligibility/clearinghouse, referral management, telephony, patient portal.
**Outcome & KPIs** — Time-to-third-next-available; abandonment rate; no-show rate; referral leakage; slot utilisation; % referrals actioned within target.
**Human gate** — Any clinical urgency determination beyond protocol; all symptom red flags; clinical questions.

### HC-02 — Insurance Eligibility & Benefit Verification
**A2 · L3 · B3 · Order-to-cash**
**Pain** — Eligibility errors are the largest single cause of downstream denials; verification is manual, payer-portal-driven and often skipped under time pressure.
**Trigger** — Appointment scheduled, admission, or a batch run before the service date.
**Workflow** — 1) Retrieve coverage from the patient record and run the 270/271 eligibility transaction. 2) Where payer responses are incomplete (routinely), interrogate the payer portal for plan-specific benefit detail. 3) Determine the specifics that actually matter: covered benefit for this service, network status of this provider at this location, deductible remaining, co-insurance, copay, visit limits, and referral/authorisation requirements. 4) Detect coverage problems early: termination, coordination-of-benefits conflicts, wrong plan on file. 5) Compute the patient's estimated responsibility and generate a good-faith estimate where required by law. 6) Update the account, and flag accounts needing financial counselling. 7) Re-verify before the date of service, because coverage changes.
**Systems** — EHR/PM, clearinghouse, payer portals, patient-estimate engine.
**Outcome & KPIs** — Verification completion before service; eligibility-related denial rate; point-of-service collections; estimate accuracy; COB issues resolved pre-service.
**Human gate** — Financial-hardship and charity-care determinations.

### HC-03 — Clinical Documentation Support (Ambient & Structured)
**A4 · L1 · B4 · Idea-to-market**
**Pain** — Clinicians spend 1–2 hours on documentation for every hour of patient care. Burnout is the primary consequence; incomplete documentation is the secondary one.
**Trigger** — Clinical encounter begins (with explicit patient consent), or clinician requests note assistance.
**Workflow** — 1) Capture the encounter with documented consent, recorded in the chart. 2) Distinguish speakers and separate clinical content from conversational content. 3) Draft the note in the required structure (SOAP/H&P/procedure), organised by clinical relevance rather than chronology. 4) Ground every clinical assertion in the encounter or the existing chart; **anything not evidenced is omitted, not inferred** — the single most important design rule in this use case. 5) Surface documentation gaps that matter for care and for coding: laterality, acuity, specificity of diagnosis, and unaddressed problem-list items. 6) Suggest orders and follow-ups **as suggestions requiring explicit clinician action** — never pre-placed. 7) Present the draft for clinician review, edit and signature. 8) Learn the individual clinician's documentation style within safety bounds.
**Systems** — EHR, ambient capture, terminology services (SNOMED, ICD-10, LOINC), order catalogue.
**Outcome & KPIs** — Documentation time per encounter; after-hours EHR time ("pyjama time"); note completeness; clinician satisfaction; **edit rate and error class on review (the safety metric)**.
**Human gate** — **The clinician reviews and signs every note. Nothing enters the legal record unsigned.** No autonomous orders, ever.

### HC-04 — Prior Authorisation Management
**A5 · L2 · B3 · Order-to-cash**
**Pain** — Prior auth is the purest administrative waste in healthcare: staff hours on portals and faxes, care delayed by days or weeks, and high rates of eventually-approved denials.
**Trigger** — Order placed that requires authorisation, or eligibility check flags a requirement.
**Workflow** — 1) Determine whether authorisation is required for this service, payer, plan and place of service — a rules problem that changes constantly. 2) Retrieve the payer's **specific medical-necessity criteria** for this service and plan. 3) Assemble the clinical evidence from the chart against each criterion, identifying exactly which criteria are met and which lack documentation. 4) Where evidence is missing, generate a precise query to the clinician: not "please document more" but "criterion 3 requires a documented trial of conservative therapy ≥6 weeks — is there a record of physical therapy?" 5) Compile and submit the authorisation via the payer's channel (X12 278, portal, or fax as required). 6) Track status; respond to payer information requests; escalate on timeline breach. 7) On approval, record the authorisation number, valid dates and unit limits against the order and the future claim. 8) On denial, hand to HC-08 with the case already assembled.
**Systems** — EHR, payer portals/EDI, authorisation rules engine, clinical criteria (InterQual/MCG), document generation.
**Outcome & KPIs** — Time-to-authorisation; approval rate on first submission; care delay days avoided; staff hours per auth; auth-related denials.
**Human gate** — Clinicians approve all clinical assertions submitted to payers. Peer-to-peer reviews are physician-conducted.

### HC-05 — Medical Coding Assistance & Audit
**A2 · L2 · B4 · Order-to-cash**
**Pain** — Coding is a scarce, expensive skill; backlogs delay billing; under-coding loses legitimate revenue and over-coding creates fraud exposure.
**Trigger** — Encounter documentation signed and ready for coding.
**Workflow** — 1) Read the complete encounter documentation including all supporting results and notes. 2) Propose diagnosis codes (ICD-10-CM) supported by explicit documentation, with the substantiating text quoted for every code. 3) Propose procedure codes (CPT/HCPCS/ICD-10-PCS) with modifiers, checking bundling and NCCI edits. 4) Determine the E/M level from the documented medical decision making or time, showing the derivation. 5) Verify medical necessity linkage between diagnoses and procedures per payer policy. 6) **Identify documentation gaps that block accurate coding and generate a compliant, non-leading physician query** — leading queries are a compliance violation, so query language is templated and rule-governed. 7) Present the coder with proposed codes, evidence and confidence; the coder validates. 8) Continuously audit coded claims for over-coding and under-coding patterns by provider and service line.
**Systems** — EHR, encoder/CAC, charge description master, NCCI edits, payer policy library, CDI workflow.
**Outcome & KPIs** — Coder productivity; coding accuracy vs. audit; DNFB (discharged-not-final-billed) days; case-mix index accuracy; query rate and response time; audit findings.
**Human gate** — **Certified coders validate every code before billing.** This is both a compliance requirement and a False Claims Act exposure boundary.

### HC-06 — Charge Capture & Revenue Integrity
**A6 · L3 · B3 · Order-to-cash**
**Pain** — Services delivered but never charged represent silent, permanent revenue loss — typically 1–3% of net revenue.
**Trigger** — Continuous reconciliation between clinical activity and charges.
**Workflow** — 1) Reconcile clinical events (orders, administrations, procedures, device implants, supply usage, time-based services) against posted charges. 2) Identify missing charges with the supporting clinical evidence. 3) Identify incorrect charges: wrong quantity, wrong site, wrong revenue code, or charges without clinical support (the compliance risk, which matters as much as the revenue). 4) Validate against the charge description master for current pricing and coding. 5) Route findings to the responsible department with the evidence and the correction. 6) Root-cause analysis: which workflows systematically drop charges, and why. 7) Track realised recovery and defect-rate reduction by department.
**Systems** — EHR, CDM, billing system, pharmacy/implant/supply systems, revenue-integrity analytics.
**Outcome & KPIs** — Net revenue recovered; charge-capture defect rate by department; compliance exceptions found; late charges; recurrence after root-cause fix.
**Human gate** — Revenue-integrity analysts approve all charge additions and corrections.

### HC-07 — Claims Submission & Edit Resolution
**A5 · L3 · B3 · Order-to-cash**
**Pain** — Claims reject on avoidable edits and cycle repeatedly between billing and clearinghouse, extending AR days.
**Trigger** — Claim ready for submission, or a rejection/edit returned.
**Workflow** — 1) Pre-submission scrubbing against payer-specific rules, NCCI edits, and the organisation's own historical rejection patterns — the last of which is the most predictive and least used. 2) Diagnose each edit precisely and, where the correct value is unambiguous and evidenced, correct it (demographics, COB order, authorisation number, modifier where documentation supports it). 3) Where correction requires clinical or coding judgement, route to the right person with the specific question. 4) Submit and track acknowledgements. 5) Monitor for claims that vanish (submitted, never acknowledged) — a routine and expensive failure mode. 6) Report rejection root causes upstream to registration, coding and clinical documentation.
**Systems** — Billing/PM system, clearinghouse, payer portals, edit-rules library.
**Outcome & KPIs** — Clean-claim rate; first-pass yield; days in AR; rejection rate by cause; rework touches per claim.
**Human gate** — Any change to coded clinical content requires coder/clinician approval; never "fix" a code to get a claim through.

### HC-08 — Denial Management & Appeals
**A3 · L2 · B3 · Order-to-cash**
**Pain** — A large share of denials are never appealed because appeals are labour-intensive — and a substantial proportion of appealed denials are overturned. This is money left on the table by design.
**Trigger** — Denial received on a remittance.
**Workflow** — 1) Classify the denial by true root cause, not just the payer's code — the codes are notoriously imprecise. 2) Determine appealability, the deadline, and the required appeal level and format for this payer and denial type. 3) Prioritise by expected value: recoverable amount × overturn probability ÷ effort. 4) Assemble the appeal evidence: clinical documentation, authorisation records, medical policy, and the contract terms that govern payment. 5) **Draft the appeal argued against the payer's own published medical policy and the contract**, quoting both — the difference between a form letter and an overturn. 6) Submit through the correct channel and track to determination. 7) Escalate to external review or contractual dispute where warranted. 8) Aggregate denial patterns and feed prevention actions upstream to authorisation, coding and registration — the compounding win.
**Systems** — Billing, EHR, payer policy library, contract management, appeal-tracking, document generation.
**Outcome & KPIs** — Appeal rate; **overturn rate**; recovered revenue; days to appeal; denial rate trend by root cause; preventable-denial reduction.
**Human gate** — Clinical appeals require clinician attestation. Contractual disputes involve legal/managed care.

### HC-09 — Patient Financial Communication & Collections
**A7 · L2 · B3 · Order-to-cash**
**Pain** — Patients receive incomprehensible bills, cannot get answers, and self-pay AR ages badly. Aggressive collection creates reputational and regulatory harm.
**Trigger** — Balance becomes patient responsibility, or the patient asks a billing question.
**Workflow** — 1) Assemble the complete account: services, insurance adjudication, adjustments, prior payments and current balance. 2) **Explain the bill in plain language**: what the service was, what insurance paid and why, and what remains — the single most requested and least delivered thing in healthcare billing. 3) Screen for financial-assistance eligibility proactively, including presumptive charity criteria; offer assistance before pursuing payment. 4) Offer payment plans within policy and set them up. 5) Handle disputes: verify the charge, check for insurance errors, and route genuine billing errors for correction rather than defending them. 6) Communicate on the patient's preferred channel and language, respecting all contact restrictions. 7) Escalate hardship, complaints and confusion to a human financial counsellor.
**Systems** — Billing/PM, payment processing, financial-assistance policy engine, communication platform, EHR.
**Outcome & KPIs** — Self-pay collection rate; days in self-pay AR; financial-assistance uptake; billing-complaint rate; payment-plan adherence; patient financial experience score.
**Human gate** — Charity determinations, any referral to external collections, and all hardship cases. Strict FDCPA/consumer-protection compliance is enforced at the platform layer.

### HC-10 — Care Coordination & Discharge Planning Support
**A5 · L2 · B4 · Issue-to-resolution**
**Pain** — Discharge delays and poor transitions drive readmissions and length-of-stay costs; coordination is phone-and-fax work done by expensive clinical staff.
**Trigger** — Admission (planning starts at admission), or a discharge-readiness milestone.
**Workflow** — 1) From admission, identify the likely discharge disposition and the barriers to it: placement, equipment, home support, transport, medication access, insurance authorisation. 2) Track barrier resolution with owners and escalation, chasing daily. 3) Identify post-acute options matching the patient's clinical needs, insurance and geography; assemble referral packets. 4) Verify authorisation for the post-acute service before discharge, not after. 5) Draft discharge instructions at the patient's literacy level and in their language, covering medications, warning signs, follow-up and contacts. 6) Schedule follow-up appointments before discharge — the strongest modifiable readmission predictor. 7) Reconcile medications and flag discrepancies for pharmacist review. 8) Post-discharge follow-up contact with protocol-driven escalation on concerning responses.
**Systems** — EHR, case-management module, post-acute network directories, payer authorisation, scheduling, patient communication.
**Outcome & KPIs** — Length of stay / avoidable bed days; discharge-barrier resolution time; follow-up appointment rate within 7 days; 30-day readmission rate; patient understanding at discharge.
**Human gate** — All clinical discharge decisions; medication reconciliation is pharmacist/clinician-verified; any concerning post-discharge response routes to a clinician immediately.

### HC-11 — Population Health & Care-Gap Outreach
**A6 · L2 · B3 · Plan-to-produce**
**Pain** — Preventive care gaps and chronic-disease management lapses drive both worse outcomes and lost value-based-care revenue; outreach capacity is limited.
**Trigger** — Continuous registry evaluation, or a quality-programme reporting cycle.
**Workflow** — 1) Evaluate the attributed population against quality measures and clinical guidelines to identify open care gaps. 2) Validate each gap against the record — the majority of apparent "gaps" are documentation or data-exchange failures, and chasing patients for care they already received destroys trust. 3) Stratify by clinical risk and by likelihood of engagement, so scarce outreach lands where it changes outcomes. 4) Generate personalised outreach explaining what is due, why it matters to *this* patient, and how to act on it. 5) Remove barriers in the same interaction: book the appointment, arrange transport support, order the home test kit. 6) Manage multi-channel, multi-attempt cadence with preference and consent respected. 7) Close the loop: confirm completion, update the registry, and report measure performance. 8) Report which gaps are data problems back to the interoperability team.
**Systems** — Population-health platform, EHR, claims data, registries, HIE, outreach channels, scheduling.
**Outcome & KPIs** — Care gaps closed; quality measure performance (HEDIS/Stars/MIPS); outreach conversion; documentation-driven false gaps eliminated; value-based revenue.
**Human gate** — Clinical protocol definitions are physician-governed; any patient response indicating symptoms routes to clinical triage.

### HC-12 — Utilisation Review & Medical Necessity Documentation
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Inpatient status determination (observation vs inpatient) and concurrent review are high-stakes, criteria-driven, and consume senior nursing time.
**Trigger** — Admission, status review point, or payer concurrent-review request.
**Workflow** — 1) Assemble the clinical picture relevant to status: presenting condition, findings, interventions, response, and expected duration of care. 2) Apply the applicable criteria set (InterQual/MCG) and show which specific criteria are met by which documented findings. 3) Where criteria are not clearly met, identify precisely what additional documentation would establish necessity if clinically true, and query the physician appropriately. 4) Prepare the payer submission with the criteria mapping. 5) Track concurrent-review deadlines and payer responses. 6) On adverse determination, assemble the peer-to-peer briefing for the physician advisor. 7) Report avoidable-day and status-determination patterns.
**Systems** — EHR, UR platform, criteria libraries, payer portals, case management.
**Outcome & KPIs** — Status determination accuracy vs audit; concurrent-review timeliness; adverse determinations overturned; observation rate; avoidable days.
**Human gate** — **Status determinations are clinical decisions** made by UR nurses and physician advisors. The agent assembles evidence and maps criteria only.

### HC-13 — Clinical Trial Matching & Research Support
**A3 · L1 · B4 · Idea-to-market**
**Pain** — Eligible patients are never told about relevant trials because matching requires reading both the protocol and the chart in detail; trial enrolment is chronically slow.
**Trigger** — New patient diagnosis, protocol activation, or a clinician request.
**Workflow** — 1) Parse trial protocols into structured inclusion and exclusion criteria. 2) Screen the patient record against each criterion, distinguishing definitively met, definitively failed, and *unknown* — the unknowns are the actionable output. 3) Produce a match report showing the evidence for each criterion, with chart citations. 4) Identify what additional testing would resolve the unknowns. 5) Present candidate matches to the treating clinician and the research team, never to the patient directly. 6) Support screening logs and enrolment documentation for regulatory compliance. 7) Track screen-failure reasons to inform protocol feasibility.
**Systems** — EHR, CTMS, trial registries, genomics/pathology systems, IRB documentation.
**Outcome & KPIs** — Patients screened per trial; match precision; enrolment rate and time-to-enrolment; screen-failure rate; trial portfolio feasibility insight.
**Human gate** — **Only the treating clinician discusses trial participation with a patient.** All consent is human-conducted per IRB requirements.

### HC-14 — Workforce Scheduling & Staffing Optimisation
**A5 · L2 · B3 · Plan-to-produce**
**Pain** — Clinical scheduling balances acuity, skill mix, regulation, union rules, preferences and cost. It is done in spreadsheets, and the failure mode is expensive agency staffing.
**Trigger** — Schedule-generation cycle, shift gap, or a demand-forecast change.
**Workflow** — 1) Forecast demand by unit and shift from census, admission patterns, seasonality, scheduled procedures and acuity trends. 2) Compute required staffing by skill mix against ratio regulations and safety standards. 3) Generate schedules satisfying hard constraints (licensure, competency, ratio law, rest rules, contract terms) and optimising soft constraints (preferences, fairness, continuity, cost). 4) Identify gaps early enough to fill them internally rather than through agency. 5) Manage open-shift offers with equitable distribution and transparent premium rules. 6) Handle real-time changes: sick calls, census surges, acuity escalation — re-solving rather than patching. 7) Report cost, overtime, agency reliance and fairness metrics.
**Systems** — Workforce management, EHR census/acuity, HR systems, credentialing, time and attendance.
**Outcome & KPIs** — Agency spend; overtime hours; ratio compliance; unfilled shifts; schedule stability; staff satisfaction and fairness measures.
**Human gate** — Nurse managers approve final schedules; all ratio and contract constraints are hard constraints the agent cannot relax.

### HC-15 — Supply Chain & Clinical Inventory Management
**A6 · L3 · B3 · Procure-to-pay**
**Pain** — Hospitals carry excessive inventory in some areas and stock out in others; preference-item variation drives cost with no outcome benefit; expiry waste is routine.
**Trigger** — Consumption event, par-level breach, or a scheduled review.
**Workflow** — 1) Track consumption against procedure schedules and forecast demand by item and location. 2) Optimise par levels using demand variability and lead time rather than historical habit. 3) Generate replenishment orders within contract terms; detect off-contract purchasing. 4) Monitor expiry and recommend redistribution before waste. 5) Manage recalls: identify affected lots, where they are, whether they were used, and which patients were exposed — a patient-safety obligation with regulatory deadlines. 6) Analyse preference-item variation across surgeons for equivalent procedures and quantify the cost difference for value-analysis committees. 7) Track supplier performance, backorders and substitution options.
**Systems** — ERP/materials management, EHR (implant/supply documentation), GPO contracts, recall feeds, point-of-use systems.
**Outcome & KPIs** — Inventory value and turns; stockouts; expiry waste; contract compliance; recall response time; preference-item cost variance.
**Human gate** — Clinical product substitutions require clinician approval; recall actions are patient-safety governed.

---
## Regulatory notes for this vertical
| Regime | Impact on agent design |
|---|---|
| **HIPAA / HITECH** | BAA required; PHI never leaves the customer tenant; minimum-necessary access enforced by identity; full access audit trail; breach-notification obligations flow to Habagat as a Business Associate. |
| **FDA SaMD / EU MDR** | Any function that diagnoses, treats or drives clinical decisions is a regulated device. Habagat's agents are **administrative and documentation support only**, with clinician sign-off, keeping them outside device classification. This boundary must be explicit in every contract and product description. |
| **21st Century Cures / information blocking** | Agents must not impede patient access to their information. |
| **False Claims Act** | Coding and billing agents create real liability. Human certification before submission is non-negotiable, and over-coding monitoring is mandatory. |
| **EU AI Act** | Triage and prioritisation of emergency care is high-risk; Habagat implements protocol-driven routing with human clinical oversight. |
