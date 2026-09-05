# Document 01 — Cross-Industry Agent Use Cases

> **20 use cases that apply to essentially every company, in every sector.**
> This is Habagat's **horizontal product line** — the fastest land, the highest reuse, the best gross margin.
> Notation defined in [Document 00](00-research-method-and-taxonomy.md).

---

## Executive take

- These 20 workflows exist in a bank, a hospital, a mine and a media company alike. Building them once and instantiating them per customer is the core of Habagat's margin structure.
- Twelve of the twenty are **L3-capable within 90 days** because their outputs are verifiable against a system of record — that is what makes them safe to automate, not their simplicity.
- The two highest-ROI entry points across every buyer we modelled are **UC-X02 Invoice & AP Processing** and **UC-X05 Support Ticket Triage & Resolution**. Both have unambiguous baselines, and both produce a defensible ROI number in under 60 days.
- The **portfolio effect matters more than any single agent**: a customer running 6 horizontal agents has 6× the switching cost and roughly 4× the retention of a customer running one.

### Portfolio at a glance

| Code | Use case | Archetype | Autonomy | Blast | Time-to-value |
|---|---|---|---|---|---|
| X01 | Enterprise Knowledge & Policy Answering | A3 | L2 | B1 | 3 weeks |
| X02 | Invoice & Accounts-Payable Processing | A2 | L3 | B3 | 6 weeks |
| X03 | Contract Review & Obligation Extraction | A2 | L2 | B2 | 8 weeks |
| X04 | Procurement Sourcing & Supplier Evaluation | A3 | L2 | B2 | 8 weeks |
| X05 | Customer Support Triage & Resolution | A1 | L3 | B3 | 5 weeks |
| X06 | Sales Lead Research, Scoring & Outreach | A7 | L2 | B3 | 4 weeks |
| X07 | RFP & Proposal Response Generation | A3 | L1 | B2 | 5 weeks |
| X08 | Recruiting Screen & Interview Scheduling | A1 | L2 | B3 | 5 weeks |
| X09 | Employee Onboarding Orchestration | A5 | L3 | B2 | 6 weeks |
| X10 | IT Service Desk & Access Management | A5 | L3 | B3 | 6 weeks |
| X11 | Financial Close & Reconciliation | A8 | L2 | B4 | 10 weeks |
| X12 | FP&A Variance Analysis & Narrative | A3 | L1 | B1 | 6 weeks |
| X13 | Collections & Dunning | A7 | L2 | B3 | 6 weeks |
| X14 | Data-Quality Steward | A6 | L3 | B2 | 6 weeks |
| X15 | Security Alert Triage (Tier-1 SOC) | A1 | L3 | B3 | 8 weeks |
| X16 | Compliance Evidence Collection & Audit Prep | A8 | L2 | B2 | 8 weeks |
| X17 | Meeting Intelligence & Commitment Tracking | A3 | L2 | B2 | 3 weeks |
| X18 | Competitive & Market Intelligence | A3 | L1 | B1 | 4 weeks |
| X19 | Vendor Risk & Third-Party Due Diligence | A8 | L2 | B2 | 7 weeks |
| X20 | Internal Process Mining & Automation Scout | A6 | L1 | B1 | 8 weeks |

---

### UC-X01 — Enterprise Knowledge & Policy Answering
**Archetype** A3 | **Autonomy** L2 | **Blast radius** B1 | **Value stream** Issue-to-resolution

**Pain** — Employees lose 4–6 hours a week hunting for policy, product and process answers across SharePoint, Confluence, ticket history and tribal knowledge. Answers are inconsistent, and the inconsistency itself creates downstream rework and compliance exposure.

**Trigger** — An employee asks a question in Teams/Slack, in the intranet search bar, or an internal ticket is created that a classifier routes here.

**Workflow**
1. **Trigger:** user posts "What's our policy on expensing client dinners in Singapore?" in Teams.
2. Agent classifies intent (`policy_lookup`) and detects entity scope: `expense`, `region=SG`, `category=client_entertainment`.
3. Agent resolves the asker's identity and entitlements from Entra ID — this determines which document sets it may search. *Retrieval is filtered by the user's ACLs, never after the fact.*
4. Hybrid retrieval (vector + keyword + semantic reranking) across the approved corpus; the agent retrieves candidate passages with document version and effective date.
5. Agent checks **recency and authority**: a 2021 policy superseded by a 2024 revision is discarded; conflicting sources are surfaced rather than silently resolved.
6. Agent synthesises an answer with inline citations to the exact clause and version.
7. Self-verification: every factual claim must be attributable to a retrieved passage. Unsupported claims are stripped and the agent states the gap explicitly.
8. If confidence is low or sources conflict, the agent routes to the named policy owner and tells the user it has done so.
9. **Outcome:** answer delivered in-channel with citations; the Q&A pair is logged; unanswerable questions become a ranked "knowledge gap" backlog for the policy team.

**Systems & tools** — Microsoft Graph (SharePoint, Teams, OneDrive), Confluence, ServiceNow KB, Entra ID for ACL-scoped retrieval, Azure AI Search.

**Outcome** — Consistent, cited, entitlement-safe answers; a continuously generated map of where the organisation's documentation is actually failing.

**KPIs** — Deflection rate vs. human-answered tickets; answer acceptance rate; % answers with valid citations; median time-to-answer; knowledge-gap closure rate.

**Human gate** — Conflicting or absent sources escalate to the document owner. Policy answers with legal consequence are marked "verify with HR/Legal" by rule, not by model judgement.

---

### UC-X02 — Invoice & Accounts-Payable Processing
**Archetype** A2 | **Autonomy** L3 | **Blast radius** B3 | **Value stream** Procure-to-pay

**Pain** — AP clerks key invoices from PDFs and emails, chase mismatches, and manually route approvals. Cost per invoice runs $6–$15 fully loaded; exception handling consumes 60% of the team's time; early-payment discounts are routinely missed.

**Trigger** — Invoice arrives in the AP mailbox, a supplier portal upload, or an EDI drop.

