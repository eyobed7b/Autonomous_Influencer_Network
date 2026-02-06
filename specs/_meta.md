# Project Chimera — High-level Vision & Constraints

Project: Autonomous Influencer Network (AIN) — codename "Chimera".

Vision
- Enable autonomous, auditable generation and publishing of short-form influencer media
  (video + transcripts) from rapidly changing trend signals while enforcing brand
  safety and human-in-the-loop review where required.

Scope
- Ingest trend signals from multiple sources, normalize them, emit `generate_video`
  tasks, run worker pipelines (script → assets → TTS → composite → render), apply
  safety/judge checks, and publish idempotently to channel APIs.

Out of scope (initial)
- Fully autonomous long-form content production, real-money billing integrations,
  advanced attribution/monetization features.

Constraints
- Security: secrets must be in a managed store (Vault / AWS Secrets Manager).
- Compliance: safety/judge checks MUST run before publishing any content.
- Observability: all task lifecycles must emit traces/metrics.
- Scalability: stateless workers, use HPA/K8s autoscaling.

Ratification
- RATIFICATION_DATE: TODO(RATIFICATION_DATE): set when governance ratifies this spec
