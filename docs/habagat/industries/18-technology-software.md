# Document 18 — Technology & Software (ISVs, SaaS, IT Services)

> 13 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Technology companies are the **fastest to buy and the hardest to keep**: they adopt quickly, but they will build it themselves the moment the value is obvious and the moat is thin. Habagat should sell where the value is in the *operational integration and the evaluation corpus*, not in the model call.
- The best entry points are the unglamorous ones: **TECH-05 Customer Support Deflection**, **TECH-08 Security & Compliance Evidence**, **TECH-10 Revenue Operations**. Engineering-productivity agents are crowded and commoditising.
- This vertical is also Habagat's **best proving ground and best reference base**. A software company that runs Habagat agents internally is a credible reference for every other vertical.
- Be honest in positioning: for a tech buyer, the pitch is "we operate this at production quality inside your tenant with evaluation, governance and an SLA, so your engineers don't" — a capacity and reliability argument, not a capability one.

---

### TECH-01 — Engineering Productivity & Code Health
**A6 · L2 · B2 · Idea-to-market**
**Pain** — Engineering leaders lack a real picture of flow and quality; they manage by velocity points and gut feel, and the real constraints (review latency, flaky tests, environment instability) go unaddressed.
**Trigger** — Continuous repository and pipeline monitoring, or a review cycle.
**Workflow** — 1) Analyse delivery flow from source control, CI/CD and issue tracking: lead time, deployment frequency, change failure rate and restore time, decomposed by team and service. 2) **Identify the actual constraint** rather than reporting the metric: if lead time is dominated by review wait, no amount of coding-agent adoption will help. 3) Analyse code health: change coupling, hotspot files with high churn and high complexity, and test coverage where it matters rather than in aggregate. 4) Detect toil: flaky tests, repeated manual steps, long builds, and environment failures, quantified in engineer-hours. 5) Correlate with outcomes — incidents, defects, and delivery predictability — so improvement work is evidenced. 6) Recommend specific, sized interventions with expected effect. 7) Track improvement after the change. 8) **Report at team and system level only, never at individual level** — individual developer metrics are corrosive, easily gamed and destroy trust in the whole programme.
**Systems** — Git platforms, CI/CD, issue tracking, incident management, test infrastructure, observability.
**Outcome & KPIs** — DORA metrics; toil hours eliminated; constraint identified and relieved; predictability of delivery; engineer-reported friction.
**Human gate** — Engineering leadership prioritises; individual performance use is architecturally excluded and stated as policy.

### TECH-02 — Code Review & Change Risk Assessment
**A4 · L2 · B3 · Idea-to-market**
**Pain** — Review is a bottleneck and its quality is uneven; risky changes get the same attention as trivial ones; production incidents trace back to changes nobody examined carefully.
**Trigger** — Pull request opened or updated.
**Workflow** — 1) Analyse the change: what it touches, its blast radius, and which services and consumers depend on the modified code. 2) **Score change risk** from the code's incident history, complexity, test coverage, author familiarity with the area, and the size of the diff — then route high-risk changes to deeper human review and let low-risk ones move fast. Uniform review is the waste. 3) Review for correctness issues: error handling, concurrency, resource management, boundary conditions, and the failure modes specific to the language and framework. 4) Check for security issues: injection, authentication and authorisation gaps, secrets, unsafe deserialisation, and dependency vulnerabilities introduced. 5) Verify tests actually exercise the changed behaviour rather than merely existing. 6) Check consistency with the codebase's own conventions rather than generic style rules. 7) Identify missing operational concerns: metrics, logging, feature flags, migration safety, and rollback. 8) Present findings prioritised, with the reasoning, and **suppress low-value comments aggressively** — a review agent that produces noise is turned off within a week.
**Systems** — Git platform, CI, static analysis, dependency scanning, incident history, observability.
**Outcome & KPIs** — Review latency; defects caught pre-merge; **comment precision (accepted vs dismissed)**; change failure rate; high-risk changes correctly routed.
**Human gate** — Human engineers approve all merges; the agent comments and assesses, never approves.

