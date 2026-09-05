# Document 17 — Agriculture & Food Production

> 12 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Agriculture and food is a **thin-margin, high-variability, compliance-heavy** industry. Agents earn their keep by reducing waste and by making traceability a capability rather than a fire drill.
- The commercially strongest buyers are not farms but the **midstream**: processors, co-operatives, food manufacturers and distributors. They have the scale, the compliance burden and the budget.
- **AG-06 Food Safety, Traceability & Recall** is the agent that sells itself: a recall executed in hours instead of days is the difference between a contained incident and a brand-ending one, and every food executive has that fear.
- Connectivity and data maturity on-farm are genuinely poor. Design for **intermittent connectivity, low data quality and mobile-first, low-literacy interfaces** — an agent that assumes clean data and good broadband will fail in this vertical.

---

### AG-01 — Crop Planning & Agronomic Decision Support
**A4 · L1 · B3 · Plan-to-produce**
**Pain** — Planting, input and rotation decisions are made with incomplete information under weather and price uncertainty; agronomic advice is scarce and inconsistent.
**Trigger** — Planning season, growth-stage milestone, or a field observation.
**Workflow** — 1) Assemble the field picture: soil test results, historical yields, rotation history, drainage, and field-level variability. 2) Integrate current conditions: weather to date, forecast, soil moisture, and growth-stage observations from imagery and scouting. 3) Recommend variety, planting rate and timing against the field's characteristics and the season's outlook, with the reasoning and the uncertainty stated. 4) Plan nutrition: nutrient requirements against soil supply and yield target, with variable-rate recommendations where the field's variability justifies it. 5) **Ensure every recommendation is compliant** — product approvals for the crop, application limits, buffer zones, nitrate-vulnerable-zone rules, and assurance-scheme requirements. Non-compliant advice risks the grower's certification and their payments. 6) Model the economics: input cost against expected yield response at current prices, so the recommendation is financial rather than merely agronomic. 7) Support in-season decisions: disease risk from weather models, pest thresholds, and irrigation scheduling. 8) Record decisions and outcomes to build a field-level evidence base over seasons.
**Systems** — Farm management software, soil and yield data, satellite/drone imagery, weather services, product approval databases, commodity prices.
**Outcome & KPIs** — Yield per hectare; input cost per tonne; nutrient-use efficiency; compliance breaches (target zero); margin per hectare.
**Human gate** — **Qualified agronomists own all agronomic advice**; regulated product recommendations require a certified adviser in most jurisdictions.

### AG-02 — Livestock Health & Welfare Monitoring
**A6 · L2 · B4 · Plan-to-produce**
**Pain** — Health problems are detected when animals are visibly sick, by which point treatment is expensive, welfare is compromised, and disease may have spread.
**Trigger** — Continuous sensor and behaviour monitoring, or a stockperson observation.
**Workflow** — 1) Monitor individual and group signals: activity, rumination, feed and water intake, weight, body condition, milk yield and composition, and environmental conditions. 2) Detect deviation from the individual animal's own baseline, which is far more sensitive than a herd threshold. 3) Correlate signals to distinguish likely causes: metabolic, infectious, lameness, reproductive, or environmental. 4) **Alert with specificity and priority**: which animal, what the signals indicate, how urgent, and what to check — a generic alert list is ignored within a week. 5) Support treatment decisions within the herd health plan, **with veterinary prescription requirements strictly enforced** — antimicrobial stewardship is a regulatory and public-health obligation. 6) Track treatment, withdrawal periods and outcomes; withdrawal-period breaches are a food-safety failure with serious consequences. 7) Monitor group-level welfare indicators and environmental conditions against standards. 8) Analyse patterns to identify management and housing causes rather than treating recurring symptoms.
**Systems** — Livestock sensors and collars, herd management software, milking systems, environmental controls, veterinary records.
**Outcome & KPIs** — Early detection lead time; treatment cost and success; mortality and culling; antimicrobial usage (should fall); welfare outcome measures; productivity.
**Human gate** — **All treatment decisions are made by the stockperson under veterinary direction.** Prescription-only medicines require a veterinary decision; the agent may never recommend a specific antimicrobial.

