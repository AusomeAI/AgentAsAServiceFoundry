# Document 20 — Automotive & Mobility

> 12 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- The automotive value chain is being restructured by electrification, software-defined vehicles and direct-to-consumer sales. Agents help most in the **transition costs**: warranty, quality, homologation, dealer operations and aftersales.
- **AUTO-04 Warranty & Field Quality** is the flagship. Warranty is a multi-billion-dollar cost line for OEMs, its data is rich and structured, and early detection of a field issue is worth an order of magnitude more than late detection.
- Homologation and regulatory compliance (**AUTO-08**) is a growing, defensible burden as software updates become regulated events under UNECE R155/R156 — a compliance-driven purchase with no in-house alternative.
- Vehicle-safety functions are entirely out of scope. Agents operate in enterprise and aftersales systems, and **never in the vehicle's safety-critical path**. This must be stated explicitly in every engagement.

---

### AUTO-01 — Dealer & Retail Customer Journey
**A1 · L3 · B3 · Demand creation**
**Pain** — Vehicle purchase involves configuration, finance, trade-in, availability and delivery timing across OEM and dealer systems. Response speed determines conversion, and most enquiries go unanswered for hours.
**Trigger** — Customer enquiry via website, marketplace, phone, or showroom.
**Workflow** — 1) Identify the customer and their context: prior vehicles, service history, finance agreement status and stage of the buying journey. 2) Understand the requirement: use case, budget, timing, and the constraints they actually care about (range, towing, seats, running cost). 3) Match against real available inventory including in-transit and buildable configurations, **with honest delivery dates** — inaccurate availability promises are the largest source of automotive customer dissatisfaction. 4) Handle the specifics: specification differences, options, and total cost of ownership including energy, tax and insurance, which matters more for EV buyers than list price. 5) Assess trade-in with an indicative valuation and the required inspection caveats. 6) Present finance options with accurate, compliant illustrations, respecting consumer-credit regulation absolutely. 7) Coordinate the next step: test drive, appointment, or order, with the calendar handled. 8) Manage the order-to-delivery journey with proactive updates, which is where most of the anxiety and most of the cancellations occur.
**Systems** — DMS, OEM order systems, inventory, CRM, finance systems, valuation providers.
**Outcome & KPIs** — Enquiry response time; conversion; delivery-date accuracy; order cancellation rate; customer satisfaction; finance attachment.
**Human gate** — **Finance advice and credit decisions are regulated activities** requiring authorised persons; pricing and trade-in commitments are commercial.

### AUTO-02 — Aftersales Service & Workshop Operations
**A5 · L3 · B3 · Issue-to-resolution**
**Pain** — Service booking, capacity planning, parts availability and technician allocation determine both workshop profitability and customer retention. Vehicles wait for parts; technicians wait for work.
**Trigger** — Service due, customer booking request, or a vehicle fault indication.
**Workflow** — 1) Identify the vehicle by VIN and retrieve its exact specification, service history, outstanding recalls and campaigns, and warranty status. 2) Determine the required work from the service schedule, reported symptoms, and any connected-vehicle diagnostics. 3) **Check recalls and safety campaigns on every interaction** — an open safety recall must always surface, regardless of why the customer contacted. 4) Estimate labour time and identify parts required, checking availability before booking rather than after. 5) Offer appointments matched to workshop capacity by skill and equipment (EV high-voltage work requires certified technicians and specific bays). 6) Provide an accurate quotation with the work explained in customer language. 7) During service, manage additional work identification with customer authorisation, and communicate delays proactively. 8) Coordinate parts, courtesy vehicles and collection. 9) Follow up on the work and on deferred items.
**Systems** — DMS, OEM technical systems, parts systems, workshop scheduling, connected vehicle data, recall databases.
**Outcome & KPIs** — Workshop utilisation; first-time-fix; parts availability at appointment; recall completion rate; customer retention; average repair order value.
**Human gate** — Technicians make all diagnostic and repair decisions; **safety-related work follows OEM procedure without deviation**.

