# Database Schema — Video Metadata ERD

## Tables

### videos

- id (UUID, PK)
- persona_id (UUID, FK -> personas.id)
- title (text)
- description (text)
- video_url (text)
- thumbnail_url (text)
- duration_seconds (int)
- status (enum: draft, pending_review, published, rejected)
- confidence (float)
- created_at (timestamp)
- updated_at (timestamp)
- state_version (int) -- for OCC

### assets

- id (UUID, PK)
- video_id (UUID, FK -> videos.id)
- type (image|audio|raw)
- url (text)
- checksum (text)

### personas

- id (UUID, PK)
- name (text)
- voice_profile (json)

### tags

- id (UUID, PK)
- name (text)

### video_tags

- video_id (UUID, FK -> videos.id)
- tag_id (UUID, FK -> tags.id)

## ERD (textual)

videos 1--_ assets
videos _--_ tags (via video_tags)
videos _--1 personas

## Notes

- Use `state_version` increments for OCC when workers update `videos` to avoid lost updates.
- Store large binary assets in object storage; save URLs and checksums in Postgres.
