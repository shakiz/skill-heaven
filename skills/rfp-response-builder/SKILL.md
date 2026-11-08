---
name: rfp-response-builder
description: Builds tailored, source-grounded responses to RFPs, RFIs, RFQs, tenders, security/vendor questionnaires and client proposal requests, using the company's approved answer library. Extracts every requirement, drafts answers from approved content, tailors them to the client, flags gaps for subject-matter experts, and outputs a branded Word proposal plus an Excel compliance matrix. Also does bid/no-bid assessments and harvests answers from finished proposals back into the library. Use this skill whenever the user shares or mentions an RFP, tender, bid, procurement document, request for proposal/information/quotation, vendor or security questionnaire, statement of work request, or asks to write, answer, review or qualify a proposal for a client, even if they don't use the word "RFP".
---

# RFP Response Builder

Turn a client's RFP (or questionnaire, tender, proposal request) into a complete, tailored, verifiable response that a bid team can review and submit.

The value of this skill comes from two things, and both matter more than polished prose:

1. **Nothing is invented.** Every factual claim (certifications, numbers, client names, team members, prices, timelines) comes from the approved library or from the user. A proposal with a fabricated certification or reference can disqualify the bid or create a contractual liability. When the library has no answer, the right output is a clearly marked gap, not a plausible guess.
2. **Nothing is missed.** Evaluators score against their own requirement list. Every requirement gets a tracked status, so a missed mandatory item is caught before submission, not after.

## Inputs to locate first

- **The RFP**: any format (PDF, DOCX, XLSX, MD, pasted text). Read all of it, including appendices, evaluation criteria and submission instructions. Those sections decide how the response is scored.
- **The answer library**: by default `library/` inside this skill folder. The user may point to another folder. Read `references/library-format.md` to understand its structure. If no library exists or it is empty, tell the user. You can still draft, but every factual claim must then be marked `[VERIFY]` and the coverage report will show it.
- **House template** (optional): a `.docx` with the company's styles. Pass it to the build script with `--template`.

## Choose the mode

| User wants | Mode | Main output |
|---|---|---|
| A full proposal for an RFP | **Full response** (steps 1–7) | `proposal.docx`, `compliance-matrix.xlsx`, `gaps.md` |
| To fill a client's spreadsheet questionnaire (security, vendor, DDQ) | **Questionnaire** (steps 1, 3–5, then `fill_questionnaire.py`) | The client's own `.xlsx`, filled in, plus `gaps.md` |
| To decide whether to bid | **Bid/no-bid** (steps 1–2 only) | `bid-assessment.md` |
| One or a few questions answered | **Quick answer** (steps 3–5 inline) | Answers in chat, with sources |
| To add a finished proposal's content to the library | **Harvest** (see the end) | New or updated library entries |

When the request is ambiguous, pick the most likely mode, say which one you picked, and proceed.

## Workflow

Work in an output folder (default `./rfp-output/<client-slug>/`). The single source of truth is `response.json`. Every script reads it, so keep it updated as you go. Its schema is in `references/response-schema.md`. Read that file before writing the JSON.

### 1. Intake

Extract into `response.json → rfp`: client, title, reference number, deadline, submission format and channel, page or word limits, language, evaluation criteria with weights, and mandatory pass/fail conditions.

Then ask the user only what you can't find and genuinely need. Usually that's at most 3 questions, for example: the relationship with the client, known competitors, the pricing approach, or which offering to propose. If the user wants you to proceed without answers, proceed and record your assumptions in `rfp.assumptions`.

### 2. Bid/no-bid check

Score the opportunity with `references/go-no-go.md` and record it in `response.json → bid`. Show the result to the user in 3–5 lines. If it's a clear no-bid (for example, a mandatory requirement you cannot meet), say so before investing in a full draft. The user decides whether to continue.

### 3. Extract every requirement

Create one entry per requirement, question, form or pricing item in `response.json → requirements`:
- Keep the RFP's own numbering (`id`) and copy the requirement text **verbatim**. Evaluators match responses to their own wording.
- Split compound items ("describe X and provide Y") into sub-items (`4.2a`, `4.2b`). Compound questions are where answers most often go half-done.
- Mark `mandatory: true` for "must / shall / required / mandatory / pass-fail" language, and capture any `word_limit`.
- Include the instructions hidden in prose, such as "proposals must include CVs of key personnel" in a cover letter section. They count as requirements too.