### AUTO-03 — Technical Diagnostics & Repair Support
**A4 · L1 · B4 · Issue-to-resolution**
**Pain** — Modern vehicles are complex electronic systems; diagnosis of intermittent and multi-system faults is difficult, and technicians vary widely in capability. Misdiagnosis means replaced parts that were not faulty.
**Trigger** — Vehicle presented with a fault, or a diagnostic session initiated.
**Workflow** — 1) Retrieve the vehicle's exact configuration, software versions and history — **fault behaviour is version-specific and diagnosing against the wrong build wastes hours**. 2) Analyse fault codes with their freeze-frame data and the conditions under which they set, rather than treating the code as the diagnosis. 3) Retrieve technical service bulletins, known issues and prior repairs on this vehicle and this model. 4) Search the resolution history of similar symptom patterns across the network, weighted by whether the repair actually fixed it — the fleet-learning that individual workshops cannot access. 5) Guide structured diagnosis: the most informative test next, given what is known, rather than a fixed decision tree. 6) Interpret measurement results against specification. 7) Recommend the repair with the parts and procedure, and state the confidence honestly. 8) Capture the confirmed outcome so the network learns, including the cases where the first repair did not fix it.
**Systems** — Diagnostic tools, OEM technical information, parts catalogue, repair history database, telematics.
**Outcome & KPIs** — First-time-fix rate; diagnostic time; parts replaced unnecessarily (a direct warranty cost); repeat repairs; technician capability uplift.
**Human gate** — **Technicians own all diagnostic and repair decisions.** Safety-critical systems (braking, steering, restraints, ADAS calibration) follow OEM procedure with qualified personnel.

### AUTO-04 — Warranty Analysis & Field Quality Detection
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Warranty is one of the largest cost lines for an OEM. Emerging field issues are detected late from claims data, by which point tens of thousands of vehicles are affected.
**Trigger** — Warranty claims data, field reports, connected vehicle signals, or a quality review cycle.
**Workflow** — 1) Analyse warranty claims for emerging patterns by part, symptom, build period, plant, supplier, and usage profile. 2) **Detect signals early using leading indicators** — technician narrative text, diagnostic session data, and connected-vehicle telemetry all move before claims do, because claims lag repair by weeks. 3) Distinguish genuine emerging issues from noise, seasonality and reporting artefacts. 4) Correlate with manufacturing data, supplier lots and design changes to localise the cause. 5) Quantify exposure: population at risk, expected claim rate, and cost projection, which determines the urgency and the response. 6) **Assess safety implications and the regulatory reporting obligation**, which carries hard deadlines and personal liability. 7) Support the containment decision: production fix, service action, field campaign or recall, with the evidence pack. 8) Manage the campaign execution and completion tracking. 9) Detect and analyse warranty fraud and improper claims from dealers.
**Systems** — Warranty systems, DMS claims, manufacturing and supplier data, connected vehicle telemetry, quality systems, regulatory reporting.
**Outcome & KPIs** — Time from first field occurrence to detection; warranty cost per vehicle; **recall scope (early detection means smaller recalls)**; regulatory reporting timeliness; claim validation accuracy.
**Human gate** — **Safety decisions and recall determinations are made by the safety committee** under regulatory obligation; regulatory notifications are legally attributable acts.

### AUTO-05 — Manufacturing Quality & Production Support
**A6 · L3 · B4 · Plan-to-produce**
**Pain** — Automotive manufacturing runs at high line rates with zero tolerance for defect escape; a quality problem discovered downstream affects hundreds of vehicles before containment.
**Trigger** — Inspection result, process signal, or a defect detection.
**Workflow** — 1) Monitor process parameters and inspection results across the line in real time, detecting drift before it produces defects. 2) On a defect, **determine containment scope immediately**: which VINs, where they are (on line, in yard, in transit, at dealer, with customer), and whether the defect is safety-related. Speed here determines cost by orders of magnitude. 3) Trace to cause across process parameters, material lots, tooling condition, operator, and recent changes. 4) Correlate across stations to detect interactions that single-station analysis misses. 5) Support the containment and correction decision with the evidence. 6) Manage supplier quality issues with the exposure quantified and the corrective action tracked and verified. 7) Analyse build quality by station, shift, model and option content to target improvement. 8) Feed field quality data (AUTO-04) back into manufacturing, closing the loop that most OEMs leave open.
**Systems** — MES, quality systems, traceability, supplier quality, vehicle tracking, plant historian.
**Outcome & KPIs** — Defects per vehicle; containment time and scope; escapes to customer; supplier quality PPM; rework cost; field issues traced to manufacturing cause.
**Human gate** — Quality engineers make all disposition decisions; safety-related defects follow the formal escalation process; **the agent never writes to production control systems**.

