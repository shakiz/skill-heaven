# Claude Skills for Marketing, Business & HR: Pain-Point Analysis

*As of 2026-11-08 · Scope: marketing, business (sales, finance, ops, strategy, leadership), HR and people ops*

---

## 1. Executive summary

**The main pain point is not a shortage of content. It is the cost of making knowledge work consistent, correct and on-brand every time.**

Across marketing, business and HR, people spend most of their time on recurring, document-heavy work. Each piece has to follow rules that live in someone's head, an old deck or a 40-page PDF. Generic AI chat doesn't fix this. Every user re-explains the context, the output changes from person to person, and nobody can trust that the policy, brand voice or legal guardrail was applied.

**Claude Skills fit this gap well.** A skill packages three things:

1. **Institutional knowledge:** brand voice, policies, pricing rules, rubrics, templates and examples.
2. **A repeatable procedure:** the steps an expert follows, including the checks.
3. **Executable helpers:** scripts, calculators, validators and file generators (docx, xlsx, pptx).

Claude loads a skill only when a task calls for it. As a result, *any* employee can produce the work the way the company's best person would, without writing prompts.

### What we're trying to solve, in one line each

| # | Root problem | What a skill does about it |
|---|---|---|
| 1 | **Tribal knowledge.** Rules and know-how sit with a few experts. | Encodes the expert's playbook and makes it available to everyone. |
| 2 | **Inconsistency.** Ten people produce ten versions of the same thing. | Templates, rubrics and validators make outputs uniform. |
| 3 | **Compliance and brand risk.** Legal, regulatory, bias and claim errors slip through. | Built-in checklists and review passes flag issues before they ship. |
| 4 | **Repetitive document assembly.** Proposals, reports, JDs, briefs and decks get rebuilt from scratch. | Generates the first draft in the right format from structured inputs. |
| 5 | **Synthesis overload.** Too many interviews, surveys, calls and reviews to read. | Structured analysis with a fixed taxonomy produces comparable insights. |
| 6 | **Slow turnaround and bottlenecks.** Work waits in the queue of a reviewer or specialist. | Self-serve first pass. Experts review instead of authoring. |

### Top recommended skills to build first

1. **Brand Voice & Content Guardian** (Marketing). Writes and reviews any copy against brand, tone, terminology and claim rules.
2. **Proposal / RFP Response Builder** (Business/Sales). Assembles tailored proposals from an approved answer library and pricing rules.
3. **Inclusive Job Description & Hiring Kit Generator** (HR). Produces a JD, scorecard, interview questions and a bias check from the role inputs.
4. **Voice-of-Customer / Feedback Synthesizer** (cross-functional). Turns reviews, surveys, tickets, interviews and exit surveys into themed, quantified insight reports.
5. **Policy & Handbook Q&A + Drafting Assistant** (HR/Ops). Answers employee questions from the actual handbook, and drafts or updates policies against a compliance checklist.
6. **Executive Report & Board Deck Builder** (Business). Turns raw KPI exports into a narrative report or deck in the house format.

---

## 1a. Ranking by business value

The catalog in section 8 balances impact against effort. This ranking ignores effort and asks one question: **which skills create the most value?** Value is weighed in this order:

1. **Revenue won.** Effect on winning or keeping business.
2. **Risk avoided.** Legal, compliance, reputational and people risk.
3. **Hours saved.** Weighted by how senior and expensive those hours are.

| Rank | Skill | Main value driver | Why it ranks here |
|---|---|---|---|
| **1** | **B1 Proposal / RFP Response Builder** | **Revenue** | The only skill tied directly to winning deals. Faster, sharper, consistent responses mean more bids and a higher win rate, and senior staff stop spending days per proposal. |
| 2 | B3 Contract First-Pass Reviewer | Risk + deal speed | One missed liability or IP clause can cost more than a year of time savings. Clears the legal queue that delays signatures. |
| 3 | B4 Executive Report & Board Deck Builder | Decision quality | Gives leadership the "so what" behind the numbers every month and frees the most expensive time in the company. |
| 4 | X1 Feedback Synthesizer (customer, employee, exit) | Retention | Shows early why clients are unhappy and why people leave. One engine serves marketing, CS and HR. |
| 5 | H3 Policy & Handbook Assistant | Hours + compliance | Answers recurring HR questions with citations all year and keeps policies consistent. |
| 6 | B2 Sales Call Prep & Deal Review | Revenue | Better discovery and earlier deal-risk detection. Value depends on the sales team's size. |
| 7 | M7 Claims & Compliance Checker | Risk | High value in regulated industries, lower elsewhere. |
| 8 | H1 Inclusive JD & Hiring Kit | Hiring quality | Better hires and a fairer process. Each mis-hire is expensive. |
| 9 | H5 Performance Review Coach & Bias Checker | People risk + quality | Fairer reviews, less calibration effort, less legal exposure. |
| 10 | M1 Brand Voice & Content Guardian | Brand + hours | Wide usage and easy to build, but each use is worth less. A good first pilot, not the top value. |