### TECH-03 — Incident Response & Reliability Engineering
**A6 · L3 · B3 · Issue-to-resolution**
**Pain** — On-call engineers are paged into unfamiliar systems at 3am and spend the first twenty minutes assembling context. Post-incident reviews are inconsistent and their actions are rarely completed.
**Trigger** — Alert fires, error-rate anomaly, or an incident is declared.
**Workflow** — 1) Assemble the incident context immediately: what alerted, what changed recently (deploys, config, feature flags, infrastructure), what else is degraded, and what the customer impact is. **Recent change is the first hypothesis in the large majority of incidents.** 2) Correlate signals across services to distinguish cause from consequence, since a cascading failure produces alarms everywhere except at the origin. 3) Retrieve relevant runbooks and prior similar incidents with what actually resolved them. 4) Form and test diagnostic hypotheses by running read-only queries against logs, traces and metrics. 5) Execute pre-authorised, reversible mitigations where the diagnosis is confident: scale out, shed load, disable a feature flag, or roll back a specific deployment. 6) Maintain the incident timeline and communications, including customer-facing status updates within the SLA. 7) After resolution, draft the post-incident review with the timeline, contributing factors and evidence — **focused on systemic factors, never on individual blame**. 8) Track action completion and detect recurring contributing factors across incidents.
**Systems** — Observability (traces, logs, metrics), incident management, deployment systems, feature flags, status page, runbooks.
**Outcome & KPIs** — Time to detect and mitigate; context-assembly time saved; auto-mitigation success; repeat incidents from the same cause; post-incident action completion.
**Human gate** — Incident commanders own all decisions; irreversible or customer-affecting mitigations beyond the pre-authorised set require human authorisation.

### TECH-04 — Technical Documentation & Developer Experience
**A2 · L2 · B2 · Idea-to-market**
**Pain** — Documentation is written once and decays. Wrong documentation is worse than none: it generates support tickets, failed integrations and churn.
**Trigger** — Code or API change, documentation gap detected, or a release.
**Workflow** — 1) Detect divergence between documentation and reality by comparing docs against the actual API surface, configuration schema and behaviour. 2) **Prioritise by usage** — the wrong page on your most-used endpoint costs more than a whole undocumented subsystem nobody touches. 3) Generate and update reference documentation from source, and draft the conceptual and task-based content that source cannot produce. 4) Verify examples actually work by executing them against a real environment; broken examples are the most damaging documentation defect. 5) Identify gaps from real signals: support tickets, community questions, search queries with no result, and documented drop-off points in onboarding. 6) Support migration and deprecation documentation, which is where developer trust is won or lost. 7) Maintain changelogs and release notes with genuine breaking-change identification. 8) Measure whether documentation changes reduced the tickets they targeted.
**Systems** — Docs platform, source repositories, API specifications, support ticketing, analytics, community forums.
**Outcome & KPIs** — Documentation accuracy; support tickets attributable to docs gaps; time to first successful API call; example test pass rate; search success rate.
**Human gate** — Technical writers and engineers review before publication; deprecation communications are product decisions.

### TECH-05 — Customer Support & Technical Troubleshooting
**A1 · L3 · B3 · Issue-to-resolution**
**Pain** — Technical support requires reproducing issues, reading logs and understanding customer configuration. Support engineers are expensive, hard to hire, and spend most of their time on issues that have been solved before.
**Trigger** — Support ticket, community post, or an in-product help request.
**Workflow** — 1) Classify the issue and identify the customer's environment: version, configuration, deployment topology, integrations, and recent changes on their side. 2) Search prior resolved tickets, known issues, and engineering bug trackers — **the majority of tickets are recurrences**, and matching them accurately is the single largest lever. 3) Analyse provided diagnostics: logs, traces, configuration and error messages, identifying the actual failure rather than the symptom the customer reported. 4) Where information is missing, request precisely what is needed with instructions on how to obtain it, rather than a generic diagnostic-bundle request. 5) Provide the resolution with the specific steps for the customer's version and configuration. 6) Identify genuine product defects and file them with a complete reproduction, which is the highest-value handoff to engineering and the one most often done poorly. 7) Detect systemic patterns: many customers hitting the same issue is an incident, not a ticket queue. 8) Feed resolutions into documentation and the knowledge base.
**Systems** — Support platform, bug tracker, product telemetry, documentation, community platform, customer environment data.
**Outcome & KPIs** — Deflection and auto-resolution rate; time to resolution; escalation rate to engineering; defect reports accepted first time; CSAT; repeat contacts.
**Human gate** — Escalations, account-affecting actions, commitments about the roadmap, and any customer-impacting incident declaration.

