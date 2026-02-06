# Database Schema (ERD overview)

The primary relational store is Postgres. Below are the key tables and relationships.

## Tables

1) `personas`
- `persona_id` UUID PK
- `name` TEXT
- `tone_profile` JSONB

2) `videos`
- `video_id` UUID PK
- `persona_id` UUID FK -> personas(persona_id)
- `title` TEXT
- `state_version` INTEGER
- `status` TEXT
- `published_at` TIMESTAMP NULLABLE
- `created_at` TIMESTAMP

3) `tasks`
- `task_id` UUID PK
- `video_id` UUID NULLABLE FK -> videos(video_id)
- `type` TEXT
- `payload` JSONB
- `state_version` INTEGER
- `status` TEXT
- `created_at` TIMESTAMP

4) `artifacts`
- `artifact_id` UUID PK
- `video_id` UUID FK -> videos(video_id)
- `s3_path` TEXT
- `kind` TEXT (script|render|thumbnail|audio)

5) `safety_reports`
- `report_id` UUID PK
- `task_id` UUID FK -> tasks(task_id)
- `score` FLOAT
- `issues` JSONB
- `requires_human_review` BOOLEAN

6) `publish_receipts`
- `publish_id` UUID PK
- `video_id` UUID FK -> videos(video_id)
- `channel` TEXT
- `status` TEXT
- `remote_id` TEXT
- `timestamp` TIMESTAMP

## Indexes & Constraints
- Indexes on `tasks(state_version)`, `videos(state_version)`, `tasks(status)`, and `publish_receipts(channel)`.
- Foreign keys enforce referential integrity; updates to `state_version` must be done via optimistic locking pattern.
