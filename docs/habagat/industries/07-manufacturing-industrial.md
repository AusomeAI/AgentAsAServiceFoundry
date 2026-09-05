# Document 07 — Manufacturing & Industrial

> 14 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Manufacturing's agent value splits cleanly: **OT/plant-floor agents** (safety-critical, hard integration, high value) and **enterprise agents** (quoting, planning, quality documentation, aftermarket). Habagat should lead with the latter and earn the right to the former.
- The highest-ROI, lowest-risk entry point is **MFG-01 Engineer-to-Order Quoting**. Quote cycle time directly gates revenue, the inputs are documents and CAD metadata, and the baseline is measured in days.
- **MFG-05 Quality Non-Conformance & 8D** and **MFG-09 Aftermarket Service & Parts** are the two agents that customers renew for: one removes recurring cost, the other creates recurring revenue.
- Plant-floor agents must respect the **Purdue model**: agents live at Level 4/5 (enterprise/DMZ) and read from Level 3 historians. **No agent writes to a control system.** This is non-negotiable and should be stated in the first customer meeting.

---

### MFG-01 — Engineer-to-Order Quoting & Technical Sales
**A3 · L2 · B3 · Demand creation**
**Pain** — Custom and configured products require engineering input to quote. Quotes take 5–20 days, engineers are the bottleneck, and win rates suffer from slow response more than from price.
**Trigger** — RFQ received with drawings, specifications, or a customer configuration.
**Workflow** — 1) Extract requirements from the RFQ package: drawings, specifications, standards referenced, quantities, delivery requirements, and commercial terms. 2) Interpret technical drawings and specifications for the parameters that drive cost: materials, tolerances, finishes, testing, certification. 3) **Search the historical quote and order library for similar past work** — the single most valuable and least-used asset in every ETO business; a near-identical job quoted two years ago is the best cost estimate available. 4) Determine manufacturability and identify features that drive disproportionate cost, generating design-for-manufacture suggestions to offer the customer. 5) Build the cost estimate: material (with current pricing), routing and cycle times, tooling, outsourced operations, quality/certification cost, and freight. 6) Identify technical and commercial risks: unfamiliar standards, tight tolerances, exotic materials, long-lead components, and onerous liability terms. 7) Apply the pricing strategy: margin targets, strategic-account rules, and capacity considerations. 8) Generate the quotation document with the technical proposal, clarifications and exclusions — **exclusions are where ETO margin is won and lost**. 9) Engineer reviews, adjusts and approves.
**Systems** — CRM, ERP, PLM/CAD, historical quote database, cost/pricing models, supplier pricing.
**Outcome & KPIs** — Quote cycle time; quotes per engineer; win rate; **quoted vs actual cost variance (the metric that proves the estimate was real)**; margin on won business.
**Human gate** — Engineering approval of all technical content; commercial approval of price and terms.

### MFG-02 — Production Planning & Scheduling
**A5 · L2 · B3 · Plan-to-produce**
**Pain** — Schedules are built weekly and invalidated hourly by breakdowns, material shortages and rush orders. Planners spend their days rescheduling rather than optimising.
**Trigger** — Planning cycle, new order, or a disruption event (machine down, material late, quality hold).
**Workflow** — 1) Build the demand picture: firm orders, forecasts, safety-stock requirements and their due dates. 2) Assess capacity: machine availability, planned maintenance, tooling, labour skills and shift patterns. 3) Verify material availability against the BOM, including in-transit and supplier commitments; identify shortages before they stop the line. 4) Generate a feasible schedule optimising the customer's stated objective — usually on-time delivery, then changeover minimisation, then WIP. 5) **On disruption, re-optimise from the current state rather than patching**: which orders slip, which can be resequenced, which need expediting, and what the customer impact is. 6) Quantify the trade-offs explicitly so the planner is choosing, not guessing: "expediting order A costs $4k in changeovers and delays order B by two days; order B's customer has a penalty clause." 7) Generate the customer-communication list for genuine date changes. 8) Measure schedule adherence and attribute variance to cause.
**Systems** — ERP/MRP, APS, MES, maintenance system, inventory, supplier portal.
**Outcome & KPIs** — On-time-in-full; schedule adherence and stability; changeover time; WIP and lead time; expedite cost; planner time on rescheduling.
**Human gate** — Planners approve schedule releases; customer-date changes are commercially owned.

