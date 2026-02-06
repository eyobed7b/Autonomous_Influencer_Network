# Chimera Skills — Overview

This directory contains modular "Skills" (capability packages) that the Chimera agent can load and execute. Each skill lives in its own subdirectory and exposes a clear Input/Output contract so orchestrator, planners, and workers can interoperate safely.

Critical skills (defined below in subfolders):

- `skill_download_youtube` — download and validate source videos for a trend.
- `skill_transcribe_audio` — transcribe audio tracks into time-aligned text with confidence.
- `skill_generate_video` — assemble assets, run TTS, and render a short-form video draft.

Guidelines:

- Skills must validate inputs against the declared schema and return structured errors.
- Side-effects (downloads, external publishes) must be idempotent and reference `task_id`.
- All skills must emit `safety_report` when relevant and include `confidence` fields.

See individual skill READMEs for Input/Output contracts and examples.
