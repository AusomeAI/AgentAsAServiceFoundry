# Document 10 — Transportation & Logistics

> 13 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Logistics runs on exceptions. The planned shipment is free; the delayed, damaged, mis-documented or mis-routed one consumes all the margin. **Every high-value agent here is an exception agent.**
- The document burden in cross-border freight is extraordinary and almost entirely unstructured: bills of lading, packing lists, certificates of origin, customs declarations. **LOG-04 Customs & Trade Documentation** is the single most defensible agent in this vertical.
- Freight forwarders and 3PLs have thin margins and huge headcount in operations. They buy agents on **cost per shipment**, and that number is easy to establish and easy to prove.
- Real-time visibility data exists but is rarely converted into decisions. **LOG-02 Shipment Exception Management** turns a dashboard into an operating system.

---

### LOG-01 — Freight Quoting & Rate Management
**A3 · L2 · B3 · Demand creation**
**Pain** — Quoting a multi-modal international shipment requires assembling carrier rates, surcharges, accessorials, customs costs and capacity availability — often manually, per quote, under time pressure.
**Trigger** — Rate request from a customer or a tender submission.
**Workflow** — 1) Parse the request: origin, destination, commodity, weight and dimensions, service level, incoterms, timing, and special requirements (hazardous, temperature, oversized). 2) Determine feasible routings and modes, including transhipment options. 3) Retrieve applicable rates: contracted rates, spot rates, and carrier tariffs, checking validity dates and conditions. 4) **Compute the all-in cost including the surcharges that make freight pricing opaque**: fuel, currency adjustment, congestion, peak season, security, terminal handling, documentation, and destination charges. Missing accessorials is the primary cause of margin loss on won freight. 5) Add customs duty and tax estimates where the incoterm makes them relevant. 6) Assess capacity and transit-time reliability on each option from historical performance, not carrier claims. 7) Present options with the genuine trade-off between cost, transit time and reliability. 8) Apply the pricing policy and generate the quote with clear validity and exclusions. 9) Track quote-to-booking conversion and margin realisation.
**Systems** — TMS, rate management, carrier portals/APIs, customs tariff data, historical performance data, CRM.
**Outcome & KPIs** — Quote turnaround; quotes per operator; win rate; **quoted vs actual margin**; accessorial capture rate.
**Human gate** — Pricing below margin floor, non-standard liability terms, and strategic account pricing.

### LOG-02 — Shipment Exception Management & Proactive Recovery
**A6 · L3 · B3 · Issue-to-resolution**
**Pain** — Delays, missed connections, port congestion, customs holds and equipment failures happen constantly. Most are discovered late, and the customer often notices before the forwarder does.
**Trigger** — Milestone missed, tracking anomaly, external disruption signal, or a customer enquiry.
**Workflow** — 1) Monitor every shipment against its planned milestone schedule, detecting deviation as soon as a milestone is at risk rather than after it is missed. 2) Diagnose the cause: carrier delay, port congestion, customs hold, documentation problem, equipment failure, weather, or a missed connection upstream. 3) Assess the impact: revised ETA, downstream connection risk, penalty and SLA exposure, and the consequence for the customer's own operation (a production-line stoppage is a different problem from a delayed retail replenishment). 4) Generate recovery options with cost and time: expedite, re-route, alternative carrier, partial shipment, or air conversion for the critical portion. 5) Execute within the authorised envelope; escalate options above it with the analysis done. 6) **Notify the customer proactively with the revised plan and the recovery action** — the difference between a service failure and a service recovery is who makes the call first. 7) Coordinate downstream: warehouse slots, delivery appointments, and onward transport. 8) Capture cause data and identify systemic problems by lane, carrier and port.
**Systems** — TMS, carrier tracking/EDI, port and terminal data, visibility platforms, customer portals, weather/disruption feeds.
**Outcome & KPIs** — Exceptions detected before the customer notices; recovery success rate; penalty and expedite cost; on-time delivery; customer escalations; systemic causes eliminated.
**Human gate** — Recovery spend above threshold; commercial commitments to customers; carrier claims.

