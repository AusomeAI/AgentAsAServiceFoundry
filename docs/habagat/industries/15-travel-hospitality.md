# Document 15 — Travel, Hospitality & Leisure

> 12 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Travel is a **disruption industry**: the value is not in taking bookings, it is in what happens when the flight cancels at 23:00 and 300 people need rebooking, hotels and communication simultaneously.
- **TRV-03 Disruption Management & Rebooking** is the single highest-value agent in this vertical by a wide margin. It attacks compensation cost, crew and asset recovery, and the moments that define brand perception.
- Revenue management and personalisation are the margin agents; service is the volume agent. Most operators should buy service first and revenue second, because service proves the ROI that funds the rest.
- Consumer-protection regimes (EU261, DOT rules, package travel directives) create **hard, automatable entitlements** — an agent that pays what is owed promptly costs less than one that fights it, and regulators are increasingly enforcing that.

---

### TRV-01 — Guest & Traveller Service
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Service volumes are enormous, multilingual, 24/7 and spike unpredictably. Booking changes, ancillary requests, and pre-arrival questions dominate.
**Trigger** — Guest or traveller contacts via any channel, in any language.
**Workflow** — 1) Identify the traveller and the booking, including bookings made through intermediaries, which is where identification usually fails. 2) Assemble context: itinerary, fare or rate rules, loyalty status, ancillaries purchased, special requirements, and history. 3) Classify intent and detect the multi-part requests typical of travel ("can I change my flight, add a bag and get a late checkout"). 4) For changes, compute the actual options under the fare or rate rules with the true cost, including any fare difference — the answer travellers most want and get least reliably. 5) Execute within the policy envelope: changes, ancillaries, seat and room assignment, special requests, and service recovery within thresholds. 6) Handle accessibility and special-assistance requirements with the required rigour, since these have regulatory force and real human consequence. 7) Escalate complaints, safety issues, medical matters and any accessibility request that cannot be fully met. 8) Operate in the traveller's language across channels.
**Systems** — PSS/CRS/PMS, booking engine, loyalty, ancillary systems, payment, CRM.
**Outcome & KPIs** — Containment rate; cost per contact; ancillary attach rate; CSAT; language coverage; special-assistance fulfilment.
**Human gate** — Complaints, compensation above threshold, medical and safety matters, and any unfulfillable accessibility requirement.

### TRV-02 — Booking, Upsell & Ancillary Revenue
**A4 · L2 · B3 · Demand creation**
**Pain** — Ancillary revenue is a large share of profit but offers are generic and badly timed; conversion is low and the experience feels like harassment.
**Trigger** — Booking in progress, pre-arrival window, or an in-stay interaction.
**Workflow** — 1) Understand the trip context: purpose, party composition, duration, and prior behaviour where consented. 2) Identify genuinely relevant ancillaries — a family with a long connection wants a lounge, a business traveller wants an early check-in, and offering the reverse trains people to ignore offers. 3) Check availability and eligibility in real time; **an unavailable offer is worse than no offer**. 4) Time the offer to the moment of relevance rather than the moment of booking, which is when most operators fire everything at once. 5) Present with honest, complete pricing including taxes and conditions, and without dark patterns — regulators are actively enforcing against pressure tactics and drip pricing. 6) Execute the purchase and update all downstream systems so the entitlement is honoured at the point of delivery. 7) Respect frequency limits and opt-outs absolutely. 8) Measure incremental revenue and, as a guardrail, the effect on satisfaction.
**Systems** — Booking engine, ancillary/merchandising platform, PMS/PSS, CRM/CDP, payment, inventory.
**Outcome & KPIs** — Ancillary revenue per booking; attach rate by product; conversion; **offer fatigue and opt-out rate (guardrail)**; satisfaction impact.
**Human gate** — Pricing and offer policy are commercially governed; consumer-protection rules on price presentation are enforced at the platform layer.

