# Document 08 — Energy & Utilities

> 14 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Utilities are being asked to run a fundamentally harder network (distributed generation, EVs, electrification, extreme weather) with the same headcount and under regulated cost control. That gap is the agent opportunity.
- The regulated-returns model changes the sales conversation: **capital deferral beats opex savings**. An agent that defers a substation upgrade by improving load visibility is worth more than one that trims a call centre — and it is a story the regulator will accept.
- Highest-value entry points: **EU-05 Outage Management & Restoration**, **EU-03 Grid Asset Health**, **EU-11 Connections & DER Interconnection** (the last is the industry's fastest-growing backlog and a political problem in most markets).
- Anything touching real-time grid control is out of scope. Agents advise the control room; **the control engineer operates the network**. NERC CIP and equivalents make this a compliance boundary, not a preference.

---

### EU-01 — Customer Billing Enquiry & Dispute Resolution
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Billing queries dominate utility contact volume, especially after estimated reads, tariff changes and price rises. Regulated complaint handling has strict timelines and penalties.
**Trigger** — Customer contacts about a bill via any channel.
**Workflow** — 1) Identify the customer, premise and account, handling the common cases of moved home, multiple premises and shared meters. 2) Retrieve the billing history, meter reads (actual vs estimated), tariff, consumption profile and any adjustments. 3) **Explain the bill by decomposition**: consumption change, tariff change, standing charges, weather effect, estimated-vs-actual correction, and levies — this is the answer customers want and rarely get. 4) Validate the bill: read plausibility against the profile, tariff application, meter multiplier, and correct billing period. 5) Detect genuine billing errors and initiate correction rather than defending the bill. 6) Investigate high-bill claims by comparing to weather-normalised history and similar premises, and identify likely causes including faulty appliances or a suspected meter fault. 7) Identify vulnerability and hardship indicators, and route to the priority-services and support processes immediately. 8) Offer payment arrangements within the regulated framework. 9) Log complaints correctly against regulatory definitions with the clock started.
**Systems** — CIS/billing (SAP IS-U, Oracle CC&B), meter data management, CRM, payment systems, vulnerability register.
**Outcome & KPIs** — First-contact resolution; billing complaints and regulatory escalations; time to correct billing errors; vulnerability identification rate; debt entering arrears.
**Human gate** — All complaints, vulnerability cases, disconnection-related matters, and any goodwill or write-off decision.

### EU-02 — Meter Data Validation & Estimation
**A6 · L3 · B3 · Record-to-report**
**Pain** — Smart meter estate generates enormous data with a persistent tail of missing, implausible and conflicting reads. Bad meter data means bad bills, bad settlement and regulatory penalties.
**Trigger** — Meter data ingestion cycle, or a validation exception.
**Workflow** — 1) Run validation, estimation and editing rules across the interval data: completeness, plausibility, register continuity, and consistency with the meter configuration. 2) Diagnose exceptions by cause: communications failure, meter fault, configuration error, tampering, or genuine consumption change — the diagnosis determines the fix, and generic estimation hides real problems. 3) Estimate missing data using the customer's own profile, weather and comparable premises, with the estimation method recorded for audit. 4) Detect meter faults and communication failures and raise field work orders with the diagnosis. 5) Detect potential tampering and theft signals and route to revenue protection without accusing the customer. 6) Reconcile against settlement obligations and flag data that will fail settlement before it does. 7) Track data quality by area, meter type and communications route to target field remediation.
**Systems** — MDM, head-end systems, CIS, asset register, settlement systems, work management.
**Outcome & KPIs** — Read success rate; estimated-bill percentage; settlement data quality; meter faults detected proactively; theft identified; time to resolve a communications failure.
**Human gate** — Theft allegations and revenue-protection actions are human-investigated with legal process.