### AUTO-06 — Supply Chain & Production Planning
**A6 · L2 · B3 · Procure-to-pay**
**Pain** — Automotive supply chains are deep, just-in-time and fragile. A single missing component stops a line at enormous cost; semiconductor and battery-material constraints have made this the industry's defining operational risk.
**Trigger** — Demand or supply change, disruption signal, or a planning cycle.
**Workflow** — 1) Maintain multi-tier visibility of critical components, at least to the tier where the actual constraint lives — which for semiconductors is often tier three or four. 2) Monitor supply risk: supplier performance and financial health, logistics disruption, geopolitical and trade developments, and single-source and single-site dependencies. 3) On a disruption signal, translate it into a production impact: which components, which models, which build weeks, and what revenue is at risk. 4) Generate mitigation options: alternate source, alternate specification, build-to-stock-without-part with rework, sequence change, or allocation across models. 5) **Support allocation decisions by margin and strategic priority** when supply is constrained — deciding which vehicles get the scarce part is a value decision, and it is often made by habit. 6) Optimise the production plan against constraints and customer order priority. 7) Manage the supplier relationship with performance data and joint problem solving. 8) Analyse structural resilience and inform dual-sourcing decisions.
**Systems** — ERP/production planning, supplier portals, logistics visibility, risk intelligence, product configuration data.
**Outcome & KPIs** — Line stoppage hours; disruptions detected before impact; allocation value optimisation; expedite and premium freight cost; single-source exposure.
**Human gate** — Sourcing and allocation decisions are commercial; engineering approval is required for any specification alternate.

### AUTO-07 — Connected Vehicle Data & Predictive Service
**A6 · L2 · B4 · Issue-to-resolution**
**Pain** — Vehicles generate enormous telemetry that is largely unused; breakdowns that were predictable happen anyway; and the data raises real privacy obligations that constrain how it can be used.
**Trigger** — Telemetry signal, degradation detection, or a scheduled analysis.
**Workflow** — 1) Ingest vehicle telemetry within the **consent and purpose limits the customer agreed to** — vehicle data is personal data in most jurisdictions and this constraint is architectural, not advisory. 2) Detect developing faults from signal patterns: battery degradation, thermal behaviour, actuator performance, and drivetrain signals. 3) Distinguish genuine degradation from usage-driven variation and environmental effects. 4) Predict failure with useful lead time and identify the specific component. 5) Generate a customer-appropriate proactive service offer: what is developing, why acting now is better, and what it will cost. Trust depends on this being genuine and not a sales pretext. 6) Prepare the workshop with the diagnosis and the parts before the vehicle arrives. 7) For fleets, aggregate into fleet health and maintenance planning. 8) Feed patterns into engineering quality (AUTO-04) and into future design.
**Systems** — Connected vehicle platform, telemetry pipelines, DMS, parts systems, CRM, consent management.
**Outcome & KPIs** — Breakdowns prevented; prediction lead time and precision; proactive service conversion; customer trust measures; consent compliance (100% required).
**Human gate** — Customer contact and service recommendations are human-delivered or clearly agent-identified; **data use beyond the consented purpose is architecturally blocked**.

