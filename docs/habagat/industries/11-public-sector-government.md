# Document 11 — Public Sector & Government

> 14 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Government is the vertical where **single-tenant isolation is not a differentiator but a procurement requirement**. Habagat's architecture is the reason it can bid at all; sovereignty, residency and auditability are threshold criteria.
- The value proposition is not headcount reduction — that is politically unsellable. It is **backlog elimination, decision consistency, and citizen wait times**. Frame every business case that way.
- Highest-value entry points: **GOV-02 Benefits & Permit Application Processing**, **GOV-06 Case Backlog Triage**, **GOV-01 Citizen Enquiry Handling**. All three attack visible, measurable, politically salient queues.
- The governance bar is the highest in the catalogue: administrative-law duties (reasons, consistency, appeal rights), transparency obligations, and in the EU an explicit high-risk classification for public-benefit eligibility. **Design every agent as decision-support with a documented human decision-maker.**

---

### GOV-01 — Citizen Enquiry & Service Navigation
**A1 · L2 · B3 · Issue-to-resolution**
**Pain** — Citizens cannot navigate government: they do not know which agency, which service, which form or which eligibility applies. Contact centres absorb the confusion at high cost, and the most vulnerable citizens fare worst.
**Trigger** — Citizen contacts by phone, web, chat, or in person.
**Workflow** — 1) Understand the citizen's actual situation and need, which is rarely expressed in the government's vocabulary ("I lost my job and I can't pay rent" is not a service name). 2) Map the situation to the relevant services across agencies — including services they did not ask about but are likely eligible for, which is the highest-value output in the whole use case. 3) Explain eligibility in plain language at an accessible reading level, in the citizen's language, and state clearly what is certain versus what depends on assessment. 4) Explain the process: what is needed, how long it takes, what happens next, and what to do if it goes wrong. 5) For a specific case enquiry, authenticate and retrieve the actual status with an honest timeline. 6) Where the citizen can act now, help them: start the application, book the appointment, or upload the document. 7) Detect urgency and vulnerability — homelessness risk, safeguarding, domestic abuse, mental health crisis — and route immediately to a human on the appropriate pathway. 8) Log the interaction and feed unmet-need patterns into service design.
**Systems** — Case management, service catalogue, eligibility rules, appointment systems, translation services, referral pathways.
**Outcome & KPIs** — Enquiries resolved at first contact; service take-up among eligible citizens; accessibility compliance; wait times; vulnerability referrals made; citizen satisfaction.
**Human gate** — **The agent never determines entitlement.** Any safeguarding, crisis or vulnerability signal routes to a human immediately; automated handling stops.

### GOV-02 — Benefits, Grants & Permit Application Processing
**A2 · L2 · B4 · Issue-to-resolution**
**Pain** — Application backlogs are the most visible failure of government. Processing is document-heavy, rule-heavy and inconsistent between assessors, and citizens wait months for decisions that change their lives.
**Trigger** — Application submitted.
**Workflow** — 1) Validate completeness against the requirements for this specific application type and circumstances; return incomplete applications immediately with precise, plain-language guidance rather than letting them sit in a queue. 2) Extract and structure the evidence: identity documents, income evidence, medical evidence, property documents, and supporting statements. 3) Verify evidence where authorised: cross-check against authoritative data sources under the applicable legal gateway, and validate document authenticity. 4) **Apply the eligibility rules transparently**, showing which criterion is met by which evidence, and — critically — which criteria are not met and why. 5) Identify where the rules require discretion or judgement, and route those explicitly to the assessor rather than guessing. 6) Detect potential fraud or error indicators for separate handling, without prejudicing the assessment. 7) Prepare the assessor's pack: the recommendation, the evidence map, the discretionary questions, and a draft decision notice with reasons. 8) Assessor decides; the agent generates the decision notice with **statutory reasons and appeal rights**. 9) Track processing times and consistency of outcomes across assessors and cohorts.
**Systems** — Case management, document intelligence, identity and data-sharing gateways, eligibility rules engine, correspondence generation.
**Outcome & KPIs** — Processing time and backlog; decisions overturned on appeal; assessor consistency; incomplete-application resubmission rate; error rate; citizen satisfaction.
**Human gate** — **Every determination is made by an authorised officer.** Under the EU AI Act, eligibility for essential public benefits is high-risk: human oversight, transparency, logging and a right to explanation are mandatory. Adverse decisions must state reasons and appeal rights.

