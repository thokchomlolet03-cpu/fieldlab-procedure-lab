# Product engineering from silicon to reliable SaaS
Use a **small** tech stack, understand it deeply, then earn the right to add complexity. All technical links are free official docs or open educational resources unless otherwise noted.

## First principles and operating systems
- [Computer Systems: A Programmer's Perspective](https://csapp.cs.cmu.edu/) — book and companion resources (book paid); understand memory/processes and executable behavior.
- [OSTEP: Operating Systems Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) — free online OS textbook, process/VM/storage.
- [MIT Missing Semester](https://missing.csail.mit.edu/) — shell, Git, debugging, profiling, security.
- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/) — sockets and networking for developers.
- [Cloudflare Learning Center](https://www.cloudflare.com/learning/) — HTTP/TLS/DNS/network practical concepts.
- [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) — the web request lifecycle.
**Deliverable:** explain from packet to backend to database commit to UI how one FieldLab test is saved and retrieved.

## Language, frameworks, database
- **[Python tutorial](https://docs.python.org/3/tutorial/)**, [typing](https://docs.python.org/3/library/typing.html), [unittest](https://docs.python.org/3/library/unittest.html), [venv](https://docs.python.org/3/library/venv.html).
- **[FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)** — routes, validation, dependencies, auth limitations.
- [Pydantic](https://docs.pydantic.dev/latest/) — typed input/output contracts.
- [SQLite documentation](https://www.sqlite.org/docs.html) — local data, transactions and concurrency constraints.
- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html) — multi-user DB later, not first.
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/) — mapping and transactions if needed.
- [MDN Learn Web Development](https://developer.mozilla.org/en-US/docs/Learn_web_development) — HTML, CSS, JS, browser/security basics.
**Deliverable:** safe round-trip of immutable versioned policies; no magic cloud dependency.

## Testing, provenance, reliability
- [pytest docs](https://docs.pytest.org/en/stable/) — tests and fixtures.
- [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) — property-based boundary tests, contradictions and invalid dates.
- [GitHub Actions](https://docs.github.com/en/actions) — CI and checks.
- [Git documentation](https://git-scm.com/doc) — commits, branches, bisect, provenance.
- [OpenTelemetry](https://opentelemetry.io/docs/) — observability once a hosted pilot exists; redact content.
- [12-factor app](https://12factor.net/) — useful concepts for future production services; avoid cargo-cult deployment.
- [Docker official get started](https://docs.docker.com/get-started/) — learn isolation and packaging; not essential for tiny local proof.
**Deliverable:** reproducible test run, pinned dependencies, failed input as failed outcome.

## Security and software quality
- **[OWASP ASVS](https://asvs.owasp.org/)** — authentication, validation, design verification.
- [OWASP Top 10 Web](https://owasp.org/www-project-top-ten/) — common web app failures.
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — model-specific attack surface.
- [NIST CSF Small Business](https://csrc.nist.gov/pubs/sp/1300/final) — realistic early security controls.
- [FTC small business cybersecurity](https://www.ftc.gov/business-guidance/small-businesses/cybersecurity).
- [GitHub Dependabot](https://docs.github.com/en/code-security/dependabot) — dependency alerts.
**Deliverable:** safe local storage, sanitization, no credentials in repo, clear cloud opt-in, threat model.

## Architecture and scaling (LATER)
- [Designing Data-Intensive Applications](https://dataintensive.net/) — paid book, systems design, only after workflow needs it.
- [System Design Primer](https://github.com/donnemartin/system-design-primer) — open repo; filter rather than mimic huge architecture.
- [Google SRE book](https://sre.google/sre-book/table-of-contents/) — free, later operational reliability.
- [Cloud Run documentation](https://cloud.google.com/run/docs) and [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — hosting trade-offs if paid customers need service.
**Rule:** avoid Kubernetes, microservices and dedicated data pipelines until a specific measured bottleneck justifies them.
