# Tea Stall Bench - GitHub Issues Template

> Use this to create GitHub Issues for sprint tasks. Each issue has checkboxes for checkpoints.

---

## How to Use This File

1. **For each task below**, create a GitHub Issue
2. **Copy the entire task** into the issue description
3. **Assign labels**: `sprint-1`, `backend`, `frontend`, etc.
4. **Track progress** by checking boxes as you complete checkpoints
5. **Close issue** when all checkpoints are ✅

---

## Sprint 1: Foundation (Week 1-2)

### Issue #1: Project Setup

**Labels:** `sprint-1`, `setup`, `infrastructure`  
**Assignee:** Backend AI Agent  
**Estimate:** 2 hours

**Description:**

Set up the initial project structure with all necessary folders and configuration files.

**Checkpoints:**

- [ ] Create folder structure (backend/agents, backend/orchestrator, backend/utils, frontend)
- [ ] Create requirements.txt with FastAPI, Uvicorn, Ollama dependencies
- [ ] Create .env.example with LLM configuration template
- [ ] Initialize Git and commit initial structure
- [ ] Push to GitHub

**Acceptance Criteria:**
- All folders exist and are visible in repository
- requirements.txt has all necessary dependencies
- Code is committed and pushed to GitHub

---

### Issue #2: Base Agent Class

**Labels:** `sprint-1`, `backend`, `core`  
**Assignee:** Backend AI Agent  
**Estimate:** 3 hours  
**Dependencies:** Issue #1

**Description:**

Create the foundational BaseAgent class that all AI agents will inherit from. Includes logging, error handling, and abstract execute method.

**Checkpoints:**

- [ ] Create `backend/agents/base_agent.py` file
- [ ] Implement BaseAgent class with `__init__` method
- [ ] Add logging capability using Python logging module
- [ ] Implement error handling wrapper in execute method
- [ ] Write comprehensive docstrings for all methods
- [ ] Create unit test file `backend/tests/test_base_agent.py`
- [ ] All tests pass
- [ ] Commit and push code

**Acceptance Criteria:**
- BaseAgent class can be instantiated
- Logging works and outputs to console
- Errors are caught and logged properly
- Tests pass: `pytest backend/tests/test_base_agent.py`

---

### Issue #3: LLM Client Integration

**Labels:** `sprint-1`, `backend`, `llm`  
**Assignee:** Backend AI Agent  
**Estimate:** 4 hours  
**Dependencies:** Issue #1

**Description:**

Create LLM client that connects to Ollama for content generation. This is the core AI integration.

**Checkpoints:**

- [ ] Create `backend/utils/llm_client.py` file
- [ ] Implement LLMClient class with Ollama integration
- [ ] Test connection to local Ollama instance
- [ ] Implement generate() method with prompt input
- [ ] Add error handling for connection failures and timeouts
- [ ] Write docstrings and type hints
- [ ] Create unit tests for LLM client
- [ ] All tests pass
- [ ] Commit and push code

**Acceptance Criteria:**
- Can connect to Ollama successfully
- `generate("Say hello")` returns a response
- Errors are handled gracefully
- Tests pass

**Prerequisites:**
- Ollama installed locally (`ollama pull llama3`)

---

### Issue #4: Writer Agent Implementation

**Labels:** `sprint-1`, `backend`, `agent`  
**Assignee:** Backend AI Agent  
**Estimate:** 4 hours  
**Dependencies:** Issue #2, Issue #3

**Description:**

Build the Writer Agent that generates articles from topics. First functional agent in the system.

**Checkpoints:**

- [ ] Create `backend/agents/writer_agent.py` file
- [ ] Implement WriterAgent class inheriting from BaseAgent
- [ ] Create effective prompt template for article generation
- [ ] Implement execute() method that takes topic and returns article
- [ ] Test with multiple topics (Python tips, meditation benefits, tea making)
- [ ] Add input validation (non-empty topic, reasonable length)
- [ ] Write unit tests for Writer Agent
- [ ] All tests pass
- [ ] Commit and push code

**Acceptance Criteria:**
- Input: `{"topic": "Python tips for beginners"}`
- Output: Coherent 500-800 word article
- No crashes or unhandled errors
- Tests pass

---

### Issue #5: FastAPI Backend Setup

**Labels:** `sprint-1`, `backend`, `api`  
**Assignee:** Backend AI Agent  
**Estimate:** 3 hours  
**Dependencies:** Issue #4

**Description:**

Create FastAPI backend with endpoint for content generation. Exposes Writer Agent as an API.

**Checkpoints:**

- [ ] Create `backend/main.py` with FastAPI app
- [ ] Configure CORS middleware for frontend access
- [ ] Create `/api/generate` POST endpoint
- [ ] Implement request/response Pydantic models
- [ ] Wire up Writer Agent to endpoint
- [ ] Add `/health` endpoint for status checks
- [ ] Test with `curl` command
- [ ] Backend starts without errors
- [ ] Commit and push code

**Acceptance Criteria:**
- `uvicorn main:app --reload` starts successfully
- `curl -X POST localhost:8000/api/generate -d '{"topic":"test"}'` returns article
- `/health` endpoint returns 200 OK
- CORS configured properly

---

### Issue #6: Frontend Web UI

**Labels:** `sprint-1`, `frontend`, `ui`  
**Assignee:** Frontend AI Agent  
**Estimate:** 4 hours  
**Dependencies:** Issue #5