### GOV-03 — Procurement & Tender Management
**A3 · L2 · B4 · Procure-to-pay**
**Pain** — Public procurement is rule-bound, slow and challenge-prone. Tender preparation and evaluation consume months, and process errors trigger legal challenge that costs more than the contract.
**Trigger** — Procurement need identified, or tender responses received.
**Workflow** — 1) Determine the applicable procurement route and thresholds from the requirement's value, nature and the governing regulations. 2) Assist specification development: draw on prior similar procurements and market intelligence, and flag specifications that may unlawfully restrict competition. 3) Generate the tender pack with the evaluation methodology defined and published up front — deviating from published criteria is the most common ground of successful challenge. 4) Manage supplier clarifications with fair, published responses to all bidders. 5) On receipt, check compliance and completeness, and identify mandatory exclusion grounds. 6) **Evaluate against the published criteria only**, producing a scored, evidenced assessment with the rationale for each score — the audit trail is the deliverable. 7) Flag inconsistencies between evaluators for moderation. 8) Generate the award recommendation, the standstill notices and the individual bidder feedback required by law. 9) Maintain the complete record for audit and challenge.
**Systems** — E-procurement platform, contract register, supplier databases, exclusion/sanctions screening, document management.
**Outcome & KPIs** — Procurement cycle time; challenges received and upheld; evaluation consistency; competition levels (bidders per tender); savings achieved; audit findings.
**Human gate** — **Evaluation panels make all scoring decisions**; the agent structures, evidences and checks. Award decisions follow the governance framework.

### GOV-04 — Regulatory Inspection & Enforcement Support
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Regulators have far more regulated entities than inspection capacity. Inspection targeting is often calendar-based rather than risk-based, so effort goes where it is least needed.
**Trigger** — Risk-assessment cycle, complaint, intelligence, or a scheduled inspection.
**Workflow** — 1) Build the risk picture per regulated entity: compliance history, complaints, intelligence, sector risk, changes in ownership or operation, and time since last inspection. 2) **Prioritise inspection effort by risk of harm**, with the reasoning documented — this is both more effective and more defensible than a cyclical programme. 3) Prepare the inspector: entity history, previous findings, outstanding actions, applicable requirements, and the specific matters to examine. 4) During and after inspection, structure findings against the regulatory requirements with the evidence. 5) Assess the appropriate regulatory response against the enforcement policy, ensuring proportionality and consistency with comparable cases — inconsistency is the primary ground of successful appeal. 6) Draft the notice or report with the required legal content, reasons and appeal rights. 7) Track compliance with actions and escalate non-compliance. 8) Analyse patterns across the regulated population to identify systemic issues and target guidance.
**Systems** — Regulatory case management, entity register, complaints, intelligence sources, inspection mobile tools, enforcement policy.
**Outcome & KPIs** — Risk coverage of inspection effort; harm prevented; enforcement consistency; appeals upheld; compliance improvement in targeted populations.
**Human gate** — **All enforcement decisions are made by authorised officers** under the enforcement policy; formal notices carry legal consequences and personal accountability.

