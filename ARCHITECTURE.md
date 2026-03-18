# Architecture Design — Scalable GitHub Data Aggregation System

## Objective
Design a system that aggregates repository data from 300+ GitHub 
repositories and serves it to a website, while minimizing API 
usage and ensuring scalability to 10 000+ repositories.

---
<img width="1096" height="1079" alt="Capture d&#39;écran 2026-03-18 234335" src="https://github.com/user-attachments/assets/40457afd-e762-4641-ae19-a1006062327c" />

## Core Components

### 1. Data Ingestion Layer
Three complementary update mechanisms:
- **GitHub Webhooks** — real-time event detection (push, release, 
  issues). Eliminates polling for active repos.
- **Cron jobs** — hourly scheduled sync for repos without webhooks.
- **Incremental updates with ETag** — GitHub returns HTTP 304 
  Not Modified if nothing changed, consuming zero rate limit quota.

### 2. Processing Layer
Normalizes raw GitHub API responses: strips unused fields, 
enriches with computed metrics (activity score, complexity), 
deduplicates contributors across repos, and prepares structured 
objects for storage.

### 3. Storage Layer (PostgreSQL)
Persisted data: repo name, description, stars, forks, 
contributors, languages, last_pushed_at, computed scores.
Dynamic data (real-time issue counts, PR status) fetched 
live from GitHub API on demand.

### 4. Cache Layer (Redis)
- TTL: 5 minutes for repo lists, 1 minute for individual repos.
- Cache-aside pattern: API layer checks Redis first, falls back 
  to PostgreSQL, then GitHub API.
- In-memory fallback if Redis is unavailable.

### 5. API Layer (NestJS)
REST endpoints consumed by the Angular frontend:
- `GET /api/v1/repos` — paginated repo list (served from cache)
- `GET /api/v1/repos/:owner/:name` — single repo detail
- `POST /webhooks/github` — webhook receiver

### 6. Frontend (Angular)
Consumes the API layer exclusively — never calls GitHub API 
directly. Displays repo cards, contributor stats, project pages.

---

## Rate Limit Strategy
- **ETag / Conditional GET**: `If-None-Match` header reuses the 
  cached ETag. GitHub returns 304 and does not count against the 
  5 000 req/h limit.
- **Token pool**: rotate multiple GitHub tokens to multiply 
  the effective rate limit.
- **Webhook-first**: only fetch via API when a webhook event 
  signals a change — avoids blind polling.
- **Priority queue**: active repos (pushed < 24h) polled every 
  hour; inactive repos (pushed > 30 days) polled weekly.

---

## Update Mechanism
1. GitHub fires a webhook on push/release/issue events.
2. The ingestion layer enqueues the repo for refresh.
3. The processing layer fetches only the changed fields 
   (using ETag for unchanged ones).
4. PostgreSQL is updated; Redis cache is invalidated.
5. Next frontend request hits the fresh cache.

---

## Scalability Plan (300 → 10 000 repos)

| Component | 300 repos | 10 000 repos |
|-----------|-----------|--------------|
| Ingestion | Single cron job | Distributed queue (BullMQ) |
| GitHub API | 1 token (5k req/h) | Token pool (10 tokens = 50k req/h) |
| Storage | Single PostgreSQL | Read replicas + connection pool |
| Cache | Single Redis instance | Redis Cluster |
| API layer | Single NestJS instance | Horizontal scaling behind load balancer |

---

## Failure Handling
- **API failure**: serve stale cache data with a `X-Cache-Stale` 
  header. Never return an empty response.
- **Rate limit exhaustion**: exponential backoff with jitter. 
  Switch to next token in pool.
- **Unavailable repo**: mark as `status: archived` in DB after 
  3 consecutive 404s. Stop polling.
- **Redis down**: fall through to PostgreSQL. Log the incident.

---

## Technology Justification

| Technology | Reason |
|------------|--------|
| NestJS | Already used in WebiU backend. TypeScript, modular. |
| PostgreSQL | Already used in WebiU. Relational, reliable. |
| Redis | Industry standard for API response caching. TTL support. |
| BullMQ | Redis-backed job queue, ideal for ingestion at scale. |
| GitHub Webhooks | Zero-polling real-time updates. |
| Angular | Already used in WebiU frontend. |
