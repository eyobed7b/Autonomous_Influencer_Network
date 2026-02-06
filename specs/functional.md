# Functional Specifications

## Overview

This document captures user stories, acceptance criteria, and primary flows for the Autonomous Influencer Network (AIN). Stories are written for agents, editors, orchestrators, and operators.

## User Stories

- As a Planner agent, I need to fetch trending topics from configured sources so that generated content is timely and relevant.
- As a Generator agent, I need to produce a draft short-form video (script, assets, rough render) given a `persona_id` and trend prompt.
- As a Judge agent, I need to run automated safety and brand-safety checks and return pass/fail and per-check confidence scores.
- As an Editor (human), I need to review generated drafts with change requests and approve or reject for publish.
- As a Publisher agent, I need to publish approved videos to target channels and report publish receipts and errors.
- As an Orchestrator (Chimera), I need to create and manage DAGs of atomic tasks with `task_id` and `state_version` for OCC and replay.
- As an Operator, I need node health and capacity metrics for load-balancing and capacity planning.

## Primary Flows

- Trend → Planner: Planner ingests trends, maps to persona(s), and emits `generate_video` tasks.
- Generate → Judge → Human Review: Worker generates draft, Judge validates; low-confidence or failed checks route to Human Review.
- Approve → Publish: Approved items are passed to Publisher which posts to channels and stores publish receipts.

## Acceptance Criteria

- All generated artifacts must include metadata: `persona_id`, `trend_source`, `task_id`, `confidence_score`.
- Worker updates must include `state_version` increments to enable OCC.
- Rejected content must include structured `rejection_reason` and optional `retry_suggestion`.
- All tasks must produce an audit trail entry with `actor`, `action`, `task_id`, `timestamp`, `state_before`, `state_after`.

## Edge Cases

- Missing assets: Workers must return a deterministic error code and a list of missing asset URLs.
- Partial success (some assets generated): Store partial artifacts with `partial: true` and allow resume.
- Rate-limited publish: Publisher should enqueue publish retries with exponential backoff and surface final status.

## Operational Acceptance

- SLOs: 95th percentile latency for atomic tasks < 180s.
- Data retention: Audit logs retained for 365 days; media retained per storage policy.