### GOV-05 — Policy Research, Consultation & Impact Analysis
**A3 · L1 · B2 · Idea-to-market**
**Pain** — Policy development requires synthesising evidence, precedent, stakeholder views and impacts under political time pressure. Consultation responses arrive in the thousands and are analysed superficially.
**Trigger** — Policy question raised, consultation closes, or a legislative programme milestone.
**Workflow** — 1) Assemble the evidence base: research literature, evaluations of comparable interventions, administrative data, and international precedent, with quality assessment. 2) Analyse the current legal and policy framework and identify the levers available. 3) **Analyse consultation responses at scale**: code responses by theme, position and respondent type; identify genuinely novel arguments as distinct from volume; and preserve minority views rather than drowning them in counts. Campaign responses are identified and reported separately. 4) Assess impacts: economic, equality (including statutory equality duties), environmental, regional and small-business impacts, with the assumptions stated. 5) Model options with costs, benefits, distributional effects and implementation feasibility. 6) Draft the analysis with clear separation between evidence, assumption and judgement. 7) Support the statutory impact assessments required before legislation.
**Systems** — Consultation platform, research databases, administrative data, economic models, document management.
**Outcome & KPIs** — Analysis turnaround; consultation coverage and depth; impact assessment quality; challenges to the evidence base; ministerial and parliamentary scrutiny outcomes.
**Human gate** — **Policy advice and ministerial submissions are authored by officials**, who carry professional and constitutional accountability. The agent never generates a recommendation as if it were advice.

### GOV-06 — Case Backlog Triage & Workflow Management
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Backlogs in immigration, justice, planning, appeals and benefits reviews are politically toxic and structurally persistent. Cases queue in arrival order regardless of complexity or urgency.
**Trigger** — New case created, or a backlog-review cycle.
**Workflow** — 1) Assess each case for complexity, completeness and urgency from its content rather than its label. 2) Identify cases that can be resolved quickly — complete, straightforward, and within settled precedent — and stream them separately. Segmentation alone typically removes a large share of a backlog. 3) Identify cases blocked on missing information and generate the specific request immediately, rather than discovering the gap when a caseworker eventually opens the file. 4) Flag urgent cases on defined criteria: statutory deadlines, vulnerability, detention, health, and safeguarding. 5) Route each case to the caseworker with the right specialism and authority level. 6) Prepare the caseworker's brief: the issues, the evidence, the applicable law and precedent, and the decision points. 7) Detect linked and duplicate cases that should be handled together. 8) Report backlog composition, ageing and flow so management acts on causes rather than totals.
**Systems** — Case management, document management, scheduling, correspondence, precedent/guidance libraries.
**Outcome & KPIs** — Backlog size and ageing; cases resolved per caseworker; time to first substantive action; urgent cases identified and expedited; decision quality maintained (a guardrail — speed must not raise overturn rates).
**Human gate** — All case decisions are made by authorised caseworkers; prioritisation criteria are set by policy, not by the model.

### GOV-07 — Fraud, Error & Debt Management
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Fraud and error in public expenditure is large; detection is retrospective; and recovery activity risks serious harm when directed at vulnerable people who made an honest mistake.
**Trigger** — Continuous risk analysis, data-matching cycle, or a referral.
**Workflow** — 1) Analyse claims and payments against risk indicators and data matches with authoritative sources under the applicable legal gateway. 2) **Distinguish fraud from error from a change of circumstances** — treating an error as fraud causes serious harm and is the most common failure of these programmes. 3) Score referrals by confidence and value, with an explicit high bar for anything that could lead to a criminal referral. 4) Assemble the evidence pack for the investigator with the data trail and the alternative explanations considered. 5) For error, generate the correction and the citizen communication in plain language. 6) For debt, assess affordability and vulnerability **before** any recovery action, and set sustainable recovery rates. 7) Analyse root causes of error at scale — most error is caused by process and guidance defects, and fixing those is worth more than any recovery. 8) Monitor for disproportionate impact across demographic groups and report it.
**Systems** — Case management, payment systems, data-matching services, debt management, investigation case management.
**Outcome & KPIs** — Fraud and error rate; recovery achieved; **false-positive rate (the critical guardrail)**; process defects fixed; disproportionality monitoring; complaints and appeals.
**Human gate** — **All fraud determinations, sanctions and prosecutions are human decisions** under legal process. Vulnerability assessment precedes all recovery action. Automated decision-making restrictions under data-protection law apply directly here.

