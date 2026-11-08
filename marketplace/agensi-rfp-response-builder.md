# Agensi listing: BidReady (rfp-response-builder)

Copy each field into the Agensi submission form (agensi.io/dashboard/submit).

## Logo
`marketplace/assets/bidready-logo-512.png` (also a 1024 px PNG and the `.svg` source).
A requirements checklist with a completion badge, in navy `#14213D` and amber `#FCA311`.

## Name (48 / 60 characters)
BidReady: RFP & Security Questionnaire Responder

## Summary (287 / 300 characters)
Turn any RFP, tender or security questionnaire into a submission-ready Word proposal and compliance matrix, built only from your own approved content. Every requirement tracked, every gap flagged with an owner, nothing invented. Builds your answer library from past proposals in minutes.

## Full description

### Win more bids without writing every proposal from scratch

Every RFP turns into the same scramble. Your best people dig through old proposals, copy-paste answers that may be out of date, and hope nobody missed a mandatory requirement buried on page 37. A generic AI assistant makes it faster, but it also writes things like *"We confirm 24/7 support with a 30-minute response time"* when your company doesn't offer that.

**BidReady gives your agent a bid manager's discipline and your company's approved answers.** The result is a response your team can review and submit with confidence.

### What it does

**📚 Builds your answer library in minutes.**
Give it 3–10 past proposals in Word, PDF or text. It extracts your company facts, certifications, standard answers, case studies, team profiles and rate card into a clean, searchable library. Where old and new proposals disagree, it keeps the newest fact and shows you what changed. It also tells you which common RFP topics you're still missing.

**🔍 Catches every requirement.**
It extracts every question, "must" and "shall" with the RFP's own numbering. It splits compound questions so nothing is half-answered, and it finds submission rules hidden in the prose.

**✍️ Drafts answers that score.**
Each answer leads with the direct response, then gives proof from your library, then ties the benefit to the client's stated goals. It respects every word and page limit, and win themes carry through the whole proposal.

**🛡️ Never invents. Never over-promises.**
This is what sets BidReady apart. Certifications, references, prices and service levels come only from your library. Anything it can't verify becomes a highlighted `[VERIFY]` item with a named owner. If the client asks for something you don't offer, it states an honest exception with your real offering instead of agreeing to it.

**🚨 Catches the mistakes that lose deals.**
Before anything leaves your desk, it checks for:
- unanswered mandatory requirements
- out-of-date certificates
- internal-only notes, such as discount limits
- answers over their word limits
- another client's name left in reused text

**📄 Delivers real files.**
- **Word proposal:** cover page, narrative sections and every requirement answered in the RFP's order, with open items highlighted.
- **Excel compliance matrix:** status, compliance, sources and owner for every requirement, plus a Gaps sheet your experts can work from.
- **The client's own questionnaire:** answers written into their spreadsheet with their layout untouched. A row is never marked "Yes" while something is unconfirmed.

**🎯 Tells you whether to bid at all.**
Knock-out checks and a weighted bid/no-bid score tell you whether a tender is worth a week of senior time, before you spend it.

### Who it's for
- **Agencies, consultancies and software vendors** answering enterprise and public-sector RFPs
- **Presales and bid teams** handling a steady stream of tenders
- **Security and compliance leads** buried in vendor questionnaires (SIG-style, due diligence, supplier security)
- **Founders** who write every proposal themselves and want them done in an afternoon

### How you use it
1. *"Set up our RFP library from these old proposals."*
2. *"Here's the tender from Acme. Draft our proposal and a compliance matrix."*
3. *"Fill in this security questionnaire from our library. Yes/No goes in column D, answers in column E."*
4. *"Should we even bid on this one?"*

### Private by design
Your content stays in your own folder. BidReady makes no network calls and uses no external services. It's plain, readable scripts and instructions.

### Requirements
Works with Claude Code and other agents that support SKILL.md skills. Word and Excel output uses Python 3.9+, and the libraries install automatically on first use. Without Python, it still works and delivers markdown and CSV.

## Category
Business / Sales (or the closest match: Productivity, Writing)

## Tags
rfp, proposal, tender, bid management, security questionnaire, vendor questionnaire, due diligence, compliance matrix, presales, sales, procurement, word, excel

## Use cases
- Public-sector tenders and open procurement
- Enterprise RFPs and RFIs
- Security, vendor and due-diligence questionnaires
- Bid/no-bid decisions
- Building and maintaining a proposal content library

## Pricing (suggestion)
One-time $39. Alternatively, $12/month if you plan regular updates. This is a judgment call; check comparable Agensi listings before deciding.

## Demo video (30–60 s, recommended by Agensi)
1. Drop in old proposals; the library appears with a list of resolved conflicts (10 s).
2. Drop in an RFP; the compliance matrix fills in (15 s).
3. Open the Word proposal and scroll to a yellow `[VERIFY]` item and an honest exception (15 s).
4. End on the gaps list with owners (10 s).

## Upload
ZIP: `dist/rfp-response-builder-v1.0.0.zip` (build with `tools/package_skill.sh rfp-response-builder 1.0.0`).

## Before submitting
- [ ] Connect Stripe Connect (or USDC) payouts and complete identity verification
- [ ] Ask Agensi support whether bundled Python scripts run for buyers who use the connector
- [ ] Record the demo video
