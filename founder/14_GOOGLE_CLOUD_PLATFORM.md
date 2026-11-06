# 14 — Google Cloud is FieldLab's development and deployment platform
**Decision:** 2026-11-06. **State:** architecture selected; no Google Cloud resources deployed by this plan. **Owner:** founder.
**Source of truth:** GitHub stays canonical for code, issues and reviews. All development environments, experiments needing compute, deployed demos and backend infrastructure will run on Google Cloud. Local inference remains a possible *future customer deployment mode* and does not imply our development has to happen on the founder's laptop.

## Important distinction
- **Development location:** Google Cloud Shell/Cloud Workstations (workstation only if justified).
- **Early product hosting:** Google Cloud Run with private access; optional public demo uses fictional documents only.
- **Research inference:** Run GCP experimental compute only with a written budget and data constraints. If using Vertex AI/Cloud Run GPU, data is processed in Google Cloud—not “on customer device”.
- **Long-term customer data location:** Decide from actual contracts and residency requirements; potential separate customer-managed edge or on-prem inference adapter.
- **Product architecture:** No AI needed for basic approved-rule test flow; model suggestions always require expert review.

## Recommended initial service map
| Job | Product | Use / cost guardrails |
|---|---|---|
| Edit/debug in browser | **Cloud Shell Editor** | 5 GB home disk and weekly time quota; not a permanent server; commit source to GitHub |
| Code + company planning | **GitHub** | Source/PR/Issues, no secrets/customer notes |
| Deploy web app | **Cloud Run** | Start with CPU-only, min instances=0, bounded max instances, IAM-authenticated, fixed region |
| Build and image packaging | **Cloud Build and Artifact Registry** | Cloud Run deploy-from-source invokes these; watch image storage and build charges |
| Application persistence | **Firestore** (when versioned shared data needed) | Cloud Run disk ephemeral; avoid SQLite on Cloud Run as authoritative database |
| Secrets | **Secret Manager** | Only after credentials exist; use service account identity/ADC, not downloaded keys |
| Logs | **Cloud Logging** | Error codes/run IDs, not raw policy content; keep log retention/cost controlled |
| Monitoring + spend | **Cloud Monitoring and Cloud Billing** | Budgets, cost alerts, API quotas and periodic billing inspection |
| Large-model inference | **Vertex AI or Cloud Run GPU/approved GPU compute** | Optional/explicitly cost-authorized experiments; never always-on for early MVP |
| Later customer-facing web | **Cloud Run (or Firebase Hosting for static)** | Select only after external pilot need; authentication/tenant isolation before client data |

