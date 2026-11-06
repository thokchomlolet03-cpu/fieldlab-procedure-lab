# 08 — Legal, security, privacy, IP and risk management
**Planning checklist only, not legal advice. Obligations depend on jurisdiction, customers, contracts and work permission.**

## Day-zero red lines
- Existing repo is PUBLIC. Never publish proprietary employer SOPs, bank/customer records, employee data, client names, personal contacts, confidential interview transcripts, API keys, private finances or contracts.
- Work on personal devices/accounts in personal time. Review employment contract for side activities, intellectual-property assignment, restrictive covenants and conflicts of interest. Seek local advice before commercial activity.
- Document ownership and licenses of existing MIT FieldLab code, later contributions, model use, dependencies, artwork and borrowed code. Commercial use requires correct third-party licensing and IP chain.
- Don't sell “guaranteed safe/compliant procedures,” financial/medical regulatory assurance, or automated determinations. Human approver remains accountable for rule meanings.

## Before any live customer-data pilot
Obtain explicit permission and scope. Prefer fictionalized scenarios. Record data classes, ownership, controller/processor roles as applicable, reason for processing, location, retention, deletion, sub-processors and model vendor use. Limit collection to minimum necessary. Provide customer-approved confidentiality/data handling terms and access controls. Never pipe client text to public model services without authorization.

## Security gates before hosted multi-client use
HTTPS, authentication and MFA as appropriate, authorization and tenant isolation, secrets management, backups with restore drills, patch/dependency policy, secure logging, input validation, HTML escaping, rate limiting, incident escalation, deletion/export and access review. Threat-model prompt injection and exfiltration through uploaded policy text. No production operation before review.

## Contracts and business readiness
Pilot agreement: deliverables, acceptance, limitations, data treatment, confidentiality, ownership, termination, refunds, responsibilities and liability allocation. Review local licensing, tax/invoicing and employment-authorization requirements before payment. Contractually allocated risk does not necessarily transfer regulatory responsibility from a company to its provider.

## Standing risk register
| Risk | Priority | Gate/mitigation |
|---|---|---|
| AI invented an interpretation | Critical | Suggested only; human approves; explicit abstention |
| Leakage of customer/employer policies | Critical | Synthetic-only public demo, confidential private pilot and permissions |
| Employment IP/moonlighting conflict | Critical | Contract/legal check, personal time/devices, no proprietary assets |
| No customers will pay | High | Interview and payment experiments, stop/pivot gate |
| Existing tools solve problem | High | Head-to-head baseline with generic AI and spreadsheets |
| Multi-tenant exposure | Critical | No hosted multi-client service before security milestone |
| Inaccurate compliance claims | High | Bounded positioning and reviewed representations |
| API/cloud spend growth | Medium | Cost caps and exact measured billing |
| Founder exhaustion | High | Rotating-shift-compatible workload and WIP limits |

## Sources for learning
[FTC small-business cybersecurity](https://www.ftc.gov/business-guidance/small-businesses/cybersecurity) and [NIST CSF](https://www.nist.gov/cyberframework). Reassess jurisdiction-specific law with qualified counsel before real contracts and payments.
