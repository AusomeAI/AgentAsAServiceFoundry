# Document 12 — Education (K-12, Higher Education, Corporate Learning)

> 13 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Education budgets are constrained and procurement is slow, but the **administrative burden on teaching staff is the sector's defining problem**. Agents that give teachers and faculty hours back sell themselves internally.
- The commercially strongest segment is **higher education administration** — admissions, student services, research administration and compliance — where the volumes and the cost baselines are enterprise-scale.
- Anything touching student assessment or academic progression is high-risk under the EU AI Act and academically contentious. **Design assessment agents as feedback and consistency tools with the educator deciding.**
- Safeguarding is the non-negotiable design constraint in K-12: any disclosure or risk signal must route to a designated safeguarding lead immediately, and this must be architecturally guaranteed.

---

### EDU-01 — Student Enquiry & Support Services
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Student services handle enormous, highly seasonal volumes on admissions, enrolment, fees, timetabling, accommodation and welfare. Peak weeks are unstaffable.
**Trigger** — Student or applicant contacts by any channel.
**Workflow** — 1) Identify the person and their status (applicant, enrolled, alumnus) and entitlements. 2) Classify the enquiry, detecting the welfare and mental-health signals that hide inside administrative questions. 3) Retrieve the authoritative answer for **this student's specific programme, cohort and regulations** — general answers are frequently wrong at the individual level. 4) For status enquiries, retrieve the real position: application stage, fee balance, module registration, or accommodation allocation. 5) Resolve within the policy envelope: register for a module, book an appointment, issue a letter, set up a payment plan, or update details. 6) Where the answer depends on academic judgement or discretion, route to the right person with the context assembled. 7) **Escalate immediately on any welfare, safeguarding, harassment or crisis signal**, with a warm handoff rather than a referral. 8) Provide 24/7 coverage in the student's language, which matters disproportionately for international students.
**Systems** — Student information system, CRM, timetabling, accommodation, finance, welfare/case management.
**Outcome & KPIs** — First-contact resolution; response time in peak periods; welfare escalations made appropriately; student satisfaction; staff time released.
**Human gate** — All welfare, safeguarding and disciplinary matters; academic judgement; fee waivers and hardship decisions.

### EDU-02 — Admissions Processing & Applicant Assessment
**A2 · L2 · B4 · Order-to-cash**
**Pain** — Admissions teams process thousands of applications with varied international qualifications, in compressed cycles, with fairness and consistency obligations.
**Trigger** — Application received.
**Workflow** — 1) Validate completeness and request missing documents immediately with specifics. 2) Extract and structure qualifications, grades and English-language evidence, **normalising international qualifications against the institution's equivalency framework** — the most specialised and time-consuming step. 3) Verify document authenticity and detect the known fraud patterns in credentials. 4) Assess against the published entry criteria, showing which criteria are met by which evidence. 5) Identify applications requiring academic judgement — contextual admissions, non-standard qualifications, portfolios, personal statements — and route them with the assessment structured. 6) **Explicitly exclude characteristics that must not influence assessment**, and monitor outcomes across demographic groups continuously. 7) Prepare the admissions officer's pack with the recommendation, the evidence, and the discretionary questions. 8) On decision, generate offers with conditions, and manage the conditions to satisfaction through to enrolment. 9) Support the clearing/late-cycle process where speed determines outcomes.
**Systems** — Admissions/SIS, qualification equivalency databases, document verification, CRM, communications.
**Outcome & KPIs** — Time-to-decision; applications per officer; conversion rate; **differential outcomes across groups (a monitored guardrail)**; offer-condition satisfaction rate; appeals.
**Human gate** — **All admission decisions are human.** Education access is EU AI Act high-risk: human oversight, transparency and appeal rights are mandatory. No auto-rejection.