### MFG-03 — Predictive Maintenance & Asset Health
**A6 · L3 · B3 · Plan-to-produce**
**Pain** — Unplanned downtime is the most expensive event in a plant. Condition data exists but is not interpreted; maintenance is calendar-based, so healthy machines are stripped and failing ones run to failure.
**Trigger** — Continuous condition monitoring, or a maintenance-planning cycle.
**Workflow** — 1) Ingest condition data from sensors and the historian: vibration, temperature, current, pressure, acoustic, and process parameters. 2) Detect deviation from the asset's learned normal operating envelope, conditioned on what the machine is currently making — the context-conditioning is what removes most false alarms. 3) Classify the developing fault mode where the signature supports it (bearing, imbalance, misalignment, lubrication, cavitation). 4) Estimate remaining useful life with an explicit confidence interval, not a point estimate. 5) Correlate with maintenance history, prior failures on this and sister assets, and recent interventions — many "random" failures follow a maintenance action. 6) Generate the work order with the diagnosis, the recommended intervention, the parts required, and a check on their availability. 7) Recommend scheduling that minimises production impact, coordinating with MFG-02. 8) After the intervention, verify the fix resolved the signal, and feed the confirmed outcome back into the model.
**Systems** — Historian (PI/Aveva), IoT platform, CMMS/EAM (SAP PM/Maximo), MES, spare-parts inventory.
**Outcome & KPIs** — Unplanned downtime; MTBF/MTTR; % maintenance planned vs reactive; false-alarm rate; parts availability at intervention; maintenance cost per unit produced.
**Human gate** — Maintenance planners approve work orders; **the agent never writes to control systems**. Safety-critical assets follow the site's formal safety process regardless of agent output.

### MFG-04 — Shop-Floor Operator Assistance
**A4 · L1 · B4 · Plan-to-produce**
**Pain** — Operators need work instructions, troubleshooting help and quality guidance; documentation is in binders and PDFs, and expertise leaves with retirement.
**Trigger** — Operator asks a question or a machine raises a fault.
**Workflow** — 1) Establish context: which line, which machine, which product, which operation, which shift. 2) Retrieve the applicable work instruction, drawing revision and quality specification for **this exact product and revision** — using a superseded revision is a quality escape. 3) For a fault, retrieve the fault code meaning, the troubleshooting tree, and the history of how this fault was resolved on this and similar assets. 4) Guide the operator step by step, confirming each step before advancing, and adapting to what they report. 5) Escalate immediately when the situation is outside the operator's authorisation, involves a safety system, or is unresolved after the defined attempts. 6) Capture the resolution and add it to the knowledge base once validated by an engineer — this is how retiring expertise gets captured. 7) Support in the operator's language, which in most plants is not the documentation's language.
**Systems** — MES, PLM/document management, CMMS, historian (read-only), tablet/HMI front end.
**Outcome & KPIs** — Time to resolve line stoppages; first-time-right rate; operator dependence on supervisor escalation; knowledge-base growth; training time for new operators.
**Human gate** — **Safety-related actions always follow the site safety procedure with human authorisation.** No agent guidance can override a lock-out/tag-out or permit-to-work process; this is enforced as a hard content rule.

