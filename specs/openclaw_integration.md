# OpenClaw Integration (Chimera availability/status)

Optional integration: Chimera publishes node availability and capacity to OpenClaw for discovery and runbook automation.

## Objective
- Allow external systems to discover Chimera nodes, their capacity, and current status for routing and orchestration.

## Schema
- Endpoint: `POST /openclaw/availability`
- Payload:
  {
    "node_id": "uuid",
    "hostname": "string",
    "version": "1.0.0",
    "capacity": {"workers": 12, "available_slots": 5},
    "queue_depth": {"planner": 12, "worker": 200},
    "last_heartbeat": "ISO-8601",
    "tags": ["region:us-east-1","gpu:true"]
  }

## Frequency
- Heartbeat interval: 30s - 2m depending on network stability and control-plane trade-offs.

## Security
- mTLS and signed JWTs for authenticity. Payloads should be rate-limited and size-bounded.

## Operational
- Add a small client library in `tools/` to publish availability; provide a toggle to enable in runtime config.
