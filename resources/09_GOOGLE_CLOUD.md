# Google Cloud FieldLab curriculum and official reference links
**Decision:** all software development, web demos and compute experiments under Google Cloud; GitHub remains canonical code history. Link to [GCP operating plan](../founder/14_GOOGLE_CLOUD_PLATFORM.md).

## Learn and apply in dependency order
### Stage 0: Account, bills, Cloud Shell and source control
- [Google Cloud getting started](https://cloud.google.com/docs/get-started) — projects, billing and service enablement.
- [Cloud Shell how it works](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works) — interactive VM limitations.
- [Cloud Shell quotas](https://docs.cloud.google.com/shell/docs/quotas-limits) — 50 hr/week, 5 GB home, ephemeral runtime.
- [Git documentation](https://git-scm.com/doc) — fetch/branch/commit/push from cloud environment.
- [Billing and alerts](https://docs.cloud.google.com/billing/docs/how-to/budgets) — **alerts-only are not spending caps**.
- [Cost calculator](https://cloud.google.com/products/calculator) — compare regions and workloads before enablement.
**Exercise:** write a private project inventory with project ID, billing linked, region, budget threshold, enabled APIs, IAM identities and cleanup rules. Never publish identifiers and billing data that can compromise account.

### Stage 1: Application runtime, build and deployments
- **[Deploy Python FastAPI on Cloud Run](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-fastapi-service)** — official starting tutorial.
- [Cloud Run source deployment](https://docs.cloud.google.com/run/docs/deploying-source-code) — buildpacks/Cloud Build/Artifact Registry.
- [Cloud Run costs](https://cloud.google.com/run/pricing) — request/resource time, free quota and egress caveats.
- [Cloud Build](https://cloud.google.com/build/docs) — continuous build and verified commits.
- [Artifact Registry](https://cloud.google.com/artifact-registry/docs) — container retention and image storage cost.
- [Cloud Run authentication](https://docs.cloud.google.com/run/docs/authenticating/overview) — private by default, invoker IAM.
**Exercise:** build a PRIVATE fictional-data app, verify health response, forbidden unauthenticated access, and logging without raw policy text.

### Stage 2: Data, identities, logs
- **[Firestore pricing](https://firebase.google.com/docs/firestore/pricing)** and [Firestore docs](https://cloud.google.com/firestore/docs) — data model, reads/writes, quotas and transactions.
- [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity) — least privilege and ADC instead of downloaded JSON keys.
- [Secret Manager](https://cloud.google.com/security/products/secret-manager) — secret rotation and access limits.
- [Cloud Logging](https://cloud.google.com/logging/docs) and [Monitoring](https://cloud.google.com/monitoring/docs) — error logs, not sensitive input dumps.
- [Cloud IAM best practices](https://cloud.google.com/iam/docs/using-iam-securely) — roles and service account management.
- [Security Command Center](https://cloud.google.com/security-command-center/docs) — later security posture if justified.
**Exercise:** persist/retrieve immutable policy versions with safe IAM and redacted logs. Destroy/recreate app instance and confirm durable database results.

### Stage 3: Model and evaluation compute (DEFER until buyer tests)
- [Cloud Run GPU services](https://docs.cloud.google.com/run/docs/configuring/services/gpu) — inference on demand, paired CPU/memory costs.
- [Cloud Run GPU jobs](https://docs.cloud.google.com/run/docs/configuring/jobs/gpu) — bounded batch evaluation.
- [Vertex AI](https://cloud.google.com/vertex-ai/docs) and [Model Garden](https://cloud.google.com/model-garden) — determine specific Gemma model availability, pricing, quota and terms *at experiment time*.
- [Gemma 4 official](https://ai.google.dev/gemma/docs/core) — model card, quantization, memory and licensing.
- [AI infrastructure pricing](https://cloud.google.com/vertex-ai/pricing) — quotas/pricing prior to model launch.
**Exercise:** freeze benchmark cases, compare deterministic/human/no model with one candidate model on fictional inputs; record actual latency, validity, accuracy, cloud charges, peak memory and failures. **GCP inference is not local-to-customer privacy.**

### Stage 4: Production maturity (later)
- [Cloud Run security](https://cloud.google.com/run/docs/securing/overview)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [Google Cloud SRE](https://sre.google/sre-book/table-of-contents/)
- [Google Cloud Well-Architected](https://cloud.google.com/architecture/framework)
- [Cloud Workstations pricing](https://cloud.google.com/workstations/pricing) — managed developer environments, pay for control plane and compute.
- [Google Cloud certifications](https://cloud.google.com/learn/certification) — optional personal learning; certification not customer validation.
**Exercise:** define backup/restore, alerting, rate limiting, security boundaries, release rollback and error budgets for actual pilots.

## Avoid for first MVP
Always-on GCE GPU VMs; dedicated Cloud SQL before requirements justify it; Kubernetes/GKE; paid managed developer workstation; multiple regions; public endpoints receiving real client text; default wide-open firewall/IAM; downloaded service account keys. Cloud Run scale-to-zero does not remove image/network/DB charges; budget alerts do not cap total spend.

## Suggested learning sequence
GCP project → budget/IAM → Cloud Shell/GitHub → Python FastAPI/Cloud Run → Firestore/version persistence → tests/CI → logs/security → opt-in AI experiment → business pilot. No need to pursue a certification before deploying the first fictional demonstration.