### AG-03 — Precision Application & Machinery Operations
**A5 · L2 · B4 · Plan-to-produce**
**Pain** — Application of seed, fertiliser and crop protection must be accurate, compliant and well-timed; equipment downtime in a narrow weather window is extremely costly.
**Trigger** — Operation planned, weather window, or a machine signal.
**Workflow** — 1) Generate the application plan: product, rate, timing, and variable-rate map where justified. 2) Check the weather window against the product's application constraints — wind speed for spray drift, temperature, rainfall risk, and soil conditions. These are legal constraints, not preferences. 3) Verify compliance: operator certification, product approval and dose, buffer zones, water-course protection, and record requirements. 4) Plan the field operation sequence for efficiency and to respect soil condition and traffic constraints. 5) Monitor machinery telemetry for developing faults and schedule maintenance into weather windows when field work is impossible. 6) **Manage spare parts and service in season, where a day of downtime can cost a crop** — availability planning ahead of the season is worth more than fast response during it. 7) Capture as-applied records automatically for compliance and assurance schemes. 8) Analyse application accuracy and its agronomic and financial effect.
**Systems** — Machinery telematics, farm management software, GNSS guidance, product databases, weather services, parts systems.
**Outcome & KPIs** — Operations completed in optimal window; application accuracy; machinery downtime in season; compliance record completeness; input savings from variable rate.
**Human gate** — Operators make all in-field decisions; **spray operations require certified operators and remain their legal responsibility.**

### AG-04 — Harvest, Grading & Post-Harvest Management
**A6 · L3 · B3 · Plan-to-produce**
**Pain** — Harvest timing, logistics and quality assessment determine value; post-harvest losses are large and often invisible until the product is rejected downstream.
**Trigger** — Crop maturity signal, harvest planning, or a delivery.
**Workflow** — 1) Assess crop maturity and quality from sampling, imagery and growing-season data to recommend harvest timing by field and block. 2) Plan harvest logistics: machinery, labour, transport and storage capacity, sequenced against the weather window. 3) Assess quality at intake: moisture, protein, contamination, size and grade, using instrument data and vision inspection. 4) **Determine grade and value against the buyer's specification**, and — where the crop is borderline — identify the interventions (drying, cleaning, blending within legal limits) that would lift it into a higher band. 5) Manage storage: allocate by grade and destination, monitor condition (temperature, moisture, pest activity), and alert on deterioration risk. 6) Optimise the marketing decision: sell now, store and sell later, with the cost of storage, shrinkage risk and price outlook made explicit. 7) Trace lots from field to delivery for assurance and traceability. 8) Analyse losses across the chain and attribute them to cause.
**Systems** — Harvest and grain management systems, intake grading equipment, storage monitoring, commodity markets, traceability systems.
**Outcome & KPIs** — Yield captured vs estimated; grade achieved and premium captured; post-harvest loss; storage condition breaches; traceability completeness.
**Human gate** — Marketing and selling decisions are commercial; grade disputes are human-resolved.

### AG-05 — Supply Chain Planning & Fresh Produce Flow
**A6 · L2 · B3 · Plan-to-produce**
**Pain** — Fresh supply chains match a biologically variable supply to a promotionally variable demand with a shelf life measured in days. Mismatch means waste at one end and unfilled orders at the other.
**Trigger** — Demand forecast update, supply signal, or a quality event.
**Workflow** — 1) Forecast supply from crop progress, growing conditions, and historical patterns, with a range rather than a point — biological supply is inherently uncertain and pretending otherwise causes the waste. 2) Forecast demand including promotional uplift, weather effects on consumption, and seasonal patterns. 3) Match supply to demand across the network, allocating by shelf life, quality and customer specification. 4) **Detect mismatch early enough to act**: excess supply can be redirected to processing, secondary markets or donation if identified with days rather than hours to spare. 5) Manage cold chain and shelf-life through the network, tracking remaining shelf life as a dynamic property rather than a printed date. 6) Optimise the flow to maximise the value recovered from the whole crop, including grades that do not meet primary specification. 7) Coordinate with growers on planting and harvest timing to smooth supply. 8) Analyse waste by cause and stage.
**Systems** — Supply planning, grower management, cold-chain monitoring, order management, customer systems, secondary market channels.
**Outcome & KPIs** — Service level to customers; waste as % of volume; value recovered from surplus; shelf life delivered to customer; grower price stability.
**Human gate** — Commercial allocation decisions between customers; grower relationship decisions.