### AUTO-08 — Homologation, Type Approval & Regulatory Compliance
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Vehicles must be homologated across markets against divergent and rapidly changing regulations; software updates are now regulated events, and non-compliance blocks sales entirely.
**Trigger** — Programme milestone, regulatory change, market entry, or a software release.
**Workflow** — 1) Maintain the requirements register across markets, mapped to vehicle variants, systems and evidence. 2) Monitor regulatory change across jurisdictions and **assess impact on the specific programmes, variants and approvals affected** — the mapping is the value, the monitoring is commodity. 3) Track evidence: test reports, technical documentation, and conformity assessments, with validity and scope verified. 4) Identify gaps against the approval requirements with the lead time to close them, so programme timing reflects reality. 5) Manage cybersecurity and software update regulation (UNECE R155/R156): the management system evidence, risk assessments, and the approval status of each software release. This has turned every OTA update into a compliance event. 6) Support conformity of production requirements with ongoing evidence. 7) Manage market-specific requirements: labelling, emissions, safety, and in-vehicle language and unit requirements. 8) Support regulatory submissions and authority queries.
**Systems** — Requirements management, PLM, test data management, regulatory intelligence, approval documentation, software release systems.
**Outcome & KPIs** — Approvals achieved on schedule; compliance gaps found before submission; software releases approved without delay; authority findings; market launch delays avoided.
**Human gate** — **Homologation submissions are made by authorised signatories** with legal accountability; technical services and approval authorities make the determinations.

### AUTO-09 — Fleet & Mobility Operations
**A5 · L3 · B3 · Plan-to-produce**
**Pain** — Fleet operators (leasing, rental, car-sharing, logistics) manage utilisation, maintenance, damage and remarketing across thousands of assets, with margin determined by residual value and downtime.
**Trigger** — Booking, vehicle event, maintenance due, or a lifecycle milestone.
**Workflow** — 1) Optimise fleet allocation against demand by location, vehicle type and time, including repositioning decisions where the cost is justified. 2) Manage maintenance scheduling to minimise off-fleet time, sequencing into low-demand windows. 3) Handle damage: detect from telematics and inspection, assess responsibility, quantify the cost, and manage recovery from the responsible party — damage recovery leakage is a large and quiet cost. 4) Manage the vehicle lifecycle: **optimal defleet timing balancing residual value decay, maintenance cost escalation and demand** — a decision that is worth a great deal and is usually made by policy rather than by analysis. 5) Support remarketing: channel selection, condition reporting, and pricing. 6) For EVs, manage charging infrastructure and state-of-charge across the fleet as an operational constraint. 7) Handle customer issues: breakdowns, accidents, and replacements, with duty of care. 8) Report utilisation, cost per vehicle and margin.
**Systems** — Fleet management, telematics, booking platforms, maintenance systems, remarketing channels, damage management.
**Outcome & KPIs** — Utilisation; off-fleet days; damage recovery rate; residual value achieved vs forecast; cost per vehicle per month; customer satisfaction.
**Human gate** — Damage liability disputes; commercial decisions on fleet purchase and disposal; accident response is human-led.

### AUTO-10 — EV Charging & Energy Management
**A6 · L3 · B3 · Issue-to-resolution**
**Pain** — Charging network reliability is the primary barrier to EV adoption. Faults are detected when a driver arrives at a broken charger, and the customer experience failure is total.
**Trigger** — Charger telemetry, session failure, or a network monitoring cycle.
**Workflow** — 1) Monitor charger health and session outcomes continuously, detecting failure and degradation — **a charger that reports "available" but fails to start sessions is the worst failure mode and requires session-outcome monitoring, not status monitoring**. 2) Diagnose failures: hardware, communication, payment, vehicle-side interoperability, or grid supply, since the fix and the owner differ for each. 3) Dispatch remote resets and configuration fixes where they resolve the fault, and field service where they do not. 4) Predict maintenance needs from usage, error patterns and component behaviour. 5) Manage energy: load balancing across a site, demand-charge management, tariff optimisation, and smart charging within grid constraints. 6) Support drivers: session support, payment issues, and honest availability information including a realistic view of whether a charger will actually work. 7) Analyse network performance by site and hardware type, and inform procurement — reliability differences between hardware vendors are large and usually undocumented. 8) Report utilisation and site economics.
**Systems** — Charge point management system, OCPP interfaces, payment systems, energy management, field service, driver apps.
**Outcome & KPIs** — Charger uptime and **session success rate (the metric that matters to drivers)**; time to detect and restore; repeat failures; energy cost per kWh delivered; driver satisfaction.
**Human gate** — Grid-affecting operations follow the connection agreement; field safety work is human.

