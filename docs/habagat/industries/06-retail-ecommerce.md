# Document 06 — Retail & E-Commerce

> 14 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Retail is the fastest **time-to-measurable-value** vertical in the catalogue: the metrics (conversion, margin, sell-through, contact cost) are instrumented already, so an agent's impact is provable within a quarter.
- The largest, least-glamorous prize is **RT-04 Product Content & Catalogue Enrichment**. Bad product data suppresses search, conversion and returns performance simultaneously, and every retailer has hundreds of thousands of defective SKUs.
- **RT-07 Markdown & Promotion Optimisation** and **RT-05 Demand Forecasting & Replenishment** move gross margin directly; they are the CFO-legible agents.
- Retail agents run at high volume and low value per run, so **unit economics discipline matters more here than anywhere else**: small-model routing, caching and batch processing are the difference between 75% and 35% gross margin.

---

### RT-01 — Customer Service & Order Support
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — "Where is my order", returns, cancellations and sizing questions dominate contact volume; peak-season spikes are 5–10× baseline and cannot be staffed economically.
**Trigger** — Customer contacts via chat, email, social, or messaging channel.
**Workflow** — 1) Identify the customer and the relevant order from partial information (email, order number, "the blue jacket I bought last week"). 2) Classify intent, detecting multi-intent messages. 3) Assemble the truth: order status, fulfilment records, carrier tracking with the actual scan history, payment state, and prior contacts. 4) For delivery issues, diagnose the real state — in transit, delayed, delivered-not-received, or lost — and apply the appropriate policy rather than a generic apology. 5) Execute within the policy envelope: reship, refund, return authorisation, address correction pre-dispatch, or expedited replacement. Value thresholds and account history bound the envelope. 6) For product questions, retrieve the product data, reviews and sizing guidance and answer specifically. 7) Detect fraud/abuse patterns (serial refunders, delivered-not-received abuse) and route them, without accusing the customer. 8) Respond in the customer's language and the brand's voice; escalate on dissatisfaction, vulnerability, or high customer lifetime value.
**Systems** — OMS, e-commerce platform, WMS, carrier APIs, payment gateway, CRM, PIM, returns platform.
**Outcome & KPIs** — Auto-resolution rate; cost per contact; CSAT; refund/reship accuracy; peak-season containment; abuse detection.
**Human gate** — Refunds above threshold, goodwill gestures beyond policy, complaints, and any legal or safety issue (product safety complaints route immediately).

### RT-02 — Personalised Shopping & Product Discovery
**A4 · L2 · B3 · Demand creation**
**Pain** — Keyword search fails on intent-rich queries ("something smart for a beach wedding in September"), and category navigation loses customers who don't know the taxonomy.
**Trigger** — Customer searches, browses, or asks a question in the storefront.
**Workflow** — 1) Interpret the intent behind the query: occasion, constraints, budget, style, size, timing. 2) Ask at most one or two clarifying questions — more and the customer leaves. 3) Retrieve candidates over the catalogue using semantic + attribute + availability filtering; **stock and delivery-by-date are constraints, not decorations** — recommending an out-of-stock item is worse than a poor recommendation. 4) Rank by fit to the stated intent, the customer's history, and margin/strategic weighting where commercially governed and disclosed. 5) Explain the recommendation in terms the customer used, and surface the trade-offs honestly. 6) Provide sizing guidance from the customer's purchase and return history — the single biggest lever on returns. 7) Support the whole journey: comparison, complete-the-look, delivery options, and add-to-basket. 8) Learn from outcomes, including returns, not just clicks.
**Systems** — E-commerce platform, PIM, inventory/ATP, CDP, search/vector index, recommendation service, reviews.
**Outcome & KPIs** — Conversion rate; average order value; **return rate (a guardrail — conversion bought with returns is a loss)**; search abandonment; assisted-revenue share.
**Human gate** — Merchandising governs ranking policy; commercial weighting must be disclosed where regulation requires; no dark patterns.