**Decision:** build **B1 Proposal / RFP Response Builder** first. Its build lives in `skills/rfp-response-builder/`.

---

## 2. Lens: when is a skill the right tool?

A skill is not always the answer. Use this test before building one.

| Signal | Good skill candidate | Better solved by something else |
|---|---|---|
| Frequency | Weekly or more, across many people | One-off. A prompt is enough. |
| Know-how | Needs company-specific rules, examples or rubrics | Generic knowledge Claude already has |
| Output form | Structured document, file or checklist with a known shape | Open-ended brainstorming |
| Correctness | Has verifiable rules (format, policy, math, claims) | Purely subjective taste |
| Data access | Works on documents or files the user provides | Needs live system writes. Pair with an MCP connector. |
| Determinism | Parts can be scripted (calculations, validation, file building) | Requires real-time transactional systems |

**Rule of thumb:** *Skill = know-how + procedure + tools. Connector (MCP) = access to data and systems.* The highest-value designs combine both. For example, a skill holds the hiring rubric and a connector pulls candidates from the ATS.

### Anatomy of a strong business skill

```
skill-name/
├── SKILL.md              # when to trigger, step-by-step procedure, quality bar
├── reference/            # brand guide, policy text, rubrics, glossaries, approved claims
├── templates/            # docx/pptx/xlsx/md templates in house format
├── examples/             # 3–5 gold-standard outputs (good & bad, annotated)
└── scripts/              # validators, calculators, file generators, linters
```

---

## 3. Cross-functional root pain points

These problems repeat in all three domains. They are the strongest argument for a **shared skill library** rather than one-off tools per team.

### 3.1 Knowledge lives in people, not systems
- Brand rules, pricing exceptions, hiring bars and policy interpretations are passed on verbally.
- New hires take months to produce "house-standard" work.
- **Skill opportunity:** encode the playbooks. Every skill doubles as onboarding.

### 3.2 First drafts are expensive, reviews are the bottleneck
- Senior people spend their time rewriting juniors' drafts rather than reviewing them.
- **Skill opportunity:** a "draft to house standard" plus a "self-review against rubric" step. Reviewers then see better inputs.

### 3.3 Unstructured input overload
- Call recordings, survey verbatims, reviews, tickets, interview notes, exit interviews and performance comments.
- Insight is lost because nobody has time to read it all, or each analyst codes it differently.
- **Skill opportunity:** a fixed taxonomy, a coding procedure and output templates give comparable insights across quarters.

### 3.4 Compliance, legal and reputational risk
- Marketing: unsubstantiated claims, regulated-industry wording, missing disclosures, trademark misuse.
- HR: biased language, inconsistent discipline documentation, jurisdiction-specific labor rules, privacy (PII).
- Business: contract terms, pricing approvals, financial reporting accuracy.
- **Skill opportunity:** checklists and validators as a mandatory step, with clear "escalate to human" rules.

### 3.5 Format and tool friction
- The same content has to become an email, a slide, a one-pager, a LinkedIn post and a report.
- **Skill opportunity:** skills that output native docx/pptx/xlsx in house templates, plus multi-channel repurposing.

### 3.6 Metrics without narrative
- Dashboards exist, but turning numbers into a "so what" for leadership is manual.
- **Skill opportunity:** KPI to narrative skills with variance explanations and recommended actions.

---

## 4. Marketing

### 4.1 Pain-point map

