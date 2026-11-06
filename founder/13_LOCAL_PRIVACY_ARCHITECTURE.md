# 13 — Local-first privacy, enterprise deployment and threat model
**Working design, not a security certification.** Device-local processing can greatly reduce third-party exposure if ALL data paths are controlled.

## Deployment patterns
| Mode | Processing location | Main advantages | Main problems |
|---|---|---|---|
| No AI, local deterministic | User machine | Predictable, cheap per run, offline, smallest attack surface | Human labor; cannot parse arbitrary policy |
| AI on individual laptop | User machine | Sensitive input need not leave device | Memory, installation, patching, theft/compromise, uneven quality |
| AI on customer's own managed server | Organization network | Central model control, shared hardware, audit | IT ownership, internal authorization/security, infrastructure |
| Hosted API (opt-in) | Third-party provider | Stronger model access, zero customer hardware | Data transfer, retention, provider terms, cost, geographic compliance |

## Data flow requirements
- Local policy text; immutable version history, accepted rules, test data, model proposals and exports have classifications and retention dates.
- App must not send content to telemetry/crash or analytics by default. Any update checker/download network activity must be explicit and not carry policy content.
- No upload to external LLM by default; cloud mode requires customer-configured approval and policy.
- Logs should record timestamps, model digests, tool versions, process state and error codes without raw confidential content by default.
- API/frontend/exports/backup all need access controls and secure storage; endpoint full-disk encryption and machine access matter.
- Work in one organization: role-based reviewer approvals and tamper-evident/auditable changes. Never claim cryptographic tamper evidence without actual verified implementation.
- For hosted multi-tenant product: tenant isolation, authentication, permission testing, retention/deletion, backups, incident response, subcontractor review and enterprise assessment BEFORE deployment.

## Threat scenarios
1. Malicious or misleading instructions embedded in a policy prompt → parse policy as untrusted data and restrict model tool access.
2. Inference app logs full policy or prompts → disable/redact logs and test with unique canary strings.
3. Laptop stolen or malware compromised → encrypted disks, OS patching, least privilege, no assumption local == secure.
4. Model update changes output silently → pinned digest and regression test before rollout.
5. Exported report leaks sensitive content → redaction/default minimal export, user awareness and permissions.
6. AI gives an apparently confident incorrect answer → explicit unapproved status and expert verification.
7. Company cloud backup copies local files → app storage location, backup policy and deletion assessment.
8. Supposed local API actually falls back to remote provider → network packet inspection and offline functional test; no implicit fallback.
9. App licenses or models permit uses differently → audit current terms for model weights, distribution, commercial use, libraries and dependencies.

## Practical acceptance tests
- Set unique canary string in fictional policy, run offline, inspect network and logs for leakage.
- Fail local-model request, observe visible error and NO silent network fallback.
- Corrupt/contradict a policy rule, verify report says unresolved and previous evidence is intact.
- Restart, restore and export; verify sensitive raw text not unintentionally included in diagnostics.
- Run under non-admin account and document requested permissions.
- Record explicit model and dependency license notices in distributor build.

## Initial risk management references
[NIST small-business CSF 2.0 quick start](https://csrc.nist.gov/pubs/sp/1300/final) · [OWASP ASVS](https://asvs.owasp.org/) · [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) · [FTC cybersecurity guidance](https://www.ftc.gov/business-guidance/small-businesses/cybersecurity).
