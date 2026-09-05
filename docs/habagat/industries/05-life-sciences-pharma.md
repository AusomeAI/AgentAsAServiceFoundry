# Document 05 — Life Sciences & Pharmaceuticals

> 14 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Pharma's cost structure is dominated by two things agents attack directly: **clinical development cycle time** (a day off a phase III is worth $1–8m in NPV for a large asset) and **regulated document production** (thousands of pages per submission, all requiring traceability).
- The regulatory constraint is **GxP validation**: any agent touching a GxP process must be validated under computerised-system-validation rules with 21 CFR Part 11 audit trails and e-signature integrity. Habagat must ship a validation package, not just software. This is a moat once built.
- Highest-value entry points: **LS-05 Regulatory Document Authoring**, **LS-03 Clinical Trial Site Selection & Feasibility**, **LS-08 Pharmacovigilance Case Processing** — the last of these is the industry's single largest pool of skilled manual labour.
- Commercial-side agents (MSL support, HCP engagement) require strict **promotional-compliance** controls: off-label discussion is a criminal-liability issue, so guardrails must be architectural.

---

### LS-01 — Scientific Literature Surveillance & Synthesis
**A3 · L1 · B1 · Idea-to-market**
**Pain** — Research and medical teams cannot keep pace with publication volume; systematic reviews take months; competitive science is missed.
**Trigger** — Scheduled surveillance run, a new publication matching a watch, or a researcher's question.
**Workflow** — 1) Query the defined sources: PubMed/Embase, preprint servers, conference abstracts, trial registries, patent databases. 2) Screen for relevance against the research question with explicit inclusion/exclusion criteria (PICO where applicable). 3) Extract structured data per publication: population, intervention, comparator, outcomes, effect sizes, study design and limitations. 4) **Assess study quality** with a recognised instrument and report it — a synthesis that weights a case series like an RCT is worse than no synthesis. 5) Synthesise across studies, identifying consistency, conflict and evidence gaps; never pool incomparable studies. 6) Produce the review with full citation traceability to the source sentence. 7) Flag findings that materially affect the company's programmes, and route to the responsible scientist.
**Systems** — Literature databases, reference management, internal research repository, trial registries, patent data.
**Outcome & KPIs** — Time to produce a review; coverage/recall against expert-curated sets; citation accuracy (must be 100% — fabricated citations are disqualifying); relevant findings surfaced before external notice.
**Human gate** — Scientific conclusions are authored and signed by qualified scientists. Anything with regulatory or safety implications routes to Medical Affairs/PV.

### LS-02 — Target & Asset Landscape Assessment
**A3 · L1 · B1 · Idea-to-market**
**Pain** — Business development and research strategy need a defensible picture of the competitive and IP landscape for a target or indication; assembling it takes analyst-weeks.
**Trigger** — A new target or in-licensing opportunity enters evaluation.
**Workflow** — 1) Map the biology: target, pathway, disease association, and the strength of genetic and translational validation evidence. 2) Map the competitive landscape: assets in development by phase, sponsor, modality and geography, from registries and disclosures. 3) Map the IP landscape: composition-of-matter and method-of-use families, expiries, and freedom-to-operate concerns — flagged for patent-counsel review, never concluded by the agent. 4) Analyse clinical precedent: what has failed in this target/indication and why (mechanism, safety, trial design, endpoint). Failure analysis is more valuable than success listing. 5) Assess the commercial context: standard of care, unmet need, payer environment, likely endpoints and regulatory precedent. 6) Produce the assessment with an explicit evidence/inference separation and a confidence statement per conclusion. 7) Identify the specific experiments or diligence that would most reduce uncertainty.
**Systems** — Trial registries, publication databases, patent databases, competitive intelligence sources, internal portfolio data.
**Outcome & KPIs** — Assessment cycle time; completeness vs expert review; decisions supported; diligence questions correctly anticipated.
**Human gate** — All investment, licensing and FTO conclusions are human; patent counsel owns all IP opinions.

