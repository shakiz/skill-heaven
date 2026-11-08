# Risk allocation

## PB-LIAB-001: Limitation of liability (we buy)
applies_to: msa, saas, services, consulting, sow, supply, vendor, dpa
role: customer
priority: must-have
last_reviewed: starter
owner: set an owner

**Standard:** A mutual cap of at least the fees paid and payable in the 12 months before the claim. The cap does not apply to breach of confidentiality, data protection breaches, IP infringement indemnities, fraud, wilful misconduct, or death and personal injury caused by negligence.
**Fallback:** A 12-month cap with a separate higher cap (2–3x annual fees) for data protection and confidentiality breaches.
**Walk-away:** The supplier's cap is below 6 months' fees, or our liability is uncapped while theirs is capped.
**Red flags:** Caps on one party only; "fees paid in the three (3) months"; caps by reference to fees "paid" (not "payable") early in the term; data loss excluded as "indirect loss".
**Preferred language:** Each party's total aggregate liability arising out of or in connection with this Agreement shall not exceed the total fees paid and payable under this Agreement in the twelve (12) months preceding the event giving rise to the claim.

## PB-LIAB-002: Limitation of liability (we sell)
applies_to: msa, saas, services, consulting, sow, supply, vendor, freelance
role: vendor
priority: must-have
last_reviewed: starter
owner: set an owner

**Standard:** A mutual cap equal to the fees paid in the 12 months before the claim. Both parties exclude indirect and consequential loss and loss of profit. Unlimited only for what law doesn't allow to be limited (fraud, death and personal injury).
**Fallback:** A cap of 1.5–2x annual fees, or a separate super-cap for data protection breaches.
**Walk-away:** Uncapped liability for us (other than the legal minimum), or uncapped indemnities.
**Red flags:** No cap at all; caps that apply only to the customer; uncapped "breach of any obligation relating to data"; liquidated damages or penalties.
**Preferred language:** Subject to clause [X] (unlimited liability), each party's total aggregate liability arising out of or in connection with this Agreement shall not exceed the total fees paid under this Agreement in the twelve (12) months preceding the event giving rise to the claim.

## PB-LIAB-003: Exclusion of indirect loss
applies_to: msa, saas, services, consulting, sow, supply, vendor, freelance
role: any
priority: important
last_reviewed: starter
owner: set an owner

**Standard:** Mutual exclusion of indirect and consequential loss. For a customer: loss or corruption of our data, and the cost of restoring it, is recoverable direct loss.
**Fallback:** Accept the exclusion of lost profit if data restoration costs stay recoverable.
**Walk-away:** The exclusion benefits only one party.
**Red flags:** "loss of data" listed as excluded (when we buy); "any loss whatsoever" exclusions; exclusions that also cover payment of fees (when we sell).
**Preferred language:** Neither party shall be liable for any indirect or consequential loss, or for loss of profits, revenue or goodwill, arising out of or in connection with this Agreement.

## PB-IND-001: Indemnities
applies_to: msa, saas, services, consulting, sow, supply, vendor, freelance
role: any
priority: must-have
last_reviewed: starter
owner: set an owner

**Standard:** Indemnities are limited to third-party claims. Supplier side: IP infringement by the product or deliverables. Customer side: content or data the customer provides. The indemnified party must notify promptly, let the indemnifier conduct the defence, and mitigate.
**Fallback (we sell):** An uncapped IP indemnity if we control the defence and can modify, replace or refund.
**Walk-away:** Indemnities for "any breach of this Agreement" or for any loss (not only third-party claims); uncapped indemnities against us beyond IP.
**Red flags:** "indemnify, defend and hold harmless ... from any and all losses ... arising out of or relating to this Agreement"; indemnities covering the other party's own negligence; no conduct-of-claims procedure.
**Preferred language:** Supplier shall defend Customer against any third-party claim alleging that the Services infringe that third party's intellectual property rights, and shall indemnify Customer against damages finally awarded or agreed in settlement, provided that Customer promptly notifies Supplier, gives Supplier sole control of the defence and settlement, and provides reasonable assistance.

## PB-WAR-001: Warranties and disclaimers
applies_to: msa, saas, services, consulting, sow, supply, vendor
role: customer
priority: important
last_reviewed: starter
owner: set an owner

**Standard:** The supplier warrants that services are performed with reasonable skill and care, that the product materially conforms to its documentation, and that it doesn't introduce malicious code. The remedy is re-performance or a fix, then termination and a refund.
**Fallback:** A 90-day warranty on deliverables. Other implied terms may be excluded if these express warranties stay.
**Walk-away:** Everything provided "as is" with no warranty at all for a paid service.
**Red flags:** "AS IS" and "AS AVAILABLE"; "sole and exclusive remedy" limited to service credits; disclaimers that the service will work as described.
**Preferred language:** Supplier warrants that the Services will be performed with reasonable skill and care and will conform in all material respects with the Documentation.

## PB-SLA-001: Service levels and credits
applies_to: saas, msa, services
role: customer
priority: important
last_reviewed: starter
owner: set an owner

**Standard:** At least 99.5% monthly availability, with defined support response times. Service credits apply automatically and do not stop us claiming damages. Persistent failure (e.g. missing the SLA 3 months in a row) gives us a termination right.
**Fallback:** Credits as the sole financial remedy for minor shortfalls, but we keep the termination right for chronic failure.
**Walk-away:** No commitment to availability for a business-critical service.
**Red flags:** "Service credits are Customer's sole and exclusive remedy"; credits only on request within 5 days; long lists of exclusions; "scheduled maintenance" without limits.
**Preferred language:** Service credits are without prejudice to Customer's other rights and remedies. If Supplier fails to meet the Availability target in any three (3) consecutive months, Customer may terminate this Agreement on written notice.

## PB-INS-001: Insurance
applies_to: msa, services, consulting, sow, supply, vendor
role: any
priority: nice-to-have
last_reviewed: starter
owner: set an owner

**Standard:** Each party keeps insurance appropriate to its obligations: professional indemnity and public liability (and cyber, for data processors). Amounts are reasonable and certificates are provided on request.
**Fallback (we sell):** Accept the specific amounts the customer asks for if we already hold them.
**Walk-away (we sell):** Insurance amounts we don't hold, or that would cost more than the deal is worth.
**Red flags:** Naming the other party as co-insured; insurance amounts presented as a minimum liability.
**Preferred language:** Each party shall maintain, with reputable insurers, insurance appropriate to its obligations under this Agreement, and shall provide evidence of cover on reasonable request.

## PB-FM-001: Force majeure
applies_to: msa, saas, services, consulting, sow, dpa, supply, vendor, freelance, reseller, partnership, licence, license
role: any
priority: nice-to-have
last_reviewed: starter
owner: set an owner

**Standard:** Mutual relief for events beyond reasonable control, with prompt notice and a duty to mitigate. Either party may terminate if the event lasts more than 60 days. Payment obligations for services actually received are not excused.
**Fallback:** 90 days before termination rights apply.
**Walk-away:** Force majeure that benefits one party only, or that covers the supplier's own subcontractors and failures in its own systems.
**Red flags:** "including labour disputes of Supplier's own staff"; "failure of Supplier's suppliers"; no termination right for prolonged events.
**Preferred language:** If a Force Majeure Event prevents a party from performing for more than sixty (60) days, the other party may terminate this Agreement on written notice.
