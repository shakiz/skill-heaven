# Delivery answers

## ANS-DEL-001: Development methodology
tags: agile, scrum, methodology, sprints, delivery approach, iterations
last_reviewed: 2026-06-10
owner: Head of delivery
approved_for: external

We work in Scrum with two-week sprints. Each sprint ends with a demo to the client's product owner, who prioritises the backlog. A typical team: product owner (client), delivery manager, 3-6 developers, UX designer and QA engineer. We start every project with a 2-4 week discovery phase to confirm scope, architecture and the release plan.

## ANS-DEL-002: Project governance and reporting
tags: governance, steering committee, reporting, status, risk management, project management
last_reviewed: 2026-06-10
owner: Head of delivery
approved_for: external

Governance has three levels: a monthly steering committee (sponsors, budget, risks), a weekly status meeting (delivery manager and client project lead) and daily team stand-ups. Clients receive a written status report every two weeks covering progress, budget burn, risks and decisions needed. Risks are tracked in a shared register.

## ANS-DEL-003: Accessibility (WCAG)
tags: accessibility, wcag, wcag 2.1, aa, universal design, screen reader, en 301 549
last_reviewed: 2026-06-10
owner: Accessibility specialist
approved_for: external

We design and build to WCAG 2.1 level AA (EN 301 549) by default. Accessibility is part of our definition of done: designs are reviewed for contrast and structure, every sprint runs automated checks (axe) in CI, and our accessibility specialist does manual testing with keyboard and screen readers (NVDA, VoiceOver) before each release. We deliver an accessibility statement draft for the client to publish.

## ANS-DEL-004: Quality assurance and testing
tags: qa, testing, test automation, quality, unit tests, regression, uat
last_reviewed: 2026-06-10
owner: Head of QA
approved_for: external

Every team includes a QA engineer. We target at least 80% unit test coverage on business logic, automate regression tests with Playwright, and run performance tests before go-live. The client runs user acceptance testing (UAT) supported by our test plan and defect triage.

## ANS-DEL-005: Documentation and handover
tags: documentation, handover, knowledge transfer, exit, source code, ownership
last_reviewed: 2026-06-10
owner: Head of delivery
approved_for: external

We deliver architecture documentation, an operations runbook and user guides. All source code lives in the client's own repository from day one, so the client owns the code. At the end of an engagement we run a structured knowledge transfer of up to 10 working days to the client or a new supplier.

## ANS-DEL-006: Support and maintenance SLA
tags: support, maintenance, sla, service level, response time, helpdesk, 24/7, incident, p1
last_reviewed: 2026-06-10
owner: Head of support
approved_for: external

Standard support hours are 08:00-17:00 CET on Danish business days. Response times: P1 (service down) 1 hour, P2 (major function impaired) 4 hours, P3 next business day, P4 within 5 business days. Out-of-hours on-call for P1 incidents is available as an add-on (see pricing). Uptime target for hosted solutions: 99.5% monthly.

## ANS-DEL-007: Cloud and DevOps
tags: devops, ci/cd, cloud, infrastructure as code, kubernetes, monitoring, deployment
last_reviewed: 2026-06-10
owner: Head of DevOps
approved_for: external

We automate builds, tests and deployments with CI/CD pipelines (GitHub Actions or Azure DevOps) and manage infrastructure as code with Terraform. Applications run on managed container services (Azure Container Apps, AKS or AWS ECS). Monitoring and alerting use Azure Monitor / CloudWatch and Grafana.

## ANS-DEL-008: UX and user research
tags: ux, design, user research, usability testing, service design, citizens, users
last_reviewed: 2026-06-10
owner: UX lead
approved_for: external

Our UX team runs user interviews and usability tests with real end users in discovery and before each major release (typically 5-8 participants per round). We build clickable prototypes in Figma and maintain a design system shared between design and code.
