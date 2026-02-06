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

### JSON Schema (trend object)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "trend_id",
    "title",
    "score",
    "source",
    "timestamp",
    "tags",
    "metrics"
  ],
  "properties": {
    "trend_id": { "type": "string" },
    "title": { "type": "string" },
    "score": { "type": "number" },
    "source": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "tags": { "type": "array", "items": { "type": "string" } },
    "metrics": {
      "type": "object",
      "properties": {
        "mentions": { "type": "integer" },
        "engagement": { "type": "number" }
      },
      "required": ["mentions", "engagement"]
    }
  }
}
```

## generate_video Task (Planner → Queue)

{
"task_id": "uuid",
"type": "generate_video",
"persona_id": "persona-123",
"payload": { /_ contains trend object plus normalization _/ },
"state_version": 1,
"created_at": "ISO-8601"
}

### JSON Schema (generate_video task)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "task_id",
    "type",
    "persona_id",
    "payload",
    "state_version",
    "created_at"
  ],
  "properties": {
    "task_id": { "type": "string" },
    "type": { "type": "string", "enum": ["generate_video"] },
    "persona_id": { "type": "string" },
    "payload": { "type": "object" },
    "state_version": { "type": "integer" },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

## Worker ACK/NACK

Success:
{
"task_id": "uuid",
"status": "completed",
"state_version": 2,
"artifacts": {"s3_path": "s3://.../render.mp4"}
}

### JSON Schema (worker ack)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["task_id", "status", "state_version"],
  "properties": {
    "task_id": { "type": "string" },
    "status": { "type": "string", "enum": ["completed", "failed"] },
    "state_version": { "type": "integer" },
    "artifacts": { "type": "object" },
    "errors": { "type": "array", "items": { "type": "object" } }
  }
}
```

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
