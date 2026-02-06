# skill_generate_video

Purpose: given a prompt, persona, and assets, generate a short-form video draft including composited visuals, music, and TTS voiceover.

Behavioral constraints:

- Output drafts must include `confidence` and `safety_report`.
- Keep renders deterministic when `seed` is provided.
- Support `partial` mode where only assets or audio are produced.

Input contract (JSON):

```json
{
  "task_id": "uuid",
  "persona_id": "uuid",
  "prompt": "Punchy 10s hook about productivity",
  "assets": [{ "type": "image|video|audio", "url": "s3://..." }],
  "length_seconds": 10,
  "style": "fast_cuts",
  "seed": 12345,
  "render_options": { "resolution": "720p", "bitrate": 1500000 }
}
```

Output contract (JSON):

```json
{
  "task_id": "uuid",
  "status": "completed|failed|partial",
  "video_url": "s3://bucket/path/draft.mp4",
  "thumbnail_url": "s3://bucket/path/thumb.jpg",
  "duration_seconds": 10,
  "render_logs": "https://logs/...",
  "confidence": 0.91,
  "safety_report": { "passed": true, "checks": [] },
  "assets_produced": [{ "type": "image", "url": "s3://..." }],
  "errors": []
}
```

Notes:

- Rendering should write intermediate artifacts (clips, audio) to object storage and report their URLs.
- Publishers will only be invoked for outputs where `status == completed` and `safety_report.passed == true` or after human approval.