### TECH-06 — Product Feedback & Roadmap Intelligence
**A3 · L1 · B2 · Idea-to-market**
**Pain** — Product feedback arrives across support, sales, community, reviews and research. Prioritisation defaults to whoever complained loudest or most recently.
**Trigger** — Feedback received, planning cycle, or a prioritisation decision.
**Workflow** — 1) Aggregate feedback from all sources with the customer, segment and revenue context attached. 2) **Resolve requests to underlying needs** rather than to stated solutions — twenty customers asking for an export button and one asking for an API may be the same need with different sophistication. 3) Quantify demand: how many customers, which segments, how much revenue, and how much churn risk is associated with each theme. 4) Correlate with product telemetry: is this a discoverability problem, a capability gap, or a workflow mismatch? The three have completely different responses. 5) Analyse competitive positioning where a gap is losing deals, using closed-lost data. 6) Assess effort and dependency in conversation with engineering inputs. 7) Present prioritisation evidence with the trade-offs explicit, without pretending the decision is arithmetic. 8) Close the loop with customers when their feedback ships — the step that generates the next round of good feedback.
**Systems** — Support and CRM, community platform, product analytics, roadmap tools, review platforms, research repository.
**Outcome & KPIs** — Feedback coverage; requests resolved to underlying need; prioritisation informed by evidence; feature adoption after release; customer loop closed.
**Human gate** — Product managers own all prioritisation and roadmap decisions.

### TECH-07 — Cloud Cost & Efficiency Management
**A6 · L3 · B3 · Record-to-report**
**Pain** — Cloud spend grows faster than usage; cost is spread across hundreds of resources and dozens of teams; nobody owns the total and finance cannot forecast it.
**Trigger** — Continuous cost monitoring, anomaly, or a budget cycle.
**Workflow** — 1) Attribute cost to teams, services, environments and — where the business needs it — to customers, which requires tagging discipline the agent should enforce and remediate. 2) Detect anomalies against expected patterns and **diagnose them**: a new deployment, a runaway job, a data-transfer pattern, a forgotten environment, or genuine growth. An unexplained cost alert is ignored; a diagnosed one is acted on. 3) Identify waste: idle and orphaned resources, over-provisioned instances, unattached storage, old snapshots, and non-production environments running out of hours. 4) Recommend commitment purchases (reservations, savings plans) with the utilisation risk quantified rather than assumed. 5) Analyse architectural cost drivers: data transfer patterns, storage tiering, and inefficient query or retry behaviour — where the large savings actually are. 6) Execute safe, reversible remediations automatically within policy: stopping non-production out of hours, deleting orphaned volumes after a hold period, and rightsizing with rollback. 7) Forecast spend with the drivers explicit. 8) Report unit economics: cost per customer, per transaction, per environment.
**Systems** — Cloud billing and usage APIs, tagging/resource inventory, monitoring, IaC repositories, FinOps tooling.
**Outcome & KPIs** — Cost per unit of business value; waste eliminated; anomaly detection and diagnosis time; commitment utilisation; forecast accuracy; tagging coverage.
**Human gate** — Production changes, commitment purchases, and anything affecting capacity or availability require owner approval.

### TECH-08 — Security Engineering & Vulnerability Management
**A6 · L2 · B3 · Risk-to-assurance**
**Pain** — Scanners generate thousands of findings; teams cannot triage them; genuinely exploitable issues are lost in noise; and remediation SLAs are missed at scale.
**Trigger** — Scan result, vulnerability disclosure, dependency alert, or a threat-intelligence signal.
**Workflow** — 1) Aggregate findings across code, dependency, container, infrastructure and cloud-posture scanning, deduplicated across tools. 2) **Assess genuine exploitability in context** — is the vulnerable code path reachable, is the component internet-facing, is there a compensating control, and is there a known exploit in the wild? Severity scores alone are close to useless for prioritisation. 3) Prioritise by real risk to this system, not by CVSS. 4) Determine remediation: patch, upgrade, configuration change, compensating control, or documented acceptance. 5) Where the fix is mechanical and well-tested (a dependency bump with passing tests), generate the change and open the pull request. 6) Route the rest to the owning team with the context, the exploit path and the deadline. 7) Track remediation against SLA and escalate ageing high-risk findings with the business exposure quantified. 8) On a new critical disclosure, determine exposure across the estate within hours — the capability that matters on the day it matters. 9) Report posture trends and systemic sources of vulnerability.
**Systems** — SAST/DAST/SCA tools, container and cloud posture scanning, asset inventory, ticketing, threat intelligence, CI/CD.
**Outcome & KPIs** — Mean time to remediate by severity; exploitable findings vs total findings; SLA compliance; time to assess exposure on a new disclosure; recurrence.
**Human gate** — Risk acceptance is a named human decision at the appropriate authority; production changes follow change management.