| Sub-area | Pain point | Severity | Why a skill fits |
|---|---|---|---|
| Brand & content | Off-brand tone, inconsistent terminology, endless review cycles | High | Brand guide, glossary and examples are perfect skill references |
| Content production | High volume across channels; repurposing is manual | High | Procedure plus channel templates (length, format, CTA rules) |
| Claims & compliance | Unsubstantiated claims, missing disclaimers (finance, health, regulated industries) | High | Approved-claims library plus a validator |
| SEO | Briefs, keyword clustering, on-page audits done inconsistently | Med-High | Repeatable brief template and audit checklist; scripts for keyword grouping |
| Campaign planning | Briefs are vague; strategy is not tied to audience or positioning | Medium | Brief framework (objective, audience, insight, message, channels, KPIs) |
| Market & competitor intel | Competitive research is ad hoc and stale | Medium | Standard battlecard and teardown templates; comparable over time |
| Customer insight | Reviews, surveys and social comments are unread or unstructured | High | Themed coding taxonomy plus sentiment and quantification scripts |
| Performance reporting | Weekly or monthly reports take hours; little insight | High | CSV export to narrative, chart and recommendation in house format |
| Personalization / ABM | Tailoring messaging per segment or account is slow | Medium | Persona and ICP references plus messaging matrix |
| Localization | Translation loses brand voice and cultural fit | Medium | Locale-specific style rules and glossaries |
| Email & lifecycle | Sequences written inconsistently; no testing discipline | Medium | Sequence templates, A/B variant generation, deliverability checklist |
| PR & comms | Press releases and crisis statements need speed plus precision | Medium | Release template, boilerplate, approval checklist |

### 4.2 Recommended marketing skills

**M1. Brand Voice & Content Guardian** *(flagship)*
- **Solves:** off-brand copy, long review loops, inconsistent terminology.
- **Modes:** `write` (create on-brand copy for a channel) · `review` (score the copy, flag violations, suggest rewrites).
- **Bundled:** voice and tone guide, do/don't word list, product naming glossary, 5 annotated gold examples per channel, a claims/disclaimer list.
- **Scripts:** terminology linter (banned words, wrong product names), readability score, length checker per channel.
- **Output:** revised copy plus a review table (issue, rule, fix).

**M2. Campaign Brief Builder**
- **Solves:** vague briefs leading to misaligned creative and wasted budget.
- **Procedure:** interviews the requester with structured questions, then produces a one-page brief (objective, audience, insight, key message, proof points, channels, budget split, KPIs, timeline).
- **Bundled:** brief template, persona library, KPI benchmarks the team uses.

**M3. Content Repurposing Engine**
- **Solves:** one asset (webinar, whitepaper, blog) needs 10+ derivative pieces.
- **Output:** a pack with a blog summary, LinkedIn posts, X thread, email, short-video script and slide outline, each meeting channel rules.
- **Pairs with:** M1 for the brand check.

**M4. SEO Content Brief & On-Page Auditor**
- **Solves:** inconsistent SEO briefs and audits.
- **Output:** brief (search intent, outline, headings, entities, internal links, FAQs) or an audit report (title/meta, heading structure, keyword coverage, readability, schema suggestions).
- **Scripts:** keyword clustering from a CSV export, on-page HTML parser.

**M5. Competitor Teardown & Battlecard Generator**
- **Solves:** stale, inconsistent competitive intel.
- **Output:** a standard battlecard (positioning, pricing, strengths and weaknesses, objection handling, landmines, win themes) that is comparable across competitors.

**M6. Marketing Performance Narrator**
- **Solves:** hours spent turning ad, web or CRM exports into a weekly or monthly report.
- **Input:** CSV/XLSX exports. **Output:** a KPI table, variance vs. target or prior period, drivers, anomalies, recommended actions, plus a deck or doc in house format.
- **Scripts:** metric calculations (CAC, ROAS, CTR, CVR, funnel drop-off), chart generation.

**M7. Claims & Compliance Checker** *(critical for regulated industries)*
- **Solves:** legal risk from claims, missing disclosures and trademark misuse.
- **Output:** a flagged list with severity, the rule, a suggested compliant wording, and "needs legal review" escalation.

---

## 5. Business (sales, finance, operations, strategy, leadership)

### 5.1 Pain-point map