**Workflow**
1. **Trigger:** PDF lands in `ap@company.com`.
2. Agent classifies the document (invoice / credit note / statement / dunning letter / not-AP) and rejects non-AP items with a templated reply.
3. Extraction: supplier, tax IDs, invoice number, date, currency, line items, quantities, unit prices, tax, totals, PO reference, bank details. Extraction returns **per-field confidence**.
4. Arithmetic verification — line items must sum to subtotal, tax must reconcile to the jurisdiction rate, total must foot. Failures are hard-routed to exception, never "reasoned around".
5. Supplier resolution against the vendor master, including fuzzy-name matching and duplicate-invoice detection (same supplier + amount + date window + similar invoice number).
6. **Three-way match**: invoice ↔ purchase order ↔ goods receipt in ERP. Tolerances come from customer policy configuration, not from the model.
7. **Fraud checks** — bank-detail change vs. vendor master history is a hard stop; new supplier + first invoice + high value is a hard stop. These are deterministic rules the model cannot override.
8. Clean match within tolerance → post to ERP as approved-for-payment, coded to the correct GL account and cost centre (learned from that customer's coding history).
9. Mismatch → agent drafts the exception: it identifies *which* field disagrees, retrieves the PO history, drafts a supplier query email, and places it in the buyer's queue with a recommended resolution.
10. Discount opportunity detection: agent flags invoices where early payment terms are still capturable and quantifies the saving.
11. **Outcome:** invoice posted, coded and scheduled; or a fully-prepared exception with a recommended action awaiting one human click.

**Systems & tools** — Exchange/Graph mail, Azure AI Document Intelligence, SAP/Oracle/Dynamics/NetSuite ERP, vendor master, banking file generation (never direct payment release).

**Outcome** — Straight-through processing for the majority of invoices; exceptions arrive at humans pre-diagnosed rather than pre-sorted.

**KPIs** — Straight-through-processing rate; cost per invoice; touchless % ; days-to-post; duplicate/fraud catches; early-payment discount capture rate.

**Human gate** — **Payment release is always human** (B4 boundary). Any bank-detail change, any new supplier, and any invoice above the customer's authority threshold require named approval.

---

### UC-X03 — Contract Review & Obligation Extraction
**Archetype** A2 | **Autonomy** L2 | **Blast radius** B2 | **Value stream** Risk-to-assurance

**Pain** — Legal reviews every inbound contract manually; commercial teams wait days for a redline on a standard NDA. Post-signature, the obligations the company just accepted are buried in PDFs nobody re-reads, so renewal, indexation and audit rights silently expire.

**Trigger** — Contract uploaded to the CLM system, emailed to legal, or attached to a procurement request.

**Workflow**
1. **Trigger:** counterparty MSA arrives as a Word attachment.
2. Agent classifies contract type and identifies governing law, parties, and effective/termination dates.
3. Clause segmentation and mapping to the customer's **clause taxonomy** (liability, indemnity, IP, data protection, termination, assignment, audit, SLA, price escalation, exclusivity, non-solicit).
4. Deviation analysis: each clause is compared against the customer's **playbook** — their preferred position, their fallback, and their walk-away. The agent labels each as `acceptable` / `negotiable` / `escalate`.
5. Risk scoring with reasoning: e.g. "Uncapped indemnity at §12.3 combined with a broad IP assignment at §8 — escalate; playbook fallback is a 12-month-fees cap."
6. Agent drafts redlines in tracked changes using the playbook's approved language, plus a negotiation note explaining each change to the business owner in plain English.
7. **Obligation extraction:** every commitment with a date, a threshold or a recurring duty is extracted into a structured obligation register (who owes what, to whom, by when, on what trigger).
8. Obligations are written to the CLM/calendar with owners and lead-time reminders.
9. **Outcome:** a redlined draft, a risk summary for the business owner, and a live obligation register — from a document that previously became inert on signature.

**Systems & tools** — CLM (Icertis/Ironclad/Agiloft/SharePoint), Word/Graph, the customer's clause playbook, matter-management system.

**Outcome** — First-pass review in minutes; obligations become managed data rather than dormant text.

**KPIs** — Cycle time to first redline; % contracts needing no lawyer touch; clause-extraction precision/recall against a lawyer-graded set; obligations captured per contract; missed-obligation incidents.

**Human gate** — A qualified lawyer approves every outbound redline. The agent never signs, never sends to a counterparty, and never provides legal advice to third parties.

---

### UC-X04 — Procurement Sourcing & Supplier Evaluation
**Archetype** A3 | **Autonomy** L2 | **Blast radius** B2 | **Value stream** Procure-to-pay

**Pain** — Sourcing events take 8–14 weeks. Buyers manually assemble supplier long-lists, normalise incomparable bids, and build scoring matrices in Excel. Maverick spend continues because the compliant path is slower than the non-compliant one.

**Trigger** — A purchase requisition above threshold is raised, or a contract is approaching renewal within its notice window.

**Workflow**
1. **Trigger:** requisition for "industrial nitrile gloves, 400k units/yr, 3 sites" exceeds the $250k competitive-bid threshold.
2. Agent checks whether an existing framework agreement already covers this — the highest-ROI step, and the one humans skip.
3. If not covered, agent builds a category brief: historical spend, incumbent performance, price trend, demand forecast, and specification from prior POs.
4. Supplier long-list assembly from the approved vendor master, prior bid history, and (where the customer permits) external market sources.
5. Agent drafts the RFQ pack — scope, specification, commercial terms, scoring weights — grounded in the customer's templates.
6. On issue, agent handles supplier Q&A: it answers from the RFQ pack, escalates novel questions to the buyer, and broadcasts answers to all bidders to preserve fairness.
7. **Bid normalisation** — the hard part. Bids arrive in different units, currencies, incoterms, payment terms and inclusion scopes. Agent normalises to a comparable total-cost-of-ownership and *shows its normalisation assumptions* line by line.
8. Scoring against the published matrix; sensitivity analysis ("if we weight lead time at 30% instead of 15%, supplier B wins — here is why").
9. Agent drafts the award recommendation with an audit trail sufficient for procurement governance.
10. **Outcome:** an award recommendation pack ready for the sourcing committee, in days rather than weeks, with the normalisation logic fully inspectable.

**Systems & tools** — ERP/P2P (SAP Ariba, Coupa, Ivalua), vendor master, contract repository, spend analytics, email.

**Outcome** — Shorter sourcing cycles, comparable bids, and an auditable rationale that survives challenge.

**KPIs** — Sourcing cycle time; realised savings vs. baseline; % spend under contract; maverick-spend reduction; supplier participation rate.

**Human gate** — Award decisions are always human and committee-governed. The agent must never contact suppliers with commercial commitments.

---

### UC-X05 — Customer Support Triage & Resolution
**Archetype** A1 | **Autonomy** L3 | **Blast radius** B3 | **Value stream** Issue-to-resolution

**Pain** — Tier-1 agents spend most of their time classifying, gathering context and re-asking questions the customer already answered. Handle time is dominated by context assembly, not by problem solving. Backlogs spike unpredictably.

**Trigger** — Inbound email, web form, chat, or voice transcript creating a ticket.

**Workflow**
1. **Trigger:** customer emails "my order hasn't arrived and I was charged twice".
2. Agent detects that this is **two intents** and splits them — a decomposition step most triage systems get wrong.
3. Customer identity resolution across CRM, billing and order systems from the email address and any order reference.
4. Context assembly: order status, carrier tracking, payment records, prior tickets, entitlement/SLA tier, sentiment and churn risk.
5. Intent-specific playbook retrieval from the knowledge base, filtered to the customer's product version and region.
6. **Resolution attempt within policy envelope:** for the duplicate charge, the agent verifies the double authorisation in the payment system and — if within the auto-refund threshold — issues the refund and confirms. For the delivery, it queries the carrier API, finds the exception, and initiates the reship.
7. Every action is checked against the policy envelope before execution: refund limits, reship eligibility, fraud flags, and account standing.
8. Agent drafts a single reply covering both issues in the customer's language and the brand's tone, and sends it (L3) or queues it (L2).
9. Anything outside the envelope — high value, angry sentiment, legal threat, VIP account, repeat failure — is escalated to a human **with a complete case summary and a recommended action**, not as a raw ticket.
10. **Outcome:** resolved-on-first-contact, or a human receives a case that is 80% pre-worked.

**Systems & tools** — Zendesk/ServiceNow/Salesforce Service Cloud, order management, payment gateway (read + bounded refund), carrier APIs, KB, CRM.

**Outcome** — First-contact resolution on routine cases; escalations arrive diagnosed; handle time falls even on the cases the agent cannot close.

**KPIs** — Auto-resolution rate; first-contact resolution; CSAT on agent-handled vs. human-handled; average handle time on escalations; escalation precision (were escalations genuinely necessary?); refund error rate.

**Human gate** — Refunds above threshold, account closures, legal or regulatory complaints, and any detected vulnerability signal (bereavement, financial hardship, safeguarding) are hard-routed to humans immediately.

---

### UC-X06 — Sales Lead Research, Scoring & Outreach
**Archetype** A7 | **Autonomy** L2 | **Blast radius** B3 | **Value stream** Demand creation

**Pain** — SDRs spend ~70% of their time researching and writing, ~30% talking. Generic sequences produce low reply rates and burn the domain's sending reputation. Good leads go cold because follow-up is manual.

**Trigger** — New inbound lead (form fill, content download, demo request), a target-account trigger event (funding, hiring, leadership change, tech-stack change), or a CRM stage timeout.

**Workflow**
1. **Trigger:** lead submits a whitepaper download form.
2. Agent enriches: firmographics, technographics, headcount trend, recent news, existing relationship in CRM, and — critically — whether this account is already owned by an AE (duplicate outreach destroys trust).
3. ICP fit scoring against the customer's actual closed-won pattern, not a generic template. Agent explains the score.
4. Intent signal assembly: what content, how many touches, which pages, which people from the same domain.
5. **Routing decision:** disqualify (with reason), nurture, or route to an AE — with the reasoning logged so the model can be tuned against real outcomes.
6. For qualified leads, agent drafts a personalised first-touch referencing a *specific, verifiable* fact about the account and connects it to a relevant customer outcome. Generic personalisation tokens are explicitly forbidden.
7. Compliance check before send: consent/opt-out status, GDPR/CAN-SPAM/CASL basis, suppression list, sending-volume policy.
8. Send (or queue for AE approval), then manage the follow-up cadence, adapting to replies and stopping instantly on any opt-out or negative-sentiment signal.
9. Meeting booking against the AE's real calendar, with a briefing note generated for the AE before the call.
10. **Outcome:** qualified, researched, consented pipeline with the AE briefed — or a clean disqualification with a reason that improves the model.

**Systems & tools** — CRM (Salesforce/Dynamics), marketing automation, enrichment providers, calendar (Graph), email, consent/suppression store.

**Outcome** — More selling time, higher reply quality, and a scoring model that learns from closed-won rather than from opinion.

**KPIs** — Reply rate; meeting-booked rate; SQL→opportunity conversion; pipeline per SDR; opt-out rate (a guardrail metric — it must not rise); AE-rated lead quality.

**Human gate** — AE approval before first touch on named/strategic accounts. Hard stop on any account flagged legal, competitive or in active negotiation.

---

### UC-X07 — RFP & Proposal Response Generation
**Archetype** A3 | **Autonomy** L1 | **Blast radius** B2 | **Value stream** Demand creation

**Pain** — RFPs arrive as 200-question spreadsheets with 10-day deadlines. SMEs are pulled off delivery to re-answer questions the company has answered 40 times before, inconsistently.

**Trigger** — RFP/RFI/security questionnaire received; or a bid/no-bid decision resolves to "bid".

**Workflow**
1. **Trigger:** 180-question RFP spreadsheet uploaded to the bid folder.
2. Agent parses the document structure and extracts every question with its section, response format, word limit and mandatory/optional flag.
3. **Bid qualification support:** agent flags disqualifying requirements early (certifications not held, mandatory local presence, revenue thresholds) — the most valuable output, because a fast no-bid saves more than a good answer.
4. For each question, retrieval against the answer library, prior winning bids, product documentation and the compliance evidence store.
5. Draft answer generation constrained to approved claims. **Claims not evidenced in the source library are never invented** — the agent marks them `NEEDS SME` and names which SME.
6. Consistency pass across the whole response: the same fact must not be stated three different ways in three sections.
7. Compliance matrix generation: every requirement mapped to where it is answered, so reviewers can verify coverage.
8. Agent routes flagged questions to named SMEs with the specific gap, and merges their answers back.
9. New approved answers are written back into the answer library — the corpus compounds with every bid.
10. **Outcome:** a complete first-draft response with a compliance matrix and a short, targeted SME task list.

**Systems & tools** — Bid repository (SharePoint), answer library (Loopio/Responsive or SharePoint), CRM, product docs, Trust Center / compliance evidence store.

**Outcome** — Days of SME time returned; consistent claims; an answer library that improves rather than decays.

**KPIs** — Response cycle time; % auto-answered; SME hours per bid; win rate (directional); answer-library reuse rate; claim-accuracy defects found in review.

**Human gate** — Bid lead owns final submission. Pricing, legal terms and any new security or regulatory claim require named human approval.

---

### UC-X08 — Recruiting Screen & Interview Scheduling
**Archetype** A1 | **Autonomy** L2 | **Blast radius** B3 | **Value stream** Hire-to-retire

**Pain** — Recruiters screen hundreds of CVs per role, coordinate calendars across four interviewers and three time zones, and lose good candidates to slow process. Screening consistency is poor and legally exposed.

**Trigger** — Application submitted to the ATS, or a sourcing campaign returns candidates.

**Workflow**
1. **Trigger:** application lands in the ATS.
2. Agent parses the CV into structured attributes, normalising titles, skills, dates and education.
3. **Structured evaluation against the job's published, pre-agreed criteria only.** The rubric is fixed before the role opens; the agent scores each criterion with an evidence quote from the CV.
4. **Bias controls are architectural, not advisory:** name, gender, age, photo, nationality, address and university prestige are excluded from the feature set; the agent produces per-criterion evidence so decisions are contestable; adverse-impact statistics are computed continuously across protected groups.
5. Agent surfaces genuine ambiguity ("8 years' experience but 5 roles in 6 years — flag for recruiter judgement") rather than silently deciding.
6. Recruiter reviews the ranked shortlist with evidence. **The agent never auto-rejects** — rejection is a human decision, both for fairness and for legal defensibility under EU AI Act high-risk classification.
7. On advance, agent handles scheduling: interviewer availability, panel composition rules, candidate time zone, room/Teams link, and rescheduling.
8. Agent generates interviewer prep packs: candidate summary, which criteria remain unverified, and suggested probing questions tied to the rubric.
9. Post-interview, agent aggregates structured scorecards and flags where interviewers materially disagree.
10. **Outcome:** faster, more consistent, more auditable screening — with the human decision preserved exactly where the law and good practice require it.

**Systems & tools** — ATS (Workday/Greenhouse/SuccessFactors), calendar (Graph), Teams, assessment platforms.

**Outcome** — Time-to-shortlist collapses; screening becomes evidence-based and defensible.

**KPIs** — Time-to-shortlist; recruiter hours per hire; interview-to-offer ratio; candidate NPS; **adverse-impact ratio monitored as a hard guardrail**; scheduling reschedule rate.

**Human gate** — All rejections and all offers are human decisions. Under the EU AI Act this is a high-risk use; the agent operates as decision support with documented human oversight, logging and candidate notification.

---

### UC-X09 — Employee Onboarding Orchestration
**Archetype** A5 | **Autonomy** L3 | **Blast radius** B2 | **Value stream** Hire-to-retire

**Pain** — Onboarding spans HR, IT, facilities, security, payroll and the hiring manager, coordinated by checklist and goodwill. New hires wait days for access; compliance training lapses; role-specific setup is reinvented per hire.

**Trigger** — Offer accepted / new-hire record created in the HRIS.

**Workflow**
1. **Trigger:** HRIS emits `hire.created` with role, department, location, start date and manager.
2. Agent derives the onboarding plan from the role profile: entitlements, hardware, software, training, physical access, regulatory registrations.
3. **Access provisioning by entitlement pattern, not by copying a colleague's access** — the single biggest source of privilege creep in most organisations, and one the agent can eliminate outright.
4. Parallel orchestration: Entra ID account and group membership, licence assignment, hardware order, badge request, payroll enrolment, benefits window, statutory training assignment.
5. Dependency management: laptop shipping address depends on remote/office status; some access depends on training completion; some depends on background-check clearance. The agent models these as real dependencies with blocking semantics.
6. Continuous status tracking with proactive chase-ups to the accountable party — the agent chases, so the manager doesn't.
7. Day-1 through day-90 journey: welcome pack, buddy assignment, scheduled check-ins, manager nudges, and a conversational assistant answering the new hire's questions (delegating to UC-X01).
8. Exception handling: start-date changes, offer withdrawal, role change mid-onboarding — each triggers a re-plan and a clean rollback of anything already provisioned.
9. **Outcome:** productive on day one, with a complete audit trail of who was granted what and why.

**Systems & tools** — HRIS (Workday/SuccessFactors), Entra ID, Intune, ITSM, payroll, LMS, facilities, procurement.

**Outcome** — Day-one readiness as the norm; least-privilege access by construction; compliance training completed on time.

**KPIs** — % day-one ready; time-to-productivity; provisioning SLA attainment; over-provisioning incidents; training completion by deadline; new-hire experience score.

**Human gate** — Privileged/admin entitlements, regulated-role registrations and anything above standard role entitlement require manager + security approval.

---

### UC-X10 — IT Service Desk & Access Management
**Archetype** A5 | **Autonomy** L3 | **Blast radius** B3 | **Value stream** Issue-to-resolution

**Pain** — 40–60% of service-desk volume is password resets, access requests, software installs and "how do I" questions. Access requests queue for days; approvals are rubber-stamped; entitlements are never reviewed.

**Trigger** — Ticket, chat message, or self-service portal request.

**Workflow**
1. **Trigger:** "I need access to the Finance Power BI workspace."
2. Agent authenticates the requester and resolves their role, department, manager and current entitlements.
3. Request interpretation: which specific resource, what access level, for how long, and why — the agent asks for the business justification if absent, because approvers cannot approve without it.
4. **Policy evaluation:** is this entitlement standard for the role (auto-approvable), sensitive (manager + data-owner approval), or a segregation-of-duties conflict (deny with explanation)? SoD conflicts are computed against the customer's SoD matrix, deterministically.
5. Approval orchestration via Teams adaptive card to the data owner, with the requester's context and the SoD analysis attached.
6. On approval, provisioning via Entra ID / PIM, with **time-bound access by default** — access expires unless renewed, which is the single most effective entitlement-hygiene control.
7. Confirmation, plus a short "how to use this" note that prevents the follow-up ticket.
8. For incidents rather than requests: agent gathers diagnostics from Intune/endpoint telemetry, matches against known issues, applies the approved remediation runbook, and verifies resolution before closing.
9. Periodic access review: agent generates recertification campaigns with usage evidence ("this person has not used this entitlement in 6 months — recommend revoke").
10. **Outcome:** minutes-not-days access, with least privilege and expiry enforced by default.

**Systems & tools** — ServiceNow/Jira SM, Entra ID + PIM, Intune, Teams, endpoint telemetry, SoD matrix.

**Outcome** — Service-desk volume falls; entitlement hygiene improves structurally rather than through annual clean-up projects.

**KPIs** — Auto-resolution rate; mean time to fulfil access requests; standing-privilege reduction; SoD violations prevented; reopen rate; cost per ticket.

**Human gate** — Privileged roles, production access, security-group changes and any SoD exception require explicit human approval. The agent may never grant itself or modify its own permissions — enforced at the identity layer, not by prompt.

---

### UC-X11 — Financial Close & Reconciliation
**Archetype** A8 | **Autonomy** L2 | **Blast radius** B4 | **Value stream** Record-to-report

**Pain** — Month-end close takes 5–10 working days of accountants chasing balances, investigating variances and preparing schedules. The work is high-volume, deadline-compressed, and largely mechanical until it suddenly isn't.

**Trigger** — Period-end calendar event, or continuous (daily) reconciliation runs.

**Workflow**
1. **Trigger:** close calendar day 1 fires.
2. Agent runs the close checklist as an orchestrated plan, tracking task status, owners and dependencies across entities.
3. **Reconciliations:** bank, intercompany, AR/AP sub-ledger to GL, payroll, fixed assets, accruals. Agent matches transactions with configurable tolerance and multi-pass matching (exact → reference → amount+date → fuzzy).
4. Unmatched items are **investigated, not just listed**: agent retrieves supporting documents, checks timing differences, tests for common causes (FX rate, cut-off, duplicate, missing accrual) and proposes a specific journal with a supported explanation.
5. Flux/variance analysis vs. prior period, budget and forecast, with materiality thresholds; the agent drafts the explanation and cites the transactions driving it.
6. Anomaly detection over journal entries: unusual posters, round numbers, weekend/after-hours postings, entries to rarely-used accounts — the classic fraud-risk pattern set.
7. Agent assembles the close binder: supporting schedules, reconciliation evidence, approvals and the audit trail an external auditor will request.
8. Proposed journals go to the accountant for review with full support attached; **the agent never posts an unapproved journal.**
9. **Outcome:** a shorter close with better evidence, and exceptions that arrive explained rather than merely flagged.

**Systems & tools** — ERP GL, bank feeds, sub-ledgers, reconciliation tooling (BlackLine et al.), close-management calendar, BI.

**Outcome** — Days off the close; reconciliation quality that improves the audit rather than surviving it.

**KPIs** — Days-to-close; % auto-reconciled; unexplained variance count at sign-off; audit adjustments; late/manual journal count; close-task on-time rate.

**Human gate** — **Every journal posting requires human approval** (B4). Segregation of duties is enforced: the agent may prepare but never approve. Materiality thresholds are set by the controller and versioned.

---

### UC-X12 — FP&A Variance Analysis & Management Narrative
**Archetype** A3 | **Autonomy** L1 | **Blast radius** B1 | **Value stream** Record-to-report

**Pain** — Analysts spend the first ten days of every month rebuilding the same variance decks and writing narratives that say "revenue was below plan" without saying why. Insight arrives too late to act on.

**Trigger** — Close completion, weekly flash cycle, or a board/exec reporting deadline.

**Workflow**
1. **Trigger:** GL is closed for period; data warehouse refresh completes.
2. Agent pulls actuals, budget, forecast and prior year across the reporting hierarchy.
3. Variance decomposition to the level that matters: price vs. volume vs. mix vs. FX vs. one-offs — computed, not narrated.
4. **Driver attribution:** agent walks down the hierarchy to find the smallest set of entities that explain the majority of the variance ("78% of the EMEA shortfall is two accounts in the German enterprise segment").
5. Cross-source corroboration: it correlates the financial variance with operational data — pipeline, churn, headcount, unit volumes, ticket backlog — to propose a *cause*, clearly labelled as hypothesis rather than fact.
6. Narrative drafting in the house style, at the right altitude for the audience (board vs. functional review).
7. Forward look: agent flags where the run-rate implies a forecast miss, and quantifies the gap.
8. Chart and deck assembly against the standard template.
9. Analyst reviews, corrects and adds the judgement the agent cannot have.
10. **Outcome:** the analyst starts from a complete draft with the arithmetic already done and defensible, and spends their time on interpretation.

**Systems & tools** — EPM (Anaplan/Pigment/OneStream/Planful), data warehouse (Fabric/Synapse), Power BI, ERP, CRM, HRIS.

**Outcome** — Reporting cycle compressed; analysts move from assembly to insight.

**KPIs** — Hours to produce the pack; time from close to distribution; % variances with an accepted explanation; forecast accuracy trend; exec satisfaction with the narrative.

**Human gate** — All external and board-facing financial commentary is human-approved. The agent may never publish financial figures externally.

---

### UC-X13 — Collections & Dunning
**Archetype** A7 | **Autonomy** L2 | **Blast radius** B3 | **Value stream** Order-to-cash

**Pain** — Collections is under-resourced and applied uniformly: the same dunning letter goes to a strategic customer with a disputed invoice and to a serial late payer. DSO drifts; relationships get damaged by tone-deaf automation.

**Trigger** — Invoice ageing crosses a bucket, a payment promise is broken, or a payment run fails.

**Workflow**
1. **Trigger:** invoice hits 15 days past due.
2. Agent assembles the account picture: full ageing, payment history and behaviour pattern, open disputes, credit limit, contractual terms, relationship value, and open support tickets (an angry customer is often a non-paying customer for a reason).
3. **Root-cause classification** — the step that separates a collections agent from a dunning robot. Is this a dispute, an invoice-delivery failure, a PO mismatch, an approval bottleneck at the customer, a genuine cash-flow problem, or simple neglect? Each demands a different action.
4. Strategy selection per the customer's collections policy and segment: gentle reminder, invoice re-issue to the right AP contact, dispute routing to the account manager, payment-plan offer within policy, or escalation.
5. Outreach drafted in the correct tone for the segment and relationship, in the right language, to the right contact — with the invoice and remittance details attached, because the most common reason for non-payment is that AP never received a usable invoice.
6. Conversation handling: the agent processes replies, recognises promises-to-pay and records them with dates, recognises disputes and routes them, and recognises hardship signals and stops automated pursuit immediately.
7. Payment-plan proposals within pre-authorised parameters; anything outside goes to a credit manager.
8. Cash forecasting: agent feeds expected-collection dates into treasury.
9. **Outcome:** faster cash, fewer damaged relationships, and disputes surfaced early instead of at 90 days.

**Systems & tools** — ERP AR, CRM, payment portal, email/telephony, credit-agency data, treasury.

**Outcome** — DSO reduction with relationship-aware treatment and early dispute detection.

**KPIs** — DSO; collection effectiveness index; promise-to-pay kept rate; disputes identified before 60 days; bad-debt write-off; complaint rate (guardrail).

**Human gate** — Legal escalation, credit-hold, service suspension and write-off are always human. Hardship and vulnerability signals immediately suspend automation and route to a person.

---

### UC-X14 — Data-Quality Steward
**Archetype** A6 | **Autonomy** L3 | **Blast radius** B2 | **Value stream** Idea-to-market / all

**Pain** — Master data rots continuously: duplicate customers, stale addresses, missing tax IDs, inconsistent product attributes. Every downstream analytic and every agent inherits the rot. Data-quality projects are one-off and decay immediately.

**Trigger** — Continuous monitoring, record creation/update events, or a scheduled sweep.

**Workflow**
1. **Trigger:** new customer record created in CRM.
2. Agent applies the data contract for that entity: required fields, formats, referential integrity, and domain-specific validity rules.
3. **Duplicate detection** using entity resolution across name, address, tax ID, domain and phone — with a similarity score and the evidence for the match.
4. Enrichment from authoritative sources: company registries, address validation, tax-ID verification, industry classification.
5. Anomaly detection against learned distributions: a customer with a $50m credit limit in a segment where the median is $50k is flagged, not because a rule said so but because the distribution says so.
6. **Auto-remediation within policy:** formatting, casing, address standardisation, classification codes — these are safe, reversible and high-volume, so they run at L3.
7. **Stewardship queue for judgement calls:** proposed merges, credit anomalies, and conflicting authoritative sources go to the data steward with the evidence and a recommendation. Merges are never automatic — they are destructive and hard to reverse.
8. Root-cause reporting: the agent tells the data-governance team *which upstream process* is generating the defects, which is the only way quality actually improves.
9. **Outcome:** master data that trends toward clean, and a defect-source report that fixes the pipe rather than mopping the floor.

**Systems & tools** — CRM, ERP, MDM/Purview, data warehouse, external reference data, data-quality rules store.

**Outcome** — Trustworthy master data as a continuous state; every downstream agent gets better inputs.

**KPIs** — Duplicate rate; completeness/validity scores by entity; defects auto-remediated; steward queue age; % defects traced to a fixed root cause.

**Human gate** — Record merges, deletions and any change to financial/credit master data require steward approval.

---

### UC-X15 — Security Alert Triage (Tier-1 SOC)
**Archetype** A1 | **Autonomy** L3 | **Blast radius** B3 | **Value stream** Risk-to-assurance

**Pain** — SOC analysts drown in alerts, most of them false positives. Investigation is repetitive context assembly. Alert fatigue means real incidents are missed, and the mean time to respond stays flat no matter how many tools are bought.

**Trigger** — Alert raised in the SIEM/XDR.

**Workflow**
1. **Trigger:** Microsoft Sentinel raises "impossible travel" for a user.
2. Agent enriches: user identity, role, sensitivity, device posture, recent authentication history, VPN/travel context, and whether the user's manager recently approved travel.
3. Multi-source correlation: was there a mailbox rule created, an OAuth consent granted, an unusual download, a token anomaly, or activity from the same IP against other accounts? The alert alone is rarely the story.
4. Threat-intelligence lookup on IPs, domains, hashes and ASNs, weighted by source reliability.
5. **Hypothesis-driven investigation** — the agent runs the analyst's actual playbook: it forms a hypothesis (compromised credential vs. benign VPN), then queries specifically to confirm or refute it, rather than dumping every available log.
6. Verdict with confidence and reasoning: benign / suspicious / malicious, and the evidence chain that supports it.
7. **Containment within the pre-authorised envelope** for high-confidence malicious verdicts: revoke sessions, require re-authentication, isolate device, disable a malicious inbox rule. All are reversible actions, which is precisely why they are pre-authorised.
8. Case file generation for the Tier-2 analyst: timeline, evidence, actions taken, what remains unknown, and the recommended next step.
9. False-positive feedback loop into detection tuning — the agent reports which rules generate noise and why.
10. **Outcome:** the majority of alerts closed or contained automatically with a full evidence trail; humans see the alerts that need a human.

**Systems & tools** — Microsoft Sentinel, Defender XDR, Entra ID, threat intel feeds, EDR, SOAR playbooks, ticketing.

**Outcome** — MTTD/MTTR collapse for common alert classes; analysts move up the value chain.

**KPIs** — Mean time to triage; % alerts auto-closed with correct verdict; **false-negative rate (the guardrail that matters most)**; containment time; analyst hours reclaimed; detection-tuning changes shipped.

**Human gate** — Irreversible or business-disruptive containment (blocking a production service, disabling an executive account, network segmentation) requires human authorisation. Any suspected insider-threat case routes immediately to a human with restricted access.

---

### UC-X16 — Compliance Evidence Collection & Audit Preparation
**Archetype** A8 | **Autonomy** L2 | **Blast radius** B2 | **Value stream** Risk-to-assurance

**Pain** — Audit season means weeks of screenshot-gathering, ticket-exporting and evidence-chasing across teams. The same evidence is collected repeatedly for SOC 2, ISO 27001, PCI and customer security reviews, in slightly different formats.

**Trigger** — Audit cycle start, continuous control monitoring schedule, or an inbound customer security questionnaire.

**Workflow**
1. **Trigger:** SOC 2 Type II observation window opens.
2. Agent loads the control framework and the customer's control-to-evidence mapping, including the crosswalk to other frameworks (collect once, satisfy many).
3. Automated evidence collection: configuration state from Azure Policy/Defender for Cloud, access reviews from Entra, change tickets from the ITSM, deployment records from the CI/CD system, training completion from the LMS, vendor assessments, and policy attestations.
4. Evidence is captured with provenance and timestamps so it is defensible: what was collected, from which system, when, and by which identity.
5. **Control testing:** the agent tests operating effectiveness, not just existence — e.g. sampling change tickets to verify approval preceded deployment, and checking that access reviews were completed within the required window.
6. Gap identification with severity and a specific remediation owner and action — "13 of 47 privileged accounts lack MFA enforcement; owner: Platform Security; fix: conditional access policy CA-014."
7. Continuous monitoring between audits: controls that drift raise an alert when they drift, not eleven months later.
8. Auditor-request handling: agent maps each auditor request to already-collected evidence and produces the package.
9. **Outcome:** an evidence library that is always audit-ready, and gaps that surface while there is still time to fix them.

**Systems & tools** — Azure Policy, Defender for Cloud, Entra ID, Purview, ITSM, CI/CD, LMS, GRC platform (Vanta/Drata/ServiceNow GRC), document store.

**Outcome** — Audit preparation shifts from a project to a state; control drift becomes a monitored signal.

**KPIs** — Evidence auto-collected %; audit-prep hours; control failures found before the auditor; time to answer an auditor request; number of audit findings; multi-framework reuse ratio.

**Human gate** — Compliance officer approves all evidence packages before release to auditors. Control-effectiveness conclusions are human-signed.

---

### UC-X17 — Meeting Intelligence & Commitment Tracking
**Archetype** A3 | **Autonomy** L2 | **Blast radius** B2 | **Value stream** All

**Pain** — Decisions and commitments made in meetings evaporate. Notes are inconsistent, actions are unowned, and the same decision is re-litigated a month later because nobody can find what was agreed.

**Trigger** — Meeting ends (Teams), or a recording/transcript is uploaded.

**Workflow**
1. **Trigger:** Teams meeting concludes; transcript available.
2. Agent identifies participants and maps them to organisational identities and roles.
3. Structured extraction — and the structure is the point: **decisions** (what was decided, by whom, on what rationale), **commitments** (who owes what, by when), **risks/blockers raised**, **open questions**, and **information shared**.
4. Each commitment is validated: does it have an owner and a date? If not, the agent flags the ambiguity rather than fabricating specificity.
5. Cross-referencing with the project backlog: is this commitment already a ticket? Does it contradict a prior decision? Does it change a dependency someone else is relying on?
6. Action creation in the work-tracking system with owner, due date and a link back to the transcript moment that created it.
7. Distribution: a concise summary to attendees, and a targeted digest to non-attendees whose work is affected — the "you weren't there but this changes your plan" note that nobody ever writes.
8. Follow-through tracking: agent monitors commitment status and nudges owners before, not after, the due date.
9. Decision register maintenance so a searchable institutional memory accumulates.
10. **Outcome:** meetings produce durable, tracked, queryable outcomes.

**Systems & tools** — Teams (transcripts/Graph), Jira/Azure DevOps/Planner, SharePoint decision register, email.

**Outcome** — Commitments survive the meeting; institutional memory becomes searchable.

**KPIs** — Commitment capture rate vs. human baseline; on-time completion of captured actions; decision-register query volume; meeting follow-up time saved; re-litigated decisions (should fall).

**Human gate** — Chair approves the summary before wide distribution. Recording, transcription and processing require consent per jurisdiction — enforced at the platform layer, and works-council constraints must be configured per country.

---

### UC-X18 — Competitive & Market Intelligence
**Archetype** A3 | **Autonomy** L1 | **Blast radius** B1 | **Value stream** Idea-to-market

**Pain** — Competitive intelligence is a heroic, sporadic effort by one person. By the time a battlecard is updated it is wrong. Sales loses deals to positioning that changed three months ago.

**Trigger** — Continuous monitoring, a scheduled briefing cycle, or a specific request ("what changed at Competitor X this quarter?").

**Workflow**
1. **Trigger:** daily monitoring sweep, or an AE asks for a competitive brief before a call.
2. Agent monitors defined sources: competitor sites and changelogs, pricing pages, job postings (the best leading indicator of strategy), filings, patents, review sites, news, and — where permitted — closed-lost reasons from the CRM.
3. Change detection with **significance filtering**: a reworded headline is noise; a new pricing tier, a removed feature, or twelve open roles in a new geography is signal.
4. Interpretation: the agent connects the observation to a strategic hypothesis and states its confidence. A job posting for compliance engineers in Frankfurt plus a new EU data-residency page is a market-entry signal, and the agent says so as an inference, labelled as one.
5. Impact analysis against the customer's own positioning and open pipeline: which live deals does this affect?
6. Battlecard updating with objection handling and proof points drawn from the customer's own win/loss data.
7. Briefing generation, tiered by audience: an alert for the affected AE, a weekly digest for product, a quarterly landscape for the exec team.
8. Win/loss correlation: the agent tests whether the intelligence actually predicts outcomes, and reports where it doesn't.
9. **Outcome:** competitive positioning that updates continuously, with inference clearly separated from observation.

**Systems & tools** — Web monitoring, CRM (closed-lost), review platforms, filings/patent sources, product analytics, enablement platform.

**Outcome** — Sales and product act on current reality rather than last quarter's.

**KPIs** — Time from competitor event to briefed field; battlecard freshness; win rate in competitive deals; signal-to-noise ratio rated by consumers; % of intelligence items later validated.

**Human gate** — Product marketing approves battlecards before field release. **Strict source-legitimacy rules: public sources only; no misrepresentation, no scraping in breach of terms, no acquisition of confidential competitor information.** This is a hard platform-level constraint, not a prompt instruction.

---

### UC-X19 — Vendor Risk & Third-Party Due Diligence
**Archetype** A8 | **Autonomy** L2 | **Blast radius** B2 | **Value stream** Risk-to-assurance

**Pain** — Third-party risk assessments are questionnaire-driven, annual, and instantly stale. Nobody re-reads a SOC 2 report. Fourth-party concentration risk is invisible until an outage makes it obvious.

**Trigger** — New vendor onboarding request, annual reassessment, or a risk event (breach, outage, sanction, adverse media, ownership change).

**Workflow**
1. **Trigger:** business requests onboarding of a new SaaS vendor.
2. Agent classifies inherent risk from the intended use: data classification processed, system criticality, access model, regulatory scope, and spend.
3. **Tiering determines depth** — a low-risk vendor gets a light-touch check; a vendor processing regulated personal data at high criticality gets full diligence. Applying the same process to both is why vendor risk programmes collapse.
4. Evidence gathering: SOC 2 / ISO 27001 certificates (checked for validity, scope and *whether the customer's actual service is in scope* — routinely missed), pen-test summaries, DPAs, sub-processor lists, insurance, financial health, sanctions and adverse-media screening.
5. **Report analysis, not report collection:** the agent reads the SOC 2 and extracts the exceptions, the carve-outs, the CUECs (complementary user entity controls the customer must themselves perform), and the sub-service organisations. This is genuinely hard human work and it is almost never done properly.
6. Gap analysis against the customer's control requirements, producing specific findings with residual-risk ratings.
7. Contract-control alignment: does the contract actually contain the security, audit, notification and exit clauses the risk rating demands? Cross-references UC-X03.
8. Continuous monitoring post-onboarding: breach news, certificate expiry, sanctions changes, ownership changes, and outage history.
9. Concentration analysis across the vendor portfolio: how many critical vendors depend on the same cloud region, the same sub-processor, the same single point of failure?
10. **Outcome:** risk-tiered, evidence-based vendor decisions and a live rather than annual risk picture.

**Systems & tools** — GRC/TPRM platform, contract repository, procurement, sanctions/adverse-media data, security-ratings services, document intelligence.

**Outcome** — Faster onboarding for low-risk vendors, genuinely rigorous diligence for high-risk ones, and visible concentration risk.

**KPIs** — Assessment cycle time; % vendors with current evidence; findings identified per assessment; CUECs implemented; time to detect a vendor risk event; concentration exposure quantified.

**Human gate** — Risk acceptance is always a named human decision at the appropriate authority level. Onboarding a high-risk vendor requires CISO and DPO sign-off.

---

### UC-X20 — Internal Process Mining & Automation Scout
**Archetype** A6 | **Autonomy** L1 | **Blast radius** B1 | **Value stream** All

**Pain** — Organisations do not know where their process pain actually is. Automation roadmaps are built from opinion and politics, so automation lands where someone lobbied, not where value is. This is also the meta-problem for Habagat itself: **which agent should we build next for this customer?**

**Trigger** — Scheduled analysis cycle, a transformation programme kickoff, or a quarterly value review.

**Workflow**
1. **Trigger:** quarterly automation-opportunity review.
2. Agent ingests event logs from core systems — ERP, CRM, ITSM, workflow — with case IDs, activities, timestamps and resources.
3. Process discovery: reconstruct the actual as-is process graph, including the variants nobody documented. In most organisations the "standard process" accounts for under half of the cases.
4. Conformance checking against the documented process: where, how often and at what cost does reality diverge?
5. Bottleneck and rework analysis: waiting times, loops, handoffs, and the specific transitions where cases stall.
6. **Automation-opportunity scoring using the agent-fit test from Document 00** — volume, judgement content, tool-mediation, verifiability, blast radius — producing a ranked, quantified backlog rather than a wish list.
7. Business-case generation per opportunity: current cost, expected automation rate, implementation effort, payback period, and the risk class.
8. Post-deployment measurement: for agents already live, did the process actually improve? Measured on the same event logs, so the claim is falsifiable.
9. **Outcome:** an evidence-based, quantified automation roadmap — and, for Habagat, the highest-integrity expansion motion in the business, because it is the customer's own data making the case.

**Systems & tools** — Process-mining engine (Celonis/Power Automate Process Mining/custom on Fabric), ERP/CRM/ITSM event logs, data warehouse, BI.

**Outcome** — Automation investment aimed at real cost, with realised benefit measured on the same evidence base.

**KPIs** — Opportunities identified and quantified; % of roadmap sourced from evidence rather than opinion; realised vs. projected benefit; process-conformance improvement; cycle-time reduction on targeted processes.

**Human gate** — Roadmap prioritisation is a human governance decision. Employee-level performance inference is **prohibited by design** — analysis is at process and role level only, and works-council/employee-representation consultation is required in applicable jurisdictions.

---

## How Habagat sells this catalogue

| Motion | Agents | Why it works |
|---|---|---|
| **30-day Landing Pack** | X01, X17 | Low blast radius, immediate visible value, no system-of-record writes. Buys credibility. |
| **90-day Value Pack** | X02, X05, X10 | Hard ROI with unambiguous baselines. This is where the business case is proven. |
| **Finance Pack** | X02, X11, X12, X13 | One sponsor (CFO), one data domain, compounding value. Highest expansion rate. |
| **Trust Pack** | X15, X16, X19 | CISO sponsor; converts security from a blocker into a buyer. Strategically decisive. |
| **Growth Pack** | X06, X07, X18 | CRO sponsor; revenue-attributable, so it survives budget cuts. |

> The sequencing matters as much as the catalogue. **Land with the Landing Pack, prove with the Value Pack, expand with the functional packs.** Every pack shares connectors, identity plumbing and evaluation infrastructure with the last — which is why the third agent in an account costs Habagat roughly a third of what the first one did.