### TECH-09 — Compliance & Trust Programme Automation
**A8 · L2 · B3 · Risk-to-assurance**
**Pain** — SaaS companies must maintain SOC 2, ISO 27001 and often HIPAA, PCI or FedRAMP, plus answer hundreds of customer security questionnaires. It consumes a disproportionate share of a small security team.
**Trigger** — Continuous control monitoring, audit cycle, or a customer security review.
**Workflow** — 1) Map controls across frameworks so evidence collected once satisfies many — the crosswalk is the highest-leverage artefact in the programme. 2) Collect evidence automatically from the systems of record: access reviews, change approvals, deployment records, encryption configuration, backup verification, training completion, and vendor assessments. 3) **Test control operation continuously rather than at audit** — a control that drifted in March should be a March alert, not a November finding. 4) Detect and diagnose drift with the specific resource, owner and remediation. 5) Handle customer security questionnaires from the evidence base and the answer library, flagging any answer that would be a new claim requiring verification. 6) Maintain the trust centre and the artefacts customers self-serve, which deflects a large share of questionnaires entirely. 7) Support audits by mapping requests to existing evidence. 8) Assess new regulatory requirements against the current control set and identify the genuine delta.
**Systems** — Cloud platform APIs, identity, CI/CD, HR systems, GRC platform, questionnaire library, trust centre.
**Outcome & KPIs** — Evidence automation rate; control drift detection time; questionnaire turnaround; audit findings; security-review-related deal delay (the metric sales cares about).
**Human gate** — Compliance officers approve evidence packages and attestations; new claims require verification before being made to a customer.

### TECH-10 — Revenue Operations & Customer Lifecycle
**A6 · L2 · B3 · Order-to-cash**
**Pain** — Revenue data is fragmented across CRM, billing, product telemetry and support. Forecasts are unreliable; expansion opportunities and churn risks are identified late.
**Trigger** — Pipeline change, usage signal, renewal approach, or a forecast cycle.
**Workflow** — 1) Consolidate the customer picture: contract, billing, product usage, support history, engagement and stakeholder map. 2) **Assess account health from behaviour, not from sentiment** — usage depth and breadth, active users against licensed, feature adoption, and the presence or absence of the champion. 3) Detect expansion signals: capacity approaching limits, adoption of adjacent features, and new teams onboarding. 4) Detect churn risk early: usage decline, champion departure, support escalations, and integration removal. 5) Improve forecast quality by testing deal-stage claims against observable evidence rather than accepting the rep's judgement uncritically — the single biggest source of forecast error. 6) Support renewals with the value evidence: what the customer actually got, quantified. 7) Automate the operational hygiene: data quality, stage discipline, and required-field completion, which otherwise consumes selling time. 8) Analyse cohort retention, expansion and unit economics.
**Systems** — CRM, billing/subscription, product analytics, support, CS platform, data warehouse.
**Outcome & KPIs** — Forecast accuracy; net revenue retention; expansion identified and converted; churn predicted with useful lead time; CRM data quality; selling time recovered.
**Human gate** — Account strategy and commercial decisions are human; usage data used in customer conversations must respect contractual and privacy terms.

### TECH-11 — Partner, Marketplace & Ecosystem Operations
**A5 · L3 · B3 · Demand creation**
**Pain** — Partner programmes involve onboarding, certification, deal registration, co-selling and revenue sharing across many partners; operations are manual and partners experience friction that suppresses the channel.
**Trigger** — Partner application, deal registration, marketplace transaction, or a certification event.
**Workflow** — 1) Process partner onboarding: verification, agreement execution, tier assignment and enablement provisioning. 2) Manage certification and competency tracking with renewal management. 3) Handle deal registration: validate, check for conflict with direct pipeline and other partners, and approve or route within the policy — **conflict resolution speed determines partner trust more than commission rates do**. 4) Support co-selling with the account context and the joint value proposition. 5) Manage marketplace listings, transactions and metering across cloud marketplaces, reconciling billing. 6) Compute partner compensation accurately against the programme rules, which is where partner disputes concentrate. 7) Monitor partner performance and health, and identify partners worth investment and partners who have gone dormant. 8) Provide partners with self-service answers on programme, product and deal status.
**Systems** — PRM, CRM, marketplace platforms, billing, LMS/certification, contract management.
**Outcome & KPIs** — Partner onboarding time; deal-registration turnaround; partner-sourced revenue; compensation accuracy and disputes; active partner ratio; marketplace transaction success.
**Human gate** — Partner agreements, tier exceptions and channel-conflict escalations are commercial decisions.

