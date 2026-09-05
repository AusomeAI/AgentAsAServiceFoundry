# Document 16 — Media, Entertainment & Publishing

> 12 agent use cases. Notation per [Document 00](../00-research-method-and-taxonomy.md).

## Executive take
- Media is the industry where generative AI is simultaneously the biggest opportunity and the biggest threat. Habagat should sell into the **operational and rights side**, not the creative side — that is where the unambiguous value is and where the cultural resistance is lowest.
- **MED-04 Rights & Licensing Management** is the most defensible agent here. Rights data is fragmented, high-value, and getting it wrong means either unexploited assets or litigation.
- **MED-02 Archive & Metadata Enrichment** unlocks assets that are already owned and currently unmonetisable because nobody can find them. It is the highest ROI-per-effort agent in the vertical.
- Provenance and disclosure are becoming regulatory requirements (EU AI Act transparency obligations, C2PA adoption). Habagat should ship **provenance metadata by default** on any generated asset — a differentiator today, table stakes in eighteen months.

---

### MED-01 — Content Production Workflow Orchestration
**A5 · L3 · B2 · Plan-to-produce**
**Pain** — Production involves many specialists, assets, versions and deadlines. Coordination is done in spreadsheets and messaging, and the failure mode is a missed delivery or a wrong version published.
**Trigger** — Production commissioned, milestone reached, or an asset delivered.
**Workflow** — 1) Build the production plan from the commission: deliverables, versions, formats, territories, deadlines and dependencies. 2) Track asset status through the pipeline: ingest, edit, review, approval, localisation, quality control, and delivery. 3) **Manage version integrity** — knowing which version is approved for which territory and platform is where publishing errors originate, and they are expensive and public. 4) Chase the specific blocker rather than sending a general status request; production delays are usually one missing approval or one missing asset. 5) Manage the review and approval cycle with feedback consolidated across reviewers and conflicts surfaced rather than averaged. 6) Verify technical compliance against each platform's delivery specification before delivery, not after rejection. 7) Track rights and clearance status as a gating condition on publication. 8) Report schedule and budget position with an honest forecast.
**Systems** — Production management, MAM/DAM, editing and post systems, review platforms, delivery systems, rights systems.
**Outcome & KPIs** — On-time delivery; delivery rejections; version errors published (target zero); approval cycle time; production cost vs budget.
**Human gate** — Editorial and creative approvals; publication decisions; rights clearance sign-off.

### MED-02 — Archive, Metadata Enrichment & Discovery
**A2 · L3 · B2 · Idea-to-market**
**Pain** — Broadcasters and publishers hold vast archives with minimal metadata. Content that cannot be found cannot be licensed, reused or monetised, so the asset is dead on the balance sheet.
**Trigger** — Asset ingested, archive enrichment programme, or a search request.
**Workflow** — 1) Analyse the asset: speech transcription with speaker separation, on-screen text, object and scene recognition, music identification, and shot segmentation. 2) Generate rich descriptive metadata: topics, entities (people, places, organisations), events, and content characteristics. 3) **Link entities to authority records** so a search for a person finds them across decades of differently-spelled credits — the step that makes an archive genuinely searchable. 4) Capture editorial context: programme, date, contributors, and provenance. 5) Flag content requiring sensitivity handling: distressing material, content requiring warnings, and material whose historical framing is now problematic. 6) Identify rights-bearing elements: music, third-party footage, contributor appearances — which determines whether the asset can be reused at all. 7) Assess reuse and licensing potential and surface high-value archive material proactively against current news and anniversaries. 8) Support search with semantic retrieval over the enriched index.
**Systems** — MAM, speech and vision analysis services, authority databases, rights systems, search index.
**Outcome & KPIs** — Archive coverage with rich metadata; search success rate; archive reuse and licensing revenue; time to find material; rights-status coverage.
**Human gate** — Archivists validate sensitive content classification and historical context; rights conclusions are verified before exploitation.