### GOV-08 — Records, FOI & Information Requests
**A2 · L2 · B4 · Risk-to-assurance**
**Pain** — Freedom-of-information and subject-access requests have statutory deadlines and require searching vast unstructured records, then applying exemptions carefully. Teams are small and deadlines are missed.
**Trigger** — FOI, EIR or subject-access request received.
**Workflow** — 1) Interpret the request precisely and identify what is actually being asked for, clarifying with the requester where genuinely ambiguous. 2) Determine the request type and the applicable statutory regime and deadline. 3) Search records across systems, email and document stores using terms derived from the request, and report the search strategy — defensible search is the core of a defensible response. 4) Identify potentially in-scope material and assess volume against cost limits. 5) **Apply exemptions and redactions**: personal data of third parties, commercial confidentiality, legal privilege, security, and policy formulation — proposing each with the specific statutory basis and the public-interest reasoning where required. 6) Prepare the response pack with the redaction schedule for the information-rights officer. 7) Draft the response letter with reasons for withholding and the requester's review and appeal rights. 8) Track deadlines and internal reviews; analyse request patterns for proactive publication opportunities.
**Systems** — Records and document management, email archive, case management, redaction tooling, publication scheme.
**Outcome & KPIs** — On-time response rate; internal reviews and appeals upheld; redaction accuracy (an incorrect disclosure is unrecoverable); search completeness; proactive publication.
**Human gate** — **Information-rights officers make every disclosure and exemption decision.** A single wrongful disclosure of personal or classified data is irreversible; the human check is mandatory.

### GOV-09 — Emergency Management & Public Safety Coordination
**A5 · L2 · B4 · Issue-to-resolution**
**Pain** — Emergency response requires rapid situational assembly across agencies under extreme time pressure, with incomplete and conflicting information.
**Trigger** — Incident declared, warning issued, or an escalating situation.
**Workflow** — 1) Assemble the situational picture from all available feeds: sensor networks, weather, agency reports, transport and utility status, and public reports. 2) Identify affected populations, including vulnerable people on registers, care facilities, schools and critical infrastructure. 3) Assess and project impact, with confidence bounds and explicit uncertainty. 4) Support resource coordination: what is available, where, and what is committed, across agencies. 5) Generate warnings and public information in accessible formats and multiple languages, targeted geographically. 6) Maintain the common operating picture and the decision log for the multi-agency command structure. 7) Support consequence management: shelter, welfare, transport, and utility restoration coordination. 8) Assemble the record for post-incident review and public inquiry, which in serious incidents will come.
**Systems** — Emergency management platform, GIS, sensor and weather feeds, agency systems, mass-notification, vulnerable-person registers.
**Outcome & KPIs** — Time to situational picture; warning reach and timeliness; vulnerable people contacted; inter-agency information consistency; decision-log completeness.
**Human gate** — **All command decisions are made by the designated commander under the statutory command structure.** The agent supports the picture; it never directs response.

