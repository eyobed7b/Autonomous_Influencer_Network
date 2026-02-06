# skill_download_youtube

Purpose: retrieve a public video from YouTube (or other supported host), validate integrity, and stage it in object storage for downstream processing.

Behavioral constraints:

- MUST respect host TOS and rate limits.
- MUST NOT attempt to download private or age-restricted content unless explicit credentials and approvals are provided.
- Downloads must be idempotent and stored with `checksum` and `task_id` metadata.

Input contract (JSON):

```json
{
  "task_id": "uuid",
  "source": "youtube",
  "url": "https://www.youtube.com/watch?v=...",
  "max_bitrate": 2000000,
  "expected_format": "mp4",
  "meta": {
    "requested_by": "planner",
    "created_at": "2026-02-05T12:00:00Z"
  }
}
```

Output contract (JSON):

```json
{
  "task_id": "uuid",
  "status": "completed|failed",
  "staged_url": "s3://bucket/path/video.mp4",
  "checksum": "sha256:...",
  "duration_seconds": 12,
  "mime_type": "video/mp4",
  "size_bytes": 12345678,
  "errors": [],
  "confidence": 0.98
}
```

Errors: use structured error codes like `NOT_FOUND`, `RATE_LIMITED`, `INVALID_URL`, `UNAUTHORIZED`.

Example flow:

- Validate `url` and `task_id`.
- Download to ephemeral storage, transcode/normalize if needed, compute checksum.
- Upload to object storage and return `staged_url` and metadata.
