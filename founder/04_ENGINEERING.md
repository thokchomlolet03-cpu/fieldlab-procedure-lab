# 04 — Engineering, test and release plan
## Starting point and truth boundary
Original procedure demo and failed model-evaluation results are preserved under procedure_lab/. Do not refactor historical, frozen evidence as though the original work never existed. New commercial prototype code should live in a product/ directory with separate test fixtures, or in a consciously documented successor package.

## Minimal architecture
Python 3.10+, FastAPI (or existing lightweight server), server-rendered HTML with minimal JS, SQLite for local persistence, structured schemas for rules and cases, deterministic decision interpreter, portable JSON/Markdown export. AI adapter is optional and OFF by default. Avoid Kubernetes, GPU hosting, vector databases and multiple autonomous agents.

## Build order
1. Baseline reproduction: run historical tests; archive command, environment and receipts.
2. Define immutable ProcedureVersion and validated Rule/TestCase/Run schemas.
3. Implement human-approval workflow for every rule and expected decision.
4. Build boundary-case generator for approved supported rule syntax; avoid arbitrary semantics.
5. Implement deterministic runner, ambiguity/error/abstention states, source references.
6. Persist and reopen; confirm no overwrites and reproducible exports.
7. Implement version diff and report; human tester can complete without founder help.
8. Separate opt-in model proposal experiment, only after first workflow works.

## Test matrix
- Boundary: day 0/29/30/31; value 99/100/101; exact threshold.
- Missing delivery timestamp; partial/inconsistent data; invalid values; timezone/date ambiguity.
- Contradictions and overlapping rules; review states; unsupported rule expression.
- Input size limit, non-ASCII, HTML escaping and XSS protection.
- Revisions never silently alter historical cases or outcomes.
- Export/re-import fidelity; corrupted storage recovery; reproducibility with recorded commit IDs.
- Absent model/API, timeout, malformed answer → explicit failure, not silent success.

## CI and engineering standards
Write small PRs; use automated unit/integration tests and formatting; pin deps; record source and license; no secrets in repo; simple changelog; manual browser smoke test before external demos. Definition of done: code + tests + failure behavior + evidence link + demo, not simply a merged commit.

## Release gates
Local fictional demo → independent usability → explicit sanitized single-client pilot → (only with security controls/contracts) hosted service. Before any multi-tenant hosting, require authentication, tenant isolation, logs, backup/restore, secrets controls, encryption in transit, access review and penetration/security testing proportionate to risk.

## Documentation
Every test receipt records code commit, case set/version, exact approved rule text or hash, run timestamp, evaluator/model if any, observed outcomes and limitations. No invented performance metrics.
