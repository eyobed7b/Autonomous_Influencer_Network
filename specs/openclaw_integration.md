# OpenClaw Integration (Chimera Availability/Status)

## Purpose

Describe how Chimera (the orchestrator) will publish its availability and status to the OpenClaw network to enable discovery and load-balancing.

## Message Schema

{
"node_id": "string",
"status": "online|degraded|offline",
"capacity": {
"workers_total": 10,
"workers_free": 4
},
"tags": ["region:us-east-1","gpu:yes"],
"timestamp": "2026-01-01T00:00:00Z"
}

## Transport

- Prefer an authenticated HTTP POST to the OpenClaw collector endpoint.
- Use signed JWT and mTLS for authentication.
- Include idempotency keys and TTLs; publish at heartbeat interval (e.g., 15s).

## Retry and Backoff

- On transient failures, retry with exponential backoff up to 5 attempts.
- On persistent auth failures, surface to operator dashboard.

## Security & Privacy

- Avoid publishing detailed task-level metadata; only publish aggregate capacity and region tags.

## Next Steps

- Implement publisher library with configurable heartbeat interval and diagnostics.