### LOG-03 — Transport Planning & Load Optimisation
**A5 · L2 · B3 · Plan-to-produce**
**Pain** — Building efficient loads and routes across orders, vehicles, drivers and constraints is a hard optimisation done under time pressure, usually with heuristics and habit.
**Trigger** — Planning cycle, new order, or a plan-disrupting event.
**Workflow** — 1) Consolidate orders with their constraints: delivery windows, service level, weight and volume, stackability, temperature, hazard segregation, and customer-specific requirements. 2) Determine available capacity: vehicles, trailers, drivers with hours-of-service remaining, and subcontractor capacity. 3) Build loads maximising utilisation while respecting axle-weight limits, load-stability rules and segregation requirements — legality and safety are hard constraints, not objectives. 4) Route with real network conditions: restrictions, tolls, ferry schedules, congestion patterns, and site access windows. 5) Assign drivers respecting hours-of-service rules, licences, ADR certifications and fair allocation. 6) Identify orders that cannot be served economically and flag them for commercial decision rather than absorbing the loss silently. 7) Re-plan on disruption from the current state. 8) Compare planned versus actual to improve the parameters — planned transit times drift from reality constantly.
**Systems** — TMS, telematics, order management, driver management, map/traffic data, subcontractor portals.
**Outcome & KPIs** — Vehicle fill rate; empty running; cost per drop; on-time delivery; plan-to-actual variance; hours-of-service compliance.
**Human gate** — Planners approve final plans; any hours-of-service or weight-limit exception is prohibited, not approvable.

### LOG-04 — Customs Declaration & Trade Compliance
**A2 · L2 · B4 · Risk-to-assurance**
**Pain** — Customs entries require accurate classification, valuation, origin determination and documentation. Errors mean delays, penalties and — in the worst case — sanctions or export-control violations with criminal exposure.
**Trigger** — Shipment requiring a declaration, or a document set received.
**Workflow** — 1) Extract data from the commercial documents: invoice, packing list, bill of lading, certificates, and licences. 2) Validate consistency across documents — the mismatch between the invoice description and the packing list is the classic cause of a customs hold. 3) **Classify goods to the tariff code** using the description, composition, function and applicable classification rules, providing the reasoning and any relevant binding rulings. Classification is the highest-skill, highest-risk step. 4) Determine origin under the applicable rules and assess preferential-treatment eligibility, including whether the required proof of origin exists. 5) Determine customs value under the applicable valuation method, including assists, royalties and freight treatment. 6) **Screen for restrictions**: sanctions, denied parties, export controls, dual-use goods, licences and permits — screening is deterministic and blocking, never probabilistic. 7) Compute duty, tax and any trade remedies. 8) Generate the declaration and submit; manage authority queries and holds. 9) Maintain the audit record for post-clearance audit, which can occur years later.
**Systems** — Customs software, tariff databases, sanctions/denied-party screening, document intelligence, ERP/TMS, government portals.
**Outcome & KPIs** — Declaration accuracy; clearance time; holds and their causes; duty overpayment recovered; preferential-origin claims captured; **compliance violations (must be zero)**.
**Human gate** — **Licensed customs brokers review and submit declarations.** Any sanctions or export-control hit stops the shipment and escalates to trade compliance immediately — never overridable by the agent.

### LOG-05 — Warehouse Operations & Inventory Accuracy
**A6 · L3 · B3 · Plan-to-produce**
**Pain** — Warehouse productivity depends on slotting, labour balance and inventory accuracy; inaccuracy causes picking failures, and picking failures cascade into service failures.
**Trigger** — Continuous operations monitoring, order wave planning, or an inventory discrepancy.
**Workflow** — 1) Forecast workload by shift from the order profile and inbound schedule, and compare against planned labour to identify imbalances early. 2) Optimise wave and batch construction for picking efficiency, respecting cut-off times and carrier collection schedules. 3) Analyse slotting: place fast-movers in optimal locations, group items frequently ordered together, and respect weight and ergonomics. 4) Detect inventory discrepancies from picking exceptions, cycle counts and system-vs-scan divergence; **diagnose the cause rather than just adjusting the balance** — an adjustment without a cause guarantees recurrence. 5) Generate targeted cycle-count tasks where discrepancy probability is highest, rather than counting on a calendar. 6) Monitor productivity by process and identify constraints: equipment, congestion, training, or process design. 7) Manage dock scheduling and yard moves to prevent detention charges.
**Systems** — WMS, labour management, ERP, scanning/RFID, dock scheduling, automation controls (read-only).
**Outcome & KPIs** — Inventory accuracy; picks per hour; order cycle time; short-picks; detention costs; labour cost per unit shipped.
**Human gate** — Inventory adjustments above threshold require supervisor approval; safety and equipment matters are human-controlled.

