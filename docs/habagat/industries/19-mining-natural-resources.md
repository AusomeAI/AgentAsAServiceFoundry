# Document 19 — Mining, Metals & Natural Resources

> 12 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Mining is capital-intensive, remote, safety-critical and increasingly scrutinised on environmental and social performance. Agents earn their place through **asset availability, safety leading indicators and permit-to-operate evidence** — not through headcount.
- The single largest financial lever is **fixed-plant and mobile-fleet availability (MIN-03, MIN-04)**: a percentage point of availability on a concentrator is worth more than the entire IT budget at most operations.
- **MIN-09 Tailings & Environmental Monitoring** is the agent with the highest consequence. Post-Brumadinho, tailings governance is board-level and the evidence obligations are formal. This is a compliance-driven purchase.
- Design constraints are physical: remote sites, intermittent satellite connectivity, harsh conditions and OT isolation. **Edge-capable, offline-tolerant design is mandatory**, not optional.

---

### MIN-01 — Exploration Data Integration & Target Generation
**A3 · L1 · B2 · Idea-to-market**
**Pain** — Exploration data spans decades, formats and companies: drill logs, assays, geophysics, geochemistry and mapping, much of it on paper or in incompatible systems. Re-interpretation is expensive and repeated.
**Trigger** — New data acquired, target review, or an acquisition due diligence.
**Workflow** — 1) Ingest and digitise historical exploration data including scanned logs and legacy formats, extracting structured records. 2) **Reconcile and validate against the geological database**: coordinate systems, datums, assay methods and detection limits, and downhole survey corrections — errors here propagate into every interpretation downstream. 3) Integrate multi-disciplinary datasets spatially: geology, geochemistry, geophysics, remote sensing and structural data. 4) Identify anomalies and coincident signatures consistent with the deposit model being targeted. 5) Generate ranked exploration targets with the supporting evidence and the confidence in each dataset, clearly separating observation from interpretation. 6) Support drill programme planning: hole placement to test the hypothesis, with cost and access considerations. 7) Maintain the audit trail for resource reporting, which requires demonstrable data provenance. 8) Assist due diligence on acquisition targets by assessing the quality and completeness of their data.
**Systems** — Geological database (acQuire/DataShed), GIS, geophysical and geochemical datasets, modelling software, document archives.
**Outcome & KPIs** — Data digitised and validated; targets generated and drill-tested; discovery cost per target; data quality issues found; due-diligence turnaround.
**Human gate** — **Geological interpretation is the geologist's**; Competent Person / Qualified Person sign-off is required under JORC/NI 43-101 for any public resource statement.

### MIN-02 — Mine Planning & Production Scheduling
**A5 · L2 · B3 · Plan-to-produce**
**Pain** — Plans are built on assumptions that diverge from reality within days; reconciliation between plan, model and actual is slow, so the plan is trusted less each week.
**Trigger** — Planning cycle, deviation from plan, or a market or geological change.
**Workflow** — 1) Build the schedule from the resource model, mine design and equipment capability, respecting geotechnical, ventilation and access constraints. 2) Optimise for value rather than tonnes: grade, blending requirements, stripping ratio, processing constraints, and price. **Optimising for volume when the constraint is mill throughput or grade destroys value.** 3) Model equipment and labour requirements and identify the binding constraint explicitly. 4) Reconcile actuals against plan and against the resource model — the grade and tonnage reconciliation that tells you whether the model is right, and which most operations do too slowly to act on. 5) Diagnose deviation: geological variance, equipment availability, weather, or execution. 6) Re-plan on deviation with the value consequence quantified for each option. 7) Support short-interval control with shift-level targets and real-time progress. 8) Model scenarios: price changes, cut-off grade changes, and equipment strategy.
**Systems** — Mine planning software (Deswik/Vulcan/MineSched), fleet management, resource model, ERP, processing data.
**Outcome & KPIs** — Plan compliance; grade and tonnage reconciliation variance; value per tonne; constraint utilisation; re-plan cycle time.
**Human gate** — Mine plans are approved by the mining engineer and manager; geotechnical constraints are absolute and set by qualified engineers.