### EDU-03 — Teaching Preparation & Curriculum Support
**A3 · L1 · B2 · Idea-to-market**
**Pain** — Teachers and lecturers spend large portions of their week on preparation, differentiation and resource creation — work that is repeated across thousands of institutions.
**Trigger** — Educator requests support for a lesson, module or scheme of work.
**Workflow** — 1) Understand the context: subject, level, curriculum specification, prior learning, class composition and time available. 2) Retrieve the applicable curriculum standards and assessment objectives, and align everything to them explicitly. 3) Generate lesson and sequence plans with learning objectives, activities, timings, resources and assessment opportunities. 4) **Differentiate for the actual class**: support for students working below expectation, extension for those above, and adjustments for identified additional needs — the task teachers most want help with and least have time for. 5) Generate resources: explanations at multiple levels, worked examples, practice questions with answers, and misconception-targeted activities. 6) Check content for accuracy, age-appropriateness, curriculum alignment and inclusive representation. 7) Suggest formative assessment aligned to the objectives and likely misconceptions. 8) Learn the educator's style and the institution's frameworks over time.
**Systems** — Curriculum frameworks, learning management system, resource repositories, assessment banks, student data (aggregate/anonymised where possible).
**Outcome & KPIs** — Preparation time saved; resource reuse; curriculum coverage; educator satisfaction; differentiation provision.
**Human gate** — **Educators review all materials before use.** Subject accuracy and pedagogical appropriateness are professional judgements.

### EDU-04 — Assessment, Feedback & Marking Support
**A4 · L1 · B4 · Idea-to-market**
**Pain** — Marking is the largest single time cost in teaching and the slowest feedback loop for students. Consistency across markers is a persistent quality problem.
**Trigger** — Submission received, or a marking cycle begins.
**Workflow** — 1) Apply the published marking rubric to the submission, identifying evidence for each criterion. 2) **Generate formative feedback that is specific and actionable**: what was done well, what specifically to improve, and how — generic feedback is the student's most common complaint. 3) Provide an indicative mark **as a recommendation to the marker**, never as a grade. 4) Support moderation: identify submissions where markers diverge, and check consistency of standards across a cohort and across markers. 5) Detect academic-integrity concerns — including AI-generated submission indicators — and refer them for human investigation, **never accuse**, because false accusations of academic misconduct cause serious harm and these detectors are unreliable. 6) Analyse cohort performance against learning objectives to identify what was not learned, which is feedback to the teaching rather than the student. 7) Track feedback turnaround and quality.
**Systems** — LMS, assessment platforms, plagiarism/integrity tools, rubrics, student records.
**Outcome & KPIs** — Feedback turnaround; feedback quality ratings by students; marker consistency (variance across markers); attainment; **integrity referral precision**.
**Human gate** — **All grades are determined by qualified educators.** Academic integrity decisions follow formal process with the student's right to respond. Assessment is EU AI Act high-risk.

### EDU-05 — Student Retention & Early Intervention
**A6 · L2 · B4 · Issue-to-resolution**
**Pain** — Students disengage gradually and visibly in the data, but institutions notice at the point of withdrawal. Retention is both a student-welfare and a financial issue.
**Trigger** — Continuous monitoring of engagement and performance signals.
**Workflow** — 1) Monitor engagement signals: attendance, VLE activity, submission patterns, library and campus access, and assessment performance. 2) Detect deviation from the **student's own baseline** rather than from a cohort average — comparing a student to a cohort mislabels the naturally low-engagement student and misses the sharp personal decline. 3) Contextualise: is this a pattern across the cohort (a teaching or assessment issue) or individual (a student issue)? The distinction determines who acts. 4) Assess risk with the contributing factors made explicit and available to the person who will make contact. 5) Route to the appropriate support: academic tutor, wellbeing, finance, disability support, or study skills. 6) Support the intervention with a briefing, avoiding a conversation that begins "the system flagged you", which is corrosive. 7) Track intervention outcomes to learn what actually works, by student segment. 8) Report systemic patterns: modules, cohorts and transitions with elevated risk.
**Systems** — Student records, VLE/LMS analytics, attendance, library and access systems, support case management.
**Outcome & KPIs** — Continuation and completion rates; time from disengagement to contact; intervention effectiveness by type; **attainment gaps across student groups**; student trust (a real risk if surveillance is perceived).
**Human gate** — **All student contact is by a human.** Predictions are never disclosed as scores to students, and never used in academic decisions. Transparency about monitoring is mandatory and should be a deliberate design feature.

