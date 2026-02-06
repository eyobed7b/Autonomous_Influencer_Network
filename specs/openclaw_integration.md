# OpenClaw Integration (Chimera Availability/Status)

## Purpose

Describe how Chimera (the orchestrator) will publish its availability and status to the OpenClaw network to enable discovery, load-balancing, and capacity-aware scheduling.

## Message Schema

Heartbeat / status message example:

```json
{
  "node_id": "chm-01.example.org",
  "status": "online",
  "capacity": { "workers_total": 10, "workers_free": 4 },
  "tags": ["region:us-east-1", "gpu:true"],
  "load": { "queue_depth": 42, "avg_task_latency_ms": 1280 },
  "timestamp": "2026-02-05T12:00:00Z",
  "version": "1.0"
}
```

Fields:

- `node_id`: unique node identifier.
- `status`: `online|degraded|offline`.
- `capacity`: aggregated worker counts.
- `tags`: discovery tags for region/capability.
- `load`: optional metrics to guide scheduling (queue depth, latency).

## Transport and Auth

- Preferred: HTTPS POST to OpenClaw collector endpoint with mTLS.
- Authentication: JWT signed by Chimera with `kid` referencing node certificate; short TTL (e.g., 30s).
- Idempotency: include `node_id` + `timestamp` and server-side TTL to ignore duplicate heartbeats.

## Heartbeat Frequency & Backoff

- Heartbeat interval: default 15s; configurable per deployment.
- If collector responds with `429` or transient error, backoff exponentially up to 5 retries and then enter degraded mode reporting `status: degraded`.

## Security & Privacy

- Do not publish task-level or PII data; publish only aggregated capacity and capability tags.
- Ensure heartbeat payloads are signed and transmitted over mTLS.

## Discovery & Load-balancing

- Scheduler consults OpenClaw registry to select nodes matching required `tags` and with sufficient `workers_free`.
- Use `load.queue_depth` and `load.avg_task_latency_ms` for capacity-aware routing.

## Implementation Notes

- Provide a lightweight publisher library with configurable heartbeat interval, TLS/JWT credentials, and circuit-breaker behavior.
- Instrument the publisher with metrics: `heartbeats_sent`, `heartbeats_failed`, `last_success_timestamp`.

## Next Steps

- Implement publisher library and tests; add operator dashboard widgets for node discovery and health.
