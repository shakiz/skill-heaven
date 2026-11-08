---
name: rfp-response-builder
description: Builds tailored, source-grounded responses to RFPs, RFIs, RFQs, tenders, security/vendor questionnaires and client proposal requests from the company's own approved answer library. Extracts every requirement, drafts answers from approved content, tailors them to the client, flags gaps for subject-matter experts, and outputs a Word proposal plus an Excel compliance matrix. Also sets up the answer library from past proposals, runs bid/no-bid assessments, fills clients' questionnaire spreadsheets, and harvests finished proposals back into the library. Use this skill whenever the user shares or mentions an RFP, tender, bid, procurement document, request for proposal/information/quotation, vendor or security questionnaire, due-diligence questionnaire, statement of work request, or asks to write, answer, review or qualify a proposal for a client, or to organize past proposals into reusable content, even if they don't use the word "RFP".
---

# RFP Response Builder

Turn a client's RFP (or questionnaire, tender, proposal request) into a complete, tailored, verifiable response that a bid team can review and submit.

The value of this skill comes from two things, and both matter more than polished prose:

1. **Nothing is invented.** Every factual claim (certifications, numbers, client names, team members, prices, timelines, service levels) comes from the user's approved library or from the user. A fabricated certification, reference or price can disqualify the bid or create a contractual liability. When the library has no answer, the right output is a clearly marked gap, not a plausible guess. This includes commitments the client asks for: if the RFP demands 24/7 support and the library offers business hours, the answer states the real offering and marks an exception. It never agrees "subject to approval" in client-facing text.
2. **Nothing is missed.** Evaluators score against their own requirement list. Every requirement gets a tracked status, so a missed mandatory item is caught before submission.

## Where things live

The skill folder itself may be read-only, so **never store the user's content or outputs inside it.**