### AG-06 — Food Safety, Traceability & Recall Management
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Food safety incidents demand identification of affected product within hours across complex supply chains. Most businesses cannot do it, and the default response is over-recall, which is enormously expensive.
**Trigger** — Test result, complaint, supplier notification, regulatory alert, or an internal deviation.
**Workflow** — 1) Maintain the traceability graph continuously: raw material lots, processing batches, rework, packaging, and finished-goods lots through to customer delivery. Rework is where traceability chains usually break. 2) On an incident, **determine the affected scope precisely and fast**: which batches, which ingredients, which finished products, and where they now are — including product already at retail or with consumers. 3) Assess the food-safety risk against the hazard, the exposure and the vulnerable-population impact. 4) Recommend the action: withdrawal, recall, or no action, with the evidence — and be willing to recommend the narrower action when the evidence supports it, because that is where the traceability investment pays back. 5) Generate regulatory notifications within the mandated timescales and the customer communications. 6) Coordinate execution: stock holds, retrieval, customer confirmation, and disposal or reprocessing with evidence. 7) Investigate root cause across the process and supply chain. 8) Monitor food-safety indicators continuously — verification results, environmental monitoring, supplier performance, HACCP deviations — to catch problems before they become incidents.
**Systems** — ERP/MES with lot tracking, LIMS, supplier systems, customer/retailer systems, regulatory portals, QMS.
**Outcome & KPIs** — **Time to determine recall scope (the metric that defines the capability)**; recall precision (product recalled vs product actually affected); regulatory notification timeliness; incidents prevented by monitoring; root causes eliminated.
**Human gate** — **Recall decisions are made by the technical director and executive team**; regulatory notification is a legal act by an accountable person.

### AG-07 — Supplier & Grower Quality Assurance
**A8 · L3 · B3 · Procure-to-pay**
**Pain** — Food businesses depend on hundreds of growers and suppliers whose certification, practices and product quality must be verified continuously, not annually.
**Trigger** — Delivery, certification event, audit cycle, or a quality signal.
**Workflow** — 1) Maintain supplier and grower records: certifications (GlobalGAP, BRC, organic, assurance schemes), audit results, approved products, and performance history. 2) **Verify certification validity and scope continuously** — an expired or out-of-scope certificate discovered at audit is a serious non-conformance, and it is entirely preventable. 3) Validate incoming product against specification: quality, residue testing, contamination, and documentation. 4) Manage residue and contaminant testing programmes risk-based rather than uniformly, targeting testing where risk is concentrated. 5) On non-conformance, quarantine, assess exposure, and raise the corrective action with the evidence. 6) Monitor supplier performance and risk, including ethical and labour-standards evidence, which is now a legal requirement in a growing number of markets. 7) Plan and support audits with the evidence assembled and the prior findings tracked. 8) Analyse quality patterns by supplier, region, season and variety.
**Systems** — Supplier management, QMS, LIMS, certification databases, ERP receiving, audit management.
**Outcome & KPIs** — Certification currency (100% required); rejection rate at intake; residue exceedances; corrective-action closure; audit findings; supplier quality trend.
**Human gate** — Supplier approval and disqualification are technical decisions; product rejection above threshold is human-confirmed.