### RT-03 — Returns Processing & Fraud Screening
**A5 · L3 · B3 · Order-to-cash**
**Pain** — Returns are 15–30% of online sales; processing is manual, disposition decisions are poor (perfectly good stock gets liquidated), and return fraud is material.
**Trigger** — Return requested by a customer, or a returned item arrives at the warehouse.
**Workflow** — 1) Validate return eligibility against policy: window, condition requirements, category exclusions, and proof of purchase. 2) Score return-abuse risk from customer history, patterns and item characteristics — with a strong bias against false positives, because accusing a good customer is expensive. 3) Determine the optimal return path: return to warehouse, return to store, keep-it-refund (where item value is below processing cost), or donate. 4) Generate the label and instructions; set expectations on refund timing. 5) On receipt, capture condition; determine disposition: restock, refurbish, outlet, liquidate, recycle, or destroy — optimised on recovery value, not on habit. 6) Process the refund with the correct amount including shipping treatment per policy. 7) Analyse return reasons at SKU level and route insight to merchandising, quality and content: **most returns are caused by a content or sizing defect that can be fixed once**.
**Systems** — Returns platform, OMS, WMS, payment gateway, PIM, fraud engine, reverse-logistics partners.
**Outcome & KPIs** — Return processing cost; refund cycle time; recovery value per returned unit; return-fraud loss; **return rate reduction from content fixes**; customer satisfaction with returns.
**Human gate** — Account-level abuse action (blocking or restricting a customer) is always human; high-value returns need inspection.

### RT-04 — Product Content & Catalogue Enrichment
**A2 · L3 · B2 · Idea-to-market**
**Pain** — Supplier-provided product data is inconsistent, incomplete and wrong. Missing attributes destroy filtered search; poor descriptions destroy conversion; wrong data destroys trust and drives returns.
**Trigger** — New product onboarding, supplier data feed update, or a content-quality sweep.
**Workflow** — 1) Ingest supplier data in whatever form it arrives (spreadsheet, PDF spec sheet, images, EDI). 2) Map to the retailer's category taxonomy and attribute schema — the mapping is the hard part and it is where humans currently spend their weeks. 3) Extract missing attributes from unstructured sources including product images and spec documents. 4) Validate against category rules and plausibility: a 40kg pair of shoes is a data error, and rules alone never catch all of them. 5) Generate merchandising copy in brand voice, at the right length for each channel, **grounded strictly in verified attributes** — inventing a feature is a consumer-protection issue, not a style issue. 6) Generate SEO metadata, structured data markup, and channel-specific variants (marketplace feeds have their own schemas). 7) Localise for each market including units, sizing conventions and regulatory phrasing. 8) Enforce compliance: mandated safety information, energy labels, ingredient/allergen declarations, and restricted-claim checks. 9) Score content quality per SKU and prioritise the backlog by revenue impact.
**Systems** — PIM, DAM, e-commerce platform, marketplace feeds, translation services, taxonomy/attribute schema.
**Outcome & KPIs** — Attribute completeness; time-to-publish for new SKUs; search-result coverage; conversion on enriched vs baseline SKUs; return rate attributable to content; compliance defects.
**Human gate** — Category managers approve taxonomy changes; regulated claims (health, safety, sustainability) require compliance review.

### RT-05 — Demand Forecasting & Replenishment
**A6 · L3 · B3 · Plan-to-produce**
**Pain** — Forecasting at SKU-location-week granularity across hundreds of thousands of combinations is beyond manual capacity; planners manage by exception and exceptions are everywhere.
**Trigger** — Planning cycle, or a demand-signal anomaly.
**Workflow** — 1) Generate baseline forecasts incorporating trend, seasonality, price elasticity, promotion effects, cannibalisation and halo. 2) Adjust for known events: promotions, marketing spend, weather, local events, competitor actions, and calendar shifts. 3) **Detect and explain forecast anomalies** — a spike is a signal that must be diagnosed (viral product, competitor stockout, data error, or a promotion nobody told planning about). 4) Compute replenishment recommendations respecting lead time, MOQ, pack size, shelf life, capacity and service-level targets. 5) Optimise allocation across locations for new and constrained products, where allocation quality matters more than forecast quality. 6) Flag risks: stockout probability by SKU-location, overstock and ageing inventory, and supplier delivery risk. 7) Present planners with exceptions ranked by financial impact, each with a diagnosis and a recommended action. 8) Measure forecast accuracy and attribute error to cause so the model and the process both improve.
**Systems** — Demand planning platform, ERP, POS/e-commerce sales data, inventory, supplier data, weather/event feeds.
**Outcome & KPIs** — Forecast accuracy (MAPE/WMAPE by tier); in-stock rate; inventory turns; excess and obsolete stock; lost sales; planner exception load.
**Human gate** — Planners approve orders above thresholds and all new-product and seasonal allocations.