| Sub-area | Pain point | Severity | Why a skill fits |
|---|---|---|---|
| Sales proposals / RFPs | RFPs take days; answers are copied from old files, often outdated | Very High | Approved answer library plus assembly procedure plus docx output |
| Sales enablement | Reps don't follow the methodology; call prep is shallow | High | Account research and call-prep templates (e.g. MEDDICC fields) |
| Call & deal analysis | Call notes are unstructured; deal risk spotted late | High | Fixed scoring rubric applied to transcripts |
| Pricing & quoting | Discount rules complex; errors and approval delays | High | Pricing rules plus calculator script plus approval thresholds |
| Contracts | First-pass review of NDAs and MSAs clogs legal | High | Playbook (fallback positions) plus clause-by-clause review procedure |
| Finance reporting | Month-end commentary, variance analysis, board packs are manual | High | Variance procedure plus narrative template plus xlsx/pptx output |
| Budgeting & forecasting | Inconsistent models; assumptions undocumented | Medium | Model templates plus assumption logs plus sanity-check scripts |
| Procurement / vendors | Vendor comparison and due diligence inconsistent | Medium | Evaluation matrix plus weighted scoring script |
| Operations / SOPs | Processes undocumented or outdated | High | SOP template plus interview procedure to extract a process |
| Meetings & decisions | Decisions and actions are lost; follow-ups missed | Medium | Minutes template, decision log, RACI extraction |
| Strategy | Market sizing, SWOT and business cases are ad hoc | Medium | Framework templates (TAM/SAM/SOM, business case, OKRs) |
| Customer success | QBRs, health reviews and renewal risk prep are slow | Medium | QBR deck template plus health scoring rubric |
| Leadership comms | All-hands updates and investor updates take senior time | Medium | Narrative templates plus prior examples for tone |

### 5.2 Recommended business skills

**B1. Proposal & RFP Response Builder** *(flagship, highest ROI)*
- **Solves:** days of manual RFP and proposal work, outdated or inconsistent answers, win-rate drag.
- **Procedure:** parse the RFP (questionnaire, PDF, xlsx), map each question to the approved answer library, tailor to the client's industry and pain, mark gaps for SMEs, then assemble into a branded docx and compliance matrix.
- **Bundled:** answer library (security, product, company, references), case studies, pricing narrative, proposal template.
- **Scripts:** question extractor, coverage report ("42/50 answered, 8 need SME").

**B2. Sales Call Prep & Deal Review**
- **Solves:** shallow prep and late detection of deal risk.
- **Modes:** `prep` (account brief, stakeholders, hypotheses, discovery questions) · `review` (score a transcript against the sales methodology, list gaps, next steps, risk flags).
- **Bundled:** methodology rubric, ICP and persona references, objection library.

**B3. Contract First-Pass Reviewer**
- **Solves:** legal bottleneck on standard agreements.
- **Output:** a clause table (clause, our standard, their language, deviation, risk level, suggested redline or fallback), and an escalation list.
- **Guardrail:** always "first pass for legal review", never final legal advice.

**B4. Executive Report & Board Deck Builder**
- **Solves:** senior time lost turning numbers into narrative.
- **Input:** KPI exports and last period's report. **Output:** an exec summary, KPI table, variance commentary ("revenue −4% vs plan, driven by…"), risks, asks, and a pptx in house template.
- **Scripts:** variance calculator, chart builder, number-consistency checker (the totals in the text match the tables).

**B5. Month-End Variance Commentary (Finance)**
- **Solves:** repetitive budget-vs-actual commentary across cost centers.
- **Output:** per-line commentary with materiality thresholds applied, plus questions for budget owners.

**B6. SOP & Process Documenter**
- **Solves:** undocumented processes and single points of failure.
- **Procedure:** interview the process owner, or ingest a meeting transcript, then produce an SOP (purpose, roles/RACI, steps, inputs and outputs, controls, exceptions) and an optional flow diagram.

**B7. Meeting-to-Action Converter**
- **Solves:** lost decisions and missed follow-ups.
- **Output:** decisions, action items (owner, due date), open questions, and a follow-up email draft in house format.

**B8. Business Case & Strategy Frameworks**
- **Solves:** inconsistent investment proposals.
- **Output:** a business case (problem, options, costs, benefits, ROI/NPV, payback, risks, recommendation) using the company's approved assumptions.
- **Scripts:** ROI/NPV/payback calculator, sensitivity table.