### MIN-03 — Fixed Plant Reliability & Process Optimisation
**A6 · L3 · B3 · Plan-to-produce**
**Pain** — Concentrator and processing plant availability and recovery drive revenue directly. Failures on critical equipment stop the whole plant, and small recovery losses compound over millions of tonnes.
**Trigger** — Continuous process and condition monitoring.
**Workflow** — 1) Monitor equipment condition on critical assets: mills, crushers, pumps, conveyors, flotation and thickeners — vibration, temperature, power draw, and acoustic signals. 2) Detect developing faults and estimate remaining useful life with confidence bounds, prioritising by criticality to throughput. 3) Monitor process performance: throughput, recovery, grade, reagent consumption and energy, normalised for ore characteristics — **unnormalised recovery reporting hides everything that matters** because ore variability dominates. 4) Correlate performance with ore feed characteristics from the block model and on-line analysis, and recommend setpoints for the current feed. 5) Detect process instability and drift, and diagnose the cause: equipment, feed, control loop, or operator intervention. 6) Recommend maintenance timing that minimises production loss, coordinating with planned shutdowns. 7) Support shutdown planning: scope, sequencing, resources and critical path, since shutdown overruns are extremely expensive. 8) Report losses by cause, quantified in recovered metal.
**Systems** — Historian/PI, control systems (read-only), condition monitoring, CMMS, on-line analysers, laboratory (LIMS), block model.
**Outcome & KPIs** — Plant availability and utilisation; recovery vs ore-adjusted target; unplanned downtime; shutdown duration vs plan; reagent and energy per tonne.
**Human gate** — Metallurgists and control-room operators make all process changes; **the agent never writes to control systems**.

### MIN-04 — Mobile Fleet Management & Maintenance
**A6 · L3 · B3 · Plan-to-produce**
**Pain** — Haul trucks, loaders and drills are enormous capital assets whose availability and productivity determine mine output; maintenance is reactive and productivity losses are poorly understood.
**Trigger** — Telemetry signal, maintenance schedule, or a productivity deviation.
**Workflow** — 1) Monitor equipment health from onboard telemetry: engine, drivetrain, hydraulics, tyres, and structural loading. 2) Detect developing faults and predict failure with the specific component identified, so the right parts and skills are ready. 3) Analyse productivity: cycle times, payload, queuing, and idle time, decomposed to identify whether the constraint is loading, hauling, dumping or dispatch. **The constraint moves, and optimising the wrong element wastes the effort.** 4) Detect operating practices affecting equipment life and safety — overloading, harsh braking, speeding — framed as coaching, with individual data handled per the site's agreements. 5) Optimise maintenance scheduling against production requirements and workshop capacity. 6) Manage the parts supply chain for remote operations, where lead times are long and stockouts are catastrophic — availability planning matters more than cost optimisation. 7) Support tyre management, a major cost and safety item with its own specific failure modes. 8) Analyse total cost of ownership and inform replacement timing.
**Systems** — Fleet management system, equipment telemetry, CMMS, parts inventory, dispatch, workshop systems.
**Outcome & KPIs** — Equipment availability and utilisation; unplanned failures; cost per tonne hauled; parts availability; tyre life; maintenance cost per operating hour.
**Human gate** — Maintenance decisions are made by qualified personnel; safety-critical defects immediately remove equipment from service, non-negotiably.

### MIN-05 — Health, Safety & Critical Risk Management
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Mining fatalities cluster around a small number of well-known material risks. Controls exist on paper; verifying that they are actually in place, every shift, is the hard part.
**Trigger** — Work planned, permit requested, observation or incident reported, or a control verification cycle.
**Workflow** — 1) Maintain the critical-risk register with its **critical controls** — the specific controls that prevent a fatality — and their verification requirements. 2) Verify controls before high-risk work: isolation, ground support, ventilation, traffic management, working at height, and confined space. Verification is the whole discipline; a control that is not verified is not a control. 3) Manage permits and authorisations with competence verification for the specific task. 4) Detect activity conflicts creating combined risk that neither activity creates alone. 5) Process observations, near-misses and incidents with structured capture, immediate escalation for high-potential events, and — critically — the same rigour for high-potential near-misses as for actual incidents. 6) **Analyse leading indicators**: control verification rates, observation quality, and the conditions preceding high-potential events. 7) Support investigation with evidence assembly, timeline reconstruction and systemic cause analysis. 8) Track actions to verified closure and report on critical control effectiveness to the board, which is now a governance expectation.
**Systems** — Safety management system, permit systems, competence and training records, incident reporting, monitoring systems.
**Outcome & KPIs** — Critical control verification rate; high-potential incident frequency; fatality and serious-injury prevention; action closure; leading-indicator trends.
**Human gate** — **All safety decisions are made by appointed competent persons.** The agent verifies, prompts and records; it never authorises work. Statutory investigation processes are human-led.

