# Database Schema — Video Metadata ERD

This document defines the relational schema for storing videos, assets, personas, tags, and audit logs. The design favors small transactional updates (Postgres) and large binary storage in object storage.

## Tables (schema + sample types)

### videos

- `id` UUID PRIMARY KEY
- `persona_id` UUID REFERENCES personas(id)
- `title` TEXT
- `description` TEXT
- `video_url` TEXT
- `thumbnail_url` TEXT
- `duration_seconds` INT
- `status` TEXT CHECK (status IN ('draft','pending_review','published','rejected'))
- `confidence` FLOAT
- `state_version` INT NOT NULL DEFAULT 1
- `created_at` TIMESTAMP WITH TIME ZONE DEFAULT now()
- `updated_at` TIMESTAMP WITH TIME ZONE DEFAULT now()

### assets

- `id` UUID PRIMARY KEY
- `video_id` UUID REFERENCES videos(id) ON DELETE CASCADE
- `type` TEXT CHECK (type IN ('image','audio','raw'))
- `url` TEXT
- `checksum` TEXT
- `created_at` TIMESTAMP WITH TIME ZONE DEFAULT now()

### personas

- `id` UUID PRIMARY KEY
- `name` TEXT
- `voice_profile` JSONB
- `style_profile` JSONB

### tags

- `id` UUID PRIMARY KEY
- `name` TEXT UNIQUE

### video_tags

- `video_id` UUID REFERENCES videos(id) ON DELETE CASCADE
- `tag_id` UUID REFERENCES tags(id)
- PRIMARY KEY(video_id, tag_id)

### task_audit

- `id` BIGSERIAL PRIMARY KEY
- `task_id` UUID
- `actor` TEXT
- `action` TEXT
- `state_before` JSONB
- `state_after` JSONB
- `state_version` INT
- `timestamp` TIMESTAMP WITH TIME ZONE DEFAULT now()

### publish_receipts

- `id` UUID PRIMARY KEY
- `video_id` UUID REFERENCES videos(id)
- `channel` TEXT
- `external_id` TEXT
- `status` TEXT
- `details` JSONB
- `created_at` TIMESTAMP WITH TIME ZONE DEFAULT now()

## ERD (textual)

videos 1--_ assets
videos _--_ tags (via video_tags)
videos _--1 personas
videos 1--\* publish_receipts

## Sample SQL (Postgres)

```sql
CREATE TABLE videos (
	id uuid PRIMARY KEY,
	persona_id uuid REFERENCES personas(id),
	title text,
	description text,
	video_url text,
	thumbnail_url text,
	duration_seconds int,
	status text CHECK (status IN ('draft','pending_review','published','rejected')),
	confidence float,
	state_version int NOT NULL DEFAULT 1,
	created_at timestamptz DEFAULT now(),
	updated_at timestamptz DEFAULT now()
);
```

## Notes

- Use `state_version` increments for OCC when workers update `videos` to avoid lost updates. Update statements must use `WHERE state_version = <expected>` and `SET state_version = state_version + 1`.
- Store large binary assets in object storage; save URLs and checksums in Postgres.
- `task_audit` provides a compact, append-only audit trail for replay and debugging.
