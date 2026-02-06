# Database Schema (ERD overview)

The primary relational store is Postgres. Below are the key tables and relationships.

## Tables

1. `personas`

- `persona_id` UUID PK
- `name` TEXT
- `tone_profile` JSONB

2. `videos`

- `video_id` UUID PK
- `persona_id` UUID FK -> personas(persona_id)
- `title` TEXT
- `state_version` INTEGER
- `status` TEXT
- `published_at` TIMESTAMP NULLABLE
- `created_at` TIMESTAMP

3. `tasks`

- `task_id` UUID PK
- `video_id` UUID NULLABLE FK -> videos(video_id)
- `type` TEXT
- `payload` JSONB
- `state_version` INTEGER
- `status` TEXT
- `created_at` TIMESTAMP

4. `artifacts`

- `artifact_id` UUID PK
- `video_id` UUID FK -> videos(video_id)
- `s3_path` TEXT
- `kind` TEXT (script|render|thumbnail|audio)

5. `safety_reports`

- `report_id` UUID PK
- `task_id` UUID FK -> tasks(task_id)
- `score` FLOAT
- `issues` JSONB
- `requires_human_review` BOOLEAN

6. `publish_receipts`

- `publish_id` UUID PK
- `video_id` UUID FK -> videos(video_id)
- `channel` TEXT
- `status` TEXT
- `remote_id` TEXT
- `timestamp` TIMESTAMP

## Indexes & Constraints

- Indexes on `tasks(state_version)`, `videos(state_version)`, `tasks(status)`, and `publish_receipts(channel)`.
- Foreign keys enforce referential integrity; updates to `state_version` must be done via optimistic locking pattern.

## Example SQL DDL (Postgres)

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE personas (
	persona_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	name TEXT NOT NULL,
	tone_profile JSONB,
	created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE videos (
	video_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	persona_id UUID REFERENCES personas(persona_id),
	title TEXT,
	state_version INTEGER DEFAULT 0,
	status TEXT,
	published_at TIMESTAMPTZ,
	created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE tasks (
	task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	video_id UUID REFERENCES videos(video_id),
	type TEXT,
	payload JSONB,
	state_version INTEGER DEFAULT 0,
	status TEXT,
	created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE artifacts (
	artifact_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	video_id UUID REFERENCES videos(video_id),
	s3_path TEXT,
	kind TEXT,
	created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE safety_reports (
	report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	task_id UUID REFERENCES tasks(task_id),
	score FLOAT,
	issues JSONB,
	requires_human_review BOOLEAN DEFAULT false,
	created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE publish_receipts (
	publish_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	video_id UUID REFERENCES videos(video_id),
	channel TEXT,
	status TEXT,
	remote_id TEXT,
	timestamp TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_tasks_state_version ON tasks(state_version);
CREATE INDEX idx_videos_state_version ON videos(state_version);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_publish_channel ON publish_receipts(channel);
```