### EU-03 — Grid Asset Health & Investment Prioritisation
**A6 · L2 · B3 · Plan-to-produce**
**Pain** — Networks hold millions of assets, many beyond nominal life. Replacement decisions are age-based rather than condition-based, so healthy assets are replaced while degraded ones fail.
**Trigger** — Continuous condition monitoring, inspection data, or an investment-planning cycle.
**Workflow** — 1) Consolidate asset condition evidence: inspection records, test results (DGA, partial discharge, thermography), SCADA operating data, fault history, and environmental exposure. 2) Compute health indices per asset using the regulator-accepted methodology where one exists — using the regulator's own framework is what makes the output fundable. 3) Estimate probability of failure and, crucially, **consequence of failure**: customers affected, critical loads, safety, environmental, and regulatory penalty exposure. 4) Rank interventions by risk reduction per pound spent. 5) Model portfolio scenarios: what a given budget buys in risk reduction, and where the risk lands if deferred. 6) Recommend intervention type — refurbish, replace, monitor, or run-to-failure — because run-to-failure is the right answer more often than utilities admit. 7) Generate the investment case with the evidence required for regulatory submission. 8) Track intervention outcomes against predicted risk reduction.
**Systems** — EAM/asset register, condition monitoring, SCADA/historian, GIS, outage history, investment planning tools.
**Outcome & KPIs** — Asset-related interruptions; risk reduction per unit of capex; unplanned replacement rate; regulatory acceptance of investment cases; deferred capital.
**Human gate** — Asset strategy and capital allocation are engineering and board decisions; regulatory submissions are formally attested.

### EU-04 — Vegetation & Third-Party Risk Management
**A6 · L2 · B4 · Risk-to-assurance**
**Pain** — Vegetation contact is a leading cause of outages and, in dry regions, of catastrophic wildfire liability. Cyclical trimming is expensive and poorly targeted.
**Trigger** — Imagery/LiDAR survey processed, weather forecast, or an inspection cycle.
**Workflow** — 1) Process aerial and satellite imagery, LiDAR and inspection data to measure vegetation clearance against conductors. 2) Model growth rates by species, location and season to project future encroachment — trimming is a scheduling problem, not a measurement problem. 3) Assess risk per span: clearance, species fall-in potential, conductor type, protection settings, ignition risk, and consequence (customers, critical loads, wildfire exposure). 4) Prioritise work by risk rather than by cycle date, and generate the work programme with access and permit requirements. 5) On extreme fire-weather forecasts, identify the highest-risk circuits for enhanced measures, feeding the utility's own public-safety power-shutoff decision process. 6) Track contractor completion with evidence, and verify the work actually achieved clearance. 7) Analyse outage causes against the vegetation programme to prove or disprove its effectiveness.
**Systems** — GIS, LiDAR/imagery platforms, outage management, weather services, work management, contractor systems.
**Outcome & KPIs** — Vegetation-caused outages; cost per span managed; risk reduction achieved; programme completion with verified clearance; wildfire risk exposure.
**Human gate** — **Public-safety power shutoff decisions are executive and regulator-governed.** The agent provides risk analysis; humans decide to de-energise.

### EU-05 — Outage Management & Restoration Support
**A5 · L2 · B4 · Issue-to-resolution**
**Pain** — During storms, control rooms are overwhelmed: thousands of calls, ambiguous fault locations, crew allocation under pressure, and customers demanding restoration estimates that nobody can produce.
**Trigger** — Outage detected by SCADA/AMI, or customer reports.
**Workflow** — 1) Correlate incoming signals — SCADA alarms, smart-meter last-gasp messages, customer calls — into distinct network events, resolving the many-reports-one-fault problem. 2) Predict the fault location from network topology, protection operation and the pattern of affected meters, narrowing the patrol distance. 3) Assess event severity: customers affected, critical and vulnerable customers, safety hazards (downed conductors), and estimated repair complexity. 4) Recommend crew allocation across concurrent events, optimising customer-minutes-lost restored per crew, while prioritising safety hazards and life-support customers absolutely. 5) Generate **honest restoration estimates** and update them as information improves — a wrong estimate does more reputational damage than a long one. 6) Manage customer communication at scale across channels, personalised to the premise. 7) Proactively contact vulnerable and life-support customers with welfare support. 8) Maintain the regulatory record for reliability reporting and post-event review. 9) Post-event, analyse response performance and network weaknesses exposed.
**Systems** — OMS/ADMS, SCADA, AMI, GIS, crew/work management, customer communication, vulnerability register.
**Outcome & KPIs** — SAIDI/SAIFI/CAIDI; time to accurate fault location; restoration-estimate accuracy; vulnerable-customer contact rate; call-centre containment during storms.
**Human gate** — **Control engineers own all switching and network operations.** The agent never issues a switching instruction. Safety hazards are dispatched under human control.