### TECH-12 — Data Platform Operations & Quality
**A6 · L3 · B3 · Plan-to-produce**
**Pain** — Data pipelines break silently; downstream consumers discover the problem in a dashboard or, worse, in a decision. Data engineers spend their time firefighting rather than building.
**Trigger** — Pipeline execution, data quality check, schema change, or a consumer report.
**Workflow** — 1) Monitor pipeline health: freshness, volume, schema conformance, and distribution characteristics of the data itself, not just job success. **A job that succeeds while producing wrong data is the dangerous case.** 2) Detect anomalies against learned baselines: volume drops, null-rate spikes, cardinality shifts, and distribution changes. 3) Diagnose the cause by tracing upstream through lineage to the originating change — an upstream schema change, a source-system issue, or a genuine business change. 4) Assess downstream impact through lineage: which tables, dashboards, models and decisions consume this, and who owns them. 5) Notify affected consumers proactively with the impact and the expected resolution, rather than letting them find it. 6) Auto-remediate within policy: retry, backfill, or quarantine bad partitions. 7) Manage schema evolution with contract enforcement so breaking changes are caught before they ship. 8) Report data-quality trends and the pipelines that consume the most operational effort.
**Systems** — Orchestration (Airflow/ADF/Fabric), data warehouse/lakehouse, lineage and catalogue, quality frameworks, alerting, BI tools.
**Outcome & KPIs** — Data incidents and their duration; freshness SLA attainment; consumers notified before they notice; time to root cause; engineer time on firefighting.
**Human gate** — Schema-breaking changes and backfills affecting reported figures require owner approval.

### TECH-13 — IT Service Delivery for Managed Service Providers
**A5 · L3 · B3 · Issue-to-resolution**
**Pain** — MSPs deliver support across many clients with different environments, tooling and contracts. Engineer context-switching is constant and margins depend on ticket efficiency.
**Trigger** — Ticket raised, monitoring alert, or a scheduled maintenance task.
**Workflow** — 1) Identify the client, their environment, their contract entitlements and their documented specifics — **client-specific context is the whole problem in MSP work**, and it lives in engineers' heads. 2) Classify and prioritise against the client's SLA and the business impact. 3) Diagnose using monitoring data, prior tickets for this client, and the documented environment. 4) Resolve within the automation envelope: standard requests, known fixes, and routine maintenance, executed per the client's change requirements. 5) Route anything else to an engineer with the diagnosis and the client context assembled. 6) Track SLA compliance and escalate at risk, not at breach. 7) Identify recurring issues per client and convert them into proactive projects — the transition from break-fix to advisory that determines MSP margin and retention. 8) Support client reporting with service performance, and generate the account review with evidence.
**Systems** — PSA/RMM tooling, monitoring, client documentation systems, ticketing, automation platforms.
**Outcome & KPIs** — Tickets per engineer; auto-resolution rate; SLA compliance; recurring issues eliminated; margin per client; client retention.
**Human gate** — Client change-management requirements govern all changes; contractual and commercial matters are human.

---
## Notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **Build-vs-buy pressure** | Tech buyers can build the naive version. Habagat's defensible value is the operated system: evaluation corpus, governance, integration depth, and SLA — sell that, not the model. |
| **Developer trust** | Noisy or low-precision agent output is uninstalled quickly. Precision thresholds should be higher here than in any other vertical. |
| **Individual metrics** | Agents must never produce individual developer performance measurement. This is both an ethical and an adoption issue. |
| **Customer data in support** | Support agents touch customer production data and logs. Access must be scoped, logged, and consistent with the customer's own contractual commitments. |
| **Open-source licence compliance** | Any agent proposing dependency changes must check licence compatibility, which is a legal exposure most teams handle informally. |
