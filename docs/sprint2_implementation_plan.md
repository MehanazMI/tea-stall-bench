# Sprint 2 Implementation Plan: The Collaborative Pipeline (Production Ready)

**Goal:** Transform the Tea Stall Bench into a robust, fault-tolerant **Research → Outline → Write** pipeline.

## 👥 The Team (New Members)
| Agent | Role | Status | Responsibility |
|-------|------|--------|----------------|
| **Scout** 🔍 | Researcher | ✅ Done | Gathering facts with hybrid search fallback |
| **Draft** 📝 | Outliner | ✅ Done | Creating logical content structures (Pydantic) |
| **Ink** ✍️ | Writer | ✅ Done | Outline-aware writing with compliance check |
| **Director** 🎬 | Orchestrator | ✅ Done | Managing Scout → Draft → Ink pipeline |

---

## 🏗️ Architecture: "Production Ready"

### 1. Robust Orchestration (`Director`) [Task 12]
**File:** `backend/orchestrator.py`
- **State:** `PipelineContext` (Dataclass) - Immutable where possible.
- **Error Handling:** Circuit Breaker pattern. If `Scout` fails 3 times, fallback to "General Knowledge" mode.
- **Logging:** Structured JSON logging (`structlog` compatible format) for observability.

### 2. Outline Agent (`Draft`) - Strict Validation [Task 11]
**File:** `backend/agents/outline_agent.py`
- **Output:** **JSON** (Validated via Pydantic).
- **Schema:**
  ```python
  class Section(BaseModel):
      heading: str
      key_points: List[str]

  class Outline(BaseModel):
      title: str
      sections: List[Section]
  ```
- **Retry Logic:** If LLM outputs invalid JSON, auto-retry with error feedback.

### 3. Research Agent (`Scout`) - Hardening [Task 10]
**User Concern:** "Where is the research plan?" -> **It needs resilience.**
- **Current:** Single provider (Parallel OR DuckDuckGo).
- **Upgrade:** **Hybrid Search Provider**.
  - Try `Parallel.AI` (Premium) first.
  - If fails/timeouts -> Fallback to `DuckDuckGo` (Free) silently.
  - Telemetry: Log the fallback event.

---

## 📅 Implementation Steps (Refined)

### Phase 1: Robust Foundations (Week 3)

#### Step 0.1: Research Agent (Scout) [Task 8] - ✅ COMPLETED
- **Implemented:** `ResearchAgent` class.
- **Features:** DuckDuckGo + Parallel.AI MCP.
- **Commit:** `4a9b73a`

#### Step 0.2: Centralized Configuration [Task 9] - ✅ COMPLETED
- **Refactored:** `WriterAgent` to use `backend/config.py`.
- **Verified:** Tests passed.
- **Commit:** `18cd75f`

#### Step 1: Research Agent Hardening [Task 10] - ✅ COMPLETED
- **Implemented:** `HybridSearchProvider` (Parallel -> DDG).
- **Verified:** `scripts/test_hybrid_search.py`.
- **Commit:** `49aef91`

#### Step 2: Create Outline Agent (`Draft`) [Task 11] - ✅ COMPLETED
- **Implemented:** `OutlineAgent` with Pydantic validation.
- **Verified:** `backend/tests/test_outline_agent.py`.
- **Commit:** `07d80d3`

#### Step 3: Build Orchestrator (`Director`) [Task 12] - ✅ COMPLETED
- **Implemented:** `Orchestrator` class in `backend/orchestrator/pipeline.py`.
- **State:** `PipelineContext` (Pydantic Model) with full pipeline tracking.
- **Pipeline:** Scout → Draft → Ink with error handling and fallback.
- **Verified:** `backend/tests/test_orchestrator.py` (7 tests passed).

### Phase 2: Integration & Stability (Week 4)

#### Step 4: Upgrade Writer (`Ink`) [Task 13] - ✅ COMPLETED
- **Implemented:** Outline-aware prompt injection in `_build_prompt()`.
- **Compliance:** `_check_compliance()` verifies article covers all outline headings.
- **Verified:** `backend/tests/test_writer_enhanced.py` (14 tests passed).
- **PR:** #14 (squash-merged).

#### Step 5: Visual Dashboard [Task 14] - ✅ COMPLETED
- **Implemented:** `frontend/index.html`, `style.css`, `app.js` (dark-mode glassmorphism).
- **API:** `POST /api/v1/pipeline` endpoint for triggering the pipeline.
- **Serving:** `main.py` serves dashboard at `http://localhost:8000`.
- **Verified:** 33 tests passed, curl 200 OK.

#### Step 6: End-to-End Stress Test
- [ ] `tests/test_pipeline_resiliency.py`: Simulate API outages and ensure pipeline finishes.

---

## ✅ Definition of Done (Production Standards)
1.  **Resiliency:** Pipeline completes even if external APIs (Parallel) flicker.
2.  **Type Safety:** All data passing between agents is Pydantic Models, not dicts.
3.  **Observability:** Every step logs `trace_id`, `agent`, `status`, `duration`.
4.  **Testing:** 90%+ coverage on new modules.