### GOV-10 — Tax Administration & Compliance
**A6 · L2 · B4 · Record-to-report**
**Pain** — Tax authorities process enormous return volumes and must target limited compliance resource; taxpayer service demand spikes seasonally and is dominated by repetitive guidance questions.
**Trigger** — Return filed, risk-assessment cycle, or a taxpayer enquiry.
**Workflow** — 1) Validate returns for completeness and internal consistency, and identify obvious errors for correction rather than enquiry — correcting an error is cheaper for everyone than investigating it. 2) Risk-assess returns using the compliance risk model, with the contributing factors documented. 3) Cross-check against third-party data under the legal gateway and identify genuine discrepancies as distinct from timing and classification differences. 4) **Prioritise compliance interventions by expected yield and by behaviour change**, and choose the proportionate intervention: nudge, guidance, enquiry, or audit. 5) Prepare the caseworker's pack with the risk analysis, the data and the questions to ask. 6) For taxpayer service, answer guidance questions with cited legislation and guidance, and clearly distinguish general guidance from a ruling on the taxpayer's own affairs. 7) Detect vulnerable taxpayers and payment-difficulty signals and route to support. 8) Analyse error patterns to improve guidance and forms — the highest-leverage output.
**Systems** — Tax administration systems, third-party data, risk models, case management, guidance libraries, payment systems.
**Outcome & KPIs** — Compliance yield per intervention hour; error correction volume; enquiry strike rate; taxpayer service resolution; appeals upheld; guidance-driven error reduction.
**Human gate** — **All assessments, penalties and enquiry decisions are made by authorised officers.** Taxpayers have statutory rights to reasons and appeal; automated determination is restricted.

### GOV-11 — Workforce, Recruitment & Vetting Support
**A1 · L2 · B4 · Hire-to-retire**
**Pain** — Public-sector recruitment is process-heavy and slow, with fair and open competition requirements; vetting and clearance backlogs delay critical hires by months.
**Trigger** — Vacancy raised, application received, or a vetting submission.
**Workflow** — 1) Support job design: role requirements, essential criteria and fair, non-restrictive language, checked against equality obligations. 2) Sift applications against the published criteria only, with evidence quoted for each criterion, and **structural exclusion of characteristics that must not influence the assessment**. 3) Produce the sift record required to demonstrate fair and open competition, which is the legal standard the process must meet. 4) Manage scheduling, panel composition and candidate communication. 5) For vetting, validate the completeness and consistency of submissions and chase the specific gaps — most vetting delay is incomplete forms, not investigation. 6) Track vetting progress across the process and identify stalled cases. 7) Manage onboarding orchestration across security, IT, facilities and payroll. 8) Monitor recruitment fairness statistics across protected groups.
**Systems** — Recruitment platform, vetting systems, HR systems, identity and security systems, scheduling.
**Outcome & KPIs** — Time to hire; vetting cycle time; sift consistency and audit compliance; diversity of shortlists (monitored, not targeted by the agent); candidate experience.
**Human gate** — **All selection and vetting decisions are human.** Recruitment is an EU AI Act high-risk area; no auto-rejection, documented oversight, and candidate transparency are mandatory.

### GOV-12 — Grants Administration & Outcome Monitoring
**A8 · L2 · B3 · Record-to-report**
**Pain** — Grant programmes distribute large sums with limited monitoring capacity; reporting is compliance theatre and outcomes are rarely evidenced.
**Trigger** — Grant application, monitoring report due, or a programme review.
**Workflow** — 1) Assess applications against the published criteria with evidence and scoring rationale. 2) Verify applicant eligibility, financial standing and prior grant performance — the last is frequently unchecked across programmes. 3) Assess deliverability and value for money against comparable projects. 4) Prepare the assessment pack for the decision panel. 5) During delivery, process monitoring reports: validate claimed expenditure against grant conditions, check milestone evidence, and identify variance. 6) Detect risk signals: delayed milestones, expenditure profile deviation, changes in the recipient organisation, and duplicate funding across programmes. 7) **Analyse outcomes against the programme's stated objectives**, distinguishing outputs from outcomes and being honest where evidence is weak. 8) Generate programme reporting and evaluation inputs.
**Systems** — Grants management, finance systems, applicant registers, evaluation frameworks, document management.
**Outcome & KPIs** — Assessment cycle time; funds distributed on schedule; monitoring coverage; irregularities detected; outcome evidence quality; audit findings.
**Human gate** — Funding decisions are made by panels or accountable officers; suspected irregularity follows formal investigation process.