### MED-03 — Editorial Research & Fact Verification
**A3 · L1 · B4 · Idea-to-market**
**Pain** — Journalists work under deadline pressure with growing verification demands. Errors damage credibility permanently, and synthetic media makes verification harder.
**Trigger** — Story in development, or a verification request.
**Workflow** — 1) Assemble background: prior coverage, primary documents, public records, and relevant data. 2) Identify and locate primary sources rather than relying on secondary reporting — the discipline that prevents error cascades, where an original mistake is amplified by citation. 3) **Verify specific factual claims** against sources, reporting exactly what each source supports and what it does not. 4) Assess source reliability and flag claims that trace back to a single unverified origin. 5) Check content provenance signals for images and video, and flag material requiring specialist verification. 6) Identify the questions the story does not yet answer and the people who should be given a right of reply. 7) Flag legal risk for editorial-legal review: defamation exposure, privacy, contempt, and reporting restrictions. 8) Maintain the verification record, which matters both for editorial standards and for defending the piece afterwards.
**Systems** — Archive and cuttings, public records, data sources, verification tools, editorial CMS.
**Outcome & KPIs** — Research turnaround; corrections issued; verification record completeness; legal complaints; primary-source rate.
**Human gate** — **Journalists and editors own all editorial judgement and publication decisions.** The agent never publishes and never determines what is true; it verifies against sources and reports what it found.

### MED-04 — Rights, Licensing & Royalty Management
**A2 · L2 · B4 · Order-to-cash**
**Pain** — Rights data is fragmented across contracts, territories, terms and windows. Rights are under-exploited because nobody knows what is available, and over-exploited into litigation because nobody checked.
**Trigger** — Contract executed, exploitation opportunity, licence request, or a royalty cycle.
**Workflow** — 1) Extract rights terms from agreements: rights granted, territories, languages, media, exclusivity, term, windows, holdbacks and restrictions. 2) Build the structured rights position per asset, **reconciling the chain of title including underlying rights** — music, footage, contributor consents, and format rights. A gap anywhere in the chain blocks exploitation. 3) On an exploitation request, determine availability definitively: is this right available, in this territory, in this window, on this platform, and what is the residual or royalty consequence? 4) Identify unexploited rights and surface them as revenue opportunities. 5) Detect and flag conflicts: overlapping exclusive grants, expired rights still in use, and holdback breaches. 6) Manage licensing: quotes, terms, deal memos, and tracking. 7) Compute royalties and residuals per the applicable agreements and collective bargaining terms, which are among the most complex calculation rules in any industry. 8) Manage rights expiry and renewal with lead time.
**Systems** — Rights management, contract repository, MAM, royalty systems, collecting-society interfaces, sales systems.
**Outcome & KPIs** — Rights coverage in structured form; availability query turnaround; unexploited rights monetised; rights conflicts detected; royalty accuracy and dispute rate.
**Human gate** — **Rights conclusions are verified by rights specialists or legal counsel before exploitation.** Chain-of-title gaps are legal matters.

### MED-05 — Audience Analytics & Content Performance
**A6 · L1 · B2 · Demand creation**
**Pain** — Audience data is abundant but insight is thin: teams know what performed, not why, and commissioning decisions are made on instinct dressed as data.
**Trigger** — Performance reporting cycle, content release, or a commissioning decision.
**Workflow** — 1) Consolidate performance across platforms with consistent, comparable metrics — cross-platform comparability is the first and hardest problem. 2) Analyse performance against expectation given the slot, promotion, competition and seasonality, rather than against a raw benchmark. 3) Decompose the audience: acquisition, retention, and completion, and identify **where in the content the audience leaves**, which is the most actionable signal available and is routinely unused. 4) Correlate performance with content attributes to identify what actually drives outcomes for this audience, distinguishing correlation from a plausible causal story and labelling which is which. 5) Analyse audience segments and their differing responses. 6) Identify content with unrealised potential — good retention, poor discovery — which is a marketing problem, not a content problem. 7) Support commissioning with evidence on gaps, saturation and audience need. 8) Report honestly where the data cannot answer the question.
**Systems** — Analytics platforms, streaming and broadcast measurement, CRM, content metadata, social data.
**Outcome & KPIs** — Reporting turnaround; commissioning decisions informed by evidence; content performance vs prediction; audience retention improvement; discovery improvements.
**Human gate** — Commissioning and editorial decisions are human; audience data use complies with privacy and consent.