**B9. Vendor Evaluation & Comparison**
- **Solves:** subjective vendor selection.
- **Output:** a weighted scoring matrix (xlsx), a due-diligence checklist and a recommendation memo.

---

## 6. HR / people operations

### 6.1 Pain-point map

| Sub-area | Pain point | Severity | Why a skill fits |
|---|---|---|---|
| Job descriptions | Inconsistent, biased or bloated JDs; slow to write | High | Leveling framework plus inclusive-language rules plus template |
| Screening | High applicant volume; inconsistent screening criteria | High | Scorecard-based structured evaluation (with human decision) |
| Interviewing | Unstructured interviews, inconsistent questions, weak debriefs | High | Competency question bank plus scorecard plus debrief template |
| Offers | Offer letters vary; comp band errors | Medium | Template plus comp band validator |
| Onboarding | Generic onboarding; managers don't know what to do | High | Role-based 30/60/90 plan and checklist generator |
| Policies & handbook | Employees ask HR the same questions; policies outdated | Very High | Grounded Q&A over the handbook plus policy drafting checklist |
| Performance reviews | Vague, biased or inconsistent feedback; calibration pain | High | Review rubric plus bias checker plus evidence-based writing guide |
| Employee relations | Investigations and PIPs need careful, consistent documentation | High (risk) | Documentation templates plus neutrality and completeness checks |
| Engagement surveys | Comments go unanalyzed; action plans generic | High | Theme coding taxonomy plus action planning template |
| Exit / attrition | Exit-interview insight never aggregated | Medium | Same synthesis engine, attrition taxonomy |
| Learning & development | Training content and skills matrices take time | Medium | Course outline, quiz and skills-gap templates |
| Internal comms | Announcements (reorgs, benefits, policy changes) need care | Medium | Comms templates plus tone guide plus FAQ generator |
| Compensation | Benchmarking and band documentation manual | Medium | Band calculator plus comp letter templates |
| Compliance | Multi-jurisdiction rules (leave, working hours, data privacy) | High | Jurisdiction reference plus checklists, with clear escalation |

### 6.2 Recommended HR skills

**H1. Inclusive Job Description & Hiring Kit Generator** *(flagship)*
- **Solves:** slow, inconsistent and biased hiring documentation.
- **Input:** role, level, team, must-haves. **Output:** a JD in house template, a competency scorecard, structured interview questions per competency (with "what good looks like"), a take-home or exercise brief, and an inclusive-language report.
- **Bundled:** leveling and career framework, competency library, EVP and boilerplate, gendered and exclusionary word list.
- **Scripts:** bias-language linter, required-vs-preferred requirement counter.

**H2. Structured Interview Debrief & Scorecard Assistant**
- **Solves:** gut-feel hiring and messy debriefs.
- **Output:** turns interviewer notes into an evidence-based scorecard per competency, flags non-job-related or biased comments, and gives a debrief summary.
- **Guardrail:** the skill organizes evidence; humans decide. No automated rejections.

**H3. Policy & Handbook Assistant** *(flagship for HR ops)*
- **Solves:** repetitive employee questions and outdated policies.
- **Modes:** `answer` (grounded answer with a citation to the handbook section, and escalation if uncertain) · `draft` (new or updated policy using the template and compliance checklist per jurisdiction) · `diff` (what changed between policy versions and a plain-language summary for employees).

**H4. Onboarding Plan Generator**
- **Solves:** generic onboarding and unprepared managers.
- **Output:** a role-specific 30/60/90 plan, first-week schedule, buddy guide, access and equipment checklist, and welcome email.

**H5. Performance Review Writing Coach & Bias Checker**
- **Solves:** vague, inconsistent and biased reviews; calibration effort.
- **Modes:** `coach` (helps managers turn notes into SBI-style, evidence-based feedback against the rubric) · `check` (flags personality-based or gendered language, recency bias and missing evidence) · `self-review` (helps employees structure their own review).

**H6. Engagement Survey, Exit Interview & Feedback Synthesizer**
- **Solves:** thousands of verbatims unread; generic action plans.
- **Output:** theme frequency, sentiment by team or tenure (with minimum group-size anonymity thresholds), representative anonymized quotes, top 3 issues, and an action plan template per manager.
- **Scripts:** theme coding with a fixed taxonomy, anonymity threshold enforcer, chart generator.