### TRV-03 — Disruption Management & Rebooking
**A5 · L2 · B4 · Issue-to-resolution**
**Pain** — A cancellation cascades: thousands of passengers, crew legality, aircraft positioning, hotel and transport needs, and statutory compensation. Manual recovery takes hours and produces poor, inconsistent outcomes.
**Trigger** — Cancellation, significant delay, overbooking, or a facility closure.
**Workflow** — 1) Determine the affected population precisely, including onward connections and multi-leg itineraries booked separately where identifiable. 2) **Prioritise by need, not by status alone**: unaccompanied minors, passengers requiring assistance, medical needs, and those with the tightest downstream consequences come first. This ordering is both right and increasingly a regulatory expectation. 3) Identify rebooking options across own network, partners and interline agreements, with realistic availability. 4) Generate personalised re-accommodation respecting the party's need to stay together, their onward arrangements and their preferences. 5) Determine **statutory entitlements automatically** — compensation, duty of care, meals, hotels, transport — under the applicable regime, and provide them proactively rather than on demand. Proactive payment costs less than a claims process. 6) Arrange the practical care: hotels within the disruption inventory, transport, and meal provision. 7) Communicate clearly and repeatedly with honest information, including when the information is bad. 8) For the operator, support the recovery plan: aircraft and crew, and the cost trade-off between cancelling and delaying. 9) Handle claims processing with entitlement determined from the operational record.
**Systems** — PSS/operations control, crew and fleet systems, partner and interline systems, hotel and ground-transport inventory, compensation engine, mass communication.
**Outcome & KPIs** — Time to re-accommodate; passengers stranded overnight; **compensation cost vs entitlement (both under- and over-payment)**; claim volume and cost to process; recovery time to normal operation; NPS in disruption.
**Human gate** — Operational recovery decisions (cancel, delay, swap) are the operations controller's; irregular compensation and goodwill above threshold; any duty-of-care shortfall escalates immediately.

### TRV-04 — Revenue Management & Dynamic Pricing
**A6 · L2 · B4 · Order-to-cash**
**Pain** — Pricing perishable inventory across dates, segments and channels is high-frequency and high-stakes; revenue managers cannot cover the whole estate at the required granularity.
**Trigger** — Continuous demand monitoring, booking-pace deviation, competitor move, or a demand event.
**Workflow** — 1) Forecast demand by date, segment and length of stay or route, incorporating seasonality, events, and the booking curve. 2) Monitor booking pace against forecast and detect deviation early enough to act — late detection means the inventory is already sold or already lost. 3) Analyse the market: competitor pricing and availability where legitimately available, and demand indicators. 4) Recommend price and inventory controls by segment and channel, optimising total revenue rather than occupancy or load factor alone. 5) Manage the trade-offs explicitly: displacement of higher-value demand, group versus transient, and channel cost. 6) **Enforce constraints**: rate parity obligations, contracted rates, loyalty entitlements, and consumer-protection rules on price presentation. 7) Explain each recommendation so the revenue manager can exercise judgement rather than rubber-stamp. 8) Measure realised revenue against the forecast and the counterfactual.
**Systems** — Revenue management system, PMS/PSS, channel manager, competitor data, event calendars, CRM.
**Outcome & KPIs** — RevPAR / yield; forecast accuracy; revenue vs comparable period; price-recommendation acceptance rate; parity compliance.
**Human gate** — Revenue managers approve strategy and override recommendations; **pricing must avoid any conduct capable of constituting collusion** — a hard architectural constraint where competitor data is used.