### Cost facts and sources
- [Cloud Shell limits](https://docs.cloud.google.com/shell/docs/quotas-limits): default 50 hours weekly, 5 GB persistent home; session VM ephemeral, not 24/7 hosting.
- [Cloud Workstations pricing](https://cloud.google.com/workstations/pricing): control-plane fee plus compute/storage; unnecessary for solo MVP unless Cloud Shell lacks required capacity.
- [Cloud Run pricing](https://cloud.google.com/run/pricing): request/CPU/memory billing; some free allowance and min-instances=0 can make low-traffic tests inexpensive, NOT universally free.
- [Cloud Run source deployment](https://docs.cloud.google.com/run/docs/deploying-source-code): gcloud run deploy --source . builds via Cloud Build and stores an image in Artifact Registry.
- [Firestore pricing](https://firebase.google.com/docs/firestore/pricing): first eligible database free quota, writes/reads/indices/storage/egress matter.
- [Cloud Run GPU docs](https://docs.cloud.google.com/run/docs/configuring/services/gpu): L4/Blackwell GPUs for selected regions, GPU must be paired with CPU and RAM; can scale to zero but per-instance seconds bill for combined resources.
- [Billing budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets): alerts-only budgets **DO NOT STOP CHARGES**. If a spend-cap option is available, examine support/limits; otherwise add technical resource controls and manual shutdown.
- [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity): dedicated least-privilege service account + ADC; avoid JSON key files.

## Initial configuration runbook (human executes after checking account and permissions)
1. Use [Google Cloud Console](https://console.cloud.google.com/), select/create a **dedicated FieldLab development project**. Choose a non-sensitive project name/id. Do not publish billing account number or credentials.
2. Enable billing only if necessary and after recording a realistic monthly maximum willingness to spend in a **private** budget. Create billing budget alerts at 50%, 80% and 100%; understand alerts do not hard-stop spending.
3. Choose a region based on service availability, pricing, privacy/residency and actual customer location; use the SAME region for most early resources. Region is a decision, not assumed “must be US”; check Cloud Run, Firestore, storage, GPU compatibility separately.
4. Use Cloud Shell Editor to clone the repo and select reviewed branch, e.g. `git clone https://github.com/thokchomlolet03-cpu/fieldlab-procedure-lab.git`; authenticate GitHub via approved method without embedding access tokens into shell history or source.
5. Run baseline tests in Cloud Shell: `python3 -m unittest discover -s procedure_lab -v`. Capture environment, commit SHA, success/failure and any mismatch with historical reports. Do not claim tests have run until actual receipt.
6. Implement new `product/` as a separate package, starting with deterministic rules and small fictional policy fixtures. Use local SQLite *inside the Cloud Shell development environment* only for short-lived tests; source of truth for collaborative deployments should become Firestore/approved persistent store.
7. When the service is deployment-ready: enable `run.googleapis.com`, `cloudbuild.googleapis.com`, `artifactregistry.googleapis.com` subject to required billing/permissions; deploy a **private** Cloud Run service from app source. Use source deploy `gcloud run deploy fieldlab-dev --source . --region REGION --no-allow-unauthenticated --min-instances=0 --max-instances=1`. Only run from deployable app subdirectory with correct entrypoint/requirements/Dockerfile; existing research repo root is **not yet** deployment-ready.
8. Use a dedicated **runtime** service account with only necessary Firestore/read-secret permissions; do not grant broad project Owner role. For early authenticated developer access, confirm the Cloud Run invoker/IAM path and do not enable public unauthenticated access.
9. Smoke-test health endpoint, permission-denied flow, version persistence, test runner, export and log redaction. Record test result, service URL privately if protected, region, monthly charges and rollback process.
10. Delete temporary demo services, unnecessary stored container images and any experimental GPU resource after each test. Establish cleanup and monthly billing review.
**Never paste service account keys, API tokens or billing identifiers into this public repo/chat.**

## Google Cloud software lifecycle
GitHub PR → Cloud Shell (pull branch, run tests) → manual approved source deploy to private `fieldlab-dev` Cloud Run → scripted smoke test → log defects and costs → review PR → only then merge to main. Once needed, automate through Cloud Build/GitHub workload identity federation (short-lived credentials, no long-lived service account key). Keep GitHub main protected/reviewed when available.

## Stateful operations warning
Cloud Run's in-container filesystem is temporary and not suitable as authoritative application persistence. When using Firestore, design document ownership and storage limits; updates must be transactional where necessary, immutable historical versions cannot be overwritten, and indexes/query cost must be measured.

## AI experiments: GCP without claiming edge privacy
Use GCP to evaluate Gemma on fictional data: experimental GPU services/jobs or supported managed model deployments ONLY after verifying availability, compatible model/version, quota, and cost. No always-on GPU. Record actual model weights/digest and compute environment. If a future local-customer version is tested, label that as a **separate** deployment/privacy experiment with customer-device hardware. Do not claim “on-device” based on a Cloud Run or Vertex AI result.

## Security and access
IAM least privilege, dedicated service accounts, no default credentials in source, no unauthenticated business-data endpoints, no real client SOPs before contractual/security review. Default no model requests or automatic third-party fallback. Keep Cloud Logging free of raw inputs; synthetic-only public demonstration. Verify cloud data region and subprocessors with actual customer.

## Stage gates
- **GCP-0** project/billing/alerts/quotas/access documented; no surprise resources.
- **GCP-1** original tests reproduced in Cloud Shell (receipt).
- **GCP-2** private CPU-only Cloud Run demo and verified health check; no real user data.
- **GCP-3** Firestore persistence with immutable version tests, least-privilege runtime identity, recoverability and log redaction.
- **GCP-4** model feasibility compared fairly, with measured money/RAM/latency; customer need demonstrated before GPU expenditures.
- **GCP-5** external pilot security/legal controls plus independently verified company value before broader release.

## Revisit conditions
If customer IT policy prohibits GCP, assess customer-managed/on-prem/edge deployments. If Cloud Shell becomes constraining, compare Cloud Workstations versus short-lived Compute Engine with shutdown scripts. If Firestore model creates query/transaction complexity, compare Cloud SQL (with known always-on cost) only when needed. Do not preemptively build multi-cloud.
