# Technical Specifications

Refer to this document for architecture, data flow, schemas, and operational guidance.

## System Overview

AIN is composed of an orchestrator (Chimera), planner agents, worker pools, judge (safety) services, vector and transactional stores, and a publisher. Components communicate via durable queues and HTTP/gRPC where appropriate.

## Core Components

- Chimera (Orchestrator): Generates DAGs, enqueues tasks, coordinates retries, and exposes operator APIs.
- Planner Agents: Ingest trends, normalize them, and emit `generate_video` tasks targeted to personas.
- Worker Pool: Autoscaled, stateless containers performing discrete steps (script generation, asset generation, TTS, compositing, render).
- Judge: Safety and brand compliance checks; returns granular check results and aggregate confidence.
- Publisher: Handles channel-specific publish logic, receipts, and idempotency.
- Stores:
  - Postgres: authoritative transactional state (tasks, videos, personas).
  - Object Storage (S3): media assets and renders.
  - Vector DB (Weaviate or similar): embeddings for search/recommendation.
  - Redis / Kafka: durable task queues and ephemeral coordination.

## Data Flow

1. Planner emits `generate_video` task JSON to queue.
2. Worker picks task, updates `state_version` in Postgres (optimistic lock), writes intermediate artifacts to Object Storage, and produces result message.
3. Judge consumes result, attaches `safety_report`, and either marks for human review or passes to Publisher.
4. Publisher posts to channel APIs and writes publish receipts to Postgres.

## Concurrency Model

- Use `state_version` integer on task/video rows for OCC. Updates MUST check `WHERE state_version = X` and increment on success.

## Security

- Service-to-service: mTLS.
- Agent actions requiring publish: signed JWTs with short TTL and audience restrictions.
- Secrets: store in a managed secrets store (e.g., AWS Secrets Manager / Vault).

## Observability

- Metrics: Prometheus for core SLOs (task latency, queue depth, publish success rate).
- Tracing: OpenTelemetry across task lifecycle (Planner → Worker → Judge → Publisher).
- Logs: Structured JSON logs sent to centralized logging (Elastic / Loki).

## Messaging & API Patterns

- Queue message format: JSON with envelope {"type": ..., "task": {...}} and optional headers for tracing and auth.
- Prefer exactly-once semantics at the application level using idempotency keys and Postgres-based transactional receipts.
- Use protobuf/gRPC for high-throughput internal RPCs; keep HTTP+JSON for cross-service vendor integrations.

## Component Interfaces

- Planner: exposes `fetch_trends()` (local) and `POST /tasks` (operator API) for manual task injection.
- Worker: subscribes to queue topic `tasks.generate_video`, processes messages, and writes ACK/NACK to `tasks.acks` stream.
- Judge: HTTP endpoint `POST /judge/evaluate` accepting `task_id` and artifact references, returning `safety_report`.
- Publisher: HTTP client with pluggable adapters per channel (YouTube, TikTok), each adapter implements `publish(artifacts, metadata)`.

## Deployment & CI

- Deploy with Kubernetes; use Helm charts for templating. Canary rollouts for judge and publisher services.
- CI: run unit tests, linting, contract tests (against `specs/api_contracts.md`) and basic integration smoke tests in pipeline.

## Testing Strategy

- Contract tests: validate that `fetch_trends()` and task messages meet `specs/api_contracts.md`.
- Integration tests: end-to-end pipeline on a small persona using local object storage and test doubles for external channels.
- Load tests: simulate planner → worker throughput and measure queue depth and task latency.

