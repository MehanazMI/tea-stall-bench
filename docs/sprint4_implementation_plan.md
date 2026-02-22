# Sprint 4 Implementation Plan: Production & Multi-Channel Publishing

**Goal:** Take Tea Stall Bench from dev tool → production-ready platform with multi-channel publishing, scheduling, and analytics.

**Duration:** Week 7-8 (2026-03-17 → 2026-03-30)

---

## 👥 The Team

| Agent | Role | Sprint 4 Work |
|-------|------|--------------|
| **Relay** 📱 | Publisher | Multi-channel: WhatsApp, Email, Telegram |
| **Director** 🎬 | Orchestrator | Scheduled pipeline runs |
| **Polish** 🎨 | Frontend | Publishing UI + Analytics dashboard |
| **Brew** 🧠 | Backend | Authentication, rate limiting, deployment |

---

## 🏗️ Architecture Changes

```
Current:  Pipeline → Article only (no publishing from dashboard)
Sprint 4: Pipeline → Article → Choose channel → Publish → Track analytics
```

---

## 📅 Tasks

### Task 20: Multi-Channel Publisher
**Agent:** Relay 📱 | **Estimate:** 6 hours

**Why:** Currently only WhatsApp is supported. Add Email and Telegram channels.

#### Changes:
- **[NEW] `backend/agents/email_publisher.py`** — SMTP-based email publishing
  - Uses `smtplib` + `email.mime`
  - Configurable SMTP settings via `.env`
  - HTML email template with article formatting
- **[NEW] `backend/agents/telegram_publisher.py`** — Telegram Bot API publisher
  - Uses `httpx` to call Telegram Bot API
  - Markdown formatting for Telegram
  - Channel/group publishing support
- **[MODIFY] `backend/agents/publisher_agent.py`** — Abstract base with `publish()` method
- **[MODIFY] `backend/config.py`** — Add email/telegram channel configs to CHANNELS

#### Tests:
- `backend/tests/test_email_publisher.py` — Mock SMTP
- `backend/tests/test_telegram_publisher.py` — Mock HTTP

---

### Task 21: Publishing from Dashboard
**Agent:** Polish 🎨 | **Estimate:** 5 hours

**Why:** Users currently can't publish directly from the dashboard.

#### Changes:
- **[NEW] `POST /api/v1/publish`** — Endpoint accepting `{run_id, channel, target}`
- **[MODIFY] `frontend/index.html`** — Add "📤 Publish" button on article output with channel selector
- **[MODIFY] `frontend/app.js`** — Publish flow: select channel → confirm → call API → show status
- **[MODIFY] `frontend/style.css`** — Publish modal with channel icons

#### Acceptance:
- After pipeline completes, "Publish" button appears
- User picks: WhatsApp / Email / Telegram
- Confirmation modal before sending
- Success/failure feedback

---

### Task 22: Content Scheduling
**Agent:** Director 🎬 | **Estimate:** 5 hours

**Why:** Enable users to schedule content generation for later (e.g., daily blog posts).

#### Changes:
- **[NEW] `backend/scheduler/scheduler.py`** — APScheduler-based task runner
  ```python
  class ContentScheduler:
      def schedule_pipeline(self, topic, cron_expression, channel) -> job_id
      def cancel_job(self, job_id)
      def list_jobs() -> List[ScheduledJob]
  ```
- **[NEW] `backend/api/v1/schedule_routes.py`** — `POST /api/v1/schedule`, `GET /api/v1/schedule`, `DELETE /api/v1/schedule/{id}`
- **[MODIFY] `frontend/index.html`** — "⏰ Schedule" tab with cron builder (daily/weekly/custom)
- **[MODIFY] `frontend/app.js`** — Schedule management UI

#### Tests:
- `backend/tests/test_scheduler.py` — Job CRUD, trigger simulation

---

### Task 23: Analytics Dashboard
**Agent:** Polish 🎨 | **Estimate:** 4 hours

**Why:** Track content generation stats: topics, word counts, styles used, compliance scores.

#### Changes:
- **[NEW] `backend/api/v1/analytics_routes.py`** — Aggregate stats from history
  ```
  GET /api/v1/analytics → {
    total_runs, avg_word_count, avg_compliance,
    top_topics, style_distribution, runs_per_day
  }
  ```
- **[MODIFY] `frontend/index.html`** — "📊 Analytics" tab
- **[NEW] `frontend/charts.js`** — Lightweight charting (Canvas-based, no dependencies)
  - Runs per day (bar chart)
  - Style distribution (pie chart)
  - Compliance trend (line chart)

#### Depends on: Task 17 (Content History from Sprint 3)

---

### Task 24: Production Deployment & Security
**Agent:** Brew 🧠 | **Estimate:** 5 hours

**Why:** Harden the backend for real-world use.

#### Changes:
- **[NEW] `backend/middleware/rate_limiter.py`** — Token-bucket rate limiting (60 req/min)
- **[NEW] `backend/middleware/auth.py`** — API key authentication (simple bearer token)
- **[MODIFY] `backend/main.py`** — Register middleware, tighten CORS
- **[NEW] `Dockerfile`** — Container image for deployment
- **[NEW] `docker-compose.yml`** — Full stack: API + Ollama
- **[MODIFY] `README.md`** — Production deployment guide

#### Tests:
- `backend/tests/test_rate_limiter.py`
- `backend/tests/test_auth.py`

---

## ✅ Sprint 4 Definition of Done

1. Publish to WhatsApp, Email, or Telegram from dashboard
2. Schedule recurring content generation
3. Analytics dashboard with charts
4. API key auth + rate limiting
5. Docker deployment ready
6. All tests passing (target: 100+ total)
7. README with full deployment guide

---

## 🏷️ GitHub Tracking

| Task | Issue | Branch |
|------|-------|--------|
| 20: Multi-Channel Publisher | To create | `feat/task-20-multi-channel` |
| 21: Dashboard Publishing | To create | `feat/task-21-publish-ui` |
| 22: Content Scheduling | To create | `feat/task-22-scheduler` |
| 23: Analytics Dashboard | To create | `feat/task-23-analytics` |
| 24: Production & Security | To create | `feat/task-24-production` |

---

## 🎉 Project Completion

After Sprint 4, Tea Stall Bench will be a **production-ready AI content pipeline** with:

| Capability | Status |
|-----------|--------|
| Research → Outline → Write pipeline | ✅ Sprint 2 |
| Streaming real-time output | Sprint 3 |
| Content history & caching | Sprint 3 |
| Multi-channel publishing | Sprint 4 |
| Scheduled content generation | Sprint 4 |
| Analytics & insights | Sprint 4 |
| Auth + rate limiting + Docker | Sprint 4 |