### MED-06 — Advertising Sales, Inventory & Yield
**A6 · L2 · B3 · Order-to-cash**
**Pain** — Advertising inventory is perishable and sold across direct, programmatic and sponsorship channels with complex targeting and delivery guarantees. Under-delivery means make-goods; over-delivery means wasted inventory.
**Trigger** — Campaign booking, delivery monitoring, or an inventory forecast cycle.
**Workflow** — 1) Forecast inventory availability by audience segment, platform and time, accounting for delivery uncertainty. 2) Assess whether a proposed campaign can be delivered against its targeting and guarantees, and identify the conflict when it cannot — accepting undeliverable bookings is the root of make-good costs. 3) Optimise allocation across direct and programmatic demand to maximise yield without breaching commitments. 4) Monitor delivery in flight and detect under-delivery early enough to correct it, rather than at campaign end when only a make-good is possible. 5) Recommend corrective action: re-weighting, added inventory, or a proactive client conversation. 6) Verify brand-safety and suitability compliance for placements — an adjacency failure is a client-losing event. 7) Support post-campaign reporting with delivery, performance and verification data. 8) Analyse yield by channel, advertiser and inventory type.
**Systems** — Ad server, SSP/DSP integrations, sales/CRM, audience measurement, brand-safety verification, billing.
**Outcome & KPIs** — Fill rate and yield; under-delivery and make-good cost; forecast accuracy; brand-safety incidents (target zero); revenue per thousand impressions.
**Human gate** — Commercial terms and client relationships; brand-safety escalations; any advertiser or content suitability judgement.

### MED-07 — Content Moderation & Trust and Safety
**A1 · L2 · B4 · Risk-to-assurance**
**Pain** — Platforms must review vast volumes of user content against complex, contested policies at speed, under regulatory obligation, while protecting moderators from psychological harm.
**Trigger** — Content posted, user report, or a proactive detection signal.
**Workflow** — 1) Classify content against the policy taxonomy with confidence, handling text, image, video and audio. 2) Apply the enforcement rules with **the policy's actual definitions and exceptions** — newsworthiness, education, documentation of abuse, satire — since these exceptions are where automated moderation causes the most harm. 3) Prioritise the human review queue by severity and confidence, routing the highest-harm content fastest. 4) **Reduce moderator exposure** by pre-classifying, blurring and summarising the most harmful material, which is a genuine welfare improvement and a real product benefit. 5) Take automated action only within the confident, low-harm-if-wrong envelope; everything contested goes to a human. 6) Generate the user notification with the specific policy basis and the appeal route, since arbitrary-seeming enforcement is the main driver of user grievance and regulatory criticism. 7) Handle appeals with fresh review, not a re-run of the same decision. 8) Report transparency metrics and support regulatory obligations. 9) Detect coordinated inauthentic behaviour at network level.
**Systems** — Moderation platform, classification services, user and content databases, appeals workflow, transparency reporting.
**Outcome & KPIs** — Review latency by severity; accuracy against human-audited samples; **appeal overturn rate (the key quality signal)**; moderator exposure reduction; regulatory compliance; enforcement consistency.
**Human gate** — **All contested, high-harm and account-level enforcement is human.** Legal removal requests follow formal process. Appeals are human-reviewed. Moderator welfare is a design requirement, not a side effect.