### 4. Match to the library

For each requirement, search the library:

```bash
python scripts/search_library.py --library <library-dir> --query "<key words of the requirement>" --top 5
python scripts/search_library.py --library <library-dir> --id ANS-SEC-004     # full text of one entry
```

Pick the best entry or entries and record their IDs in `sources`. Prefer recently reviewed entries; the script flags entries older than 12 months as `STALE`. If nothing fits, set `status: gap` and write in `notes` what an expert must supply. Suggest an `owner` role (for example "Security lead", "Delivery manager").

### 5. Tailor and write

Read `references/writing-guide.md`. In short:
- **Answer the question first**, in the evaluator's own terms, then give evidence (from the library), then the client-specific benefit.
- **Tailor**: mention the client's stated goals, context and constraints from the RFP. A generic library answer pasted unchanged loses points to a competitor who tailored.
- **Use 2–4 win themes** (in `win_themes`) and repeat them where they're relevant: the executive summary, approach and key differentiators.
- **Stay within word and page limits.**
- **Keep facts locked.** You may rephrase and shorten library content. You may not change numbers, certifications, names or commitments. Anything you're unsure of gets `[VERIFY: what to check]` inline, so reviewers find it.
- Set `compliance` honestly (`comply`, `partial`, `exception`). A hidden non-compliance discovered after award is worse than a stated exception.

Also write the narrative `sections` the RFP asks for, or a sensible default: executive summary, understanding of needs, proposed solution/approach, delivery and timeline, team, relevant experience, and commercials (pricing only from the library's pricing guidance or the user).

### 6. Validate

```bash
python scripts/check_response.py rfp-output/<client>/response.json --library <library-dir> \
  [--forbid "Old Client Name" --forbid "Competitor"]
```

The script reports unanswered mandatory items, answers without sources, unknown or stale source IDs, leftover placeholders, word-limit breaches and forbidden names. Leftover names of other clients are a common and embarrassing copy-paste error. Fix everything you can, then rerun. Whatever remains is a real gap for humans.

### 7. Build the deliverables

```bash
python scripts/build_proposal.py rfp-output/<client>/response.json -o rfp-output/<client>/proposal.docx [--template house.docx] [--company "Company name"]
python scripts/build_matrix.py rfp-output/<client>/response.json -o rfp-output/<client>/compliance-matrix.xlsx
```

Write `gaps.md`: one row per gap or `[VERIFY]` item, with the requirement ID, what is needed, the suggested owner, and whether it is mandatory. The bid manager forwards this to experts, so make each row understandable on its own.

### 8. Hand over

Tell the user in a short summary:
- Coverage: X of Y requirements answered, Z partial, N gaps (M of them mandatory).
- The bid/no-bid score and the main risks.
- Where the files are.
- The 3 most important next actions, for example "Security lead to confirm penetration-test date (req 5.3, mandatory)".

## Questionnaire mode

When the client sends a spreadsheet to fill in, the answers must go into **their** file and layout. Do steps 1 and 3–5, using the spreadsheet rows as requirements (use the row's question ID, or `R<row number>` if there is none). Then run:

```bash
python scripts/fill_questionnaire.py client.xlsx rfp-output/<client>/response.json -o rfp-output/<client>/client-filled.xlsx \
  --sheet "Questions" --id-col A --answer-col D [--compliance-col C] [--first-row 2]
```

Inspect the sheet first to find the right columns. Short answers suit spreadsheets: lead with Yes/No/Partial where the question invites it, then 1–3 sentences of evidence.

## Harvest mode

After a proposal is finished (ideally won), offer to add new, reusable answers to the library. Propose entries in the library format with new IDs, and let the user approve them before writing. Strip client-specific details from reusable text, and set `last_reviewed` to today. This keeps the library growing, and the library is what makes every future proposal faster.

## Reference files

- `references/response-schema.md`: the `response.json` structure. Read it before step 1.
- `references/library-format.md`: how the answer library is organized. Read it when locating the library or harvesting.
- `references/go-no-go.md`: the bid qualification rubric (step 2).
- `references/writing-guide.md`: how to write scoring answers (step 5).