### AUTO-11 — Battery Lifecycle, Health & Circularity
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Batteries are the highest-value component in an EV and the largest driver of residual value, warranty exposure and regulatory obligation. Health is poorly characterised and end-of-life obligations are growing.
**Trigger** — Telemetry, service event, warranty claim, or an end-of-life decision.
**Workflow** — 1) Assess battery state of health from usage data: charge and discharge patterns, thermal history, depth-of-discharge distribution, and fast-charging frequency. 2) Detect anomalous degradation and cell-level issues that indicate a defect rather than normal ageing — the distinction that determines warranty liability. 3) **Flag thermal and safety anomalies immediately**, since battery thermal events are catastrophic and the precursor signals are detectable. 4) Predict remaining life and residual capacity for warranty, residual value and customer information. 5) Support warranty determination with the evidence on usage versus defect. 6) Assess second-life suitability and value at end of vehicle life, which is becoming a material revenue stream. 7) Manage regulatory obligations: battery passport requirements, material declarations, recycling and take-back obligations. 8) Support material traceability and due diligence on the supply chain, which is a legal requirement in an expanding set of markets.
**Systems** — Vehicle telemetry, battery management system data, warranty systems, PLM, recycling partners, regulatory reporting.
**Outcome & KPIs** — State-of-health prediction accuracy; battery warranty cost; safety events prevented; second-life value recovered; battery passport compliance.
**Human gate** — **Safety determinations and any field action are made by the safety organisation**; warranty decisions are human; regulatory declarations are legally attributable.

### AUTO-12 — Software-Defined Vehicle Release Management
**A8 · L2 · B4 · Idea-to-market**
**Pain** — Vehicles now receive software updates over the air. A bad update reaches a fleet of hundreds of thousands and can be a safety event; the release process must be as rigorous as manufacturing.
**Trigger** — Software release candidate, deployment stage, or a field signal post-deployment.
**Workflow** — 1) Verify release readiness: test coverage and results, requirements traceability, safety analysis, cybersecurity assessment, and regulatory approval status under R155/R156. 2) Determine the compatibility matrix: which vehicle variants, hardware versions and existing software versions this release is valid for — **compatibility errors are the primary cause of OTA failures that brick functions**. 3) Plan a staged rollout: internal fleet, then a small canary population, then progressive expansion with defined hold criteria. 4) Monitor deployment: installation success, failure modes, and post-update vehicle behaviour compared against the pre-update baseline. 5) **Detect regression fast and hold the rollout automatically** on defined signals, because the cost of a delayed halt is measured in thousands of vehicles per hour. 6) Manage rollback where supported, and manage the vehicles that cannot be rolled back, which is the harder problem. 7) Handle customer communication: what changed, what is required of them, and what to do if something is wrong. 8) Maintain the release record for regulatory and liability purposes.
**Systems** — OTA platform, software configuration management, vehicle telemetry, test management, regulatory documentation, customer communication.
**Outcome & KPIs** — Update success rate; time to detect regression; vehicles affected by a bad release; rollout completion; regulatory compliance of releases; customer disruption.
**Human gate** — **Release approval is a formal, human, safety-governed decision.** Rollout expansion beyond canary requires human authorisation. Nothing touching a safety function is ever automated.

---
## Safety & regulatory notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Functional safety (ISO 26262) & SOTIF** | Agents are entirely outside the vehicle safety path. They operate in enterprise, manufacturing and aftersales systems only. This boundary must be explicit and contractual. |
| **UNECE R155/R156** | Cybersecurity and software-update management systems are type-approval requirements. Every OTA release is a regulated event with evidence obligations. |
| **Safety recall obligations** | Defect reporting carries hard statutory deadlines and personal liability. Recall determinations are human and formally governed. |
| **Vehicle data & privacy** | Connected-vehicle data is personal data. Purpose limitation and consent are architectural constraints; secondary use without a lawful basis is blocked. |
| **Consumer credit regulation** | Finance illustrations and advice are regulated activities requiring authorised persons. |
| **Battery regulation** | Battery passports, material due diligence and take-back obligations are expanding; traceability is becoming a compliance requirement rather than a differentiator. |
