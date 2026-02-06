# API Contracts

This file defines the JSON inputs/outputs for core agent interactions.

## Trend Fetcher Output

Type: list of objects

Example:

{
  "trend_id": "str-uuid",
  "title": "Short headline",
  "score": 0.87,
  "source": "twitter",
  "timestamp": "2026-02-06T12:34:56Z",
  "tags": ["tag1","tag2"],
  "metrics": {"mentions": 1234, "engagement": 0.42}
}

Contract requirements:
- `fetch_trends()` MUST return a list of trend objects as above.

## generate_video Task (Planner → Queue)

{
  "task_id": "uuid",
  "type": "generate_video",
  "persona_id": "persona-123",
  "payload": { /* contains trend object plus normalization */ },
  "state_version": 1,
  "created_at": "ISO-8601"
}

## Worker ACK/NACK

Success:
{
  "task_id": "uuid",
  "status": "completed",
  "state_version": 2,
  "artifacts": {"s3_path": "s3://.../render.mp4"}
}

Failure:
{
  "task_id": "uuid",
  "status": "failed",
  "state_version": 1,
  "errors": [{"code":"TRANSFORM_ERROR","message":"..."}]
}

## Judge Response

{
  "task_id": "uuid",
  "safety_report": {"score": 0.96, "issues": [], "requires_human_review": false}
}

## Publisher Receipt

{
  "publish_id": "uuid",
  "task_id": "uuid",
  "channel": "youtube",
  "status": "posted",
  "remote_id": "remote-123",
  "timestamp": "ISO-8601"
}