### EU-06 — Field Work Scheduling & Crew Optimisation
**A5 · L3 · B3 · Plan-to-produce**
**Pain** — Utilities run large field workforces against a mix of planned, cyclical and emergency work with skill, certification and access constraints. Scheduling is manual and productivity is low.
**Trigger** — Work order created, schedule-generation cycle, or a disruption.
**Workflow** — 1) Consolidate the work portfolio: planned maintenance, capital projects, inspections, connections, faults and emergency work. 2) Determine requirements per job: skills, certifications, crew size, vehicles, plant, materials, permits, outages required, and access arrangements. 3) Verify prerequisites are actually satisfied before scheduling — the single largest cause of wasted visits is dispatching work whose permit, material or planned outage is not in place. 4) Optimise schedules for travel, skills utilisation, appointment commitments and work-type balance. 5) Coordinate planned network outages with the control room and affected customers, respecting notice obligations. 6) Manage real-time disruption: emergency work displaces planned work, and the agent re-optimises and re-communicates rather than leaving customers waiting. 7) Track completion, capture as-built data, and identify follow-on work. 8) Report productivity and its constraints, honestly attributing lost time to cause.
**Systems** — Work and asset management, scheduling engine, GIS, mobile workforce app, materials, permit systems, customer communication.
**Outcome & KPIs** — Jobs per crew day; wasted visits; appointment adherence; travel time ratio; emergency response times; planned-work completion.
**Human gate** — Network outage approvals are control-room decisions; safety-critical work follows formal authorisation.

### EU-07 — Load Forecasting & Network Planning
**A6 · L1 · B3 · Plan-to-produce**
**Pain** — Electrification (EVs, heat pumps, solar, batteries) is changing load shapes faster than planning cycles can track. Traditional forecasting under-predicts local constraints and over-predicts system-wide need, producing both stranded assets and unexpected constraints.
**Trigger** — Planning cycle, connection application, or a constraint signal.
**Workflow** — 1) Build granular demand forecasts at feeder and substation level from AMI data, incorporating weather, calendar and behavioural patterns. 2) Model the adoption of EVs, heat pumps, rooftop solar and storage by area using local demographic, housing and economic data — adoption is intensely local and system-average assumptions are useless. 3) Project resulting load shapes including coincidence factors, which is where naive forecasts fail most expensively. 4) Identify emerging constraints: thermal, voltage and fault-level, with the timing of each. 5) Evaluate solutions and compare **non-network alternatives** (flexibility services, demand response, storage, dynamic ratings) against reinforcement on whole-life cost — regulators increasingly require this comparison. 6) Generate the planning case with scenarios and sensitivities. 7) Monitor actual against forecast and recalibrate, reporting where local adoption is running ahead of plan.
**Systems** — AMI/MDM, GIS/network model, planning tools (power flow), weather and demographic data, DER registers.
**Outcome & KPIs** — Forecast accuracy at feeder level; constraints identified before they bind; capital deferred through non-network solutions; connection refusals avoided; stranded-asset risk.
**Human gate** — Network planners own all investment recommendations; power-system studies require engineering sign-off.

### EU-08 — Energy Trading & Portfolio Analytics Support
**A6 · L1 · B4 · Order-to-cash**
**Pain** — Traders and portfolio managers must synthesise fundamentals, weather, plant availability, market signals and position data under time pressure; analysis is manual and fragmented.
**Trigger** — Market open, position change, or a market/weather event.
**Workflow** — 1) Assemble the market picture: prices, curves, spreads, volumes, and cross-commodity relationships. 2) Integrate fundamentals: weather forecasts and their uncertainty, generation availability and outages, interconnector flows, storage levels, and demand forecasts. 3) Analyse the portfolio position: exposures by commodity, tenor and location; hedge ratios; and limit utilisation. 4) Identify and explain material market moves, distinguishing fundamental drivers from noise — the analyst question that consumes the morning. 5) Run scenario and stress analyses on the portfolio. 6) Monitor limits and generate breach alerts with the contributing positions identified. 7) Support regulatory reporting (REMIT/EMIR/Dodd-Frank) and surveillance for market-abuse indicators. 8) Draft the morning market commentary.
**Systems** — ETRM, market data, weather services, plant availability feeds, risk engine, regulatory reporting.
**Outcome & KPIs** — Analysis turnaround; limit-breach detection latency; reporting completeness and timeliness; forecast contribution to P&L; surveillance findings.
**Human gate** — **All trading decisions and executions are human.** Market-abuse surveillance findings go to compliance. Position limits are hard system controls, not agent judgement.