**H7. Employee Relations Documentation Assistant**
- **Solves:** inconsistent, legally risky documentation (warnings, PIPs, investigation reports).
- **Output:** structured, neutral, fact-based documents and a completeness checklist (dates, policy cited, expectations, support offered, timeline).
- **Guardrail:** strict neutrality rules, "consult HR/legal" escalation, no conclusions about intent.

**H8. Internal Change Communications Kit**
- **Solves:** high-stakes announcements (reorgs, policy and benefit changes) written in a rush.
- **Output:** announcement, manager talking points, employee FAQ, and a timeline of who hears what and when.

**H9. L&D Course & Skills-Matrix Builder**
- **Solves:** slow creation of training material.
- **Output:** learning objectives, course outline, slides outline, quiz with answer key, and a skills-gap matrix template.

---

## 7. Shared / horizontal skills (build once, used by all three)

| Skill | Used by | Solves |
|---|---|---|
| **X1. Feedback & Voice Synthesizer** (shared engine of M-insight, H6, CS) | Marketing, HR, CS, Product | Unstructured text into a quantified theme report |
| **X2. House-Format Document Builder** (docx/pptx/xlsx in company templates) | All | Format friction; inconsistent branding on documents |
| **X3. Executive Summary & Narrative Writer** | All | Turning long material into a decision-ready one-pager |
| **X4. Meeting-to-Action Converter** (B7) | All | Lost decisions and follow-ups |
| **X5. Company Glossary & Fact Checker** | All | Wrong product names, outdated facts, inconsistent numbers |

These horizontal skills are the **platform layer**. Domain skills call them, for example "H6 uses X1 for coding and X2 for the deck".

---

## 8. Prioritized skill catalog

Scoring: **Impact** (time saved × frequency × risk reduced) and **Effort** (reference material to gather, scripts, validation needed), each 1–5.

| Rank | Skill | Domain | Impact | Effort | Priority |
|---|---|---|---|---|---|
| 1 | B1 Proposal & RFP Response Builder | Business | 5 | 3 | **Quick win, high value** |
| 2 | M1 Brand Voice & Content Guardian | Marketing | 5 | 2 | **Quick win, high value** |
| 3 | H1 Inclusive JD & Hiring Kit | HR | 4 | 2 | **Quick win, high value** |
| 4 | X1 Feedback & Voice Synthesizer | Shared | 5 | 3 | **Strategic platform** |
| 5 | H3 Policy & Handbook Assistant | HR | 5 | 3 | **Strategic** |
| 6 | B4 Executive Report & Board Deck Builder | Business | 4 | 3 | Strategic |
| 7 | M6 Marketing Performance Narrator | Marketing | 4 | 3 | Strategic |
| 8 | H5 Performance Review Coach & Bias Checker | HR | 4 | 2 | Quick win (seasonal) |
| 9 | B2 Sales Call Prep & Deal Review | Business | 4 | 2 | Quick win |
| 10 | X2 House-Format Document Builder | Shared | 4 | 2 | Platform enabler |
| 11 | B3 Contract First-Pass Reviewer | Business | 5 | 4 | High value, needs legal sign-off |
| 12 | M7 Claims & Compliance Checker | Marketing | 4 | 3 | Must-have in regulated sectors |
| 13 | B6 SOP & Process Documenter | Business | 3 | 2 | Quick win |
| 14 | H4 Onboarding Plan Generator | HR | 3 | 2 | Quick win |
| 15 | M2 Campaign Brief Builder | Marketing | 3 | 1 | Quick win |
| 16 | M3 Content Repurposing Engine | Marketing | 3 | 2 | Quick win |
| 17 | H7 ER Documentation Assistant | HR | 4 | 4 | High risk, build carefully |
| 18 | M4 SEO Brief & Auditor | Marketing | 3 | 3 | Fill-in |
| 19 | M5 Competitor Battlecards | Marketing/Sales | 3 | 2 | Fill-in |
| 20 | B8 Business Case Frameworks | Business | 3 | 2 | Fill-in |
| 21 | H2 Interview Debrief Assistant | HR | 3 | 2 | Fill-in |
| 22 | H6 Survey/Exit Synthesizer | HR | 4 | 1 (on top of X1) | Do right after X1 |
| 23 | H8 Change Comms Kit | HR | 3 | 1 | Fill-in |
| 24 | B5 Month-End Variance Commentary | Finance | 3 | 3 | Fill-in |
| 25 | B9 Vendor Evaluation | Business | 2 | 2 | Later |
| 26 | H9 L&D Course Builder | HR | 2 | 2 | Later |