### EDU-06 — Timetabling & Resource Scheduling
**A5 · L2 · B3 · Plan-to-produce**
**Pain** — Timetabling balances rooms, staff, student pathways, equipment and constraints across thousands of events. It is done annually under time pressure and produces poor student experience.
**Trigger** — Timetabling cycle, or a change requiring reschedule.
**Workflow** — 1) Assemble requirements: modules, enrolments, staff availability, room and equipment needs, and pathway combinations students must be able to take. 2) Identify genuine conflicts in the pathway structure — combinations that cannot be timetabled — and surface them to programme design early, when they are still fixable. 3) Generate a timetable satisfying hard constraints (capacity, availability, statutory rest, accessibility requirements) and optimising soft ones (student travel and gaps, staff preference, room utilisation). 4) Model the student experience explicitly: fragmented days and long gaps are the most common complaint and are rarely optimised for. 5) Handle changes in-term with minimal disruption and clear communication. 6) Manage examination timetabling with its own constraints, including reasonable adjustments. 7) Report utilisation to inform estate decisions.
**Systems** — Timetabling system, SIS, estates/room booking, HR/staff availability, accessibility requirements.
**Outcome & KPIs** — Constraint violations; room utilisation; student timetable quality (gaps, travel, day fragmentation); change volume in-term; staff satisfaction.
**Human gate** — Timetabling managers approve publication; accessibility adjustments are individually reviewed.

### EDU-07 — Research Grant Administration & Compliance
**A8 · L2 · B4 · Record-to-report**
**Pain** — Research administration is a compliance burden on academics: proposal preparation, costing, ethics, funder rules, reporting and audit. Non-compliance risks clawback and reputational damage.
**Trigger** — Funding call, proposal preparation, award, or a reporting deadline.
**Workflow** — 1) Monitor funding calls and match them to researcher profiles and institutional priorities. 2) Support proposal preparation: funder requirements, eligibility, page limits, mandatory sections, and prior successful examples. 3) Build the costing against the funder's rules and the institution's rates, including full economic costing where applicable — a specialised and error-prone task. 4) Check compliance requirements: ethics approval, data management plan, open access, export control, dual-use, and partner due diligence. 5) On award, set up the project with the funder's terms encoded so eligibility rules are enforced at spend rather than discovered at audit. 6) Monitor spend against budget and eligibility rules, flagging ineligible or at-risk expenditure early. 7) Assemble financial and technical reports to the funder's format from the underlying evidence. 8) Support audit with the evidence trail.
**Systems** — Research management (Pure/Converis), finance/ERP, HR, ethics systems, funder portals, publication repositories.
**Outcome & KPIs** — Proposal submission rate and success rate; costing accuracy; ineligible expenditure prevented; report timeliness; audit findings and clawback.
**Human gate** — Ethics approvals, funder submissions and financial certifications are made by authorised officers; research integrity matters follow formal process.