### LOG-06 — Last-Mile Delivery & Customer Experience
**A5 · L3 · B3 · Issue-to-resolution**
**Pain** — Last mile is the most expensive leg and the most visible to the end customer. Failed deliveries are expensive and are usually preventable with better information.
**Trigger** — Delivery scheduled, in progress, or failed.
**Workflow** — 1) Confirm delivery details and preferences with the recipient before dispatch, including access instructions and safe-place authorisation — the cheapest possible intervention. 2) Provide accurate, narrowing time windows as the route progresses, based on actual position and remaining stops. 3) Handle recipient change requests within the operational envelope: reschedule, redirect to a neighbour or locker, or leave in a safe place. 4) On a failed attempt, diagnose the cause and choose the right next action rather than defaulting to a repeat attempt at the same time — repeating a failure is the industry's most expensive habit. 5) Handle enquiries with the actual delivery status and honest expectations. 6) Manage claims for damage and loss with evidence collection and policy application. 7) Analyse failure causes by driver, area and time to target improvement. 8) Optimise for repeat-delivery reduction, which is where last-mile cost actually lives.
**Systems** — Delivery management, driver mobile app, customer communication, locker/PUDO networks, claims system, telematics.
**Outcome & KPIs** — First-attempt success rate; cost per delivery; repeat attempts; customer contacts per delivery; claims rate; recipient satisfaction.
**Human gate** — Claims settlement above threshold; any safety or driver-conduct issue.

### LOG-07 — Fleet Maintenance & Compliance
**A6 · L3 · B4 · Plan-to-produce**
**Pain** — Fleet compliance (roadworthiness, inspections, driver licensing, tachograph) is legally mandated with serious consequences; maintenance scheduling competes with vehicle availability.
**Trigger** — Telematics fault, inspection due, defect reported, or a compliance deadline.
**Workflow** — 1) Track compliance obligations per vehicle and driver: inspections, certifications, licences, and tachograph analysis. 2) Monitor telematics and diagnostic data for developing faults and detect degradation before failure. 3) Process driver defect reports, triage severity, and **immediately prohibit use of any vehicle with a safety-critical defect** — a hard, non-negotiable rule. 4) Schedule maintenance balancing vehicle availability against transport demand, coordinating with LOG-03. 5) Manage the workshop: parts availability, technician capacity, and warranty recovery. 6) Analyse tachograph and telematics data for hours-of-service compliance and driving-behaviour risk, with the analysis framed as coaching rather than surveillance. 7) Maintain the compliance evidence record for regulatory inspection, which can occur without notice. 8) Analyse total cost of ownership by vehicle and specification to inform fleet renewal.
**Systems** — Fleet management, telematics, workshop/maintenance system, tachograph analysis, driver licensing checks, parts inventory.
**Outcome & KPIs** — Vehicle availability; roadside prohibition rate (target zero); compliance record completeness; maintenance cost per kilometre; breakdown frequency; warranty recovery.
**Human gate** — **All roadworthiness decisions are made by qualified technicians.** Driver conduct matters involve HR; the safety-defect prohibition is absolute and not overridable.