### Impact × effort view

```
 Impact
   5 |  M1          B1, X1, H3        B3
   4 |  H1,H5,B2,X2 B4, M6, M7, H6*   H7
   3 |  M2,M3,B6,H4,H8,M5,B8,H2   M4, B5
   2 |              B9, H9
     +-------------------------------------- Effort
        low (1-2)       medium (3)      high (4)
   * H6 is low effort once X1 exists
```

**Read:** start in the top-left (high impact, low effort). Then invest in the shared platform (X1, X2). Take on high-risk skills (B3, H7) only with legal and HR sign-off.

---

## 9. Recommended roadmap

| Phase | Weeks | Build | Goal / gate to move on |
|---|---|---|---|
| **0. Foundations** | 1–2 | Collect brand guide, handbook, leveling framework, answer library, templates. Define the skill folder standard and an eval harness. | Reference material approved by owners |
| **1. Quick wins** | 3–6 | M1 Brand Guardian, H1 JD & Hiring Kit, B1 RFP Builder, X2 Doc Builder | Each skill passes ≥ 80% of eval cases; 2 pilot teams using weekly |
| **2. Insight platform** | 7–10 | X1 Feedback Synthesizer, then H6, M6, B4 on top of it | Report produced in < 30 min vs. days; owners rate it "usable as-is or light edit" |
| **3. Policy & people** | 11–14 | H3 Policy Assistant, H5 Review Coach, H4 Onboarding, B2 Call Prep | Answer accuracy ≥ 95% on a handbook test set; zero uncited answers |
| **4. High-risk, high-value** | 15–20 | B3 Contract Reviewer, M7 Claims Checker, H7 ER Docs | Legal and HR sign-off; human-in-the-loop enforced |
| **5. Scale** | ongoing | Remaining catalog; connectors (CRM, ATS, HRIS, ad platforms) for live data | Adoption and time-saved metrics reviewed monthly |

---

## 10. Design principles for these skills

1. **Ground, don't invent.** Every factual claim comes from the bundled reference or user input. The skill cites its source, such as a handbook section or an approved answer ID.
2. **Procedure first.** SKILL.md reads like an expert's checklist: gather inputs, draft, self-review against the rubric, flag gaps, output.
3. **Ask before assuming.** A short structured intake (5–8 questions) beats a long, wrong draft.
4. **Validate with code where possible.** Linters for banned words, calculators for numbers, consistency checks between text and tables, template conformance.
5. **Explicit escalation rules.** Legal, ER, compensation and regulated claims get "flag for human review", never a silent pass.
6. **Gold examples beat long instructions.** 3–5 annotated good and bad examples per output type.
7. **Native output formats.** Ship docx, pptx and xlsx in house templates. People work in files, not chat.
8. **Small and composable.** Domain skills reuse the horizontal skills (X1–X5) instead of duplicating them.
9. **Owned and versioned.** Each skill has a business owner who keeps its reference material current, plus a changelog.

---

## 11. Risks and mitigations

| Risk | Where it bites | Mitigation |
|---|---|---|
| Hallucinated facts or claims | Proposals, marketing claims, policy answers | Grounding plus citations; "not found → say so"; answer-library-only mode |
| Bias in people decisions | Screening, reviews, debriefs | Skills organize evidence, never decide; bias linters; no automated rejection; audit sampling |
| Legal or regulatory exposure | Contracts, ER docs, employment law, claims | First-pass framing, mandatory escalation, legal-approved playbooks, jurisdiction scoping |
| Privacy / PII | HR data, survey comments, candidate data | Anonymity thresholds, PII redaction scripts, data handling rules in SKILL.md, approved environments only |
| Stale reference material | All | Named owner, review cadence, version date shown in outputs |
| Low adoption | All | Start where pain is felt weekly; embed in existing tools; show before/after time savings |
| Over-trust of outputs | All | "Draft for review" labeling; reviewer checklists; spot-check audits |

---

## 12. Success metrics