- **Answer library** (the user's approved content): find it in this order:
  1. a path the user names;
  2. `./rfp-library/` in the current working directory;
  3. any folder nearby whose `.md` files contain entries like `## ANS-SEC-001: Title` (`search_library.py --list` confirms).
  If none exists, say so and offer **Setup mode** before drafting. See `references/library-format.md` for the format.
- **Outputs**: `./rfp-output/<client-slug>/` unless the user names another folder.
- **The RFP**: any format. Read `.md`, `.txt` and `.pdf` directly; run `scripts/extract_text.py` for `.docx` and `.xlsx`.

## Choose the mode

| User wants | Mode | Main output |
|---|---|---|
| To start using the skill, or has no library yet | **Setup** | A library in `./rfp-library/` built from their past proposals |
| A full proposal for an RFP | **Full response** (steps 1–8) | `proposal.docx`, `compliance-matrix.xlsx`, `gaps.md` |
| To fill a client's spreadsheet questionnaire (security, vendor, DDQ) | **Questionnaire** | The client's own `.xlsx`, filled in, plus `gaps.md` |
| To decide whether to bid | **Bid/no-bid** (steps 1–2 only) | `bid-assessment.md` |
| One or a few questions answered | **Quick answer** (steps 4–5 inline) | Answers in chat, with sources |
| To add a finished proposal's content to the library | **Harvest** | New library entries |

When the request is ambiguous, pick the most likely mode, say which one you picked, and proceed.

## First-time check (all modes)

Install the script dependencies once, quietly: `python3 -m pip install -q -r <skill-dir>/requirements.txt` (use `python` if `python3` is not found). If Python or the install isn't available, follow **Without scripts** at the end. The skill still works, just with markdown and CSV outputs instead of Word and Excel.

## Setup mode: build the library from past proposals

A new user's library is empty. This mode decides whether the skill is useful on day one, so make it smooth.

1. Run `python scripts/init_library.py ./rfp-library` to create the folder structure and guides.
2. Ask for 3–10 past proposals (winning ones first), questionnaire answers, the company profile, CVs and rate cards. Any format works; use `extract_text.py` where needed.
3. Read them and extract reusable entries: company facts, certifications (with expiry dates), standard answers by topic, case studies, team summaries, and pricing rules. Follow `references/library-format.md`:
   - **Generalize** answers: remove the old client's name and specifics.
   - **Keep facts exact.** When two sources disagree (an older proposal says 120 employees, a newer one 140), keep the newest. Note the conflict in the entry's `owner` check list and in the summary to the user.
   - Set `last_reviewed` to the date of the source document, not today. Content copied from an old proposal is only as current as that proposal.
   - Mark pricing rules, margins, discount limits and internal weaknesses `approved_for: internal-only`.
   - Get the next free ID with `search_library.py --library ./rfp-library --next-id ANS-SEC`.
4. Show the user a short table of proposed entries (ID, title, source document, any conflict or uncertainty). Write them after the user approves, or straight away if the user asked you to just do it, then list what still needs owner review.
5. Finish with a **coverage report**: which of the common RFP topics the library now covers, and what's missing. The common topics are company profile, certifications, insurance, financials, security, GDPR/privacy, delivery method, QA, accessibility, support SLA, hosting, case studies, team and pricing. Missing topics are the next things to collect.

If the user has no documents at all, interview them briefly about the high-value basics instead: company profile, certifications, insurance, 2–3 case studies, support SLA and rate card. Write those as entries.

## Full response workflow

The working file is `response.md` in the output folder. Every script reads it. Read `references/response-format.md` before creating it. Append requirement blocks as you go; don't write the whole file at once.

### 1. Intake

Fill the `# RFP` block: client, title, reference, deadline, submission format, page or word limits, language, evaluation criteria with weights, client goals, and mandatory pass/fail conditions.

Ask the user only what you can't find and genuinely need, usually at most 3 questions (relationship with the client, known competitors, pricing approach). If the user wants you to proceed, record your assumptions in `assumptions`.

### 2. Bid/no-bid check

Score the opportunity with `references/go-no-go.md` and fill the `# Bid` block. Show the result in 3–5 lines. If it's a clear no-bid (for example, a mandatory requirement you cannot meet), say so before drafting. The user decides whether to continue.

### 3. Extract every requirement

Add one `# Requirement <id>` block per requirement, question, form or pricing item:
- Keep the RFP's numbering, and copy the text **verbatim** into `text:`. Evaluators match responses to their own wording.
- Split compound items ("describe X and provide Y") into sub-items (`4.2a`, `4.2b`). Compound questions are where answers most often go half-done.
- Set `mandatory: yes` for "must / shall / required / pass-fail" language, and record any `word_limit`.
- Include instructions hidden in prose, such as "proposals must include CVs".

### 4. Match to the library

```bash
python scripts/search_library.py --library ./rfp-library --query "<key words of the requirement>" --top 5
python scripts/search_library.py --library ./rfp-library --id ANS-SEC-004     # full text of one entry
```

Record the entries you use in `sources`. The script flags `STALE` entries (expired, or not reviewed in 12 months) and `INTERNAL-ONLY` ones. Stale facts get `[VERIFY]`. Internal-only entries guide your judgment, for example what not to promise, but their wording and internal facts never appear in the answer. If nothing fits, set `status: gap`, say in `notes` exactly what an expert must supply, and name an `owner` role.

### 5. Tailor and write

Read `references/writing-guide.md`. In short:
- **Answer first**, in the evaluator's terms. Then give evidence from the library, then the benefit for this client.
- **Tailor** to the client's stated goals and context, and use 2–4 win themes consistently.
- **Stay within word and page limits.**
- **Keep facts locked.** You may rephrase and shorten library content. You may not change numbers, certifications, names, prices or commitments. Anything uncertain gets `[VERIFY: what to check]` inline.
- **Never invent a price.** Quote rates and prices that are in the library. Totals that need an estimate (a fixed price, a monthly fee) stay `[VERIFY: …]` with the inputs an estimator needs, and go to an owner.
- **Be honest about compliance.** Use `comply`, `partial` or `exception`. A hidden non-compliance found after award is worse than a stated exception.

Write the narrative sections the RFP asks for as `# Section:` blocks, or this default set: executive summary, understanding of needs, solution/approach, delivery and timeline, team, relevant experience, commercials.

### 6. Validate

```bash
python scripts/check_response.py rfp-output/<client>/response.md --library ./rfp-library [--forbid "Old Client"]
```

The script reports unanswered mandatory items, unsourced answers, unknown or stale sources, internal-only sources, placeholders, word-limit breaches and forbidden names. Pass `--forbid` for every *other client* named in the library's case studies or reused answers (not suppliers or partners such as your pen-test vendor or cloud provider, which may legitimately appear). A leftover client name is a common, embarrassing error. Fix what you can and rerun; what remains is a real gap.

### 7. Build the deliverables

```bash
python scripts/build_proposal.py rfp-output/<client>/response.md -o rfp-output/<client>/proposal.docx [--template house.docx] [--company "Name"]
python scripts/build_matrix.py rfp-output/<client>/response.md -o rfp-output/<client>/compliance-matrix.xlsx
```

Write `gaps.md`: one row per gap or `[VERIFY]` item, with the requirement ID, what is needed, the owner, and whether it is mandatory. Each row must make sense on its own, because the bid manager forwards it.

### 8. Hand over

Tell the user, briefly:
- Coverage: X of Y answered, Z partial, N gaps (M mandatory).
- Bid score and main risks.
- Where the files are.
- The 3 most important next actions, each with an owner.

## Questionnaire mode

The answers go into **the client's own file and layout**. Inspect the sheet to find the question-ID, answer and compliance columns. Then do steps 1, 3, 4 and 5, with one requirement block per row (use the row's ID, or `R<row number>` if there is none). Short answers suit spreadsheets: Yes/No/Partial where the question invites it, then 1–3 sentences of evidence.

```bash
python scripts/check_response.py rfp-output/<client>/response.md --library ./rfp-library --mode questionnaire
python scripts/fill_questionnaire.py client.xlsx rfp-output/<client>/response.md -o rfp-output/<client>/<client-file>-completed.xlsx \
  --sheet "Questions" --id-col A --answer-col D [--compliance-col C] [--first-row 2]
```

A Yes/No column must never say "Yes" while the answer still has `[VERIFY]` in it. Use "Partial", or leave it blank and list it in `gaps.md`.

## Harvest mode

After a proposal is finished (ideally won), propose new reusable entries from it, using the Setup-mode rules. Write them after the user approves. A library that grows with every bid is what makes each future proposal faster.

## Without scripts

If Python can't run, do the same work by hand and produce:
- `proposal.md`, with the same structure as the Word document;
- `compliance-matrix.csv`, with columns ID, Section, Requirement, Mandatory, Compliance, Status, Sources, Owner, Notes;
- `gaps.md`.

Do the checks yourself: mandatory gaps, sources, placeholders, word limits, other clients' names. Tell the user the outputs are markdown and CSV because the scripts couldn't run.

## Reference files

- `references/response-format.md`: the `response.md` format. Read it before step 1.
- `references/library-format.md`: the library structure and entry format. Read it in Setup and Harvest modes, or when the library looks unusual.
- `references/go-no-go.md`: the bid qualification rubric (step 2).
- `references/writing-guide.md`: how to write answers that score (step 5).
