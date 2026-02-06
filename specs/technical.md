# Technical Specifications

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

## Messaging & Schemas

- Task messages are JSON with `task_id`, `type`, `payload`, `persona_id`, and `state_version`.
- Workers must ack/nack with structured responses including `state_version`, `status`, `errors`, and `confidence`.

## Concurrency Model

- Use `state_version` integer on task/video rows for OCC. Updates MUST check `WHERE state_version = X` and increment on success.
- Long-running tasks should checkpoint intermediate artifacts and state to enable resume.

## Security

- Service-to-service: mTLS.
- Agent actions requiring publish: signed JWTs with short TTL and audience restrictions.
- Secrets: store in a managed secrets store (e.g., AWS Secrets Manager / Vault).

## Scalability & Deployment

- Workers run in Kubernetes with HPA based on queue length and worker concurrency.
- Use spot instances or ephemeral Fargate-style containers for cost-sensitive workloads.
- Database: Primary Postgres with read replicas; object storage in multi-AZ.

## Observability

- Metrics: Prometheus for core SLOs (task latency, queue depth, publish success rate).
- Tracing: OpenTelemetry across task lifecycle (Planner → Worker → Judge → Publisher).
- Logs: Structured JSON logs sent to centralized logging (Elastic / Loki).

## Testing & CI

- Unit tests for agent logic, contract tests for message schemas.
- Integration tests: end-to-end pipeline on small personas and trend inputs.

## Operational Runbook Highlights

- Heartbeats & Node Discovery: Each Chimera node reports heartbeat (OpenClaw integration) and capacity.
- Incident: Roll back planner or pause publishers if moderation backlog exceeds threshold.