### TRV-05 — Group, Event & MICE Management
**A5 · L2 · B3 · Order-to-cash**
**Pain** — Group and event enquiries require checking availability across space, rooms and services, pricing complex packages, and coordinating delivery. Response speed determines win rate.
**Trigger** — Group or event enquiry received.
**Workflow** — 1) Parse the enquiry: dates, numbers, space, catering, accommodation, AV, and budget. 2) Check availability across all required components simultaneously and identify near-miss alternatives (adjacent dates, different space configuration) rather than declining. 3) Assess the commercial value including displacement: what transient business would this group displace, and at what rate? **Group business that displaces higher-value demand loses money**, and this is the calculation most operators skip under time pressure. 4) Build the proposal with the package, pricing and terms, applying the yield policy. 5) Respond fast — in group sales the first credible proposal wins disproportionately. 6) On acceptance, orchestrate delivery: rooming lists, function sheets, catering, AV, staffing and special requirements. 7) Manage changes and cut-off dates with proactive chasing. 8) Post-event, capture the actuals, reconcile the billing, and analyse profitability.
**Systems** — Sales and catering system, PMS, function-space inventory, CRM, banqueting and operations systems.
**Outcome & KPIs** — Response time; conversion rate; group profitability after displacement; delivery accuracy; billing disputes; repeat business.
**Human gate** — Pricing and contract terms above threshold; displacement decisions on high-demand dates.

### TRV-06 — Housekeeping, Operations & Service Delivery
**A5 · L3 · B2 · Plan-to-produce**
**Pain** — Daily operations balance labour against occupancy, arrival patterns and service standards; poor sequencing means guests wait for rooms and staff are simultaneously overworked and idle.
**Trigger** — Daily planning, real-time operational event, or a guest request.
**Workflow** — 1) Forecast the workload from occupancy, arrivals and departures, room types, stay-overs and known service requirements. 2) Plan labour against the workload, respecting contracts, skills and fair scheduling — and flag genuine understaffing rather than quietly degrading the standard. 3) Sequence room cleaning by expected arrival time, guest priority and floor efficiency, updating dynamically as early arrivals and late departures change the picture. 4) Track progress in real time and re-optimise on deviation. 5) Coordinate maintenance: out-of-order rooms, defects reported by housekeeping, and their impact on sellable inventory — which feeds directly back to revenue management. 6) Manage guest requests with routing, tracking and verified completion. 7) Monitor service standards with inspection and guest feedback correlation. 8) Analyse productivity and its constraints honestly.
**Systems** — PMS, housekeeping and task management, maintenance, workforce management, guest messaging.
**Outcome & KPIs** — Rooms ready by target time; guest wait for room; labour cost per occupied room; request response time; out-of-order room hours; cleanliness scores.
**Human gate** — Managers own staffing decisions; safety and security matters escalate immediately.

### TRV-07 — Loyalty & Customer Lifecycle
**A7 · L2 · B3 · Demand creation**
**Pain** — Loyalty programmes are expensive and most members are inactive. Communications are generic; the point at which a member is lapsing is visible in the data and acted on too late.
**Trigger** — Member behaviour change, lifecycle milestone, or a campaign cycle.
**Workflow** — 1) Segment members by value, behaviour, and lifecycle stage — and specifically by **trajectory rather than state**, since a declining high-value member matters more than a stable mid-value one. 2) Identify the specific reason for declining engagement where the data supports an inference: a service failure, a competitor relationship, a changed travel pattern, or life change. 3) Design the intervention: a genuinely valuable recognition, a relevant offer, a service recovery, or simply an appropriate acknowledgement. 4) Verify consent and preference status before any contact, and respect frequency limits. 5) Personalise using their actual history rather than a template token. 6) Manage the economics: reward liability, redemption behaviour, and true incremental value — loyalty programmes routinely reward behaviour that would have happened anyway, and the agent should measure that against holdouts. 7) Support service recovery with proportionate, timely gestures rather than delayed, grudging ones. 8) Report programme economics honestly.
**Systems** — Loyalty platform, CDP/CRM, booking systems, campaign management, consent management.
**Outcome & KPIs** — Active member rate; incremental revenue vs holdout; redemption and liability management; lapse rate; member satisfaction; opt-out rate.
**Human gate** — Programme economics and reward policy are commercial decisions; high-value member relationships are human-owned.

