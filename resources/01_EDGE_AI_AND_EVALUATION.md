# AI engineering, local inference and rigorous evaluation
**Current priority:** HIGH for feasibility exploration, SECONDARY to customer discovery. Read [edge AI decision](../founder/11_EDGE_AI_DECISION.md), [benchmark protocol](../founder/12_EDGE_AI_EVALUATION.md), [privacy architecture](../founder/13_LOCAL_PRIVACY_ARCHITECTURE.md).

## Model choice and architecture
- **[Google Gemma model families and releases](https://ai.google.dev/gemma/docs/releases)** — what exists as of now, release chronology. Verify latest before selecting.
- **[Gemma 4 get started](https://ai.google.dev/gemma/docs/get_started)** — hardware-appropriate variants and deployment.
- **[Gemma 4 overview and memory](https://ai.google.dev/gemma/docs/core)** — effective vs total parameters, quantization and approximate load requirements.
- **[Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4)** — claimed benchmarks, limitations, modalities and license; benchmark scores are not FieldLab scores.
- [Gemma 4 QAT](https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/) — accuracy/performance trade-offs of reduced precision.
- [Hugging Face LLM course](https://huggingface.co/learn/llm-course/chapter1/1) — tokenization, transformers, fine-tuning and evaluation.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — first-principles transformer paper (advanced; not a prerequisite to interviews).
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — approachable architecture explanation.

## On-device runtimes (test ONE before accumulating alternatives)
- **[Ollama Gemma 4](https://ollama.com/library/gemma4)** — easy Mac/local demo; log exact tag, quantization and model digest.
- [llama.cpp](https://github.com/ggml-org/llama.cpp) — low-level CPU/Metal/GPU GGUF inference and CLI/server.
- [MLX](https://github.com/ml-explore/mlx) and [MLX-LM](https://github.com/ml-explore/mlx-lm) — Apple silicon local inference and experiments.
- [LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM) — Google edge inference stack for supported mobile/other devices.
- [Google AI Edge Gallery](https://github.com/google-ai-edge/gallery) — device/model compatibility experiments, not evidence of enterprise approval.
- [vLLM](https://docs.vllm.ai/) — future private/hosted serving, NOT needed in v0.
- [ONNX Runtime](https://onnxruntime.ai/docs/) — general on-device inference alternative.
- [Hugging Face model hub](https://huggingface.co/models) — model cards and license checks; verify publisher and file hashes.

## Structured generation, reliability, evaluation
- **[Amazon SOP-Bench blog](https://www.amazon.science/blog/sop-bench-a-new-benchmark-for-evaluating-ai-agents-on-real-business-procedures/)** — real SOP agent limitations and methodological inspiration.
- **[SOP-Bench code](https://github.com/amazon-science/SOP-Bench)** — inspect dataset, terms, ground-truth methods and whether the benchmark matches FieldLab's interpretation task; don't import sensitive materials blindly.
- [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) — benchmark framework; task-specific new data still required.
- [Hugging Face Evaluate](https://huggingface.co/docs/evaluate/index) — metric implementation, not a substitute for expert labels.
- [Pydantic validation](https://docs.pydantic.dev/latest/) and [JSON Schema](https://json-schema.org/) — strict structured-output validation.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — governance and evaluation.
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — prompt injection, sensitive information, output handling.
- [Google Responsible Generative AI Toolkit](https://ai.google.dev/responsible) — responsible development references; verify specific tools and licenses.

## What to implement/learn from each
1. Run one local Gemma 4 E4B exploratory test with **fictional** SOPs, offline if possible. Record peak RAM, startup time, output quality, invalid JSON, abstention and any network activity.
2. Compare against no model and a strong comparator on exactly the same novel cases.
3. Test quoted-clause grounding and boundary generation; human reviewer must confirm meaning.
4. Reject invented facts and schema-invalid responses; errors are results, not “success”.
5. Only test fine-tuning after demonstrating a repeatable gap not solvable with constrained output or product workflow. Fine-tuning can memorize artifacts and reduce portability.

## Research questions
Does model size improve *useful, expert-confirmed* findings? What is the actual cost per completed review? What hardware do customers already own? Would buyers pay more for local-only? Does model deployment create an IT procurement barrier? Can the deterministic test engine remain valuable without AI?

## Avoid
Relying on leaderboards; equating context length with long-document comprehension; claiming local storage == complete privacy; using LLM self-rating as ground truth; overfitting original exposed eight cases; claiming general “AI understands policy”.