### RT-06 — Supplier & Vendor Collaboration
**A5 · L3 · B2 · Procure-to-pay**
**Pain** — Purchase-order lifecycle management with hundreds of suppliers is email-driven; delivery problems surface when the truck doesn't arrive.
**Trigger** — PO issued, supplier confirmation due, ASN received, or a delivery-date risk signal.
**Workflow** — 1) Transmit POs and chase confirmations, escalating on non-response before it becomes a shortage. 2) Reconcile supplier confirmations against the PO: quantity, price, date, and specification differences flagged individually. 3) Monitor in-transit and supplier production signals for delivery risk, and quantify the impact on in-stock position — risk without impact is noise. 4) On confirmed delay, generate mitigation options: alternate supplier, partial shipment, expedite, substitute, or demand shaping. 5) Manage goods-receipt discrepancies: short, over, damaged, or wrong item, with the claim documentation assembled automatically. 6) Track supplier performance: on-time-in-full, quality, responsiveness, and price compliance. 7) Generate supplier scorecards and prepare the review agenda with the specific evidence.
**Systems** — ERP/purchasing, supplier portal/EDI, WMS, transport visibility, supplier master.
**Outcome & KPIs** — PO confirmation rate and speed; OTIF; expedite costs; receipt discrepancy resolution time; supplier-caused stockouts.
**Human gate** — Commercial negotiations, supplier claims above threshold, and supplier exit decisions.

### RT-07 — Pricing, Markdown & Promotion Optimisation
**A6 · L2 · B4 · Order-to-cash**
**Pain** — Markdowns are taken too late and too deep; promotions are repeated because they were run last year; competitive price response is manual and inconsistent.
**Trigger** — Pricing review cycle, competitor price change, sell-through threshold, or a promotion planning cycle.
**Workflow** — 1) Monitor sell-through against the plan by SKU, store cluster and week; identify products deviating materially. 2) Estimate price elasticity from historical price and promotion response, controlling for confounders — naive elasticity estimates are the main reason pricing models fail. 3) Recommend markdown timing and depth optimising total gross margin over the remaining life, not this week's revenue. 4) For promotions, forecast incremental volume, cannibalisation, forward-buy and halo effects, and compute true incremental margin — most promotions are margin-negative once cannibalisation is included, and the agent should say so. 5) Monitor competitor pricing where legitimately available and recommend responses within the pricing strategy. 6) **Enforce hard constraints**: price-match commitments, MAP agreements, regulatory pricing rules (unit pricing, prior-price display rules for sale claims), and margin floors. 7) Simulate the P&L impact of a proposed pricing calendar. 8) Measure realised vs predicted and recalibrate.
**Systems** — Pricing/markdown optimisation, POS/e-commerce sales, inventory, competitor price data, ERP, promotion planning.
**Outcome & KPIs** — Gross margin; sell-through at full price; end-of-season residual inventory; promotion ROI; price-compliance exceptions.
**Human gate** — **All price changes are human-approved.** Competitor price monitoring must be legally sourced, and any algorithmic pricing must avoid conduct that could constitute collusion — a hard architectural constraint, not a policy note.

### RT-08 — Store Operations & Task Management
**A5 · L3 · B2 · Plan-to-produce**
**Pain** — Head office pushes tasks to stores with no view of store capacity; compliance with planograms, promotions and safety routines is inconsistent and unverified.
**Trigger** — Task generated centrally, exception detected, or a shift starts.
**Workflow** — 1) Aggregate demands on the store: promotions, resets, replenishment, audits, safety routines, and training. 2) Estimate the labour required and compare against the scheduled hours — surfacing the overload that causes silent non-compliance. 3) Prioritise and sequence tasks by sales impact and deadline; drop or defer low-value tasks explicitly rather than letting stores drop them silently. 4) Deliver tasks to store colleagues with clear, visual, mobile-first instructions. 5) Verify completion with evidence (photo of the display, count confirmation) and validate it. 6) Detect operational exceptions: shelf gaps from POS/inventory divergence, planogram non-compliance, price-label mismatches. 7) Escalate genuinely blocked tasks with the reason. 8) Report compliance and its correlation with sales performance by store.
**Systems** — Task management, workforce management, POS, inventory, planogram/space planning, mobile store app.
**Outcome & KPIs** — Task completion rate and evidence quality; on-shelf availability; planogram compliance; labour-hours vs task load; sales lift from compliance.
**Human gate** — Store managers can defer or reject tasks with a recorded reason — which is itself the most useful data the system produces.

