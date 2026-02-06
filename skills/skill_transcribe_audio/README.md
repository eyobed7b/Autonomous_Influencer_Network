# skill_transcribe_audio

Purpose: take a staged audio or video asset, produce a time-aligned transcript, and return per-segment confidence scores.

Behavioral constraints:

- Transcription models must be specified (model name + version) in the input when determinism is required.
- PII detection: flag potential PII and include `pii_flags` in `safety_report`.

Input contract (JSON):

```json
{
  "task_id": "uuid",
  "asset_url": "s3://bucket/path/audio.mp4",
  "language_hint": "en",
  "model": { "name": "wav2vec2", "version": "1.0" },
  "segments": { "start_offset": 0, "end_offset": null }
}
```

Output contract (JSON):

```json
{
  "task_id": "uuid",
  "status": "completed|failed",
  "transcript": [
    { "start_ms": 0, "end_ms": 1200, "text": "Hello world", "confidence": 0.97 }
  ],
  "language": "en",
  "duration_ms": 12000,
  "safety_report": { "pii_flags": [], "passed": true },
  "errors": []
}
```

Notes:

- Provide timestamps in milliseconds for precise alignment.
- Support outputting VTT/JSON and optional word-level timestamps when requested.
