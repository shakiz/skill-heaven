# What to check, by contract type

Use the playbook topics for the contract type and role, plus the traps below. Traps are where first-pass reviews usually fail: the clause looks routine, but the risk sits in a definition, a cross-reference or another document.

## Read in this order

1. **Parties and structure.** Who signs? Is it the right legal entity, or a parent or affiliate? Which documents make up the contract: order form, terms, DPA, SOW, policies by URL? What is the order of precedence?
2. **Definitions.** Broad definitions change every clause that uses them ("Services", "Confidential Information", "Losses", "Affiliate").
3. **Money.** Fees, payment trigger, price changes, renewal pricing, expenses, taxes, set-off.
4. **Term and exit.** Initial term, renewal mechanics, notice deadlines, termination rights for each side, what happens on exit (data, transition, fees due).
5. **Risk.** Liability caps (for each party), exclusions, indemnities, warranties, insurance, service credits.
6. **IP and data.** Who owns what, licences, use of data, AI training, confidentiality, data protection, security.
7. **Boilerplate that matters.** Governing law, jurisdiction, assignment, non-solicit and non-compete, publicity, audit, notices, entire agreement, variations.

## Traps to always look for

**Asymmetry.** A cap, termination right, cure period, notice right, indemnity or assignment right that exists for one side only. Compare each "Supplier" clause with its "Customer" counterpart.

**Incorporation by reference.** For example "subject to the AUP at [URL]", "as updated from time to time" or "Supplier's then-current policies". You can't review what you can't see, and it may change. List each one under `# Not reviewed`, ask for a copy, and push for PB-AMEND-001 protection.

**Order of precedence.** Online terms that override the signed agreement. A purchase order that brings in the buyer's standard terms.

**Entire agreement versus promises.** Features, discounts or service levels that sales promised but aren't in the contract will be wiped out by the entire-agreement clause. Ask the user what was promised.

**Renewal mechanics.** Automatic renewal combined with a long notice period, renewal for the original multi-year term, or renewal at list price. Always calculate the actual notice deadline and put it in `# Key dates`.

**Sole-remedy clauses.** For example "Service credits are the sole and exclusive remedy". These quietly turn an SLA into a ceiling.

**"Fees paid" versus "fees paid and payable".** A cap on fees *paid* in the last 12 months is close to zero early in the term.

**Indirect loss.** "Loss of data" or "loss of business" listed as indirect, which wipes out the main risk of a data service.

**Indemnity breadth.** "Any and all losses arising out of or relating to this Agreement". That turns an indemnity into unlimited liability for any breach.

**Hidden restrictive covenants.** Non-competes, customer non-solicits, exclusivity or standstills inside NDAs, freelance contracts and reseller terms.

**IP grabs.** Assignment of "all work product including pre-existing materials", "whether or not created for Client", or ownership passing before payment.

**Data use.** "Improve our services", "aggregate data", "machine learning". Check what the supplier may do with your data during and after the term.

**Unilateral changes.** "Supplier may modify these terms by posting...", or continued use counting as acceptance.

**Number mismatches and blanks.** "thirty (60) days", "[●]", "____". These come from `scan_contract.py`. Raise them all; never guess which number was meant.

**Cross-references.** "Subject to clause 14.3" when there is no 14.3, or it points to the wrong clause after renumbering.

**Defined-term drift.** "Vendor" in one clause and "Supplier" everywhere else; a capitalised term that is never defined.

**Survival.** Which clauses survive termination: confidentiality, indemnities, payment, liability. Missing survival can wipe out protections at the moment you need them.

**Notices.** Notice by email allowed or not? A required physical address? Failing a formal notice requirement can make a non-renewal notice invalid.

## Type-specific focus

| Type | Must not miss |
|---|---|
| **NDA** | Mutuality; breadth of the definition and its exceptions; term and survival; residuals; hidden non-solicit, non-compete or standstill; compelled disclosure; return and destruction; no licence and no obligation to proceed |
| **SaaS / subscription** | Auto-renewal and notice; price increases; suspension; SLA and sole remedy; data use and AI training; data export at exit; liability cap for data breaches; unilateral changes; DPA and sub-processors |
| **MSA + SOW** | Order of precedence; change control; acceptance; who owns deliverables; termination of individual SOWs; rate changes; non-solicit |
| **DPA** | Roles (processor or controller); sub-processor approval; breach notice time; international transfers; audit; deletion; liability under the DPA (often outside or inside the main cap) |
| **Freelance / services (selling)** | Acceptance and deemed acceptance; payment trigger and days; revisions; kill fee; pre-existing IP; IP only on payment; non-compete; portfolio use; late payment |
| **Supply / vendor terms (buying)** | Delivery, risk and title; warranties; recall; minimum volumes; exclusivity; price changes; termination for supplier failure |
| **Reseller / partnership** | Exclusivity and territory; minimum targets; pricing and margin changes; brand use; termination and what happens to customers; non-compete |

## Out of scope: say so and recommend a lawyer

- Employment contracts and settlement agreements, consumer contracts, real estate, loans and security, M&A, litigation and settlement documents, and regulated industries (financial services, healthcare and similar). These need specialist and jurisdiction-specific advice. You may still give a plain-English summary and point out obvious issues, labelled clearly as a first pass, with `overall: escalate`.
- Questions like "is this enforceable?" or "what are my legal rights?". Explain the general principle and the risk, but don't give an opinion on enforceability; recommend a lawyer qualified in the governing law.