### RT-09 — Loss Prevention & Shrink Analytics
**A6 · L2 · B3 · Risk-to-assurance**
**Pain** — Shrink runs 1–3% of sales; it is a mix of theft, process failure, waste and administrative error, and most retailers cannot distinguish between them.
**Trigger** — Continuous transaction and inventory monitoring, or a stock-count variance.
**Workflow** — 1) Analyse transaction data for anomaly patterns: voids, refunds without receipt, discounts, no-sales, and manual price overrides by operator, time and store. 2) Correlate with inventory variance at SKU and category level. 3) **Distinguish causes** — theft, receiving error, markdown not recorded, damage/waste, or system error. Treating a process failure as theft destroys trust and fixes nothing. 4) Score and rank investigation leads by expected recoverable value and evidential strength. 5) Assemble the case file for the loss-prevention team with the data trail. 6) Identify process root causes and route them to operations for a fix. 7) Track shrink trend by cause and the effectiveness of interventions.
**Systems** — POS transaction logs, inventory, stock counts, workforce data, exception-reporting platform, video (metadata only).
**Outcome & KPIs** — Shrink rate by cause; investigation hit rate; process defects fixed; recovered value; false-accusation incidents (must be zero).
**Human gate** — **All investigations of individuals are human-led with HR and legal involvement.** Employee monitoring is subject to strict jurisdictional constraints and works-council consultation; the agent reports patterns, never accusations.

### RT-10 — Marketing Campaign Creation & Optimisation
**A3 · L2 · B3 · Demand creation**
**Pain** — Campaign production is the bottleneck: dozens of assets per campaign across channels, markets and audiences, each requiring approval.
**Trigger** — Campaign brief approved, or a performance signal during a live campaign.
**Workflow** — 1) Interpret the brief: objective, audience, offer, channels, budget, timing and brand guardrails. 2) Define audience segments from the CDP with consent status verified per segment — consent is a hard filter applied before any creative work. 3) Generate channel-specific copy variants in brand voice, respecting each channel's constraints and each market's regulatory requirements. 4) Assemble creative from approved assets in the DAM; never generate imagery implying claims the product cannot support. 5) Compliance check: pricing claims, sustainability claims (a fast-growing enforcement area), health claims, comparative advertising rules, and mandated disclosures. 6) Route for brand and legal approval with the compliance evidence attached. 7) Deploy across channels, then monitor performance and reallocate budget within pre-authorised bounds. 8) Analyse results with proper attribution and feed learnings into the next brief.
**Systems** — Marketing automation, CDP, DAM, ad platforms, e-commerce, analytics, consent management.
**Outcome & KPIs** — Time from brief to launch; assets produced per campaign; ROAS/CAC; consent-compliance (must be 100%); approval-cycle time; creative-variant performance lift.
**Human gate** — Brand and legal approval before publication; all budget changes beyond the pre-authorised envelope.

### RT-11 — Omnichannel Order Orchestration
**A5 · L3 · B3 · Order-to-cash**
**Pain** — Deciding where to fulfil each order from — which warehouse, which store, split or whole — determines margin, speed and store-labour load, and is usually governed by crude static rules.
**Trigger** — Order placed, or a fulfilment exception occurs.
**Workflow** — 1) Determine sourcing options from real available-to-promise across all nodes, accounting for safety stock and store operational capacity. 2) Optimise the sourcing decision against total cost — shipping, labour, packaging, split-shipment penalty — and the promised delivery date, while respecting inventory-strategy rules (protect store sell-through, clear ageing stock). 3) Handle constrained inventory fairly across concurrent orders. 4) Release to the chosen node with priority and carrier selection. 5) Monitor for exceptions: node rejection, pick failure, carrier delay, damage. 6) On exception, **re-source automatically** rather than cancelling — most cancellations are avoidable and each one costs a customer. 7) Communicate proactively to the customer at every state change with an accurate date. 8) Analyse fulfilment cost and node performance for network decisions.
**Systems** — OMS, WMS, store inventory, carrier APIs, e-commerce, ERP.
**Outcome & KPIs** — Fulfilment cost per order; on-time delivery; split-shipment rate; cancellation rate; store pick accuracy and time; margin per order.
**Human gate** — Network policy and node-capacity rules are set by operations; large-scale re-routing during a disruption is human-approved.