**Description:**

Build beautiful web interface for Tea Stall Bench with topic input and article display.

**Checkpoints:**

- [ ] Create `frontend/index.html` with semantic structure
- [ ] Design tea stall themed UI in `frontend/styles.css`
- [ ] Implement form for topic input
- [ ] Create JavaScript in `frontend/app.js` to call backend API
- [ ] Add loading indicator while content generates
- [ ] Display generated article with proper formatting
- [ ] Add error handling and display error messages
- [ ] Test end-to-end flow (input topic → display article)
- [ ] Commit and push code

**Acceptance Criteria:**
- Page loads and looks professional
- Can enter topic and click "Brew Story" button
- Article appears within 30 seconds
- Loading state is visible
- Errors are handled gracefully

---

### Issue #7: Sprint 1 Integration & Testing

**Labels:** `sprint-1`, `testing`, `milestone`  
**Assignee:** Testing AI Agent  
**Estimate:** 2 hours  
**Dependencies:** Issue #6

**Description:**

End-to-end testing and Sprint 1 demo preparation. Verify all components work together.

**Checkpoints:**

- [ ] Run all backend tests: `pytest backend/tests/`
- [ ] Test full workflow: Frontend → Backend → LLM → Frontend
- [ ] Test with 5 different topics
- [ ] Verify performance (< 30 seconds per generation)
- [ ] Check all code is committed to GitHub
- [ ] Update README with "How to Run" instructions
- [ ] Record demo video or create screenshots
- [ ] Mark Sprint 1 complete in documentation

**Acceptance Criteria:**
- All tests pass
- End-to-end workflow works reliably
- Documentation is complete
- Demo ready to show

---

## Sprint 2: Multi-Agent Pipeline (Week 3-4)

### Issue #8: Research Agent Implementation

**Labels:** `sprint-2`, `backend`, `agent`  
**Estimate:** 4 hours  
**Dependencies:** Sprint 1 complete

**Checkpoints:**

- [ ] Create `backend/agents/research_agent.py`
- [ ] Integrate DuckDuckGo Search API
- [ ] Implement execute() method
- [ ] Format results as structured JSON
- [ ] Error handling for API failures
- [ ] Write tests
- [ ] Tests pass
- [ ] Commit and push

**Acceptance Criteria:**
- Input: topic → Output: 5 relevant sources with summaries
- Tests pass

---

### Issue #9: Outline Agent Implementation

**Labels:** `sprint-2`, `backend`, `agent`  
**Estimate:** 3 hours  
**Dependencies:** Issue #8

**Checkpoints:**

- [ ] Create `backend/agents/outline_agent.py`
- [ ] Implement outline generation from research data
- [ ] Structure output as JSON with sections
- [ ] Write tests
- [ ] Tests pass
- [ ] Commit and push

**Acceptance Criteria:**
- Creates logical outline with intro, body sections, conclusion
- Tests pass

---

### Issue #10: Pipeline Orchestrator

**Labels:** `sprint-2`, `backend`, `orchestrator`  
**Estimate:** 4 hours  
**Dependencies:** Issue #9

**Checkpoints:**

- [ ] Create `backend/orchestrator/pipeline.py`
- [ ] Implement sequential agent execution
- [ ] Add progress tracking
- [ ] Error handling for agent failures
- [ ] Write tests
- [ ] Tests pass
- [ ] Commit and push

**Acceptance Criteria:**
- Research → Outline → Write pipeline works
- Each agent receives previous agent's output
- Tests pass

---

### Issue #11: Enhanced Writer Agent

**Labels:** `sprint-2`, `backend`, `agent`  
**Estimate:** 3 hours  
**Dependencies:** Issue #10

**Checkpoints:**

- [ ] Modify Writer Agent to accept outline + research
- [ ] Update prompt template
- [ ] Test with full pipeline
- [ ] Write tests
- [ ] Tests pass
- [ ] Commit and push

**Acceptance Criteria:**
- Uses outline structure
- References research data
- Tests pass

---

### Issue #12: Frontend Pipeline Visualization

**Labels:** `sprint-2`, `frontend`, `ui`  
**Estimate:** 3 hours  
**Dependencies:** Issue #11

**Checkpoints:**

- [ ] Add pipeline progress visualization
- [ ] Show each agent's status
- [ ] Display intermediate outputs
- [ ] Update UI for new workflow
- [ ] Test end-to-end
- [ ] Commit and push

**Acceptance Criteria:**
- User sees each agent working
- Can view intermediate results
- UI is responsive

---

## Sprint 3 & 4 Issues

[To be created after Sprint 2 completion]

---

## Labels to Create in GitHub

Create these labels in your repository:

- `sprint-1` (color: #0E8A16)
- `sprint-2` (color: #1D76DB)
- `sprint-3` (color: #5319E7)
- `sprint-4` (color: #E99695)
- `backend` (color: #D93F0B)
- `frontend` (color: #0075CA)
- `agent` (color: #FBCA04)
- `testing` (color: #C2E0C6)
- `infrastructure` (color: #6A737D)
- `milestone` (color: #FF6B6B)

---

## How to Create Issues

1. Go to: https://github.com/MehanazMI/tea-stall-bench/issues/new
2. Copy a task from above
3. Create issue with appropriate labels
4. Assign to yourself or AI agent
5. Link dependencies if needed

**Start with Issue #1 and work sequentially!**
