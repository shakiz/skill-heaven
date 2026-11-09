# Agensi listing: RedlineReady (contract-review-redliner)

Copy each field into the Agensi submission form (agensi.io/dashboard/submit).

## Logo
`marketplace/assets/redlineready-logo-512.png` (also a 1024 px PNG and the `.svg` source).
A contract page with a red strike-through and an inserted line, plus a pen badge, in navy `#14213D` and redline red `#E63946`. Same family look as BidReady.

## Name (45 / 60 characters)
RedlineReady: Contract Review & Word Redlines

## Summary (297 / 300 characters)
Review any contract against your own playbook and get a Word redline with real tracked changes and margin comments, ready to send. Every clause risk-rated in plain English, your fallbacks kept internal, and silent untracked edits caught when they send it back. For NDAs, MSAs, SaaS, SOWs and more.

## Full description

### Stop signing contracts you haven't really read

Someone sends you their paper and says "just sign by Friday." It's 14 pages of their lawyer's best positions: an uncapped liability clause, a three-year auto-renewal with 180 days' notice, payment at Net 90. You can skim it and hope, or you can pay a lawyer to read yet another routine NDA. And when you do push back, it turns into a long email thread of "in clause 9.2, could we change…" that nobody can follow.

**RedlineReady gives your agent a careful first-pass contract review, measured against *your* positions, and hands you a marked-up Word file you can send straight back.**

### What it does

**📘 Reviews against your playbook, not generic advice.**
Your playbook holds your standard position on each topic, the fallback you'd accept, your walk-away point and the red flags to watch for. RedlineReady ships with a starter playbook of 42 market-standard positions for both buyers and sellers, so it's useful on day one. It can also build your own playbook from your preferences or from contracts you've negotiated before.

**🚦 Rates every clause.**
Each clause gets a high, medium or low risk rating, a plain-English explanation and the position it recommends. A checklist makes sure no standard topic is skipped, and protections that are *missing* from the contract are flagged too.

**✍️ Produces a real Word redline.**
This is the headline. You get a genuine .docx with real tracked changes and margin comments, ready to send to the other side. Redlines are surgical: only the words that change are struck or inserted. It works on the original .docx and keeps its formatting and auto-numbering. Track Changes is left switched on, so the conversation continues in Word. PDFs and text files are rebuilt as a plain Word document.

**🔒 Keeps your internal positions internal.**
Your fallbacks, walk-away points and internal reasoning go into an internal summary only. The Word file contains only counterparty-facing comments, and a validation script checks for leaks before anything is built. It also cleans the file itself: colleagues' internal comments left in the draft, hidden text, and document properties like author and notes are found and stripped before the redline goes out.

**🧐 Catches the mistakes that slip through.**
The validation step also flags:
- redline text that uses an undefined term or the wrong party name (for example "Vendor" when the contract says "Supplier")
- cross-references to clauses that don't exist
- unfilled blanks such as [●] or ____
- number words that don't match their digits, such as "thirty (60) days"

**🕵️ Spots silent edits in their counter-redline.**
When the other side sends back their markup, RedlineReady lists their tracked changes and comments. It also detects edits they made *without* Track Changes, a known negotiation trick that is easy to miss when you're only reading the red ink.

**📄 Gives you everything you need to decide.**
- **Internal review summary (.docx):** a verdict (sign / sign with changes / negotiate / escalate to a lawyer / do not sign), key terms, an issues table, and your must-haves versus your tradeables.
- **Negotiation email:** a draft to the counterparty that goes with the redline.
- **Signed-contract summary:** key dates, renewal and notice deadlines, and obligations for a contract you've already signed.
- **Quick check:** ask "can I sign this?" and get the answer in chat.

### Contracts it handles
NDAs (mutual or one-way), MSAs, SaaS and subscription terms, SOWs, DPAs, consulting and freelance agreements, vendor and supplier terms, and similar commercial contracts.

### Who it's for
- **Freelancers and agencies** signing client MSAs, SOWs and NDAs
- **Startup founders and small-business owners** who sign without a lawyer on every deal
- **Sales and procurement teams** working through customer paper and supplier terms
- **Ops managers and in-house legal teams of one** who need a consistent first pass, fast

### How you use it
1. *"Set up our contract playbook. We're usually the supplier, and our standard cap is 12 months' fees."*
2. *"Review this MSA from Brightloom and redline it."*
3. *"They sent it back. What did they change, and did they change anything without tracking it?"*
4. *"Can I sign this NDA?"*
5. *"We signed this last year. When's the notice deadline?"*

### A first pass, with honest limits
RedlineReady is a first-pass review to support your decision, not legal advice. It recommends a lawyer for high-stakes, regulated or jurisdiction-specific points, never claims a clause is enforceable, and asks which side you're on if that isn't clear.

### Private by design
Your contracts stay in your own folder. RedlineReady makes no network calls and uses no external services. Reviews go to `./contract-reviews/<counterparty>/` and your playbook lives in `./contract-playbook/`. It's plain, readable scripts and instructions.

### Requirements
Works with Claude Code and other agents that support SKILL.md skills. Word output uses Python 3.9+ with python-docx (1.2 or later) and pypdf, which install on first use. Without Python, it still works and delivers a markdown redline (strike-through and bold) plus a list of comments.

## Category
Legal & Compliance (closest alternatives: Business, Productivity)

