# Procedure experiment v1 · November 3, 2026

**The replay works. Automatic interpretation failed the first eight-case evaluation.** Nine software tests passed. In the actual browser, the original curated rule produced two different decisions at the middle arrival. Adding the first-item definition changed that case to “take the rush order.” Moving the arrival later changed the decision to “continue the regular order.”

## Live local-model results

The approved Ollama download installed Meta Llama 3.2 1B, a 1,321,098,329-byte quantized package. Ollama returned model digest `baf6a787fdffd633537aa2eb51cfd54cb93ff08e28040095462bb63daf552878`. All scored calls used this local model. The deck, prompts and scoring executable were frozen at Git commit `2cea1183938bcfa0362dded96c692fcebae82780` before outcome access.

| On the eight original procedures | Interpretation plus replay | Direct review |
|---|---:|---:|
| Correct ambiguous/clear classification | 0/8 | 0/8 |
| Valid in-scope classifications | 0/8 | 0/8 |
| Returned an accepted abstention | 5/8 | 3/8 |
| Output rejected by validation | 3/8 | 5/8 |

Neither method raised a false ambiguity alarm on the four clear cases. Both also missed every ambiguity. The proposed readings produced zero correct executable witnesses across four ambiguous procedures and zero successful paired repairs across four additional model requests. All 20 scheduled calls have response receipts. The sum of measured chat-request durations was 88.9 seconds.

In case p02, for example, Llama returned an outside-scope status along with two proposed readings. The adapter rejected that inconsistent output. In p03 it returned a priority quotation absent from the supplied procedure. The canonical opening rule was also tried separately, and Llama abstained. The browser displayed that abstention under the local-model source label. The curated example has prewritten readings and is presented under its own label.

The deck contains fictional variations of a single queue rule. Its answers were supplied by the developers. Independent semantic grading and real operational testing remain pending. No prompts were changed or cases retried for the scored run.

## Decision

**GO** for demonstrating and reviewing the deterministic replay, including the controls on either side of the ambiguous event.

**NO-GO** for presenting this model configuration as a reliable automatic reviewer. The next bounded experiment would have the model select numbered source clauses and a start-boundary category, eliminating the need to reproduce quotes verbatim. That approach requires a fresh deck, a frozen protocol and a new evaluation before making a reliability claim.

[Scores by case](results/v1/summary.json) · [Execution identity and input hashes](results/v1/start.json) · [Canonical live response](results/v1/canonical-live-v1.json) · [Software test output](results/v1/software-tests.txt)
