---
tags: [skill-creator]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

can you turn this into my standup for our Teams channel? jira is acme.atlassian.net

ok so yesterday — spent most of the morning chasing that flaky checkout test (CHK-88), turned out to be a timezone thing in the fixture, fixed + merged. had the usual 1:1 with Marco and standup. afternoon paired w/ Lena on CHK-91 the guest checkout address validation, we got the postcode regex done but not the country-specific stuff. also reviewed like 3 small PRs, nothing big. answered some questions in #frontend about the new button component.
today: continue CHK-91 country rules, then maybe start on CHK-95 if time. nothing blocking really
