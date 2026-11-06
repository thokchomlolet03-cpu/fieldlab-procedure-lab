# 11 — Edge AI strategy for FieldLab (6 November 2026)
**Status: architectural hypothesis, not an implementation decision.** Local-first is a privacy/product hypothesis that must be tested against accuracy, hardware and cost. Models mentioned here have NOT been run on FieldLab cases.

## Decision in one sentence
Explore **Gemma 4 E4B** as the first laptop-local *proposal generator*, with **Gemma 4 12B** as a stronger local comparison. Keep the verified product's **human-approved, deterministic test engine independent from the LLM**. Do not make arbitrary automatic policy interpretation a requirement to launch v0.1.

## Current official model evidence
Google launched Gemma 4 in April 2026; added 12B in June 2026. Official resources:
- [Gemma releases](https://ai.google.dev/gemma/docs/releases)
- [Model overview, quantization and memory](https://ai.google.dev/gemma/docs/core)
- [Model card, benchmark caveats and Apache 2.0](https://ai.google.dev/gemma/docs/core/model_card_4)
- [Get started](https://ai.google.dev/gemma/docs/get_started)
- [Google launch notes](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)
- [Google quantization-aware training](https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/)

Approximate Q4_0 weights+Google's stated 20% overhead: E2B 2.9GB, E4B 4.5GB, 12B 6.7GB, 26B A4B 14.4GB, 31B 17.5GB. These are **loading estimates**, not peak application RAM: KV cache/context, runtime, OS, GPU and background applications add use. Google also lists special mobile formats; do not compare them as equivalent to desktop Q4_0 binaries. An E4B model has more TOTAL than 4B parameters (embedding tables), so its download/weight size does not equal its effective compute footprint.

## The exact AI tasks to test
1. **Bounded clause extraction:** find quoted spans containing thresholds, temporal boundaries, exceptions, approvals and missing data.
2. **Candidate interpretations:** propose up to two rival meanings anchored to verbatim clause IDs; mark unverified.
3. **Scenario suggestions:** propose 1–3 *discriminating* boundary cases per approved rule, not random creative questions.
4. **Schema translation:** propose small typed JSON with enumerated actions and validated field names; human reviews.
5. **Uncertainty detection:** say “cannot determine from text” when ambiguous or underspecified.

## Tasks NOT delegated to model
- Authenticating/authorizing users, storing secrets, enforcing privacy policies.
- Deciding compliance, warranty, safety or lawful interpretation.
- Approving expected outcomes without domain expert.
- Executing final decisions when exact approved rules can run deterministically.
- Treating fluent explanations as proof or judging its own output as ground truth.

## Practical model decision matrix
| Candidate | First purpose | Constraint to measure |
|---|---|---|
| No model: scripted prompts + reviewer | Necessary product baseline | User time and independent usefulness |
| Gemma 4 E2B | Low-resource edge baseline | Local quality, abstentions, CPU/GPU speed |
| Gemma 4 E4B | **First local candidate** | JSON validity, clause faithfulness, measured useful findings |
| Gemma 4 12B | Stronger laptop benchmark if hardware supports | Memory, latency and measured accuracy delta |
| Gemma 4 26B A4B | Optional workstation/on-prem candidate | Weight memory, support costs and throughput |
| Strong hosted model (authorized synthetic data only) | Capability reference | Privacy trade-off, cost per completed approved review |
| Existing Llama 3.2 1B | Historic failure anchor | Prior 0/8 result was a different test and cannot be treated as comparative Gemma performance |

## Local runtimes (choose based on user hardware)
- [Ollama Gemma 4 library](https://ollama.com/library/gemma4) — fastest exploratory path; verify exact tag and digest; no default cloud fallback.
- [llama.cpp](https://github.com/ggml-org/llama.cpp) — GGUF and Apple Metal, broad device support.
- [MLX-LM](https://github.com/ml-explore/mlx-lm) — Apple silicon local experimentation.
- [LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM) — Google on-device/mobile-oriented inference.
- [AI Edge Gallery](https://github.com/google-ai-edge/gallery) — convenient phone tests (not enterprise deployment proof).

**Do not claim a model works on a specific Mac/phone until RAM, OS, quant, context, runtime and measured tokens/sec are known.** The founder's own computer configuration must be logged rather than inferred.

## Cost, speed and privacy are separate tests
Local avoids **per-token cloud inference charges**, not hardware, support, model licensing review, electricity, integration, updates or endpoint security. It also removes *one* data-transfer path, not all exposure paths. Consider download/update logs, app analytics, crash reports, backups, compromised endpoints, disk encryption, caches, internal network, extensions, third-party plugins, exported reports and user consent.

Enterprise choice may be customer-hosted inference on company-approved servers, not necessarily a model on every worker's laptop. A no-AI workflow should always remain available.

## Scale: the actual startup question
For 3 pilots, desktop-local inference can be low-cost, reversible and fast to learn. For 3,000 users, version distribution, hardware heterogeneity, IT approval, support and reliability can dominate inference savings. Scale model by *active runs and concurrent users*, not total staff at client company. Compare actual cost per successful manager-approved review, not just token prices.

## Product architecture recommendation
Client local app → versioned procedure store → bounded clause parser/model adapter (optional) → **unapproved proposals** → manager approval → validated rules → deterministic test runner → diff/report → local encrypted storage/export.
Interface: a provider abstraction with explicit modes **none / local / organization-hosted / cloud (explicit opt-in only)**. Default **none** for v0.1. Cloud must never be an undisclosed fallback.
For untrusted policy text: no shell execution, no arbitrary tool calls, input length controls, prompt injection defenses, strict JSON schema, failed extraction as abstention.

## Go/no-go
Local-first becomes a product differentiator only if buyers say privacy prevents their existing workflow and local mode clears acceptable quality/latency/IT deployability thresholds. If the local model is too unreliable, keep local deterministic rules and human review; allow optional company-approved models rather than forcing bad automated reasoning.

## Historical comparison
[November 3 FieldLab results](../procedure_lab/RESULTS.md) show deterministic replay worked; the tested Llama 3.2 1B automatic interpretation arm scored 0/8. That experiment is not evidence Gemma 4 succeeds or fails. Do not rewrite/erase the failure.