### MIN-06 — Environmental Monitoring & Permit Compliance
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Operations run under complex permits covering water, air, noise, dust, land disturbance and rehabilitation. Breaches carry criminal liability, production stoppages and licence-to-operate consequences.
**Trigger** — Monitoring data, permit condition, weather event, or a reporting deadline.
**Workflow** — 1) Maintain the permit and obligation register with conditions, limits, monitoring requirements and reporting deadlines per site. 2) Ingest monitoring data: water quality and quantity, air quality and dust, noise, vibration and blast monitoring, and biodiversity surveys. 3) Compare against limits continuously and **detect trend toward exceedance before breach**, which is the difference between managing and reporting. 4) On exceedance, determine reportability and generate the notification within the statutory deadline. 5) Correlate environmental signals with operational activity to identify the cause and the controllable action. 6) Manage water balance across the site, which in many operations is the binding operational constraint and a major risk in both drought and flood. 7) Track rehabilitation obligations, progress and the closure liability provision. 8) Assemble regulatory returns and community-facing reporting with the data lineage.
**Systems** — Environmental monitoring networks, LIMS, weather, GIS, permit register, ERP/finance for provisioning.
**Outcome & KPIs** — Permit compliance rate; exceedances predicted and prevented; notification timeliness (100% required); rehabilitation progress vs plan; closure liability accuracy.
**Human gate** — All regulatory notifications and environmental conclusions are made by the accountable environmental manager; closure provisions are governed accounting judgements.

### MIN-07 — Metallurgical Accounting & Reconciliation
**A8 · L2 · B4 · Record-to-report**
**Pain** — Reconciling metal from resource model to mine to plant to product is complex and error-prone; unexplained losses are common and disputes with joint venture partners and customers are expensive.
**Trigger** — Production period end, or a continuous reconciliation cycle.
**Workflow** — 1) Assemble the mass and metal balance across the chain: mined tonnes and grade, stockpiles, plant feed, concentrate, tailings, and product shipped. 2) Validate measurement data: weightometers, sampling, assay and moisture, checking calibration currency and sampling protocol compliance — **most reconciliation disputes are measurement problems, not accounting problems**. 3) Compute the balance with error bounds derived from the measurement uncertainty, rather than presenting a false-precision number. 4) Identify and investigate discrepancies beyond the expected error, distinguishing measurement error, stockpile estimation error, model error and genuine loss. 5) Reconcile back to the resource model to inform model reconciliation factors, which is how the model improves. 6) Support metal accounting to the standard required by joint venture agreements, offtake contracts and financial reporting. 7) Generate the reconciliation report with the evidence and the uncertainty stated. 8) Support commercial settlement including assay exchange and umpire processes.
**Systems** — Plant historian, LIMS, weightometers, survey data, resource model, ERP, shipping systems.
**Outcome & KPIs** — Reconciliation variance and its trend; unexplained loss; measurement system compliance; settlement disputes; model reconciliation factors.
**Human gate** — Metal accounting is signed by the accountable metallurgist and finance; commercial settlements are contractual decisions.