| Metric | How to measure | Target example |
|---|---|---|
| Time saved per task | Before/after timing on pilot tasks | 50–80% on first drafts |
| Review cycles | Rounds of edits before approval | From 3+ to ≤ 1 |
| Consistency / quality score | Rubric scoring of samples by domain owners | ≥ 4/5 average |
| Compliance catches | Issues flagged before publication or sending | Trending up early, then down as quality improves |
| Adoption | Weekly active users per skill | ≥ 60% of target team in 8 weeks |
| Business outcomes | RFP win rate, time-to-hire, policy ticket volume, report turnaround | Track per skill vs. baseline |

The targets above are illustrative starting points. Set real baselines during each pilot.

---

## 13. Open questions to settle before building

1. Which industry or regulatory context applies (e.g. finance, health)? This sets the priority of M7 and B3.
2. Where will skills run: Claude.ai, Claude Code, API or the Agent SDK? This affects file outputs and connector choices.
3. Which systems hold the source data (CRM, ATS, HRIS, ad platforms, Drive/Confluence)? This decides which connectors to pair with skills.
4. Who owns each reference corpus (brand guide, handbook, answer library), and how often does it change?
5. Which jurisdictions do HR skills need to cover?
6. Pilot teams: which marketing, sales and HR teams will commit to weekly use and give feedback?

---

## Appendix A: Skill one-liners (catalog index)

| ID | Skill | One-line purpose |
|---|---|---|
| M1 | Brand Voice & Content Guardian | Write or review any copy against brand voice, terminology and claim rules |
| M2 | Campaign Brief Builder | Turn a vague request into a complete, KPI-linked campaign brief |
| M3 | Content Repurposing Engine | One asset into a channel-ready content pack |
| M4 | SEO Brief & On-Page Auditor | Standard SEO briefs and page audits |
| M5 | Competitor Battlecard Generator | Comparable, current competitive battlecards |
| M6 | Marketing Performance Narrator | Channel exports into a KPI narrative and deck |
| M7 | Claims & Compliance Checker | Flag risky claims, missing disclosures and trademark misuse |
| B1 | Proposal & RFP Response Builder | Tailored proposals from an approved answer library |
| B2 | Sales Call Prep & Deal Review | Account prep and methodology-based call scoring |
| B3 | Contract First-Pass Reviewer | Clause-by-clause deviation and risk table against the playbook |
| B4 | Executive Report & Board Deck Builder | KPIs into an exec narrative and house-format deck |
| B5 | Month-End Variance Commentary | Budget-vs-actual commentary with materiality rules |
| B6 | SOP & Process Documenter | Interviews or transcripts into structured SOPs |
| B7 | Meeting-to-Action Converter | Transcripts into decisions, actions and a follow-up email |
| B8 | Business Case Frameworks | Standard business cases with ROI/NPV calculations |
| B9 | Vendor Evaluation & Comparison | Weighted vendor scoring and a recommendation memo |
| H1 | Inclusive JD & Hiring Kit | JD, scorecard, interview questions and bias check |
| H2 | Interview Debrief Assistant | Notes into an evidence-based scorecard and debrief |
| H3 | Policy & Handbook Assistant | Cited answers, policy drafting and version diffs |
| H4 | Onboarding Plan Generator | Role-specific 30/60/90 onboarding kit |
| H5 | Performance Review Coach & Bias Checker | Evidence-based, bias-checked reviews |
| H6 | Survey & Exit Synthesizer | Anonymized themes and manager action plans |
| H7 | ER Documentation Assistant | Neutral, complete warnings, PIPs and investigation docs |
| H8 | Change Communications Kit | Announcement, talking points, FAQ and timeline |
| H9 | L&D Course & Skills-Matrix Builder | Course outlines, quizzes and skills-gap matrices |
| X1 | Feedback & Voice Synthesizer | Shared engine: unstructured text into a quantified theme report |
| X2 | House-Format Document Builder | Native docx/pptx/xlsx in company templates |
| X3 | Executive Summary Writer | Long material into a decision-ready one-pager |
| X4 | Meeting-to-Action Converter | Shared version of B7 |
| X5 | Glossary & Fact Checker | Correct names, facts and numbers across outputs |

---

*Note: this analysis draws on common, well-documented patterns in marketing, sales, finance and HR operations. It does not use survey data from your organization. Validate the severity scores with 5–10 short interviews of the target teams before committing the roadmap.*