### MFG-05 — Quality Non-Conformance, RCA & 8D
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Non-conformances are logged and closed with shallow root causes; the same defects recur; customer 8D reports take weeks and are inconsistent.
**Trigger** — Non-conformance raised in inspection, production, or by a customer complaint.
**Workflow** — 1) Capture the non-conformance with structured detail: part, revision, quantity, defect mode, detection point, and the process context. 2) **Containment first**: identify all potentially affected material — WIP, finished goods, in transit, at the customer — and quantify the exposure. This is the time-critical step and the one done worst manually. 3) Assemble investigation context: process parameters at the time of production, material lots, equipment, tooling condition, operators, recent changes, and prior similar events. 4) Support structured root-cause analysis (5-why, fishbone, fault tree), challenging shallow answers — "operator error" is a symptom, not a root cause, and the agent should say so. 5) Correlate across events to find systemic causes invisible in a single investigation. 6) Draft the 8D report to the customer's required format with evidence. 7) Propose corrective actions with defined effectiveness criteria and verification method. 8) Track effectiveness and reopen if the defect recurs.
**Systems** — QMS, MES, ERP, historian, PLM, supplier quality system, customer portals.
**Outcome & KPIs** — Containment time; investigation cycle time; **recurrence rate (the only metric that proves root cause was found)**; cost of poor quality; customer complaint closure time; PPM defect rate.
**Human gate** — Quality engineers own root-cause conclusions and disposition decisions; customer-facing reports are approved before submission.

### MFG-06 — Supplier Quality & Incoming Inspection
**A8 · L3 · B3 · Procure-to-pay**
**Pain** — Supplier quality problems are found on the line rather than at receipt; supplier documentation (certificates, PPAP) is checked superficially or not at all.
**Trigger** — Goods receipt, supplier documentation submission, or a supplier quality event.
**Workflow** — 1) Determine the inspection requirement from the part's control plan and the supplier's current quality status — dynamic, risk-based inspection, tightened for suppliers with recent issues. 2) Validate supplier documentation: material certificates, test reports, CoCs, and PPAP submissions — checking that the certificate actually corresponds to the delivered lot and that values meet specification. This check is routinely skipped and routinely matters. 3) Compare inspection results against specification and trend them by supplier and part. 4) On non-conformance, quarantine, quantify exposure, and generate the supplier corrective action request with the evidence. 5) Track supplier CAR responses and validate the corrective action rather than accepting the form. 6) Maintain supplier quality scorecards: PPM, on-time documentation, CAR responsiveness, and audit findings. 7) Recommend inspection-level changes and supplier development actions based on evidence.
**Systems** — QMS, ERP receiving, supplier portal, inspection/gauge data, PLM specifications.
**Outcome & KPIs** — Supplier PPM; escapes to production from receipt; documentation compliance; CAR closure time and effectiveness; inspection cost.
**Human gate** — Supplier disqualification and material-acceptance concessions are quality-engineering decisions.

### MFG-07 — Engineering Change Management
**A5 · L2 · B4 · Idea-to-market**
**Pain** — Engineering changes ripple across BOMs, routings, tooling, documentation, suppliers, inventory and in-flight orders. Missed impacts cause obsolescence, quality escapes and shipment failures.
**Trigger** — Engineering change request raised.
**Workflow** — 1) Parse the proposed change and identify every affected item: parts, assemblies where used, documents, tools, fixtures, test programmes, and packaging. 2) **Impact analysis across the full where-used tree**, including service parts and legacy configurations still supported — the omission that generates the most expensive surprises. 3) Assess inventory and commitment exposure: stock on hand, WIP, in transit, supplier commitments, and customer orders in flight. 4) Determine the change classification and the required approvals, including customer or regulatory approval where the part is controlled. 5) Recommend an effectivity strategy: immediate, use-up, serial-number break, or retrofit, with the cost of each. 6) Generate the change-implementation plan with tasks, owners and sequencing. 7) Orchestrate execution: BOM updates, document releases, supplier notifications, tooling changes, and inspection updates. 8) Verify implementation and close, confirming that no legacy configuration was left inconsistent.
**Systems** — PLM, ERP, MES, supplier portal, document management, customer/regulatory submission systems.
**Outcome & KPIs** — Change cycle time; obsolescence cost from changes; implementation defects; changes requiring rework of the change; on-time effectivity.
**Human gate** — Change approval boards own all decisions; customer and regulatory approvals are human-managed.