## Tags
contract review, redline, redlining, tracked changes, nda, msa, saas agreement, sow, dpa, negotiation, playbook, legal, procurement, freelance, word, docx

## Use cases
- Reviewing and redlining NDAs, MSAs, SaaS terms and SOWs before signing
- Checking customer or supplier paper against your standard positions
- Handling a counterparty's counter-redline, including untracked edits
- "Can I sign this?" quick checks
- Tracking renewal and notice deadlines in signed contracts
- Building a negotiation playbook from past contracts

## Pricing (suggestion)
**One-time $49.** If you want to test demand first, launch at $39 for the first weeks and move to $49.

Evidence from agensi.io (checked 2026-11-09):
- Most paid skills on the first page of `/skills` cost $5–$39, and one-time pricing is the most common. Examples: $9.99 (Skill of the Month), $12, $14, $19, $25, and a $39 bundle.
- Agensi's creator guide (`/learn/how-to-price-skill-md-skills`) puts single-purpose skills at $3–$9 and comprehensive skills with scripts and references at $12–$25. It also notes that skills with supporting files sell for more.
- The `/sell` page uses a $29 one-time sale as its example, and its illustrative listings include a compliance skill at $49 one-time and subscriptions up to $49/month.
- No priced legal or contract skill could be read: the Legal & Compliance category (229 skills) did not render its listings to a fetch, so there's no direct comparable.

Reasoning: $49 sits above the typical Agensi price, matching the illustrative compliance-skill example. That premium is justified because RedlineReady is a multi-script product with real .docx output, a starter playbook and a validation step, and because it replaces work buyers otherwise pay a professional for. $79 would be well above every price observed on the site, so keep it for a later "Pro" tier or bundle rather than the launch. BidReady's suggested price is $39, so $49 also positions RedlineReady as the more specialised of the two. Prices can be changed later from the creator dashboard.

## Bundle with BidReady
Pair it with **BidReady** (rfp-response-builder) as a "Ready" bundle for anyone who wins and signs deals: BidReady writes the proposal, RedlineReady negotiates the contract that follows. A suggested bundle price is $69 (about 20% off $39 + $49). Agensi's pricing guide says formal bundle pricing isn't available yet, but the site already shows `/bundles` pages and a bundle listing, so check what the dashboard offers. If bundles aren't available, cross-link the two listings in their descriptions.

## Demo video (30–60 s, recommended by Agensi)
Rendered: `marketplace/video-redlineready/out/redlineready-demo.mp4` (1920×1080) and `redlineready-demo-square.mp4` (1080×1080), about 55 s. Thumbnail: `redlineready-thumbnail.png`. Source and re-render: `cd marketplace/video-redlineready && npm ci && npm run render`. The music is a synthesized placeholder (`scripts/make_music.py`); swap in a royalty-free track before publishing.
1. Hook: "Another 14-page contract. Just sign by Friday." (5 s)
2. Problem: unclear clauses, lawyer fees for routine NDAs, email-thread negotiation. A buried auto-renewal clause is highlighted. (8 s)
3. Solution: the RedlineReady logo and one-line promise. (4 s)
4. Step 1: the playbook with standard, fallback and walk-away; fallbacks are marked internal. (6 s)
5. Step 2: a risk-rated issues table (high, medium, low, missing). (6 s)
6. Step 3: a Word redline with strike-through, insertions, a margin comment and Track Changes on. (7 s)
7. Their counter-redline: 4 tracked changes, 2 comments and one untracked edit caught. (6 s)
8. Benefits, then CTA "Available on Agensi" with the first-pass disclaimer. (13 s)

All company names in the video are fictional (Brightloom Software).

## Upload
ZIP: `dist/contract-review-redliner-v1.0.0.zip` (build with `tools/package_skill.sh contract-review-redliner 1.0.0`).

## Permissions form (suggested)
- **Tools used:** Read, Write, Edit, Bash. No Browser, no web fetch, no network access.
- **Bash usage:** runs the bundled Python scripts (`scan_contract.py`, `check_review.py`, `redline.py`, `build_summary.py`, `compare_versions.py`, `init_playbook.py`) and a one-time `pip install -r requirements.txt` (python-docx, pypdf).
- **File scopes:**
  - `contract-playbook/**`: read/write (the buyer's playbook)
  - `contract-reviews/**`: read/write (review files, redlines, summaries, email drafts)
  - the contract files the user points to: read only. The original is never edited; the redline is written as a copy.
- **Notes:** no network calls, telemetry or external services. Contracts never leave the user's machine. The skill folder is only read (the starter playbook is copied out on setup). The one-time pip install is the only step that touches the network, and it uses the standard package index.

## Before submitting
- [ ] SKILL.md and README.md are final in `skills/contract-review-redliner/`
- [ ] Build the ZIP and confirm the script reports "No network calls in scripts."
- [ ] Recount the name and summary if you edit them (limits are 60 and 300)
- [ ] Search agensi.io (on-site search or the MCP connector) for "RedlineReady" and "redline". Only the first page of 805 could be checked automatically, and no conflict appeared there.
- [ ] Replace the placeholder music and re-render the video
- [ ] Ask Agensi support whether bundled Python scripts run for buyers who use the connector
- [ ] Set up the BidReady bundle or cross-links
- [ ] Payouts (Stripe Connect or USDC) and identity verification are complete