### LS-03 — Clinical Trial Feasibility & Site Selection
**A3 · L2 · B2 · Idea-to-market**
**Pain** — Roughly a third of trial sites under-enrol or never enrol a patient. Site selection is relationship-driven and poorly evidenced, and it is the largest controllable driver of trial timelines.
**Trigger** — Protocol synopsis available; feasibility phase begins.
**Workflow** — 1) Translate protocol eligibility into a queryable patient profile. 2) Estimate the eligible population by geography from epidemiology, claims/EHR-derived real-world data and registry data, with stated assumptions. 3) Assess site performance history: prior enrolment rates in comparable studies, data quality, query rates, startup time, and staff turnover — the company's own data is the best predictor and is usually unused. 4) Assess the competitive trial landscape per site: how many competing studies are recruiting the same patients? 5) Model startup timelines by country: regulatory, ethics, and contract/budget cycle times. 6) Recommend a site portfolio and country mix optimised for enrolment rate, data quality and cost, with a sensitivity analysis. 7) Generate site-specific feasibility questionnaires targeted at the remaining unknowns. 8) During conduct, monitor actual vs predicted and recommend rescue actions early.
**Systems** — CTMS, EDC history, real-world data, trial registries, epidemiology sources, country regulatory databases.
**Outcome & KPIs** — Enrolment vs plan; % non-enrolling sites; time to first-patient-in and last-patient-in; cost per enrolled patient; forecast accuracy.
**Human gate** — Site selection is approved by clinical operations; investigator relationships are human-owned.

### LS-04 — Clinical Data Review & Query Management
**A6 · L2 · B4 · Idea-to-market**
**Pain** — Data management and medical monitors review enormous volumes of trial data for inconsistencies; queries are generated late and inconsistently, delaying database lock.
**Trigger** — Data entry/update in EDC, or a scheduled review cycle.
**Workflow** — 1) Run programmed edit checks and, beyond them, **cross-domain consistency review**: does the adverse-event record agree with the concomitant medication, the lab values and the visit narrative? This cross-domain reasoning is where automated checks stop and humans start. 2) Detect protocol deviations, including subtle eligibility and visit-window violations. 3) Identify data patterns warranting attention: implausible values, digit preference, unusual site-level distributions, and duplicate-subject signals. 4) Draft precise, non-leading queries to sites — query quality determines response time, and vague queries cost weeks. 5) Prioritise findings by impact on subject safety, primary endpoint integrity and submission readiness. 6) Support risk-based monitoring by ranking sites for on-site visits from data signals. 7) Track query resolution and escalate ageing items.
**Systems** — EDC (Medidata/Veeva), CTMS, safety database, statistical environment, RBQM platform.
**Outcome & KPIs** — Query rate and query-to-lock time; time to database lock; protocol deviations detected before monitoring visits; site-monitoring efficiency; critical data errors at lock.
**Human gate** — Medical monitors own all clinical interpretation and all safety judgements. GxP validation applies to the whole workflow.

### LS-05 — Regulatory Document Authoring & Submission Assembly
**A2 · L1 · B4 · Risk-to-assurance**
**Pain** — A single submission runs to tens of thousands of pages authored by dozens of people, requiring absolute internal consistency and full traceability to source data. Medical writing is a bottleneck at every milestone.
**Trigger** — Milestone reached (study report due, submission planned), or a health-authority information request.
**Workflow** — 1) Retrieve the applicable template and the authority's guidance for the document type (CSR, protocol, IB, Module 2 summaries, briefing book). 2) Assemble source content: statistical outputs, safety data, prior documents and approved standard text. 3) Draft sections with **every quantitative statement traceable to a specific output table** — the traceability is the deliverable, as much as the prose. 4) Enforce cross-document consistency: the same number must be identical in the CSR, the summary and the label discussion. Inconsistency is the most common and most damaging review finding. 5) Apply controlled terminology and house style. 6) Generate the traceability matrix and reviewer package. 7) Route through the review and approval workflow with 21 CFR Part 11-compliant e-signature and audit trail. 8) Assemble the eCTD structure and run technical validation before submission.
**Systems** — Document management (Veeva Vault RIM), statistical outputs, safety database, submission publishing tools, controlled terminology.
**Outcome & KPIs** — Authoring cycle time; review cycles per document; cross-document inconsistencies found in QC; technical validation errors; health-authority information requests attributable to document quality.
**Human gate** — **Qualified medical writers and regulatory professionals author and approve everything submitted.** GxP validation and Part 11 controls are mandatory.