### MFG-08 — Plant Performance & OEE Analysis
**A6 · L1 · B2 · Plan-to-produce**
**Pain** — OEE is reported but not explained; losses are attributed to generic buckets; improvement effort goes to whatever is most visible rather than most costly.
**Trigger** — Shift end, daily review, or a performance-deviation signal.
**Workflow** — 1) Compute OEE and its components by line, product and shift from MES and historian data. 2) Decompose losses into specific, actionable causes rather than categories: not "minor stops" but "infeed jam on filler at product changeover to 500ml, 34 occurrences this week, 71 minutes." 3) Quantify each loss in throughput and margin terms so priorities are financial, not emotional. 4) Correlate losses with conditions: product, speed setting, material lot, operator, ambient conditions, and time since maintenance. 5) Identify the best-demonstrated performance for each product and quantify the gap to it — the most credible improvement target available. 6) Generate the shift review pack with the top three losses, their evidence, and the recommended action. 7) Track improvement actions and verify their effect on the specific loss they targeted.
**Systems** — MES, historian, ERP, quality data, maintenance system, BI.
**Outcome & KPIs** — OEE and component trends; loss reduction attributable to actions; time to identify a new loss pattern; improvement-action closure and verified effect.
**Human gate** — Production leadership owns improvement priorities and resourcing.

### MFG-09 — Aftermarket Service & Spare Parts
**A5 · L3 · B3 · Order-to-cash**
**Pain** — Aftermarket carries the margin in most industrial businesses but is run reactively. Identifying the right part for an installed machine of unknown configuration is slow and error-prone.
**Trigger** — Customer service request, part enquiry, or a predictive signal from connected equipment.
**Workflow** — 1) Identify the customer's specific asset: serial number, build configuration, installed changes, and service history. 2) For a part request, resolve the correct part for **that specific configuration**, including supersessions and regional variants — the highest-frequency error in aftermarket, and it ships the wrong part across an ocean. 3) Check availability, lead time and alternatives, including refurbished and equivalent options. 4) For a fault report, diagnose from symptoms, machine data and service history; recommend the likely cause and the parts required. 5) Determine warranty and contract coverage before quoting — arguing about coverage after the fact destroys the relationship. 6) Generate the quotation or dispatch the service order with the parts kit, the technical documentation and the skill requirement. 7) Proactive opportunity: identify assets due for overhaul, out-of-warranty, running on superseded parts, or showing degradation signals, and generate targeted offers. 8) Capture the service outcome back into the asset record and the reliability knowledge base.
**Systems** — Service management/FSM, ERP, PLM configuration data, IoT/connected assets, warranty system, parts catalogue.
**Outcome & KPIs** — Part identification accuracy; first-time-fix rate; quote-to-order conversion; aftermarket revenue and attach rate; service response time; warranty cost.
**Human gate** — Warranty exceptions and goodwill decisions; safety-related field actions are engineering-governed.

