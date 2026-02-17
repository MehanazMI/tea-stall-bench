# Sprint 2 Implementation Plan: The Collaborative Pipeline (Production Ready)

**Goal:** Transform the Tea Stall Bench into a robust, fault-tolerant **Research → Outline → Write** pipeline.

## 👥 The Team (New Members)
| Agent | Role | Status | Responsibility |
|-------|------|--------|----------------|
| **Scout** 🔍 | Researcher | ✅/🔄 | Gathering facts (Hardening required) |
| **Draft** 📝 | Outliner | 🚧 New | Creating logical content structures |
| **Ink** ✍️ | Writer | 🔄 Upgrade | Writing content based on research & outline |
| **Director** 🎬 | Orchestrator | 🚧 New | Managing the workflow & state |

---

## 🏗️ Architecture: "Production Ready"

### 1. Robust Orchestration (`Director`)
**File:** `backend/orchestrator.py`
- **State:** `PipelineContext` (Dataclass) - Immutable where possible.
- **Error Handling:** Circuit Breaker pattern. If `Scout` fails 3 times, fallback to "General Knowledge" mode.
- **Logging:** Structured JSON logging (`structlog` compatible format) for observability.

### 2. Outline Agent (`Draft`) - Strict Validation
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

### 3. Research Agent (`Scout`) - Hardening [Task 8.5]
**User Concern:** "Where is the research plan?" -> **It needs resilience.**
- **Current:** Single provider (Parallel OR DuckDuckGo).
- **Upgrade:** **Hybrid Search Provider**.
  - Try `Parallel.AI` (Premium) first.
  - If fails/timeouts -> Fallback to `DuckDuckGo` (Free) silently.
  - Telemetry: Log the fallback event.

---

## 📅 Implementation Steps (Refined)

### Phase 1: Robust Foundations (Week 3)

#### Step 0: Centralized Configuration [Task 8.9]
- [ ] Create `backend/config.py` with shared constants (`CONTENT_TYPES`, `STYLES`, etc.).
- [ ] Refactor `WriterAgent` to import from config.
- [ ] Ensure `Scout` and `Draft` refer to these constants for context.

#### Step 1: Research Agent Hardening [Task 8.5]
- [ ] Create `HybridSearchProvider` in `backend/utils/search_client.py`.
- [ ] Implement fallback logic (Parallel -> DDG).
- [ ] Add `test_hybrid_search.py` (Mocking failures).

#### Step 2: Create Outline Agent (`Draft`) [Task 9]
- [ ] Implement `OutlineAgent` class.
- [ ] Enforce **JSON Output** with Pydantic validation.
- [ ] Add `test_outline_agent.py`.

#### Step 3: Build Orchestrator (`Director`) [Task 10]
- [ ] Create `Orchestrator` class with `PipelineContext`.
- [ ] Implement **Circuit Breaker** logic.
- [ ] Add structured logging.

### Phase 2: Integration & Stability (Week 4)

#### Step 4: Upgrade Writer (`Ink`) [Task 11]
- [ ] Update Prompt to ingest `Outline` (JSON).
- [ ] strict compliance check ("Did I miss any section?").

#### Step 5: Visual Dashboard [Task 12]
- [ ] Real-time polling UI.
- [ ] Display "Fallback" status (e.g., "⚠️ Research failed, using backup").

#### Step 6: End-to-End Stress Test
- [ ] `tests/test_pipeline_resiliency.py`: Simulate API outages and ensure pipeline finishes.

---

## ✅ Definition of Done (Production Standards)
1.  **Resiliency:** Pipeline completes even if external APIs (Parallel) flicker.
2.  **Type Safety:** All data passing between agents is Pydantic Models, not dicts.
3.  **Observability:** Every step logs `trace_id`, `agent`, `status`, `duration`.
4.  **Testing:** 90%+ coverage on new modules.