### LOG-08 — Carrier Procurement & Performance Management
**A8 · L2 · B2 · Procure-to-pay**
**Pain** — Carrier networks are large and performance is uneven; procurement events are periodic and analysis-heavy, and underperforming carriers persist because switching is hard.
**Trigger** — Procurement cycle, performance threshold breach, or a capacity need.
**Workflow** — 1) Analyse the freight profile by lane, mode, volume and seasonality to define the sourcing scope. 2) Build the carrier long-list from current carriers, market options and capability fit. 3) Run the tender: package the lanes, issue the RFQ, and normalise responses — carrier bids arrive in incomparable structures and normalisation is where errors hide. 4) Evaluate on total landed cost, service reliability, capacity commitment, and financial and compliance standing. 5) Model award scenarios including capacity concentration risk and the operational cost of switching. 6) Monitor carrier performance continuously: on-time, damage, documentation accuracy, invoice accuracy and responsiveness. 7) Generate performance reviews with evidence and specific improvement requirements. 8) Manage rate maintenance and detect off-contract usage.
**Systems** — TMS, procurement platform, carrier scorecards, freight audit data, market rate benchmarks.
**Outcome & KPIs** — Freight cost per unit; carrier on-time performance; contract compliance; tender cycle time; capacity availability during peaks.
**Human gate** — Award decisions and contract terms are commercial; carrier termination is a relationship decision.

### LOG-09 — Freight Audit, Payment & Claims
**A2 · L3 · B3 · Procure-to-pay**
**Pain** — Carrier invoices contain errors at material rates (duplicate charges, wrong accessorials, wrong rates, unearned surcharges). Manual audit catches a fraction; over-payment is normalised.
**Trigger** — Carrier invoice received.
**Workflow** — 1) Match the invoice to the shipment record and the contracted rate structure. 2) Validate every charge line: base rate, fuel surcharge calculation, accessorials against evidence that the service was actually performed, and detention/demurrage against actual timestamps. 3) Detect duplicates across invoices and across carriers on the same shipment. 4) **Verify accessorial charges against operational evidence** — detention claimed without corresponding gate timestamps is the most common and most disputed overcharge. 5) Approve clean invoices for payment; generate disputes with the specific evidence for the rest. 6) Track dispute resolution and recovery. 7) Allocate freight cost accurately to business units, customers and shipments for margin analysis. 8) Report overcharge patterns by carrier and charge type.
**Systems** — Freight audit platform, TMS, carrier invoices/EDI, contracts, ERP/AP, gate and telematics timestamps.
**Outcome & KPIs** — Overcharges detected and recovered; audit coverage; invoice processing cost; dispute win rate; cost allocation accuracy; payment cycle time.
**Human gate** — Payment release; disputes above threshold; carrier relationship escalation.

### LOG-10 — Cold Chain & Sensitive Cargo Monitoring
**A6 · L3 · B4 · Risk-to-assurance**
**Pain** — Temperature-controlled and high-value cargo requires continuous monitoring; excursions must be detected and acted on within minutes, not discovered at delivery.
**Trigger** — Sensor reading outside range, or a monitoring gap.
**Workflow** — 1) Monitor continuously against the cargo's specific requirements, which vary by commodity and by customer specification. 2) Distinguish genuine excursions from sensor faults and door-opening events — false alarms destroy trust and cause real alarms to be ignored. 3) On a genuine excursion, assess severity against the product's stability tolerance and compute the cumulative time-out-of-range. 4) Alert the responsible parties immediately with the location, duration and projected impact. 5) Recommend intervention: reefer adjustment, re-icing, transfer, expedite to destination, or diversion to the nearest facility. 6) Assemble the evidence package for the disposition decision by the cargo owner or their quality function. 7) For high-value cargo, monitor security signals: unplanned stops, route deviation, and door events in unexpected locations. 8) Analyse excursion patterns by lane, equipment and carrier to fix systemic causes.
**Systems** — IoT telematics and sensors, TMS, carrier systems, customer quality systems, alerting.
**Outcome & KPIs** — Excursions detected within target time; product loss value; false-alarm rate; intervention success; systemic causes eliminated; claims avoided.
**Human gate** — **Product disposition is always the cargo owner's decision** (and for pharma, their QA function). Security incidents escalate to human security response.

