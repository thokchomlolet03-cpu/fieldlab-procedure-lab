# 12 — Local-model evaluation protocol E-AI-001
**Protocol draft (NOT run, no outcome claims).** Review/freeze before any scored run. Separate this from the old FieldLab eight-case benchmark; that set is already exposed and cannot be a fresh blinded test.

## Research question
Can a small, fully local model generate *valid, source-grounded, discriminating policy test proposals* that let human reviewers catch more consequential ambiguities or spend less time, compared with (A) no AI and (B) a strong general model on authorized non-sensitive cases?

## Stage 0 — hardware and privacy inventory
Record device model, RAM, CPU/GPU/NPU, OS version, local storage, temperature/throttling considerations, runtime/version, model tag, full model hash, quantization, context and actual peak RAM/latency. Run with network disabled where technically safe. Audit if application sends any prompt, telemetry or diagnostics outside device; verify not by product marketing alone.

## Stage 1 — restricted, independently authored dataset
- Initially 20–30 fictional **customer-support refund/escalation policies** across distinct semantic patterns, not repeated paraphrases of one queue rule.
- Include known clear cases, ambiguous terms, edge boundary cases, contradictions, omissions, mixed mechanisms and impossible/unanswerable cases.
- Independent experienced reviewers author or validate ground truth *without seeing model outputs*.
- Each case has original policy, relevant quoted clause, intended competing interpretations, minimum discriminator, expected outcome, expert confidence, disputes.
- Keep separate development and frozen test sets at **procedure-family level**, not random rows from same policy; no synthetic leakage.
- Log unresolved reviewer disagreement instead of forcing fake certainty; preserve source and case hashes.

## Stage 2 — five arms
1. Human using simple checklist/spreadsheet.
2. Human + deterministic supported rules only.
3. Human + Gemma 4 E2B / E4B and optionally 12B.
4. Human + hosted strong model on fictional/sanitized cases only with explicit authorization.
5. Human + FieldLab integrated rule/test workflow.
Use matched budget, same input and task instructions, randomized/blinded order where feasible. A larger model is a quality reference, not necessarily a deployable privacy option.

## Model contract
INPUT: numbered procedure clauses (not instructions to execute), limited structured context, available decision actions.
OUTPUT JSON: clause_ids[], exact quote[], interpretations[] {reason, required_assumptions}, discriminating_scenario {inputs, expected_difference}, uncertainty enum, refusal/error.
Reject mismatched quotes, nonexistent clause references, invalid schema, invented facts, unsafe requests. Never silently repair bad outputs or count abstention as successful detection.

## Metrics (report by type, not just one overall score)
- Exact quote/span grounding precision and recall.
- Valid in-scope JSON rate; unsupported interpretation rate.
- Expert-confirmed important ambiguities detected; false alarms on clear cases.
- Discriminating scenarios verified by independent expert or approved deterministic oracle.
- Appropriate abstention when unanswerable; missed ambiguity and false-confidence rates.
- Human-reviewed task completion, review time, unresolved cases, subjective usefulness (secondary).
- End-to-end latency P50/P95, tokens/sec, peak RAM, loaded model size, energy where measurable, install friction and actual money spent.
- Privacy/data-flow verification and offline test pass/fail.

## Decision gates — PROVISIONAL until agreed pre-run
Functional: no unauthorized network payloads; no silently approved AI decisions; schema failures visible; reproducible model/version.
Reliability: set acceptable *error type specific* thresholds with customer and subject expert before looking at test outputs; do NOT declare success based on 100% on five familiar toy cases.
Utility: reviewer notices important issues faster or more often than baseline; no material increase in harmful false positives.
Feasibility: acceptable performance on customer-approved hardware without excessive installation/support overhead.

## Experiment ledger
Freeze prompt, code, temperature, decoding, context, model binary/digest, data, order, scoring rubric and cost limit. Preserve all first attempts, errors, invalid outputs and manual edits. Any tuning after scoring uses a fresh never-seen test set. Document leakage risks and that tiny samples carry wide uncertainty.

## First small exploratory experiment (not a formal benchmark)
1. Install Ollama locally after checking hardware; download an official Gemma 4 E4B tag.
2. Use 5–10 wholly fictional **development** policies and a restrictive JSON output schema.
3. Compare three conditions: manual-only, Gemma proposals, and stronger local/hosted model using authorized fictional inputs.
4. Inspect source-grounding and abstentions; record actual failures before any prompt repair.
5. Decide if effort should continue toward an independently blinded 20–30-case evaluation.
No API purchasing or model training is necessary for the first exploratory pass.

## Additional reading
[Google Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4) · [Amazon SOP-Bench](https://www.amazon.science/blog/sop-bench-a-new-benchmark-for-evaluating-ai-agents-on-real-business-procedures/) · [SOP-Bench code](https://github.com/amazon-science/SOP-Bench) · [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/).