### AG-08 — Processing Operations & Yield Optimisation
**A6 · L3 · B3 · Plan-to-produce**
**Pain** — Food processing yield is the dominant margin driver; small yield losses compound enormously, and the causes are distributed across raw material, process settings and equipment condition.
**Trigger** — Continuous production monitoring, or a batch completion.
**Workflow** — 1) Track yield by batch, line, shift and raw-material source, reconciling input to output including by-products and waste. 2) **Decompose yield loss into causes**: raw material variability, process settings, equipment condition, giveaway on weight, trim losses, and rework. Undecomposed yield reporting cannot drive action. 3) Identify optimal process settings for each raw material profile, learned from historical performance rather than from the manual. 4) Detect and quantify giveaway — overfilling to guarantee minimum weight is one of the largest and least visible losses in food manufacturing. 5) Monitor equipment condition affecting yield: blade sharpness, calibration drift, and seal integrity. 6) Balance yield against quality and food-safety constraints, which are absolute limits, not trade-offs. 7) Recommend specific actions with quantified value. 8) Support planning: which raw material to run on which line, for which product, to maximise total value.
**Systems** — MES, weighing and inspection systems, ERP, quality systems, equipment monitoring.
**Outcome & KPIs** — Yield percentage and trend; giveaway reduction; rework rate; value per tonne of raw material; quality and safety compliance maintained.
**Human gate** — Process changes affecting food safety require technical approval; HACCP critical limits are never adjustable by the agent.

### AG-09 — Sustainability, Carbon & Regulatory Reporting
**A8 · L2 · B3 · Risk-to-assurance**
**Pain** — Food and agriculture face intense and rapidly expanding reporting: carbon footprints, deforestation-free supply chains, water, biodiversity, and animal welfare — with data spread across thousands of suppliers and farms.
**Trigger** — Reporting cycle, customer requirement, or a regulatory deadline.
**Workflow** — 1) Collect farm and supplier data with the lightest possible burden, because data collection burden is the binding constraint — pre-fill from known data and ask only for what is genuinely unknown. 2) Compute footprints using recognised methodologies with **data quality graded and disclosed**, since most agricultural emissions data is modelled and pretending otherwise is greenwashing. 3) Support deforestation-regulation compliance: geolocation of production plots, risk assessment, and due-diligence evidence. 4) Assess water, biodiversity and soil metrics where required. 5) Aggregate through the supply chain with correct allocation across co-products. 6) Identify and quantify reduction opportunities with cost, so the report drives action rather than sitting on a shelf. 7) Generate customer, regulatory and voluntary disclosures with methodology and assurance readiness. 8) **Verify claims against evidence before publication** — unsubstantiated environmental claims in food are actively enforced.
**Systems** — Supplier and farm data platforms, carbon calculation engines, geospatial data, ERP, reporting platforms.
**Outcome & KPIs** — Supplier data coverage and quality; footprint per unit; deforestation compliance evidence; reduction achieved; assurance findings; claims substantiated.
**Human gate** — Public claims and regulatory submissions are executively approved and increasingly externally assured.

### AG-10 — Commodity Risk & Procurement
**A6 · L1 · B4 · Procure-to-pay**
**Pain** — Food businesses are exposed to volatile agricultural commodity, energy and freight markets. Hedging and buying decisions are made with limited analysis under time pressure.
**Trigger** — Market movement, procurement cycle, or a position review.
**Workflow** — 1) Track exposures across commodities, currencies and freight, mapped to product costs and contracted selling prices — the mismatch between fixed selling prices and floating input costs is the actual risk. 2) Monitor market fundamentals: crop conditions and progress globally, stocks, export policy, currency, and energy. 3) Analyse price drivers and explain market moves, distinguishing fundamental shifts from noise. 4) Assess the position against the hedging policy: coverage ratios by horizon, and the risk of the uncovered portion quantified. 5) Model scenarios: what a defined price move does to gross margin over the next four quarters. 6) Identify procurement opportunities and timing considerations, framed as analysis rather than as a trading recommendation. 7) Support supplier negotiation with cost-model transparency: what the input costs actually justify. 8) Report the position and its risk to the risk committee.
**Systems** — Commodity market data, ERP, hedging/treasury systems, crop and weather intelligence, cost models.
**Outcome & KPIs** — Margin volatility; hedge coverage against policy; procurement cost vs benchmark; forecast accuracy; policy breaches (target zero).
**Human gate** — **All hedging and purchasing decisions are human** and governed by the risk policy. The agent analyses; it never trades.