### MED-08 — Localisation, Subtitling & Accessibility
**A2 · L2 · B3 · Plan-to-produce**
**Pain** — Content must be localised and made accessible across many languages and markets, with regulatory accessibility quotas in several jurisdictions. Manual subtitling and dubbing is slow and expensive.
**Trigger** — Content ready for localisation, or an accessibility requirement.
**Workflow** — 1) Generate the transcript with speaker identification and timing. 2) Produce subtitles conforming to the platform's standards: reading speed, line length, positioning, and shot-change alignment — conformance is what makes subtitles usable rather than merely present. 3) Generate audio description scripts for visually impaired audiences, describing what matters narratively within the available gaps. 4) Translate for target markets with attention to **cultural adaptation rather than literal translation**: idiom, humour, references, and sensitivity, flagging content that does not transfer. 5) Flag regulatory and cultural compliance issues per market: content restrictions, classification implications, and material requiring editorial decision. 6) Support dubbing workflows with adapted scripts timed to lip movement. 7) Route to human linguists for review at a depth proportionate to the content's prominence and risk. 8) Verify accessibility compliance against quota obligations and report.
**Systems** — Localisation management, subtitling tools, translation memory, MAM, compliance systems.
**Outcome & KPIs** — Localisation cycle time and cost; linguist review effort; accessibility coverage against quotas; quality scores; market compliance issues.
**Human gate** — **Qualified linguists review all published localisation**; cultural sensitivity and editorial adaptation decisions are human.

### MED-09 — Publishing Editorial & Production
**A5 · L2 · B2 · Idea-to-market**
**Pain** — Book and journal publishing involves long workflows across acquisition, editing, production and distribution, with metadata errors directly suppressing discoverability and sales.
**Trigger** — Manuscript submitted, production milestone, or a publication cycle.
**Workflow** — 1) Support acquisition assessment: market comparables, category performance, and audience fit — as evidence for the editor, never as a substitute for editorial judgement. 2) Manage the production workflow: editing stages, design, typesetting, proofing and print/digital output, with dependencies tracked. 3) Perform consistency checks: style guide, terminology, cross-references, citations, figures and permissions — the mechanical checks that consume copyediting time. 4) **Verify permissions and rights clearance for third-party material** before publication, which is a common and expensive failure. 5) Generate and validate metadata: ONIX records, subject classification, keywords, and descriptions — metadata quality is a direct and measurable driver of discoverability and sales. 6) Support distribution setup across channels and formats with specification compliance. 7) For journals, manage peer review: reviewer matching, conflict checking, and process tracking. 8) Monitor post-publication performance and support marketing.
**Systems** — Editorial and production management, typesetting, metadata/ONIX systems, distribution platforms, peer-review systems.
**Outcome & KPIs** — Time to publication; production cost per title; metadata completeness and quality; permissions failures (target zero); discoverability and sales; peer-review cycle time.
**Human gate** — Editorial and acquisition decisions; peer-review outcomes; all content changes.

### MED-10 — Music & Talent Rights Administration
**A6 · L3 · B3 · Record-to-report**
**Pain** — Music and talent payments involve complex splits, collecting societies, residuals and territory rules. Underpayment causes disputes; unclaimed royalties sit unallocated across the industry.
**Trigger** — Usage reported, royalty cycle, or a claim received.
**Workflow** — 1) Identify works and recordings used, matching against authoritative identifiers (ISWC, ISRC) and resolving the ambiguity that arises from inconsistent metadata. 2) Determine the rights holders and their splits from the registration data and the agreements. 3) **Detect unmatched and unclaimed usage** and investigate it, since unmatched usage is where money goes missing at industry scale. 4) Compute payments per the applicable rates: statutory rates, collective agreements, contract terms, and territory-specific rules. 5) Handle residuals and repeat-use payments under the relevant collective bargaining agreements, which have intricate rules and hard deadlines. 6) Reconcile against collecting-society statements and identify discrepancies. 7) Process claims and disputes with the evidence assembled. 8) Report to rights holders with the transparency they are increasingly entitled to demand.
**Systems** — Royalty systems, rights databases, collecting-society interfaces, usage reporting, contract repository.
**Outcome & KPIs** — Match rate on usage; unclaimed royalty reduction; payment accuracy; dispute rate and resolution time; statement clarity.
**Human gate** — Disputed splits and contract interpretation are legal matters; payment release follows finance controls.