### EDU-08 — Alumni Engagement & Development
**A7 · L2 · B3 · Demand creation**
**Pain** — Development offices manage large alumni populations with small teams; engagement is generic and philanthropic potential is poorly identified.
**Trigger** — Engagement cycle, alumni interaction, or a campaign.
**Workflow** — 1) Maintain alumni records with career progression and engagement history, using consented and legitimately sourced data only. 2) Segment by affinity, engagement and capacity, with **strict ethical boundaries on wealth screening** and full transparency in the privacy notice. 3) Personalise communications around genuine relevance: their subject, their cohort, their location, their expressed interests. 4) Identify engagement opportunities that are not asks: mentoring, guest lectures, placements, and networks — engagement precedes giving and is more valuable in aggregate. 5) Support the development officer with a relationship briefing before any meeting. 6) Manage campaign execution, response handling and stewardship, including timely and specific thanks. 7) Track engagement and giving outcomes; report on donor retention rather than only acquisition.
**Systems** — Alumni/CRM (Raiser's Edge, Advance), events, communications, finance/gift processing, consent management.
**Outcome & KPIs** — Engagement rate; volunteer participation; donor retention; funds raised; opt-out rate (guardrail); data-protection complaints.
**Human gate** — Major-gift relationships are human-owned; all data use complies with consent and legitimate-interest assessments.

### EDU-09 — Safeguarding & Wellbeing Case Management
**A1 · L1 · B4 · Risk-to-assurance**
**Pain** — Safeguarding concerns arrive across many channels; recognising patterns across fragmented records is exactly where the serious case reviews find failure.
**Trigger** — Concern raised by staff, student, parent, or detected in a communication.
**Workflow** — 1) Capture the concern with structured, factual detail and immediate timestamping — contemporaneous records are the evidential backbone of safeguarding. 2) Assess urgency against the safeguarding framework and **escalate immediately to the designated safeguarding lead for anything meeting the threshold**; there is no queue for this. 3) Assemble relevant history across records with strict access control, surfacing patterns across time and across sources that individual staff cannot see. 4) Prompt the required process steps: referrals to statutory agencies, parental contact rules, and record requirements. 5) Track actions, deadlines and outcomes. 6) Support information sharing with statutory partners under the correct legal basis. 7) Analyse aggregate patterns for prevention — locations, times, cohorts — without individual profiling. 8) Maintain a fully auditable record for inspection and inquiry.
**Systems** — Safeguarding case management (CPOMS/MyConcern), student records, communications monitoring (where lawfully deployed), referral pathways.
**Outcome & KPIs** — Time from concern to DSL review; statutory referral timeliness; record completeness; pattern detection; inspection outcomes.
**Human gate** — **Every safeguarding decision is made by the designated safeguarding lead.** The agent never assesses risk to a child as a conclusion; it surfaces, structures and prompts. Access is tightly restricted and fully audited.

### EDU-10 — Corporate Learning & Skills Development
**A4 · L2 · B2 · Hire-to-retire**
**Pain** — Corporate L&D produces generic catalogues; learners cannot find what they need; skills gaps are asserted rather than measured; completion is confused with capability.
**Trigger** — Learner request, role change, skills assessment, or a capability-planning cycle.
**Workflow** — 1) Build the skills picture: role requirements, current capability evidence, and career aspiration. 2) Identify gaps against both the current role and the target role, distinguishing critical from nice-to-have. 3) Recommend learning paths, prioritising **application over consumption** — a stretch assignment usually beats a course, and the agent should say so. 4) Curate content from internal and external sources matched to the learner's level, context and time available. 5) Support learning in the flow of work: answer questions with grounded explanations at the point of need. 6) Assess capability through applied evidence rather than completion, where the domain allows. 7) Aggregate skills data to give the organisation a genuine capability picture and inform workforce planning. 8) Measure whether learning changed performance, which almost no L&D function can currently evidence.
**Systems** — LMS/LXP, HRIS, skills taxonomy, content libraries, performance data.
**Outcome & KPIs** — Skills gap closure; time-to-competence; learning applied (manager-verified); internal mobility; capability coverage in critical roles.
**Human gate** — Skills data used in performance or promotion decisions requires HR governance and employee transparency; works-council consultation applies in many jurisdictions.

### EDU-11 — Institutional Reporting & Regulatory Returns
**A8 · L2 · B4 · Record-to-report**
**Pain** — Statutory returns (student data, staff data, finance, outcomes) are large, definition-heavy and carry funding consequences for errors.
**Trigger** — Return deadline or a data-collection cycle.
**Workflow** — 1) Map each return's requirements to source data and owners. 2) Extract and validate against the regulator's rules and definitions, which differ subtly from internal usage and are the main source of error. 3) Detect and diagnose data-quality issues at source, with the specific records identified for correction. 4) Reconcile across returns — the same student or staff member must be reported consistently in different collections, and inconsistency triggers regulatory queries. 5) **Explain year-on-year movements** before the regulator asks. 6) Assemble the submission with sign-off evidence. 7) Manage regulator queries and corrections. 8) Track the metrics that drive funding and rankings, so the institution sees the consequence before submission rather than after.
**Systems** — SIS, HR, finance, data warehouse, regulatory submission platforms.
**Outcome & KPIs** — On-time submission; data-quality errors; amendments and resubmissions; funding impact of data errors; query response time.
**Human gate** — Returns are attested by the accountable officer; data-quality corrections at source require the record owner.