### LOG-11 — Yard, Port & Terminal Coordination
**A5 · L3 · B3 · Plan-to-produce**
**Pain** — Congestion at terminals and yards causes detention, demurrage and missed connections. Coordination across carriers, terminals and hauliers is phone-and-email work.
**Trigger** — Container availability, appointment window, or a congestion signal.
**Workflow** — 1) Track container and trailer status across terminals: discharge, customs status, free-time expiry, and availability for collection. 2) **Prioritise collections by free-time expiry and cost exposure** — demurrage accrues daily and is entirely avoidable with visibility. 3) Book terminal appointments within available slots, coordinating haulier capacity. 4) Optimise moves for dual-transactions (deliver and collect in one trip) to reduce empty running. 5) Monitor terminal congestion and adjust plans, including re-sequencing to avoid peak windows. 6) Manage yard capacity: dwell time, stacking, and equipment positioning. 7) Handle exceptions: customs holds, damaged containers, missing documentation, and appointment failures. 8) Report detention and demurrage by cause, with accountability attribution.
**Systems** — Terminal operating system interfaces, TMS, haulier systems, customs status feeds, yard management.
**Outcome & KPIs** — Demurrage and detention cost; container dwell time; appointment adherence; dual-transaction rate; free-time expiry breaches.
**Human gate** — Commercial escalation with terminals and carriers; disputes over charges.

### LOG-12 — Network Design & Capacity Strategy
**A3 · L1 · B3 · Plan-to-produce**
**Pain** — Network decisions (facility location, mode mix, inventory positioning) are long-horizon and capital-intensive, and are usually revisited only during a crisis.
**Trigger** — Network review, volume shift, cost pressure, or a service-failure pattern.
**Workflow** — 1) Model the current network: flows, costs, service levels, and capacity by node and lane. 2) Analyse demand geography and its trend, including channel shift and customer-mix change. 3) Model scenarios: facility additions, closures, relocations, mode shifts, and inventory-positioning changes. 4) Compute total cost to serve including transport, facility, inventory carrying, and the cost of service failure — the last is routinely omitted and it changes the answer. 5) Assess service impact by customer segment and geography. 6) Stress-test against disruption scenarios and demand variability, because a network optimised only for the mean is fragile. 7) Recommend the network strategy with the transition plan, cost and risk. 8) Monitor realised performance against the model and recalibrate.
**Systems** — Network optimisation tools, TMS/WMS historical data, demand data, cost models, geographic data.
**Outcome & KPIs** — Total cost to serve; service level by segment; network resilience under stress scenarios; realised vs modelled savings.
**Human gate** — All network and capital decisions are executive and board governed.

### LOG-13 — Sustainability & Emissions Reporting for Freight
**A8 · L2 · B3 · Risk-to-assurance**
**Pain** — Customers increasingly require verified emissions data per shipment; regulation is tightening; most operators cannot produce auditable numbers.
**Trigger** — Shipment completion, customer reporting request, or a compliance cycle.
**Workflow** — 1) Compute emissions per shipment using a recognised methodology (GLEC/ISO 14083), with primary data where available and modelled data where not — and label which is which, because data quality is the whole credibility question. 2) Allocate emissions across consignments sharing a vehicle or container using the standard allocation rules. 3) Aggregate by customer, lane, mode and period for reporting. 4) Identify reduction opportunities: modal shift, load consolidation, routing, fleet renewal, and fuel alternatives — quantified in both tonnes and cost. 5) Model the cost and service impact of reduction options so the trade-off is explicit. 6) Generate customer-facing reports and regulatory disclosures with the methodology and data quality declared. 7) Track performance against reduction targets and verify claims are substantiated before publication.
**Systems** — TMS, telematics/fuel data, carrier emissions data, emissions calculation engine, reporting platform.
**Outcome & KPIs** — Emissions per tonne-kilometre; primary-data coverage; reduction achieved; customer reporting requests met; assurance readiness.
**Human gate** — Public claims and disclosures require sign-off; **unsubstantiated environmental claims are blocked at the platform layer** given active greenwashing enforcement.

---
## Regulatory notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Customs & trade law** | Declarations are legally attested by a licensed broker or the importer of record. Sanctions and export-control screening is deterministic and blocking. Records must be retained for post-clearance audit periods (typically 3–7 years). |
| **Transport safety (hours of service, roadworthiness, ADR)** | These are hard constraints the agent enforces; it may never propose a plan that breaches them, and safety defects are non-overridable. |
| **Dangerous goods** | Classification, segregation and documentation errors are criminal offences in most jurisdictions; agent output requires qualified DGSA review. |
| **Carrier liability conventions (CMR, Montreal, Hague-Visby)** | Claims handling must apply the correct convention and its time bars; missing a time bar forfeits the claim. |
