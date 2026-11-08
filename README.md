# Skill Heaven

Claude Skills for marketing, business and HR teams. Each skill packages company know-how, an expert's procedure and helper scripts, so anyone can produce work to house standard every time.

## Skills

| Skill | What it does | Status |
|---|---|---|
| [`rfp-response-builder`](skills/rfp-response-builder/) | Turns RFPs, tenders and security questionnaires into tailored proposals from an approved answer library. Outputs a Word proposal, an Excel compliance matrix and a gap list. Also runs bid/no-bid checks. | Iteration 1 tested |

## Research

[`claude-skills-marketing-business-hr-analysis.md`](claude-skills-marketing-business-hr-analysis.md) maps the main pain points in marketing, business and HR. It proposes 30 skills, ranked by business value and by impact versus effort, with a roadmap, design principles and risks.

## Using a skill

1. Copy the skill folder (e.g. `skills/rfp-response-builder/`) into your Claude skills directory (`~/.claude/skills/` for Claude Code), or upload it as a skill in Claude.ai.
2. Fill in the skill's content folder. For `rfp-response-builder`, that is `library/`: see [`library/README.md`](skills/rfp-response-builder/library/README.md) for what to collect.
3. Ask Claude naturally, e.g. *"Here's the RFP from Acme, draft our response"*.

Scripts need Python 3.9+ with `python-docx` and `openpyxl` (`pip install python-docx openpyxl`).

## Tests

Each skill has test cases in `evals/`, in the format `claude plugin eval` reads. The sample data in them belongs to a fictional company (Northwind Digital).