### MED-11 — Marketing, Promotion & Social Distribution
**A3 · L2 · B3 · Demand creation**
**Pain** — Promoting content requires assets across many formats, platforms and audiences at a volume that outstrips creative capacity, and timing is critical to a launch.
**Trigger** — Content release approaching, campaign launch, or a performance signal.
**Workflow** — 1) Plan the campaign against the content, audience and platform mix. 2) Generate promotional variants from approved assets: clips, stills, copy and formats per platform, respecting each platform's specification. 3) **Ensure every promotional claim and every clip is rights-cleared for promotional use** — promotional rights are frequently narrower than exploitation rights, and this is a routine and avoidable breach. 4) Personalise messaging by audience segment while maintaining a coherent campaign identity. 5) Schedule and publish across channels with timing optimised per platform and territory. 6) Monitor performance and reallocate spend within the authorised envelope. 7) Monitor audience response and detect reputational risk early, including reaction the campaign did not intend. 8) Report performance with attribution to the extent the data honestly supports it.
**Systems** — Social management, DAM, ad platforms, analytics, rights systems, CMS.
**Outcome & KPIs** — Assets produced per campaign; time to launch; engagement and conversion; rights compliance (100% required); spend efficiency; sentiment.
**Human gate** — Brand and editorial approval before publication; rights clearance verified; any reputational escalation.

### MED-12 — Subscription, Churn & Lifecycle Management
**A7 · L2 · B3 · Order-to-cash**
**Pain** — Subscription media businesses live or die on churn. Cancellations are handled with blunt retention offers; the reasons are recorded in useless categories; and win-back is untargeted.
**Trigger** — Churn-risk signal, cancellation attempt, billing failure, or a lifecycle milestone.
**Workflow** — 1) Monitor engagement: consumption frequency, depth, breadth and trajectory, detecting decline against the subscriber's own pattern. 2) Diagnose the likely cause: content fit, price, competing service, technical experience, or a change in life circumstances. 3) Intervene proportionately and appropriately — a content recommendation for a content problem, a plan change for a price problem, and a technical fix for a technical problem. A discount for a content problem is wasted money. 4) **Handle involuntary churn**, which is a large share of total churn and is almost entirely recoverable: failed payments, expired cards, and retry strategy optimised against issuer behaviour. 5) At cancellation, offer a genuine alternative (pause, downgrade, plan change) rather than friction — and comply with click-to-cancel regulation, which now prohibits obstruction in several jurisdictions. 6) Capture the real cancellation reason in a form that supports action. 7) Manage win-back with targeting based on why they left and what has changed since. 8) Measure incrementality against holdouts.
**Systems** — Subscription management, billing and payments, streaming analytics, CRM, campaign tools.
**Outcome & KPIs** — Voluntary and involuntary churn; payment recovery rate; retention offer incrementality; win-back conversion; lifetime value; cancellation friction complaints (guardrail).
**Human gate** — Offer policy is commercial; **cancellation must never be obstructed** — this is a hard platform-level rule given active regulatory enforcement.

---
## Regulatory & ethical notes for this vertical
| Topic | Impact on agent design |
|---|---|
| **AI transparency & provenance** | Generated or substantially AI-modified content should carry provenance metadata (C2PA) by default. EU AI Act transparency obligations apply to synthetic content and deepfakes. |
| **Rights & chain of title** | Automated exploitation without verified rights is a litigation event. Rights conclusions require human verification before use. |
| **Editorial independence** | Agents support journalism; they never make editorial judgements or determine truth. Corrections and right-of-reply processes remain human. |
| **Platform regulation (DSA, Online Safety Act)** | Content moderation carries statutory obligations on notice, appeal, transparency reporting and risk assessment. Enforcement decisions must be explainable to the user and to a regulator. |
| **Performer and creator rights** | Voice, likeness and performance rights require explicit consent for synthetic use. Collective agreements increasingly govern this; Habagat should refuse deployments that lack documented consent. |
| **Accessibility quotas** | Subtitling and audio description obligations are quantitative and reportable in several jurisdictions. |