### TRV-08 — Distribution, Channel & OTA Management
**A6 · L3 · B3 · Order-to-cash**
**Pain** — Inventory and rates are distributed across dozens of channels with parity obligations, commission costs and constant content drift; errors cause overbooking or lost revenue.
**Trigger** — Rate or inventory change, channel performance signal, or a content update.
**Workflow** — 1) Manage rate and availability distribution across channels with mapping verified — mis-mapped room or fare types cause revenue loss and guest disputes, and they are common. 2) Monitor parity and detect breaches, including those caused by third-party discounting outside the operator's control, and identify the source. 3) Analyse channel economics: gross revenue less commission, less cost to serve, less cancellation and no-show rates — **net contribution by channel, which frequently reverses the apparent ranking**. 4) Detect and resolve content drift: descriptions, images, amenities and policies differing across channels, which drives complaints and refunds. 5) Manage overbooking risk with real-time inventory reconciliation across channels. 6) Optimise channel mix within contractual constraints and shift demand to higher-contribution channels where possible. 7) Handle channel-originated booking modifications and cancellations consistently.
**Systems** — Channel manager, PMS/CRS, OTA extranets, rate-shopping tools, content management.
**Outcome & KPIs** — Parity compliance; channel net contribution; direct-booking share; content consistency; overbooking incidents; mapping errors.
**Human gate** — Channel contracts and commercial terms; decisions to withdraw from a channel.

### TRV-09 — Safety, Security & Incident Management
**A8 · L2 · B4 · Risk-to-assurance**
**Pain** — Travel and hospitality operators carry duty-of-care obligations for guests and staff; incidents require immediate, correct response and thorough documentation.
**Trigger** — Incident reported, security alert, or a safety inspection.
**Workflow** — 1) Capture the incident with structured detail and immediate severity assessment. 2) **Trigger the correct response protocol immediately** — medical, fire, security, safeguarding, or food safety — with the notifications the protocol requires. 3) Assemble the relevant context: location, persons involved, CCTV availability (metadata and retention, not content analysis), and prior incidents at the location. 4) Manage regulatory notification obligations with their deadlines. 5) Support investigation with evidence gathering, timeline reconstruction and structured root-cause analysis. 6) Track corrective actions to verified closure. 7) Manage compliance programmes: food safety (HACCP), fire safety, water hygiene, pool safety, licensing conditions, and staff training currency. 8) Analyse leading indicators and incident patterns across the estate.
**Systems** — Incident management, EHS platform, PMS, training records, compliance registers, insurance systems.
**Outcome & KPIs** — Incident rate; response protocol compliance; regulatory notification timeliness; corrective actions closed; compliance audit outcomes; claims frequency.
**Human gate** — **All incident response is human-led.** Safeguarding, serious injury and criminal matters follow statutory process. Duty-of-care decisions are management responsibilities.

### TRV-10 — Workforce Scheduling & Labour Optimisation
**A5 · L2 · B3 · Plan-to-produce**
**Pain** — Hospitality labour is the largest controllable cost and the largest driver of guest experience. Scheduling against volatile demand, high turnover and complex rules is done manually and badly.
**Trigger** — Scheduling cycle, demand change, or an absence.
**Workflow** — 1) Forecast demand by department and time interval: covers, occupancy, arrivals, and event schedules. 2) Compute labour requirements against service standards and productivity models, by skill. 3) Generate schedules satisfying hard constraints (contracts, working-time law, minor-employment rules, rest periods, fair-scheduling and predictive-scheduling laws where they apply) and optimising cost, fairness and preference. 4) **Treat fair-scheduling regulation as a hard constraint** — in a growing number of jurisdictions, late schedule changes carry mandatory premium pay. 5) Manage real-time changes: absence, demand deviation, and event changes, with equitable open-shift offers. 6) Track actual versus scheduled hours and productivity, and diagnose deviation. 7) Support retention analysis: which scheduling patterns correlate with turnover, which in this sector is the dominant cost.
**Systems** — Workforce management, PMS/POS, time and attendance, HR systems, forecasting.
**Outcome & KPIs** — Labour cost percentage; schedule stability and premium-pay incidents; overtime; service standards maintained; turnover; employee satisfaction.
**Human gate** — Managers approve schedules; all working-time and fair-scheduling constraints are non-negotiable.