### MIN-08 — Supply Chain & Logistics for Remote Operations
**A6 · L2 · B3 · Procure-to-pay**
**Pain** — Remote operations depend on long, fragile supply chains. A stockout of a critical spare can stop production for weeks; carrying everything is capital-destructive.
**Trigger** — Demand signal, inventory threshold, supply disruption, or a planning cycle.
**Workflow** — 1) Classify inventory by criticality — the consequence of a stockout, not the cost of the item, which is the classification most operations get backwards. 2) Optimise stocking policy per item against lead time, demand variability, criticality and shelf life. 3) Forecast demand from maintenance plans, production schedules and consumption patterns. 4) Monitor supply chain risk: supplier performance, transport disruption, weather windows for seasonal access, port and border issues. 5) Detect and respond to disruption with alternatives: alternate supplier, expedited freight, borrowing from a sister site, or manufacturing locally. 6) Manage the logistics constraints specific to the operation: barge or road seasons, air freight limits, and dangerous-goods requirements. 7) Reduce obsolete and slow-moving inventory, which accumulates enormously at remote sites, with disposal or redistribution recommendations. 8) Report working capital against service level so the trade-off is explicit.
**Systems** — ERP/inventory, CMMS, supplier systems, logistics providers, weather and access data.
**Outcome & KPIs** — Critical-item availability; stockout production loss; inventory value and obsolescence; expedite cost; supplier on-time performance.
**Human gate** — Sourcing decisions and expedite spend above threshold; safety-critical parts require engineering approval of alternates.

### MIN-09 — Tailings, Geotechnical & Structural Monitoring
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Tailings storage facilities and pit walls are catastrophic-consequence structures. Monitoring data is voluminous, and the signals preceding failure are subtle and easily lost.
**Trigger** — Continuous instrumentation monitoring, inspection, or a triggering event (rainfall, seismic, operational change).
**Workflow** — 1) Ingest instrumentation data continuously: piezometers, inclinometers, survey prisms, radar, seismic and settlement monitoring. 2) Validate instrument health and identify failed or drifting instruments — **a quiet instrument may be a failed instrument, and treating silence as safety is a documented failure pattern**. 3) Compare readings against the trigger action response plan thresholds and detect trend toward them. 4) Correlate across instruments and with drivers: rainfall, water level, deposition rate, seismic events, and adjacent mining activity. 5) Detect anomalous patterns that individual thresholds would miss, such as accelerating displacement within the alert band. 6) On threshold breach, trigger the TARP response with the defined notifications and actions, immediately and without discretion. 7) Support the engineer of record and the independent review with data packages and trend analysis. 8) Maintain the governance evidence required under the tailings standards, which is now formally auditable.
**Systems** — Geotechnical instrumentation networks, monitoring platforms, survey systems, weather and seismic data, document management.
**Outcome & KPIs** — Instrument data availability and validity; threshold breaches detected and responded to within TARP timeframes; governance evidence completeness; independent review findings.
**Human gate** — **The engineer of record and the accountable executive own all geotechnical judgements.** TARP escalations are executed by humans; the agent detects, alerts and evidences. This is the highest-consequence use case in the entire catalogue and it is designed accordingly.

### MIN-10 — Community, Land Access & Social Performance
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Social licence to operate determines project viability. Commitments to communities are made across years by many people and are poorly tracked; grievances escalate when they are not addressed.
**Trigger** — Community interaction, grievance raised, commitment due, or a reporting cycle.
**Workflow** — 1) Maintain the stakeholder register and the interaction record across the operation's history. 2) **Track every commitment made to communities and authorities** with owner, deadline and evidence of delivery — undelivered commitments are the primary cause of social conflict, and they are usually undelivered because nobody recorded them. 3) Manage grievances: log, categorise, assign, track to resolution within committed timeframes, and analyse patterns. 4) Support land access and resettlement processes with the documentation and compliance requirements of the applicable standards (IFC Performance Standards where relevant). 5) Track local content and employment commitments with the evidence. 6) Monitor community sentiment and emerging concerns from engagement records and public sources, respecting privacy and avoiding surveillance of individuals. 7) Support indigenous engagement and free, prior and informed consent processes with rigorous documentation. 8) Generate social performance reporting for the board, lenders and standards.
**Systems** — Stakeholder management systems, grievance registers, commitment registers, land management, HR/local content data.
**Outcome & KPIs** — Commitments delivered on time; grievance resolution time and recurrence; community incidents and disruptions; local content achievement; lender and standard compliance.
**Human gate** — **All community engagement is conducted by people.** Consent processes, resettlement and indigenous engagement are human and rights-based; the agent tracks and evidences only.

