# 03 — FieldLab Policy Test Bench v0.1 (product specification)
## Single user problem
“Did changing our refund/escalation policy change the approved decisions on important boundary and exception cases?”

## Four-screen flow
1. **Procedure editor:** paste short policy, save immutable version, source text, timestamp and content hash. No arbitrary PDFs.
2. **Rule review:** reviewer enters/approves bounded structured rules linked to exact clause; model suggestions marked unapproved and optional. Missing/contradictory rule → unresolved, never pass.
3. **Test bench:** save input scenarios and expected reviewer-approved actions; boundary test generation (day 29/30/31; refund value 99/100/101; missing delivery date). Run deterministic decisions and record discrepancies.
4. **Version comparison:** rerun fixed tests after a policy edit; show changed decisions, mismatches, unresolved cases and source links. Export JSON and human-readable summary with run/version identity.

## Illustrative fiction only
V1: “Refunds may be requested within 30 days. Refunds above $100 require approval.”
V2: “From confirmed delivery, days 0–30 inclusive are eligible; $100 or more needs supervisor approval; missing delivery date requires manual review; otherwise deny.”
These are fictional test cases, not legal guidance or claims about actual client procedures.

## Minimum data model
Procedure(id), Version(id, procedure_id, source_text, hash, timestamp), Rule(id, version_id, span, expression, approval_state), TestCase(id, inputs, expected_action, approval), Run(id, version_id, testcase_id, actual_action, error, code_version, timestamp). Preserve old versions and provenance.

## Demo acceptance criteria
- Local zero-API-key demonstration.
- New tester can save/edit/reopen two versions and run five scenarios.
- Correct deterministic boundary handling for all golden cases.
- Unknown inputs, contradictions, model errors and missing labels result in unresolved/abstain.
- Export retains source links and failed runs; cannot silently overwrite history.
- At least three unassisted external usability observations recorded.
- Clear disclaimer: tested coverage is not full policy correctness, absence of ambiguity or regulatory compliance.

## Not in v0
Customer SSO, billing, data uploads, automatic live decision approvals, unrestricted SOP understanding, multi-agent reasoning, enterprise integrations, mobile app, hosted multi-tenant service, multilingual policy analysis and compliance certificates.

## Differentiation to test
Against (a) manual spreadsheet and (b) capable general AI + prompt: correctness on fresh independently validated cases, review time, missed issues, false alarms, explanation traceability and willingness to use again. If not demonstrably better, rethink the product.
