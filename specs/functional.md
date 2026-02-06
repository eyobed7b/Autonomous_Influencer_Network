# Functional Specifications (User Stories)

## Overview
This document lists user stories and acceptance criteria for the core flows of Project Chimera.

### Planner / Trend ingestion
- As an Agent, I need to fetch trends so that the system can detect candidate topics for content.
  - Acceptance: system exposes a `fetch_trends()` contract; trends include id, title, score, source, timestamp, tags, and metrics.

### Generation pipeline
- As an Orchestrator, I need to emit a `generate_video` task for a normalized trend so that workers can produce content.
  - Acceptance: `generate_video` task includes `task_id`, `persona_id`, `payload` (trend metadata), and `state_version`.

### Worker processing
- As a Worker, I need clear step inputs (script, assets, TTS params) so that each stage can be performed independently and checkpointed.
  - Acceptance: workers read task payloads from queue and produce intermediate artifacts to object storage, updating task `state_version`.

### Safety / Judge
- As a Safety service, I need access to final artifacts and context to produce a `safety_report` before publish.
  - Acceptance: judge returns structured reasons, confidence, and any required human review flag.

### Publisher
- As a Publisher, I need to receive judged tasks and publish idempotently to target channel APIs, emitting receipts.
  - Acceptance: receipts include `publish_id`, `channel`, `status`, `remote_id`, and `timestamp`.

### Operational
- As an Operator, I need observability (metrics, traces, logs) across task lifecycles.
  - Acceptance: Prometheus metrics for queue depth, task latency; traces for Planner→Worker→Judge→Publisher.
