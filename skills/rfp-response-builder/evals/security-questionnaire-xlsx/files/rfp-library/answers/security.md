# Security answers

## ANS-SEC-001: Encryption of data at rest and in transit
tags: security, encryption, aes, tls, data protection, at rest, in transit
last_reviewed: 2026-05-14
owner: Security lead
approved_for: external

All data is encrypted in transit with TLS 1.2 or higher (TLS 1.3 preferred) and at rest with AES-256, using the cloud provider's managed key services (Azure Key Vault or AWS KMS). Keys are rotated at least annually. Backups are encrypted with the same standard.

## ANS-SEC-002: Access control and authentication
tags: access control, mfa, multi-factor, authentication, least privilege, sso, identity
last_reviewed: 2026-05-14
owner: Security lead
approved_for: external

Access follows least privilege and is role-based. Multi-factor authentication is mandatory for all employees on all internal systems and cloud consoles. Access rights are reviewed quarterly and removed within 24 hours when an employee leaves. Production access is restricted to named DevOps engineers and logged.

## ANS-SEC-003: Penetration testing
tags: penetration test, pentest, vulnerability, security testing, third party
last_reviewed: 2025-02-10
owner: Security lead
approved_for: external

We commission an independent penetration test of our internal infrastructure annually; the most recent was performed by SecureNorth A/S in January 2025 with no critical findings open. For client solutions we recommend and can arrange a third-party penetration test before go-live.

## ANS-SEC-004: GDPR and data processing
tags: gdpr, privacy, data processing agreement, dpa, personal data, dpo
last_reviewed: 2026-06-02
owner: DPO
approved_for: external

We act as data processor under a Data Processing Agreement (DPA) based on the Danish Data Protection Agency's template. We have a designated Data Protection Officer, keep records of processing, and run privacy-by-design reviews at solution design. Personal data is processed and stored within the EU/EEA only.

## ANS-SEC-005: Security incident response
tags: incident, breach, notification, incident response, security event
last_reviewed: 2026-05-14
owner: Security lead
approved_for: external

We operate a documented incident response procedure aligned with ISO 27001. Clients are notified of any security incident affecting their data without undue delay and no later than 24 hours after detection, enabling the client to meet the GDPR 72-hour notification duty.

## ANS-SEC-006: Backup and disaster recovery
tags: backup, disaster recovery, dr, rpo, rto, business continuity, bcp
last_reviewed: 2026-05-14
owner: Security lead
approved_for: external

Standard hosting setup: automated backups every hour with point-in-time restore, retained for 35 days, stored in a second availability zone. Target RPO 1 hour and RTO 4 hours. Restore tests are performed twice a year. A business continuity plan covering loss of an office or key supplier is tested annually.

## ANS-SEC-007: Secure development lifecycle
tags: secure development, sdlc, owasp, code review, sast, dependency scanning, devsecops
last_reviewed: 2026-05-14
owner: Security lead
approved_for: external

Developers follow OWASP ASVS level 2 as the default standard and receive annual secure-coding training. Every change is peer reviewed. CI pipelines run static analysis (SonarQube) and dependency vulnerability scanning (Dependabot / Snyk); builds with high-severity findings are blocked.

## ANS-SEC-008: Hosting and data residency
tags: hosting, cloud, azure, aws, data residency, data location, eu, sub-processors
last_reviewed: 2026-05-14
owner: Security lead
approved_for: external

We host on Microsoft Azure (West Europe / North Europe) or AWS (Frankfurt / Stockholm), per client preference. All data stays in the EU. Our sub-processor list (cloud providers, monitoring tools) is maintained and shared with clients; changes are notified 30 days in advance.

## ANS-SEC-009: Monitoring coverage (internal note)
tags: soc, 24/7, monitoring, security operations centre, siem
last_reviewed: 2026-05-14
owner: Security lead
approved_for: internal-only

Internal: we do not run a 24/7 SOC. Alerting is monitored during business hours (08-17 CET) with on-call for P1 alerts only on contracts that pay for on-call. Do not claim 24/7 monitoring; offer on-call or a partner SOC as an option, priced separately.

## ANS-SEC-010: Data location (from 2024 Nordlys proposal)
tags: data location, hosting, countries, residency, sweden, norway
last_reviewed: 2024-03-12
owner: Security lead
approved_for: external

For Nordlys Insurance all data is hosted in AWS Stockholm (Sweden) and never leaves the Nordics. Nordlys's claims data is backed up to a second AWS region in Ireland.