### MFG-10 — Field Service Dispatch & Technician Support
**A5 · L3 · B3 · Issue-to-resolution**
**Pain** — Dispatching the right technician with the right parts and skills is a constrained optimisation done manually; first-time-fix rates sit in the 60–75% range and every failed visit costs a day.
**Trigger** — Service request created, or a machine-generated fault from a connected asset.
**Workflow** — 1) Triage the issue: severity, safety implication, contractual response commitment, and whether remote resolution is possible. 2) **Attempt remote resolution first** — a meaningful proportion of dispatches are avoidable, and this is the largest cost lever in field service. 3) If a visit is required, determine the skills, certifications, tools and parts needed from the diagnosis and asset configuration. 4) Optimise the assignment across technicians on skills, location, current schedule, parts on van, and contractual commitments. 5) Ensure parts availability before dispatch: from van stock, local depot, or overnight ship, and delay the visit rather than send a technician without the part. 6) Brief the technician: asset history, prior visits, likely cause, procedure, safety requirements and site access details. 7) Support the technician on site with documentation, diagnostics and expert escalation. 8) Capture the outcome: what was actually wrong, what was done, parts consumed, time, and follow-up needed. 9) Feed confirmed diagnoses back into the triage model.
**Systems** — FSM (ServiceMax/Dynamics FS/Salesforce FS), IoT platform, parts inventory, workforce scheduling, knowledge base, mobile app.
**Outcome & KPIs** — First-time-fix rate; remote-resolution rate; travel time per job; SLA attainment; jobs per technician per day; repeat visits.
**Human gate** — Dispatchers can override assignments; all safety-critical work follows formal authorisation processes.

### MFG-11 — Health, Safety & Environment Compliance
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Safety management depends on inspections, observations and incident reports that are filed but rarely analysed; leading indicators are ignored until a lagging indicator arrives.
**Trigger** — Incident or near-miss reported, inspection completed, or a scheduled compliance cycle.
**Workflow** — 1) Capture the incident or observation with structured detail, in the reporter's language, with minimal friction — reporting friction is the primary cause of underreporting. 2) Classify severity and regulatory reportability, and flag reportable events immediately with their deadlines. 3) Assemble context: location, task, equipment, permits in force, training records, prior events at the same location or task. 4) Support root-cause investigation focused on systemic and organisational causes, not just the immediate act. 5) **Analyse near-misses and observations for leading-indicator patterns** — this is where safety systems actually prevent harm, and it is the analysis nobody has time to do. 6) Track corrective actions with verification of effectiveness. 7) Manage the compliance calendar: permits, inspections, statutory testing, training currency, and environmental monitoring and reporting. 8) Generate regulatory reports and management HSE reporting.
**Systems** — EHS platform, HR/training records, permit-to-work, maintenance system, environmental monitoring, regulatory portals.
**Outcome & KPIs** — TRIR/LTIFR trend; near-miss reporting rate (should rise); leading indicators identified and acted on; corrective-action closure; regulatory reportability compliance (100%); permit compliance.
**Human gate** — **All incident investigations and safety conclusions are human-owned.** Serious incidents follow formal legal process; the agent supports evidence assembly only.

### MFG-12 — Supply Chain Risk & Disruption Response
**A6 · L2 · B3 · Procure-to-pay**
**Pain** — Multi-tier supply chains are opaque; disruption is discovered when a shipment fails to arrive, and response is improvised.
**Trigger** — Continuous risk monitoring, or a disruption event.
**Workflow** — 1) Maintain the supply-chain map: direct suppliers, and — where obtainable — sub-tier dependencies for critical components. 2) Monitor risk signals: supplier financial health, natural events, geopolitical developments, logistics disruption, labour action, and regulatory changes such as sanctions and export controls. 3) On a signal, determine exposure precisely: which parts, which products, which customer orders, and over what time horizon. This translation from event to impact is the whole value. 4) Quantify the impact: production stoppage timing, revenue at risk, and contractual penalties. 5) Generate mitigation options with cost and lead time: alternate supplier, alternate part, design substitution, expedite, inventory build, or allocation. 6) Support execution of the chosen option, including qualification requirements for an alternate source. 7) Maintain structural resilience analysis: single-source dependencies, geographic concentration, and single-points-of-failure across tiers.
**Systems** — ERP, supplier master, PLM, risk-data providers, logistics visibility, news/geopolitical feeds.
**Outcome & KPIs** — Disruptions detected before impact; time from event to impact assessment; production stoppage days avoided; single-source exposure reduction; expedite cost.
**Human gate** — Sourcing changes, qualification decisions and customer allocation are commercial and engineering decisions.

