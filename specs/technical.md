# Technical Specifications

## Components

- Planner: Task DAG generator, reads `SOUL.md`, emits tasks to Redis queue.
- Worker Pool: Stateless containers executing atomic tasks (image gen, TTS, render).
- Judge: Runs safety checks, OCC via `state_version` and PostgreSQL.
- Memory Stores: Weaviate for vectors, Postgres for transactional state, Redis for queues.

## Messaging

- Task messages are JSON with `task_id`, `type`, `payload`, `persona_id`, `state_version`.
- Workers must ack/nack with structured responses including `state_version` increments.

## Observability

- Structured logs (JSON), metrics (Prometheus), and distributed traces (OpenTelemetry).

## Security

- Mutual TLS for inter-service RPCs; signed JWT for agent actions requiring publish permissions.