### LS-06 — Regulatory Intelligence & Change Impact
**A6 · L2 · B3 · Risk-to-assurance**
**Pain** — Requirements change constantly across dozens of health authorities. Missing a change means a compliance failure or a submission rejection; tracking it manually is impossible at scale.
**Trigger** — Regulatory publication, guidance update, or a scheduled surveillance cycle.
**Workflow** — 1) Monitor authority sources across markets: guidances, regulations, pharmacopoeia updates, safety communications, and procedural changes. 2) Classify the change by type, market, therapeutic area and lifecycle stage affected. 3) **Impact assessment against the company's actual portfolio**: which products, which submissions in flight, which manufacturing sites, which labels. This mapping is the value; the monitoring is commodity. 4) Determine required actions and deadlines with the responsible function named. 5) Generate the impact assessment for the regulatory affairs lead. 6) Track actions to completion and evidence compliance. 7) Maintain the requirements library that other agents (LS-05) draw on.
**Systems** — Regulatory intelligence sources, RIM system, product registrations database, quality management system.
**Outcome & KPIs** — Changes detected within SLA; impact assessments completed on time; compliance actions closed by deadline; regulatory findings avoided; portfolio coverage.
**Human gate** — Regulatory strategy and compliance conclusions are made by qualified regulatory affairs professionals.

### LS-07 — Manufacturing Deviation & CAPA Management
**A8 · L2 · B4 · Plan-to-produce**
**Pain** — GMP deviations require investigation, root-cause analysis and CAPA within tight timelines; investigations are inconsistent and repeat deviations are common because root causes are never truly found.
**Trigger** — Deviation raised on the shop floor or in QC.
**Workflow** — 1) Capture the deviation with structured detail: what, when, where, batch, equipment, personnel, and immediate impact. 2) Retrieve context: batch record, equipment history, environmental monitoring, prior similar deviations, and change history — the last is the most frequent hidden cause. 3) Assess product impact and whether other batches are affected — a patient-safety and recall question that must be answered fast. 4) Support structured root-cause analysis, driving the investigation past the proximate cause to the systemic one. 5) **Trend analysis across deviations** to reveal the systemic issues that individual investigations always miss. 6) Draft the investigation report to the QMS standard with evidence citations. 7) Propose CAPAs with effectiveness checks defined up front — CAPAs without effectiveness criteria are the most common inspection finding. 8) Track CAPA execution and verify effectiveness.
**Systems** — QMS (Veeva/TrackWise), MES, LIMS, batch records, environmental monitoring, change control.
**Outcome & KPIs** — Investigation cycle time; repeat deviations; CAPA effectiveness rate; overdue investigations; inspection findings.
**Human gate** — **Quality Assurance approves every investigation conclusion, product-impact assessment and batch disposition.** The Qualified Person's release decision is never automated.

### LS-08 — Pharmacovigilance Case Processing
**A2 · L2 · B4 · Risk-to-assurance**
**Pain** — Adverse-event case processing is enormous, growing, deadline-bound (15-day expedited reporting) and almost entirely manual. It is the largest skilled-labour pool in pharma operations.
**Trigger** — Adverse event report from any source: HCP, patient, literature, clinical trial, social media, partner.
**Workflow** — 1) Determine whether the report is a **valid case**: identifiable patient, identifiable reporter, suspect product, and an event. Validity determination gates everything downstream. 2) Extract case data: demographics, product details including dose/route/dates, event description, dates, outcome, concomitant medications, medical history. 3) Code events and medications to MedDRA and WHO-DD with the correct level of specificity. 4) Assess seriousness against the regulatory criteria (death, life-threatening, hospitalisation, disability, congenital anomaly, medically important) — a definitional test, applied deterministically. 5) Assess expectedness against the reference safety information. 6) Draft the causality assessment with the reasoning: temporal relationship, dechallenge/rechallenge, alternative explanations, and biological plausibility. 7) Draft the case narrative to the required standard. 8) Determine reporting obligations by market and generate the E2B submission. 9) Identify follow-up questions needed and draft the query to the reporter. 10) Detect duplicate cases across sources.
**Systems** — Safety database (Argus/ArisG/Veeva Safety), MedDRA/WHO-DD dictionaries, literature sources, E2B gateways, RSI documents.
**Outcome & KPIs** — Cases processed per FTE; **on-time regulatory submission (must be 100%)**; coding accuracy vs QC; duplicate detection rate; narrative quality scores; case cycle time.
**Human gate** — **Qualified PV professionals review every case; the QPPV owns the system.** Causality and seriousness assessments are human-confirmed. Full GxP validation and Part 11 compliance required.