### EDU-12 — Estates, Facilities & Campus Operations
**A5 · L3 · B2 · Plan-to-produce**
**Pain** — Campus estates are large, ageing and heavily utilised; maintenance is reactive and space is simultaneously scarce and under-utilised.
**Trigger** — Fault reported, maintenance schedule, or a space-planning cycle.
**Workflow** — 1) Triage reported faults for safety, impact and urgency, and dispatch with the diagnosis and likely parts. 2) Manage planned and statutory maintenance: fire safety, water hygiene, lifts, electrical testing — compliance items with legal deadlines. 3) Monitor building systems for energy waste and developing faults. 4) Analyse space utilisation against timetabled and actual occupancy — timetabled utilisation systematically overstates real usage, and the gap is the estate strategy. 5) Support space planning and rationalisation with evidence. 6) Manage the maintenance backlog with risk-based prioritisation, and quantify the consequence of deferral for capital planning. 7) Coordinate campus events, access and safety requirements.
**Systems** — CAFM/estates management, BMS, timetabling, occupancy sensing, compliance registers.
**Outcome & KPIs** — Statutory compliance rate; fault response and fix times; energy cost per square metre; space utilisation; backlog risk profile.
**Human gate** — Safety-critical compliance is signed by qualified persons; capital decisions are governed.

### EDU-13 — Quality Assurance & Programme Review
**A8 · L2 · B3 · Risk-to-assurance**
**Pain** — Programme approval, monitoring and periodic review are documentation-heavy exercises that consume academic time and produce limited insight.
**Trigger** — Programme approval, annual monitoring, or a periodic review cycle.
**Workflow** — 1) Assemble the evidence base per programme: recruitment, progression, attainment (including gaps across student groups), satisfaction, employment outcomes, and external examiner reports. 2) Benchmark against comparable programmes internally and, where available, sector data. 3) **Identify issues from the evidence rather than from the narrative** — annual monitoring reports overwhelmingly report that everything is fine, and the data frequently disagrees. 4) Check curriculum alignment against professional body requirements and qualification frameworks. 5) Analyse external examiner and student feedback for themes and unresolved recurring issues. 6) Draft the monitoring or review report with evidence and specific actions. 7) Track action completion and verify impact in the following cycle. 8) Prepare evidence packs for external quality review and accreditation.
**Systems** — SIS, survey platforms, external examiner systems, curriculum management, quality management records.
**Outcome & KPIs** — Review cycle effort; issues identified from evidence; action completion and verified impact; attainment gap reduction; accreditation outcomes.
**Human gate** — Academic quality judgements and programme decisions are made by academic governance bodies.

---
## Governance notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **EU AI Act** | Education access, assessment, and monitoring during exams are **high-risk**. Emotion recognition in education is **prohibited**. Human oversight, transparency to students, and appeal routes are mandatory. |
| **Child protection & safeguarding** | Any signal of harm routes to a designated lead immediately, bypassing all queues. Access to safeguarding records is tightly restricted and fully audited. |
| **Student data protection (GDPR, FERPA)** | Purpose limitation is strict; learning analytics require transparency and, in many jurisdictions, a lawful basis beyond consent. Students must know they are monitored. |
| **Academic integrity** | AI-detection tools are unreliable; they may generate a referral for human investigation but never a finding. False accusations cause serious harm. |
| **Equality & attainment gaps** | Differential outcomes across student groups must be monitored and reported for every agent that touches selection, assessment or intervention. |
