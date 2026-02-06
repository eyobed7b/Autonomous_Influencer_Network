# OpenClaw Integration (Chimera availability/status)

Status: optional integration

This spec documents a safe, auditable way for Chimera nodes to publish availability,
capacity, and health information to the OpenClaw network to support discovery,
routing, and operational automation.

## Goals

- Provide a compact, authenticated heartbeat that enables external controllers or
  orchestrators to discover node capacity and routing hints.
- Keep payloads privacy-preserving and size-bounded.
- Support intermittent connectivity: design for eventual consistency and expirations.

## API Endpoints

- POST /openclaw/availability
  - Description: node heartbeat/availability publish endpoint (receiver in control-plane)
  - Auth: mTLS client cert + JWT signed by Chimera service account
  - Idempotency: use `node_id` + `last_heartbeat` timestamp as idempotency key

Example request payload

```json
{
  "node_id": "uuid-1234",
  "hostname": "chimera-01.prod",
  "version": "1.2.0",
  "capacity": {"workers": 24, "available_slots": 5},
  "queue_depth": {"planner": 3, "worker": 120},
  "last_heartbeat": "2026-02-06T12:34:56Z",
  "tags": ["region:us-east-1","gpu:true"],
  "uptime_seconds": 86400
}
```

Fields

- `node_id` (string, UUID): stable node identifier.
- `hostname` (string): human-friendly name.
- `version` (string): agent/service version.
- `capacity` (object): current configured capacity (workers, slots, other resources).
- `queue_depth` (object): queue depths for planner/worker topics.
- `last_heartbeat` (ISO-8601): time sent.
- `tags` (array[string]): freeform tags for routing/placement (region, gpu).
- `uptime_seconds` (integer): optional uptime metric.

## Security and Authenticity

- Mutual TLS for transport-level authenticity.
- JWT in `Authorization: Bearer <token>` for short-lived service identity; token audience must
  match OpenClaw receiver.
- Payload signatures are optional but recommended for high-security deployments.

## Delivery Semantics & Frequency

- Heartbeat frequency: default 60s (configurable 30–120s).
- Receiver should treat heartbeats as best-effort: publishers must include `last_heartbeat` and
  receivers should expire nodes after 2x the heartbeat interval by default.
- Use exponential backoff on publish errors (4xx: fail-fast, 5xx/network: backoff + jitter).

## Operational Behavior & Backpressure

- If local queue depth is high (above configurable threshold), `available_slots` should be reduced
  to indicate capacity pressure.
- Tagging convention: `region:<zone>`, `gpu:true|false`, `env:prod|staging`.

## Client Library & Runtime

- Implement a small, dependency-light client in `tools/openclaw_client.py` that reads runtime config
  and publishes heartbeats with retries, logging, and metrics.
- Runtime toggle: `OPENCLAW_ENABLED=true/false` and `OPENCLAW_ENDPOINT` in config.

## Observability & Monitoring

- Export metrics for `openclaw.publish.success_total`, `openclaw.publish.failure_total`, and
  `openclaw.latency_seconds`.
- Add a Grafana dashboard showing node counts, publish success rate, and expired nodes.

## Failure Modes & Recovery

- Network partitions: client should buffer the last known heartbeat locally and attempt replay when
  connectivity resumes (bounded buffer size).
- Receiver unavailability: nodes should continue operating; OpenClaw integration is advisory, not
  required for runtime correctness.

## Testing & Acceptance Criteria

- Unit tests for client serialization and retry/backoff policies.
- Integration smoke test: publish a heartbeat to a test endpoint and assert receiver records node.
- Load test: simulate 1000 nodes publishing at 60s interval to validate receiver scalability.

## Privacy & Data Retention

- Avoid embedding PII in heartbeats. If more detailed telemetry is needed, use separate
  authenticated telemetry channels with explicit retention rules.

## Rollout Plan

1. Implement client library and feature flag in Chimera.
2. Enable in staging, run smoke tests and monitor metrics for 48 hours.
3. Gradual rollout to production by percentage, monitoring expired node counts and publish errors.