### LS-09 — Signal Detection & Benefit-Risk Monitoring
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Detecting a genuine safety signal early in a sea of noise is the core of post-market safety; statistical methods generate many candidates and evaluating each is expensive.
**Trigger** — Scheduled signal-detection cycle, or a threshold breach in disproportionality statistics.
**Workflow** — 1) Run disproportionality analyses across the safety database and external sources (FAERS, EudraVigilance, VigiBase). 2) Filter statistical signals for clinical plausibility and known confounding (indication bias, notoriety bias, protopathic bias) — the step that separates a signal from an artefact. 3) Assemble the evidence dossier: case series review, literature, clinical trial data, mechanistic plausibility, and class effects. 4) Characterise the potential signal: affected population, risk factors, severity, reversibility, and time-to-onset pattern. 5) Draft the signal evaluation with an explicit benefit-risk framing. 6) Recommend actions for the safety committee: further monitoring, label change, risk-minimisation measure, or study. 7) Track signal status and regulatory commitments.
**Systems** — Safety database, external safety data sources, statistical tools, literature, clinical data warehouse.
**Outcome & KPIs** — Signals evaluated per cycle; time from statistical signal to evaluation; validated-signal rate; regulatory commitments met; label updates supported.
**Human gate** — **Signal validation and all benefit-risk conclusions belong to the Safety Committee and the QPPV.** No safety conclusion is ever agent-authored.

### LS-10 — Medical Information Response
**A3 · L2 · B4 · Issue-to-resolution**
**Pain** — Medical information teams answer high volumes of HCP and patient product questions under strict promotional-compliance constraints, with mandated response times.
**Trigger** — Enquiry received by phone, email, web or from a field team.
**Workflow** — 1) Classify the enquiry and identify the requester type (HCP, patient, payer) — which determines what may be said. 2) Screen for an **adverse event or product-quality complaint embedded in the enquiry**; if present, route to PV/QA immediately and in parallel. This is a legal obligation and the most common failure point. 3) Retrieve the approved standard response document if one exists. 4) If not, draft from approved sources only: label, approved data, published literature. 5) **Enforce promotional-compliance boundaries architecturally**: off-label information may only be provided in response to an unsolicited request, in a scientific and balanced manner, with the constraints enforced by system rules rather than model judgement. 6) Include mandated safety information and full references. 7) Route for medical review and approval per the response's risk tier. 8) Deliver, log, and feed recurring enquiries into the standard-response library and to Medical Affairs strategy.
**Systems** — Medical information system, approved-content library, safety database, CRM, document management.
**Outcome & KPIs** — Response time vs SLA; % answered from standard responses; AE capture rate from enquiries (a compliance metric); medical-review pass rate; compliance findings (must be zero).
**Human gate** — Medical affairs approval on all non-standard responses; **all off-label content is human-reviewed without exception.**

### LS-11 — Field Medical (MSL) Insight & Engagement Support
**A4 · L1 · B4 · Demand creation**
**Pain** — MSLs generate valuable field insights that are captured inconsistently and rarely reach the organisation in usable form; preparation for KOL engagements is time-consuming.
**Trigger** — Upcoming engagement, or an interaction record submitted.
**Workflow** — 1) Prepare the engagement brief: the KOL's publications, trial involvement, prior interactions, stated interests and open scientific questions. 2) Assemble relevant approved scientific content and recent data. 3) Identify the scientific questions worth exploring, aligned to the medical plan. 4) After the interaction, structure the MSL's notes into coded insights: clinical practice observations, unmet need, competitive intelligence, and data gaps. 5) **Strip and route any adverse event or product complaint immediately to PV**, and any commercially-sensitive content away from prohibited audiences — the compliance firewall between Medical and Commercial is legally mandated. 6) Aggregate insights across the field into themes for the medical strategy team. 7) Track whether insights actually influenced strategy — the closing of a loop that almost never closes.
**Systems** — Medical CRM (Veeva), publication databases, approved-content library, safety database, insights repository.
**Outcome & KPIs** — Insight volume and quality; preparation time per engagement; insights influencing strategy; AE capture compliance; medical-plan coverage of priority KOLs.
**Human gate** — MSLs own all scientific exchange. The medical/commercial firewall is enforced by identity and data-access controls, not by prompt.