### EU-09 — Regulatory Reporting & Price Control Submissions
**A8 · L2 · B4 · Record-to-report**
**Pain** — Regulated utilities face heavy periodic reporting and, every few years, an enormous price-control submission requiring evidence for every pound of proposed spend.
**Trigger** — Reporting deadline, regulator query, or a price-control cycle.
**Workflow** — 1) Orchestrate the reporting calendar with data-readiness verification per submission. 2) Assemble data from source systems with full lineage from the reported number back to the transaction. 3) Apply the regulator's definitions precisely — regulatory definitions differ subtly from management definitions, and that gap is where restatements come from. 4) Validate against the regulator's rules and against prior submissions for continuity. 5) **Explain every material movement** with evidence, because this is the regulator's first question. 6) For price-control submissions, assemble the evidence base: asset health, risk, options analysis, benchmarking, deliverability and customer engagement. 7) Draft narrative sections grounded in the evidence. 8) Manage regulator queries by mapping each to the prepared evidence. 9) Track commitments made in submissions through to delivery evidence.
**Systems** — Regulatory reporting systems, asset and financial systems, data warehouse, document management, lineage/metadata.
**Outcome & KPIs** — On-time submissions; restatements (target zero); query response time; regulatory determinations vs proposals; commitment delivery evidence.
**Human gate** — All regulatory submissions are executive-attested; regulatory strategy is board-governed.

### EU-10 — Demand Response & Flexibility Orchestration
**A5 · L2 · B4 · Plan-to-produce**
**Pain** — Flexibility from distributed resources is contracted but poorly utilised: dispatch decisions are slow, settlement is disputed, and participant experience is poor enough to drive attrition.
**Trigger** — Constraint forecast, market signal, or a system event.
**Workflow** — 1) Forecast the need: which constraint, what magnitude, which hours, and with what confidence. 2) Determine the available flexibility portfolio: contracted capacity by location, resource type, availability, response time and cost. 3) Optimise the dispatch stack against the network requirement and cost, respecting each resource's contractual limits and comfort constraints. 4) **Verify the network effect** — flexibility that does not relieve the actual constrained element is worthless, and location matters more than volume. 5) Issue dispatch signals through the approved control path with acknowledgement tracking. 6) Measure delivered response against baseline using the contracted methodology, and settle — baseline disputes are the single biggest source of participant dissatisfaction, so the methodology and its evidence must be transparent. 7) Report participant performance and portfolio reliability. 8) Identify recruitment gaps by location for the flexibility procurement team.
**Systems** — DERMS/ADMS, flexibility platform, AMI, market systems, settlement, participant portal.
**Outcome & KPIs** — Constraint relief delivered; dispatch reliability; settlement disputes; participant retention; cost vs network reinforcement alternative.
**Human gate** — Network operations authorise all dispatch affecting the network; commercial terms are human-contracted.

### EU-11 — Connections & DER Interconnection Processing
**A2 · L2 · B3 · Order-to-cash**
**Pain** — Connection queues (especially for renewables, storage and EV infrastructure) have become multi-year backlogs. Application processing is manual, studies are repetitive, and the queue itself is clogged with speculative applications.
**Trigger** — Connection application submitted.
**Workflow** — 1) Validate application completeness and technical data; return incomplete applications immediately with specifics rather than queuing them. 2) Classify the connection type and determine the applicable process, standards and study requirements. 3) Perform initial network capacity screening at the point of connection using the network model — resolving many applications without a full study. 4) Where studies are required, prepare the study inputs and run standard analyses (thermal, voltage, fault level, protection coordination), flagging cases needing specialist engineering. 5) Determine required reinforcement and generate the cost apportionment per the regulated methodology. 6) Draft the connection offer with terms, conditions and timescales. 7) **Manage the queue actively**: identify stalled and speculative applications against milestone requirements so capacity can be released to projects that will actually build. 8) Track projects through to energisation with milestone management and compliance verification.
**Systems** — Connections management, network model/power-flow tools, GIS, asset register, customer portal, cost models.
**Outcome & KPIs** — Application processing time; offers issued on time; queue length and age; capacity released from stalled projects; connection cost accuracy; energisation on schedule.
**Human gate** — Connection offers and reinforcement designs require chartered-engineer approval; queue-management decisions follow the regulated process.

