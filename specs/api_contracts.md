# API Contracts (Agent Message Schemas)

This file describes the JSON contracts used between Chimera, agents, and workers. All messages are UTF-8 JSON, follow snake_case keys, and must validate against the schemas below.

## Common Headers

- `task_id` (string, uuid): global unique id for the task.
- `created_by` (string): actor that created the task (planner, operator).
- `created_at` (string, RFC3339 timestamp).

## Agent Task Message (input)

Example (generate_video task):

```json
{
  "task_id": "11111111-1111-1111-1111-111111111111",
  "type": "generate_video",
  "persona_id": "22222222-2222-2222-2222-222222222222",
  "payload": {
    "prompt": "Short comedic skit about coffee and productivity",
    "assets": [],
    "length_seconds": 15,
    "style": "fast_cuts,bright_colors"
  },
  "meta": {
    "created_by": "planner",
    "created_at": "2026-02-05T12:00:00Z"
  },
  "state_version": 1
}
```

Validation rules:

- `type` must be one of the registered task types (see spec registry).
- `state_version` is the expected current version for OCC updates.

## Agent Response (output)

Standard response fields for workers:

```json
{
  "task_id": "...",
  "status": "completed",
  "result": {
    /* type-specific */
  },
  "errors": [],
  "state_version": 2,
  "confidence": 0.92
}
```

- `status`: one of `completed`, `failed`, `in_progress`, `retriable`.
- `errors`: structured list with `code`, `message`, and optional `details`.

## generate_video.payload

Fields:

- `prompt` (string, required)
- `assets` (array of {type, url}, optional)
- `length_seconds` (int)
- `style` (string, optional)

Example result for `generate_video`:

```json
{
  "video_url": "https://s3/.../video.mp4",
  "thumbnail_url": "https://s3/.../thumb.jpg",
  "duration_seconds": 15,
  "render_log": "https://logs/...",
  "safety_report": {
    "passed": true,
    "checks": [
      { "name": "no_pii", "passed": true, "confidence": 0.98 },
      { "name": "brand_safety", "passed": true, "confidence": 0.95 }
    ]
  }
}
```

## fetch_trends.payload

```json
{
  "source": "twitter|youtube|trend_api",
  "region": "us",
  "limit": 10
}
```

Result:

```json
{
  "trends": [{ "id": "t1", "title": "...", "score": 0.85 }]
}
```

## Error contract

Standard error object:

```json
{
  "code": "INVALID_PAYLOAD",
  "message": "Detailed message",
  "details": {
    /* optional */
  }
}
```

## Idempotency & Ordering

- Publishers and external side-effects MUST support idempotency via `task_id` and explicit `idempotency_key` when present.

Agents must validate messages against these schemas and return informative errors for invalid inputs.