### MIN-11 — Energy, Emissions & Decarbonisation
**A6 · L2 · B3 · Plan-to-produce**
**Pain** — Mining is energy-intensive; diesel, power and process emissions are large, and customers and investors now demand credible, verified decarbonisation pathways.
**Trigger** — Continuous monitoring, planning cycle, or a reporting requirement.
**Workflow** — 1) Monitor energy consumption by process and asset, normalised for production and ore characteristics. 2) Identify waste and inefficiency: idling, compressed air, ventilation on demand, and pumping — the recurring large opportunities in mining. 3) Optimise energy cost against tariffs and, where applicable, on-site generation and storage dispatch. 4) Compute emissions across scopes with methodology and data quality declared, including fugitive and process emissions which are frequently the hardest to quantify credibly. 5) Model decarbonisation options: electrification of the fleet, renewable generation, ventilation on demand, and process changes — with capital cost, abatement, and the operational risk of each. 6) Sequence the pathway realistically against technology maturity and site constraints, rather than presenting an aspirational curve. 7) Track progress against targets with verified data. 8) Support customer and regulatory reporting including product carbon intensity, which is becoming a commercial differentiator in metals.
**Systems** — Energy monitoring, historian, fleet telemetry, ERP, carbon accounting, generation and grid data.
**Outcome & KPIs** — Energy intensity per tonne; emissions intensity; abatement delivered vs plan; energy cost; assurance readiness of reported data.
**Human gate** — Capital decisions and public targets are board-governed; disclosures are executively approved and externally assured.

### MIN-12 — Workforce, FIFO Rostering & Competence
**A5 · L2 · B4 · Hire-to-retire**
**Pain** — Remote operations run fly-in-fly-out rosters with travel, accommodation, fatigue management, competence and licensing constraints. Errors mean people at site without valid competence — a safety and legal failure.
**Trigger** — Roster cycle, absence, competence expiry, or a travel disruption.
**Workflow** — 1) Generate rosters satisfying hard constraints: fatigue management rules, statutory rest, competence and licence currency for the roles rostered, and medical fitness. 2) **Verify competence and medical currency before a person is rostered to a task**, not on arrival at site — the check that prevents the most common compliance failure. 3) Coordinate travel and accommodation with the roster, and manage the cascading disruption when a flight is cancelled or weather closes the site. 4) Manage fatigue risk actively: hours worked, shift patterns, travel time, and the accumulation across swings. 5) Fill gaps from the qualified pool with equitable distribution. 6) Track competence, training and licence renewals with lead time so renewals happen off-swing. 7) Support workforce planning: attrition risk, critical role coverage, and succession for site-critical competencies. 8) Report on compliance, fatigue exposure and roster fairness.
**Systems** — Rostering and workforce management, competence and training records, travel and accommodation, medical records (restricted), time and attendance.
**Outcome & KPIs** — Competence compliance (100% required); fatigue rule breaches (target zero); roster fill rate; travel disruption recovery; turnover; overtime.
**Human gate** — Fitness-for-work decisions are made by qualified medical and supervisory personnel; fatigue rules are absolute constraints; medical data access is strictly restricted.

---
## Design & regulatory notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Remote connectivity** | Satellite links are intermittent and expensive. Agents must operate at the edge with local buffering and reconcile when connected. Azure Arc / Stack HCI patterns are the default, not the exception. |
| **OT isolation** | Control systems are isolated. Agents read from historians and OT DMZ replicas; **no agent writes to a control system.** |
| **Resource reporting (JORC/NI 43-101/SAMREC)** | Public statements require Competent/Qualified Person sign-off with personal liability. Agents support analysis; they never conclude on resources or reserves. |
| **Tailings governance (GISTM)** | Formal accountability structures, engineer of record, independent review, and auditable evidence. The agent's role is detection and evidence, never judgement. |
| **Social performance (IFC PS, UNDRIP, FPIC)** | Community engagement is human and rights-based. Agents track commitments and grievances; they never conduct engagement or infer community sentiment as fact. |
| **Safety legislation** | Statutory duties fall on appointed competent persons. Agents verify and prompt; authorisation is always human. |