### AG-11 — Farm Labour, Compliance & Worker Welfare
**A8 · L2 · B4 · Hire-to-retire**
**Pain** — Agricultural labour is seasonal, often migrant, and subject to intense scrutiny on right-to-work, pay compliance and modern-slavery risk. Failures are both legal and reputational catastrophes.
**Trigger** — Recruitment, work period, payroll cycle, or an audit.
**Workflow** — 1) Manage recruitment compliance: right-to-work verification, visa and scheme conditions, and licensed-labour-provider verification where gangmaster licensing applies. 2) Track working time, rest periods and accommodation standards against the applicable rules. 3) Verify pay compliance: minimum wage including piece-rate conversion, deductions for accommodation and transport within legal limits, and no unlawful charges — **the arithmetic of piece rates against minimum wage is where non-compliance usually hides**. 4) Detect modern-slavery and exploitation indicators: shared bank accounts, common addresses, third-party control of pay, and unusual deduction patterns. Escalate immediately and never confront. 5) Manage training, competence and safety requirements per task. 6) Support welfare: accommodation standards, grievance mechanisms in workers' languages, and access to support. 7) Assemble audit evidence for customer and scheme audits. 8) Report on labour standards for supply-chain due diligence.
**Systems** — Labour management, payroll, time and attendance, right-to-work verification, accommodation records, grievance systems.
**Outcome & KPIs** — Pay compliance rate (100% required); right-to-work coverage; working-time breaches; exploitation indicators escalated; audit findings; grievance resolution.
**Human gate** — **Any modern-slavery or exploitation indicator escalates immediately to a designated human and, where required, to authorities.** The agent never investigates or confronts. Worker data use is tightly constrained.

### AG-12 — Farm Financial Management & Support Schemes
**A2 · L2 · B3 · Record-to-report**
**Pain** — Farm businesses manage complex subsidy and environmental scheme applications with strict rules and heavy penalties for error, alongside thin-margin financial management.
**Trigger** — Scheme application window, compliance deadline, or a financial cycle.
**Workflow** — 1) Maintain land, cropping and livestock records to the standard the schemes require. 2) Identify applicable schemes and options against the farm's land, practices and objectives, and model the financial outcome of each. 3) Prepare applications with the required evidence, validating against the scheme rules before submission — **most penalties result from avoidable declaration errors, not from wrongdoing**. 4) Track compliance obligations through the scheme year: dates, practices, record-keeping and environmental conditions. 5) Alert on deadlines and on actions that would breach scheme conditions before they are taken. 6) Prepare for inspection with the evidence assembled. 7) Support financial management: enterprise-level costing, cash-flow forecasting, and benchmarking against comparable farms. 8) Model business decisions — enterprise changes, capital investment, diversification — with realistic assumptions.
**Systems** — Farm management software, scheme portals, land registry and mapping, accounting systems, benchmarking data.
**Outcome & KPIs** — Scheme payments received vs entitlement; penalties (target zero); application accuracy; deadline compliance; margin by enterprise; forecast accuracy.
**Human gate** — Scheme applications are legally declared by the farmer; financial and business decisions are theirs.

---
## Regulatory notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Food safety law & HACCP** | Critical control limits are absolute and never adjustable by an agent. Recall decisions are human and legally attributable. Traceability records have mandated retention. |
| **Veterinary medicines & antimicrobial stewardship** | Prescription decisions are veterinary acts. Withdrawal periods are food-safety critical and enforced deterministically. |
| **Plant protection products** | Application is governed by approval, dose, operator certification and environmental conditions. The agent enforces; it never advises around a restriction. |
| **Deforestation & due-diligence regulation (EUDR and analogues)** | Requires plot-level geolocation and documented due diligence — a data-collection problem at supplier scale that agents are well suited to. |
| **Labour & modern slavery** | Indicators escalate to humans immediately. Pay-compliance arithmetic (piece rates vs minimum wage) must be exact. |
| **Environmental claims** | Substantiation is required before publication; unevidenced claims are blocked at the platform layer. |