### RT-12 — Assortment Planning & Range Review
**A3 · L1 · B3 · Idea-to-market**
**Pain** — Range reviews are periodic, politically driven and evidence-poor; a poor range decision is locked in for a season.
**Trigger** — Range review cycle, or a new supplier/product proposal.
**Workflow** — 1) Analyse current range performance: sales, margin, sell-through, rate of sale by store cluster, and space productivity. 2) Identify true incrementality vs cannibalisation — a bestselling SKU that only steals from its siblings adds no value, and this is the analysis range reviews consistently skip. 3) Assess customer coverage: which needs, price points and occasions are unserved, and which customer segments are lost as a result. 4) Analyse market and competitor assortment for gaps, using legitimately sourced data. 5) Evaluate proposed new products against the criteria and forecast their incremental contribution. 6) Recommend a range with delist candidates justified by evidence, and quantify the transferable demand from each delist. 7) Model the space and financial impact by cluster. 8) Track post-implementation performance against the prediction.
**Systems** — Category management/space planning, sales and margin data, market data, customer analytics, supplier proposals.
**Outcome & KPIs** — Sales and margin per space unit; range productivity; delist accuracy (did demand transfer as predicted?); new-product success rate; customer coverage.
**Human gate** — Category managers own all range decisions; supplier negotiations are human.

### RT-13 — Sustainability & Product Compliance
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Product regulation (safety, chemicals, packaging, energy, ESG reporting) is expanding fast; non-compliance means recalls, fines and delisting. Data lives with suppliers, who are slow to provide it.
**Trigger** — New product onboarding, regulatory change, or a compliance review cycle.
**Workflow** — 1) Determine applicable requirements by product category and destination market. 2) Assess whether the required evidence exists: test reports, certificates, declarations, safety data sheets, and supplier attestations. 3) Chase suppliers for missing evidence with specific, deadline-bound requests. 4) Validate submitted documents: authenticity, currency, scope coverage, and issuing-body accreditation — expired or out-of-scope certificates are the most common defect. 5) Screen product composition against restricted-substance lists. 6) Verify sustainability and origin claims against evidence — **greenwashing enforcement is now a real and rising legal exposure**, so unevidenced claims are blocked. 7) Assemble reporting data for CSRD/packaging/EPR obligations. 8) Monitor recall and enforcement feeds for affected products and act on them immediately.
**Systems** — PIM, supplier portal, compliance/testing databases, regulatory feeds, ESG reporting platform, DAM.
**Outcome & KPIs** — % products with complete compliance evidence; time-to-compliant-launch; unsupported claims blocked; recall response time; regulatory findings.
**Human gate** — Compliance sign-off before launch; all recall decisions are executive and safety-governed.

### RT-14 — Store Network & Space Planning Analytics
**A3 · L1 · B3 · Plan-to-produce**
**Pain** — Location, format and space decisions are long-term and capital-intensive, but the analysis behind them is often a spreadsheet and an opinion.
**Trigger** — Network review, lease event, or a new-site opportunity.
**Workflow** — 1) Model catchment demographics, competition, traffic and accessibility for each location. 2) Analyse existing store performance against catchment potential to identify under- and over-performance, controlling for format and maturity. 3) Model cannibalisation and transferable demand for proposed openings and closures — the analysis that determines whether a new store adds or shuffles revenue. 4) Assess the omnichannel role of each store: fulfilment node, returns hub, click-and-collect, and its contribution to online demand in the catchment. 5) Evaluate lease economics against performance, including the option value of flexibility. 6) Recommend network actions with the financial case and sensitivities. 7) For space, analyse category productivity and recommend space reallocation by cluster.
**Systems** — Location analytics, POS/sales data, lease management, demographic and mobility data, space planning, e-commerce demand by postcode.
**Outcome & KPIs** — Sales per square unit; new-store performance vs forecast; cannibalisation accuracy; lease-cost ratio; network contribution to omnichannel.
**Human gate** — All property and capital decisions are board/executive governed.

---
## Regulatory & commercial notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Consumer protection & advertising** | Generated content must be substantiated. Price-comparison and "was/now" claims are regulated in most markets. Sustainability claims face active enforcement. |
| **Algorithmic pricing & competition law** | Competitor-price-responsive pricing must be designed to avoid signalling or tacit collusion; no shared pricing infrastructure with competitors, ever. |
| **Privacy & consent (GDPR, ePrivacy, CCPA)** | Consent state is a hard filter applied before any personalised action. Profiling limits and opt-out must be enforced at the data layer. |
| **Product safety & EPR** | Recall obligations carry hard deadlines; the agent must be able to identify affected stock and customers within hours. |
| **Employee monitoring** | Loss-prevention analytics must operate at pattern level; individual monitoring requires legal basis, notice and consultation. |
