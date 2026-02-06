# Functional Specifications (User Stories)

## Overview
This document lists user stories and acceptance criteria for the core flows of Project Chimera.

### Planner / Trend ingestion
- As an Agent, I need to fetch trends so that the system can detect candidate topics for content.
  - Acceptance: system exposes a `fetch_trends()` contract; trends include id, title, score, source, timestamp, tags, and metrics.

  **Scenarios & Edge Cases**
  - Happy path: `fetch_trends()` returns multiple normalized trend objects.
  - Empty source: when upstream returns no trends, `fetch_trends()` returns an empty list and the planner logs a no-op.
  - Partial failure: if one source fails, planner continues with remaining sources and emits a warning.
  - Rate limiting: upstream rate limits should be retried with exponential backoff and circuit breaker.

### Generation pipeline
- As an Orchestrator, I need to emit a `generate_video` task for a normalized trend so that workers can produce content.
  - Acceptance: `generate_video` task includes `task_id`, `persona_id`, `payload` (trend metadata), and `state_version`.

  **Scenarios & Edge Cases**
  - Duplicate trend suppression: the planner should detect near-duplicates and avoid emitting duplicate tasks.
  - Persona mismatch: if no persona matches a trend, the planner flags the trend for manual review.

### Worker processing
- As a Worker, I need clear step inputs (script, assets, TTS params) so that each stage can be performed independently and checkpointed.
  - Acceptance: workers read task payloads from queue and produce intermediate artifacts to object storage, updating task `state_version`.

  **Scenarios & Edge Cases**
  - Transient failures: worker retries failed steps with backoff and emits structured errors after retry exhaustion.
  - Checkpointing: partial artifacts must be storable and idempotent so a resumed job can continue safely.

### Safety / Judge
- As a Safety service, I need access to final artifacts and context to produce a `safety_report` before publish.
  - Acceptance: judge returns structured reasons, confidence, and any required human review flag.

  **Scenarios & Edge Cases**
  - False positive handling: flagged content is queued for human review and review results are correlated back into judge training data.
  - Latency-sensitive flows: judge timeouts must be handled (e.g., fail-safe to human review if judge is unavailable).

### Publisher
- As a Publisher, I need to receive judged tasks and publish idempotently to target channel APIs, emitting receipts.
  - Acceptance: receipts include `publish_id`, `channel`, `status`, `remote_id`, and `timestamp`.

  **Scenarios & Edge Cases**
  - Rate limits and quota errors: implement exponential backoff and queueing for retryable remote errors.
  - Partial publish: when only some channels succeed, record per-channel receipts and expose retry controls.

### Operational
- As an Operator, I need observability (metrics, traces, logs) across task lifecycles.
  - Acceptance: Prometheus metrics for queue depth, task latency; traces for Planner→Worker→Judge→Publisher.

  **Acceptance Tests / Monitoring Checks**
  - Ensure Prometheus exports `task_latency_seconds` histogram and `queue_depth` gauges.
  - Traces should show the full task lifecycle including span tags for `task_id`, `persona_id`, and `state_version`.

## Acceptance Criteria Summary
- `fetch_trends()` contract satisfied and contract tests pass.
- Planner emits `generate_video` tasks with idempotency and duplicate suppression.
- Workers checkpoint artifacts and update `state_version` with OCC semantics.
- Judge produces `safety_report` for 100% of publish-bound artifacts.
- Publisher emits receipts and supports per-channel retry.