### EU-12 — Debt, Vulnerability & Customer Support
**A7 · L2 · B4 · Order-to-cash**
**Pain** — Energy debt is a social and regulatory issue as much as a commercial one. Blunt collections harm vulnerable customers and attract regulatory penalty; passive collections destroy cash.
**Trigger** — Arrears threshold, missed payment plan, or a hardship signal.
**Workflow** — 1) Build the customer picture: debt level and trajectory, payment history, consumption relative to premise type, tariff appropriateness, and prior support. 2) **Screen for vulnerability first, before any collections activity** — health conditions, life support, age, disability, recent bereavement, and financial hardship indicators. This ordering is the entire design. 3) Where vulnerability is indicated, route to the support pathway: priority services registration, grants, tariff review, energy-efficiency support, and third-party referral. 4) For customers able to pay, determine an affordable arrangement based on real affordability data rather than a formula. 5) Communicate in accessible language on the customer's preferred channel, with clear options and no pressure tactics. 6) Detect self-disconnection patterns in prepayment customers — an urgent welfare signal that is visible in the data and routinely missed. 7) Escalate to human support at any distress signal. 8) Report on outcomes and regulatory compliance.
**Systems** — CIS/billing, payment systems, vulnerability register, third-party referral networks, AMI consumption data.
**Outcome & KPIs** — Debt recovered; customers moved to sustainable arrangements; vulnerability identification rate; self-disconnection detected and resolved; complaints; regulatory compliance.
**Human gate** — **All disconnection, warrant and enforcement actions are human with senior authorisation.** Any vulnerability or distress signal stops automation immediately.

### EU-13 — Environmental Compliance & Emissions Reporting
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Environmental permits, emissions monitoring, water discharge, waste and spill reporting carry criminal liability and hard deadlines, managed largely by spreadsheet.
**Trigger** — Monitoring data, permit condition due date, incident, or a reporting cycle.
**Workflow** — 1) Maintain the permit and obligation register per site with conditions, limits and reporting requirements. 2) Monitor emissions and discharge data against permit limits continuously, flagging trend toward breach before breach — after the fact is a notification, before is a prevention. 3) On exceedance, determine reportability, deadline and required notification content, and generate it immediately. 4) Manage monitoring equipment calibration and data-availability requirements, which are themselves permit conditions. 5) Assemble periodic regulatory returns with full data lineage. 6) Compute emissions inventories and carbon reporting including scheme-specific methodologies. 7) Manage incidents: spills, releases and near-misses with investigation, notification and remediation tracking. 8) Track permit renewals and variation applications against lead times.
**Systems** — Continuous emissions monitoring, environmental data systems, permit register, EHS platform, regulatory portals.
**Outcome & KPIs** — Permit compliance rate; notification timeliness (100% required); exceedances predicted and prevented; data availability against permit requirements; regulatory findings and penalties.
**Human gate** — All regulatory notifications and environmental conclusions are made by the accountable environmental manager; incidents follow legal process.

### EU-14 — Water Network Leakage & Non-Revenue Water
**A6 · L2 · B3 · Plan-to-produce**
**Pain** — Water utilities lose 20–30% of treated water to leakage. Detection relies on district metering and manual analysis; finding the leak is slow and disruptive.
**Trigger** — Continuous flow monitoring, acoustic sensor data, or a customer report.
**Workflow** — 1) Analyse district metered area flows, especially minimum night flow, against expected legitimate consumption. 2) Detect anomalies indicating new leakage, distinguishing them from consumption changes, meter errors and network configuration changes — the discrimination problem that generates most wasted field visits. 3) Correlate acoustic sensor, pressure and satellite data to localise the leak. 4) Prioritise investigation by estimated loss volume, ground conditions, damage risk and access constraints. 5) Generate field work orders with the localisation evidence and recommended detection method. 6) Optimise pressure management to reduce both leakage and burst frequency, modelling the customer service impact. 7) Track repair outcomes against predicted loss to validate detection accuracy. 8) Report non-revenue water components: real losses, apparent losses (metering and theft), and unbilled authorised consumption.
**Systems** — SCADA/telemetry, DMA flow monitoring, acoustic loggers, GIS/network model, work management, customer billing.
**Outcome & KPIs** — Leakage volume and non-revenue water percentage; time from leak occurrence to repair; detection accuracy (found on first dig); repair cost per megalitre saved; burst frequency.
**Human gate** — Network intervention and pressure-management changes require operational approval; supply interruptions follow the customer-notification process.

---
## Regulatory & safety notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **NERC CIP / NIS2 / equivalent** | Agents are enterprise-zone systems. No agent has access to or influence over control systems. Access to OT data is via a one-way replica or historian in a DMZ. |
| **Regulated cost recovery** | Agent-enabled benefits must be expressible in the regulator's framework (risk reduction, capital deferral, service metrics) to be fundable. Habagat should build the evidence pack, not just the agent. |
| **Consumer protection & vulnerability** | Vulnerability screening precedes every collections or disconnection-adjacent action. This is a design ordering, enforced in the workflow. |
| **Market abuse (REMIT/FERC)** | Trading agents must not generate or act on inside information; surveillance obligations apply to the agent's own activity records. |
| **Public safety** | De-energisation, switching and shutoff decisions are always human. Agent output is advisory input to a formal operational process. |