### GOV-13 — Planning, Licensing & Development Control
**A2 · L2 · B4 · Issue-to-resolution**
**Pain** — Planning and licensing applications involve complex policy, consultation, technical assessment and statutory deadlines. Backlogs delay housing and economic development and attract appeals.
**Trigger** — Application submitted.
**Workflow** — 1) Validate the application against submission requirements and return invalid applications immediately with specifics. 2) Identify applicable policies, designations and constraints for the site: local plan policies, conservation, flood risk, heritage, ecology, highways, and contamination. 3) Determine consultation requirements — statutory consultees, neighbours, publicity — and manage the process with deadlines. 4) Analyse consultation responses and objections by material planning consideration, **separating material from non-material objections** since only the former can lawfully influence the decision. 5) Assess the proposal against each relevant policy with the reasoning. 6) Draft the officer report with the assessment, the balance of considerations, and recommended conditions or reasons for refusal. 7) Track statutory determination deadlines and extension agreements. 8) Support appeals with the evidence base and the decision record.
**Systems** — Planning/licensing case management, GIS and constraint layers, policy documents, consultation platform, document management.
**Outcome & KPIs** — Determination within statutory period; appeals allowed against refusals; officer report quality; validation-stage rejections; consultation compliance.
**Human gate** — **Determination is made by planning officers under delegated authority or by committee.** Reports must reflect the officer's professional judgement; the agent drafts and evidences.

### GOV-14 — Internal Audit & Public Accountability
**A8 · L2 · B3 · Risk-to-assurance**
**Pain** — Public bodies face intense accountability (external audit, parliamentary scrutiny, public inquiry) with limited internal assurance capacity, so assurance is thin and reactive.
**Trigger** — Audit plan cycle, control monitoring, or an accountability request.
**Workflow** — 1) Build the audit universe and risk-assess it against strategic objectives, spend, change and prior findings. 2) Perform continuous control testing across the full transaction population — expenses, procurement, payroll, grants, and access. 3) Investigate exceptions with evidence assembly and cause classification. 4) Draft audit findings with condition, criteria, cause, consequence and recommendation. 5) Track management actions and verify implementation rather than accepting assertion. 6) Support external audit and scrutiny requests by mapping them to existing evidence. 7) **Assemble accountability responses**: parliamentary questions, committee requests and inquiry submissions, with accurate, complete and traceable evidence. 8) Report assurance coverage and residual risk to the audit committee.
**Systems** — Finance and HR systems, procurement, GRC/audit management, document management, data warehouse.
**Outcome & KPIs** — Population coverage vs sampling; findings raised and closed; repeat findings; external audit reliance; accountability response timeliness and accuracy.
**Human gate** — Audit opinions and conclusions are professional judgements of the head of internal audit; accountability responses are ministerially or executively cleared.

---
## Governance notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Administrative law** | Decisions must be made by an authorised person, with reasons, consistently, considering only relevant factors. This is why nearly every agent here is capped at L2 with a documented human decision-maker. |
| **EU AI Act (and analogues)** | Public benefit eligibility, law enforcement, migration and essential services are **high-risk or prohibited** categories. Social scoring is prohibited outright. Habagat must maintain conformity documentation and register systems where required. |
| **Automated decision-making (GDPR Art. 22 and equivalents)** | Citizens have rights regarding solely automated decisions with legal effect. Habagat's architecture must make the human decision genuine, not a rubber stamp — and must evidence that. |
| **Transparency & records** | Agent decision records are themselves public records subject to FOI and inquiry. Design logs to be disclosable: no gratuitous personal data, clear reasoning, retained per schedule. |
| **Sovereignty & residency** | Data residency, sovereign operation, and in some cases national-cloud requirements. Habagat's per-tenant Azure model supports this; multi-tenant SaaS generally cannot bid. |
| **Equality duties** | Public bodies have positive duties to assess and monitor differential impact. Bias monitoring is a statutory obligation here, not a best practice. |
