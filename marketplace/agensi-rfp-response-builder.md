# Agensi listing: RFP Response Builder

Fill-in sheet for the Agensi submission form at agensi.io/dashboard/submit. The form's exact fields weren't visible before login; Agensi ranks listings on name, tags, description, use cases and compatibility.

## Name
RFP Response Builder

## Tagline (one line)
Turn any RFP, tender or security questionnaire into a submission-ready response, built only from your approved content.

## Category
Business / Sales (pick the closest category in Agensi's list)

## Tags
rfp, proposal, tender, bid management, security questionnaire, vendor questionnaire, due diligence, compliance matrix, sales, presales, procurement, docx, xlsx

## Compatibility
Claude Code, Claude (skills-enabled). Needs Python 3.9+ for Word and Excel output; falls back to markdown and CSV without it.

## Description

Responding to RFPs eats days of senior time. Answers get copied from old proposals, a mandatory requirement gets missed, or someone promises a service level the company doesn't offer.

**RFP Response Builder** gives your agent a bid manager's process and your company's approved answers:

- **Builds your answer library from past proposals.** Hand it a few old proposals and it extracts company facts, certifications, standard answers, case studies, team profiles and rates. Where sources conflict, it keeps the newest and tells you what changed.
- **Extracts every requirement** with the RFP's own numbering, and splits compound questions so nothing is half-answered.
- **Drafts tailored answers from your library only.** It answers first, gives proof, and links the benefit to the client's stated goals, within word limits.
- **Flags gaps and never invents.** Missing references, unconfirmed prices and service levels you don't offer become highlighted `[VERIFY]` items, each with an owner. It isn't allowed to make them up.
- **Catches the embarrassing errors:** out-of-date certificates, internal-only notes and another client's name left in reused text.
- **Delivers real files:** a Word proposal, an Excel compliance matrix with a gaps sheet, or the client's own questionnaire spreadsheet, filled in.
- **Bid/no-bid first.** Knock-out checks and a weighted score tell you whether a tender is worth a week of work.

Your content stays in your own folder. No network calls, no external services.

## Use cases
- Public-sector tenders and open procurement
- Enterprise RFPs and RFIs for agencies, consultancies and software vendors
- Security, vendor and due-diligence questionnaires (SIG-style spreadsheets)
- Go/no-go decisions on incoming tenders
- Building and maintaining a proposal content library

## Example prompts
- "Set up our RFP library from these five old proposals."
- "Here's the tender from Vestby Municipality, draft our proposal and a compliance matrix."
- "Fill in this security questionnaire from our library. Yes/No goes in column D, answers in column E."
- "Should we bid on this SAP tender? Check it against our library."

## Pricing (suggestion)
One-time $39. Alternative: $12/month if regular template and checklist updates are planned. This is a judgment call, not checked against comparable Agensi listings.

## Demo video idea (30–60 s)
Drop an RFP in, show the compliance matrix filling in, the Word proposal with yellow `[VERIFY]` items, and the gaps list with owners.

## Before submitting
- [ ] Build the ZIP: `tools/package_skill.sh rfp-response-builder 1.0.0` produces `dist/rfp-response-builder-v1.0.0.zip`
- [ ] Connect a payout method (Stripe Connect or USDC) and complete identity verification
- [ ] Record the demo video
- [ ] Confirm with Agensi how bundled Python scripts run for buyers who get skills through the connector