### MFG-13 — Energy & Sustainability Management
**A6 · L2 · B3 · Plan-to-produce**
**Pain** — Energy is a major and increasingly volatile cost; carbon reporting obligations (CSRD, CBAM, Scope 3) demand data most manufacturers do not have.
**Trigger** — Continuous monitoring, tariff event, or a reporting cycle.
**Workflow** — 1) Monitor energy consumption by asset, line and product, normalised for production volume and mix — unnormalised energy reporting is noise. 2) Detect anomalies and quantify waste: idle consumption, compressed-air leaks, out-of-hours load, and degraded equipment efficiency. 3) Optimise consumption against tariffs: load shifting, peak-demand management, and on-site generation/storage dispatch recommendations. 4) Compute product-level energy and carbon intensity for customer and regulatory reporting. 5) Assemble Scope 1, 2 and 3 emissions data, including supplier-provided product carbon footprints, with data-quality grading — because most Scope 3 data is estimated and the estimate quality must be disclosed. 6) Generate regulatory and voluntary disclosures with full traceability. 7) Model and rank decarbonisation and efficiency projects by cost per tonne and payback.
**Systems** — Energy monitoring, historian, MES/ERP, utility data, carbon accounting platform, supplier data.
**Outcome & KPIs** — Energy per unit produced; peak-demand cost; identified waste eliminated; carbon intensity; reporting completeness and assurance readiness.
**Human gate** — Energy-trading and contracting decisions; disclosure sign-off is executive (and increasingly externally assured).

### MFG-14 — New Product Introduction & Industrialisation
**A5 · L2 · B3 · Idea-to-market**
**Pain** — NPI is cross-functional and gate-driven, but gate reviews are dominated by status-chasing rather than risk assessment; late-discovered manufacturability problems are the most expensive class of defect.
**Trigger** — NPI project stage gate, or a design release.
**Workflow** — 1) Track deliverables, owners and dependencies across engineering, manufacturing, quality, supply chain and commercial. 2) Assess design releases for manufacturability, testability and supply risk early: tolerance stack-ups, special processes, single-source components, and long-lead items. 3) Verify readiness of the production system: process design, tooling, gauges, control plan, PFMEA, work instructions, training, and capacity. 4) **Assess gate readiness against the actual evidence** rather than the reported status — the value is in finding the deliverable that is marked green and isn't. 5) Identify risks with quantified schedule and cost impact and track mitigations. 6) Manage supplier readiness including PPAP/FAI submissions. 7) Generate the gate-review pack with evidence, open risks and a recommendation. 8) Post-launch, track early-life quality and cost against plan and feed the learning into the next NPI.
**Systems** — PLM, project management, ERP, QMS, supplier portal, MES.
**Outcome & KPIs** — Launch on time and on cost; gate-review preparation effort; issues found before vs after launch; early-life quality; time to stable production yield.
**Human gate** — Gate decisions are governance decisions made by the review board.

---
## Architecture & safety notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Purdue model / IEC 62443** | Agents operate at Level 4/5. They read from the Level 3 historian or an OT DMZ replica. **No agent writes to PLC/SCADA/DCS.** Any actuation is a recommendation into an authorised human workflow. |
| **Functional safety (IEC 61508/61511)** | Safety-instrumented systems are entirely out of scope for agents. Agent output must never be a link in a safety function. |
| **OT data gravity & latency** | Historian data volumes are large and often on-premises; expect an Azure Arc / edge component with local buffering rather than pure cloud ingestion. |
| **Product regulation (CE/UKCA/FDA)** | For regulated products, agents touching design or quality records fall under the quality-management system and require validation. |
| **Trade compliance** | Export control and sanctions screening must be deterministic rules, not model judgement. |
