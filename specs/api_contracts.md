# API Contracts (Agent Message Schemas)

## Agent Task Message (input)

{
"task_id": "string",
"type": "string", // e.g. "generate_video", "fetch_trends"
"persona_id": "string",
"payload": { /_ type-specific payload _/ },
"meta": {
"created_by": "planner",
"created_at": "2026-01-01T00:00:00Z"
}
}

## Agent Response (output)

{
"task_id": "string",
"status": "completed|failed|in_progress",
"result": { /_ type-specific result _/ },
"errors": [ { "code": "string", "message": "string" } ],
"state_version": 3,
"confidence": 0.92
}

## Example: generate_video.payload

{
"prompt": "string",
"assets": [ { "type": "image|audio", "url": "string" } ],
"length_seconds": 15,
"style": "string"
}

## Example: generate_video.result

{
"video_url": "https://...",
"thumbnail_url": "https://...",
"duration": 15,
"render_log": "string"
}

Agents must validate messages against these schemas and return informative errors for invalid inputs.