### TRV-11 — Reviews, Reputation & Experience Analytics
**A6 · L2 · B3 · Issue-to-resolution**
**Pain** — Reviews arrive across many platforms; responses are slow or templated; the operational causes behind ratings are rarely identified with enough specificity to fix.
**Trigger** — Review or survey response posted, or an analysis cycle.
**Workflow** — 1) Aggregate feedback across review platforms, surveys, social channels and direct complaints. 2) Analyse at the level of the specific operational driver: not "cleanliness" but "bathroom cleanliness in the refurbished wing, reported by 14 guests in the last 30 days, concentrated on Sundays" — the granularity that makes a finding actionable. 3) Link feedback to the underlying stay or trip record where possible, so operational data can be correlated with the experience. 4) Detect emerging issues early, before they become a rating trend. 5) Draft responses that are specific, take genuine ownership, and avoid the templated language guests recognise instantly. 6) Route service-recovery opportunities with the context and the authorised gesture. 7) Detect fake and manipulated reviews and handle them through platform processes. 8) Report to operations with the ranked, quantified drivers of rating movement.
**Systems** — Review aggregation, survey platforms, PMS/CRM, social monitoring, operational systems.
**Outcome & KPIs** — Rating trend; response rate and time; issues detected before rating impact; service recovery conversion; operational fixes traced to feedback.
**Human gate** — Responses to serious allegations (safety, discrimination, criminal) are human-drafted with legal input; recovery gestures above threshold.

### TRV-12 — Travel Programme & Corporate Account Management
**A6 · L2 · B3 · Order-to-cash**
**Pain** — Corporate travel programmes require policy compliance, supplier management and duty-of-care tracking; travellers book outside policy and travel managers cannot see the whole picture.
**Trigger** — Booking made, policy review, traveller in a risk location, or an account review.
**Workflow** — 1) Check bookings against travel policy and identify exceptions with the reason, at the point of booking where influence is possible rather than in a retrospective report. 2) Guide travellers to compliant options that meet their genuine need — most out-of-policy booking is caused by policy that does not fit the trip. 3) Consolidate the travel picture across booking channels, including bookings made outside the programme, since **duty of care fails on the traveller you do not know about**. 4) Track traveller location and safety exposure against risk information, and support emergency response and communication. 5) Analyse programme performance: spend, savings, compliance, supplier performance, and traveller satisfaction. 6) Support supplier negotiation with volume and performance evidence. 7) Report sustainability metrics for corporate reporting. 8) Identify policy improvements from the pattern of exceptions.
**Systems** — Online booking tool, TMC systems, expense, HR data, risk-intelligence providers, supplier contracts.
**Outcome & KPIs** — Policy compliance; savings realised; traveller satisfaction; duty-of-care coverage (% travellers tracked); supplier performance; emissions per trip.
**Human gate** — Policy exceptions requiring approval; emergency response is human-led; traveller-tracking data use is bound by employment and privacy law and requires transparency.

---
## Regulatory notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Passenger rights (EU261, DOT, package travel)** | Entitlements are computable from the operational record. The agent should determine and provide them proactively; under-payment is a regulatory risk and over-payment is a cost, so accuracy matters both ways. |
| **Accessibility obligations** | Special-assistance requirements have regulatory force; a request that cannot be met must escalate to a human immediately. |
| **Consumer protection / price transparency** | Drip pricing, pressure tactics and misleading availability claims are actively enforced. These are platform-level prohibitions, not tone guidance. |
| **Competition law** | Where competitor pricing data informs recommendations, the design must preclude signalling or coordination. |
| **Employment & fair scheduling** | Predictive-scheduling laws impose premium pay for late changes; these are hard constraints in the scheduler. |
| **Duty of care & traveller tracking** | Location tracking of employees requires a lawful basis, transparency and proportionality; in many jurisdictions it requires consultation. |