### LS-12 — Quality Control Laboratory Support
**A8 · L2 · B4 · Plan-to-produce**
**Pain** — QC labs handle high volumes of testing with strict documentation requirements; out-of-specification investigations are lengthy and inconsistent.
**Trigger** — Test result recorded, or an OOS/OOT result generated.
**Workflow** — 1) Review results against specifications and trend limits. 2) On an OOS, execute the phase-1 laboratory investigation checklist: analyst technique, instrument performance, standard preparation, calculation verification, system suitability. 3) Retrieve context: instrument calibration and maintenance history, reagent lots, analyst history, prior results on the same batch and method. 4) Support hypothesis-driven investigation and, where laboratory error is not confirmed, escalate to a full manufacturing investigation. 5) Trend analysis across results to detect method drift and instrument degradation *before* they generate OOS results. 6) Draft the investigation documentation to GMP standards. 7) Manage stability study scheduling, testing and trending, with shelf-life projections.
**Systems** — LIMS, chromatography data systems, instrument logs, QMS, stability programme.
**Outcome & KPIs** — OOS investigation cycle time; invalidated-OOS rate; method/instrument issues detected proactively; stability testing on schedule; data-integrity findings (must be zero).
**Human gate** — QA approves all OOS conclusions and batch dispositions. Data integrity (ALCOA+) requirements govern the entire workflow.

### LS-13 — Commercial Analytics & Field Force Effectiveness
**A6 · L1 · B3 · Demand creation**
**Pain** — Commercial teams have vast data (prescription, claims, call activity) and limited analyst capacity, so targeting and resource allocation are driven by habit.
**Trigger** — Planning cycle, performance review, or an anomaly detection.
**Workflow** — 1) Integrate prescription, claims, call-activity and market data at the permitted level of aggregation. 2) Analyse performance by territory, segment and account, decomposing market share into acquisition, retention and share-of-voice effects. 3) Detect anomalies: unexpected share shifts, access changes, formulary movements, and supply issues. 4) Diagnose causes by correlating with payer coverage, competitor activity and field effort. 5) Recommend resource reallocation with an expected-impact estimate. 6) Generate territory-level briefings that tell a representative what changed in *their* accounts and what to do about it. 7) Measure whether recommended actions produced the predicted effect.
**Systems** — Commercial data warehouse, prescription/claims data, CRM, payer/formulary data, BI.
**Outcome & KPIs** — Forecast accuracy; share trend vs market; call effectiveness; resource-reallocation impact; time to detect a market shift.
**Human gate** — All HCP-directed activity must comply with promotional rules; data use is bound by patient-privacy and data-licence terms (no patient-level re-identification, ever).

### LS-14 — Supply Chain Serialisation & Cold-Chain Integrity
**A6 · L3 · B4 · Plan-to-produce**
**Pain** — Track-and-trace regulations (DSCSA, EU FMD) and cold-chain requirements generate enormous transaction volumes with zero tolerance for integrity failures.
**Trigger** — Serialisation event, temperature excursion alert, or a verification request.
**Workflow** — 1) Monitor serialisation transactions for exceptions: missing events, aggregation mismatches, and verification failures. 2) Investigate exceptions by reconstructing the product's event chain across trading partners. 3) Detect potential counterfeit or diversion signals: duplicate serial numbers, impossible chains of custody, unexpected geographies. 4) On a **cold-chain excursion**, retrieve the product's stability data and the excursion profile, and compute the impact against the approved stability budget. 5) Recommend disposition (release, quarantine, destroy) with the full data package for QA. 6) Manage regulatory notifications and partner communications within required timelines. 7) Trend excursions by lane, carrier and packaging to fix the systemic cause.
**Systems** — Serialisation platform, ERP/WMS, IoT temperature monitoring, stability database, QMS, trading-partner EDI.
**Outcome & KPIs** — Serialisation exception rate and resolution time; excursion product loss ($); suspect-product investigations; regulatory notification timeliness; lane-level excursion reduction.
**Human gate** — **QA makes every product-disposition decision.** Suspect-counterfeit findings escalate immediately to Quality and Security.

---
## Regulatory notes for this vertical
| Regime | Impact on agent design |
|---|---|
| **GxP / CSV (GAMP 5)** | Any agent in a GxP process requires validation: URS, risk assessment, IQ/OQ/PQ, traceability matrix, and change control. Habagat must ship a **validation pack per agent**; model or prompt changes are change-controlled events. |
| **21 CFR Part 11 / EU Annex 11** | Audit trails, e-signature integrity, record retention and access controls are mandatory and must be demonstrably tamper-evident. |
| **ALCOA+ data integrity** | Every agent action must be attributable, legible, contemporaneous, original and accurate — this shapes the logging architecture, not just the policy. |
| **Promotional compliance (FDA OPDP, EFPIA)** | Off-label content controls must be architectural. The medical/commercial firewall is enforced by identity and data segregation. |
| **PV regulations (ICH E2B, GVP)** | Reporting deadlines are absolute; the QPPV holds personal accountability, which caps autonomy at L2. |
