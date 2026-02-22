# Sprint 3 Implementation Plan: Quality & Real-Time Experience

**Goal:** Elevate the pipeline from working prototype → polished product with streaming output, resilience testing, and enhanced dashboard.

**Duration:** Week 5-6 (2026-03-03 → 2026-03-16)

---

## 👥 The Team

| Agent | Role | Sprint 3 Work |
|-------|------|--------------|
| **Director** 🎬 | Orchestrator | Streaming pipeline + Server-Sent Events |
| **Polish** 🎨 | Frontend | Real-time streaming UI + History panel |
| **Brew** 🧠 | Backend | Content history DB + Resiliency suite |
| **Scout** 🔍 | Researcher | Caching layer for repeat topics |

---

## 🏗️ Architecture Changes

```
Current:  Frontend → POST /api/v1/pipeline → wait 5-15 min → JSON response
Sprint 3: Frontend → POST /api/v1/pipeline/stream → SSE stream → real-time updates
```

---

## 📅 Tasks

### Task 15: Server-Sent Events (SSE) Pipeline Streaming
**Agent:** Director 🎬 | **Estimate:** 6 hours

**Why:** Users currently wait up to 15 minutes with no feedback. SSE streams each stage's output as it completes.

#### Changes:
- **[NEW] `backend/api/v1/stream.py`** — SSE endpoint using `StreamingResponse`
- **[MODIFY] `backend/orchestrator/pipeline.py`** — Yield events after each stage:
  ```
  event: stage_start    data: {"stage": "scout", "status": "running"}
  event: stage_complete data: {"stage": "scout", "result": {...}}
  event: stage_start    data: {"stage": "draft", "status": "running"}
  ...
  event: pipeline_done  data: {"full_context": {...}}
  ```
- **[MODIFY] `backend/api/v1/routes.py`** — Register streaming router

#### Tests:
- `backend/tests/test_streaming.py` — Mock SSE response parsing

---

### Task 16: Real-Time Dashboard UI
**Agent:** Polish 🎨 | **Estimate:** 5 hours

**Why:** Dashboard needs to consume SSE stream and show live progress.

#### Changes:
- **[MODIFY] `frontend/app.js`** — Replace `fetch()` with `EventSource` for `/api/v1/pipeline/stream`
- **[MODIFY] `frontend/index.html`** — Add per-stage result panels (research summary, outline preview, article)
- **[MODIFY] `frontend/style.css`** — Animated pulse/glow on active stage, typewriter effect for article

#### Acceptance:
- Each stage card lights up in sequence
- Research sources displayed as they arrive
- Outline sections shown before writing starts
- Article appears with typewriter animation

---

### Task 17: Content History & Persistence
**Agent:** Brew 🧠 | **Estimate:** 5 hours

**Why:** Generated articles are lost on page refresh. Store and browse past runs.

#### Changes:
- **[NEW] `backend/storage/history.py`** — SQLite-backed history store
  ```python
  class ContentHistory:
      async def save_run(self, context: PipelineContext) -> str  # returns run_id
      async def get_run(self, run_id: str) -> PipelineContext
      async def list_runs(self, limit=20) -> List[dict]  # summaries
  ```
- **[NEW] `backend/api/v1/history_routes.py`** — `GET /api/v1/history`, `GET /api/v1/history/{run_id}`
- **[MODIFY] `frontend/index.html`** — Add "📚 History" sidebar panel
- **[MODIFY] `frontend/app.js`** — Fetch and display past runs

#### Tests:
- `backend/tests/test_history.py` — CRUD operations

---

### Task 18: Research Caching
**Agent:** Scout 🔍 | **Estimate:** 3 hours

**Why:** Identical topics re-search the web every time. Cache research results for repeat topics.

#### Changes:
- **[NEW] `backend/utils/cache.py`** — TTL-based in-memory cache (default 1 hour)
- **[MODIFY] `backend/agents/research_agent.py`** — Check cache before searching
- **[MODIFY] `backend/orchestrator/pipeline.py`** — Pass cache to Scout

#### Tests:
- `backend/tests/test_cache.py` — Hit/miss/expiry scenarios

---

### Task 19: Pipeline Resiliency Test Suite
**Agent:** Brew 🧠 | **Estimate:** 4 hours

**Why:** Sprint 2 plan listed this as Step 6 but it was deferred.

#### Changes:
- **[NEW] `backend/tests/test_pipeline_resiliency.py`**
  - Simulate LLM timeout → pipeline completes with fallback
  - Simulate research failure → pipeline continues with general knowledge
  - Simulate outline validation failure → retry logic works
  - Simulate all agents failing → graceful error response
  - Concurrent pipeline runs don't interfere

#### No production code changes — pure test coverage.

---

## ✅ Sprint 3 Definition of Done

1. Pipeline streams events in real-time (SSE)
2. Dashboard shows live stage updates with animations
3. Past runs saved to SQLite and browsable
4. Research cached for repeated topics
5. Resiliency suite passes (5+ failure scenarios)
6. All existing tests still pass

---

## 🏷️ GitHub Tracking

| Task | Issue | Branch |
|------|-------|--------|
| 15: SSE Streaming | To create | `feat/task-15-sse-streaming` |
| 16: Real-Time UI | To create | `feat/task-16-realtime-ui` |
| 17: Content History | To create | `feat/task-17-content-history` |
| 18: Research Caching | To create | `feat/task-18-research-cache` |
| 19: Resiliency Tests | To create | `feat/task-19-resiliency-tests` |
