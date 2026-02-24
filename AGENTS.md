# 🍵 Tea Stall Bench — AGENTS.md

> **Read this file completely before doing anything else.**
> This is the authoritative instructions file for all AI agents working on this project.
> It overrides any conflicting assumptions from your training data.

---

## 📌 What Is This Project?

**Tea Stall Bench** is a multi-agent AI system that takes a topic and produces polished content published to WhatsApp (and multi-channel in Sprint 4). The pipeline is:

```
User Topic → Scout (Research) → Draft (Outline) → Ink (Write) → Relay (Publish)
```

All agents are coordinated by the **Director** (`backend/orchestrator/pipeline.py`).

**Tech stack:** Python 3.10+, FastAPI, Ollama (local LLM), pywhatkit (WhatsApp), DuckDuckGo search.

---

## 🚦 BEFORE YOU WRITE A SINGLE LINE OF CODE

Run the `/start-task` workflow. No exceptions.

```
Read: AI-TEAM-CHARTER.md → PROGRESS.md → TEAM-REVIEW.md
Then: gh issue create → git checkout -b <branch>
Only then: write code
```

The full workflow is in `.agent/workflows/start-task.md`.

---

## 🚫 HARD RULES — Violations Are Not Acceptable

| Rule | Detail |
|------|--------|
| ❌ Never commit directly to `main` | Every change goes through a branch + PR |
| ❌ Never use `git add .` blindly | Always `git status` first, stage specific files |
| ❌ Never group multiple tasks in one PR | 1 task = 1 issue = 1 branch = 1 PR |
| ❌ Never open a PR without a linked issue | `Closes #N` must be in the PR body |
| ❌ Never skip tests before committing | All tests must pass — zero failures |
| ❌ Never hardcode values that belong in `config.py` | Channels, styles, content types → `backend/config.py` |
| ❌ Never reference the Editor Agent | It does not exist in the codebase yet |

---

## ✅ MANDATORY WORKFLOW — Every Task

### Step 1 — Create GitHub Issue (BEFORE coding)
```bash
gh issue create \
  --title "<type>: Task <N> - <description>" \
  --body "## Goal\n<what and why>\n\n## Checkpoints\n- [ ] ...\n\n## Success Criteria\n<how we know it is done>" \
  --label "sprint-3,<type>"
```

### Step 2 — Create Branch
```bash
git checkout main && git pull origin main
git checkout -b <type>/task-<N>-<short-description>
# Examples:
# feat/task-15-sse-streaming
# fix/task-16-cors-lockdown
# docs/task-17-sprint3-plan
```

### Step 3 — Write Code + Run Tests
```bash
python -m pytest backend/tests/ -v
# STOP if any test fails. Fix before proceeding.
```

### Step 4 — Commit (Conventional Commits)
```bash
git add <specific files>
git commit -m "<type>(<scope>): <description> (closes #<N>)"
git push origin <branch>
```

| Commit type | When |
|-------------|------|
| `feat` | New feature or agent |
| `fix` | Bug fix |
| `test` | Tests only |
| `docs` | Documentation only |
| `refactor` | Code restructure, no behaviour change |
| `chore` | Config, tooling, build |

### Step 5 — Open Pull Request
```bash
gh pr create \
  --title "<type>: <description> (Task <N>)" \
  --body "Closes #<N>\n\n## Changes\n- ...\n\n## Tests\n<X passing, 0 failing>"
```

### Step 6 — Squash Merge + Update PROGRESS.md
```bash
gh pr merge <PR-number> --squash

# Then update PROGRESS.md on main:
git checkout main && git pull origin main
# edit PROGRESS.md → mark task ✅ DONE
git add PROGRESS.md
git commit -m "chore(progress): mark Task <N> complete"
git push origin main
```

The full workflow is in `.agent/workflows/complete-task.md`.

---

## 🧪 Test Commands

```bash
# Run all tests (always use this before committing)
python -m pytest backend/tests/ -v

# Run specific test file
python -m pytest backend/tests/test_api.py -v

# Run with short traceback for quick diagnosis
python -m pytest backend/tests/ -v --tb=short

# Run just orchestrator + api (fastest smoke test)
python -m pytest backend/tests/test_orchestrator.py backend/tests/test_api.py -v
```

**Test coverage target: ≥ 1.0 test/code ratio** (PR #10 set this benchmark at 1.08)

---

## 🏃 How to Run the App

```bash
# Start the backend (from project root)
python -m backend.main

# Or with reload for development
uvicorn backend.main:app --reload --port 8000

# Test API is live
curl http://localhost:8000/api/v1/health
# Expected: {"status":"healthy","service":"Tea Stall Bench API","version":"2.0.0"}

# Access the dashboard
open http://localhost:8000
```

---

## 📁 Project Structure

```
tea-stall-bench/
├── AGENTS.md                   ← YOU ARE HERE
├── AI-TEAM-CHARTER.md          ← Team norms, workflow, code standards
├── PROGRESS.md                 ← Sprint task tracker (update after every merge!)
├── TEAM-REVIEW.md              ← Sprint 2 code review findings
├── README.md                   ← Project overview
├── requirements.txt            ← All dependencies
│
├── backend/
│   ├── config.py               ← SINGLE SOURCE OF TRUTH for all constants
│   ├── main.py                 ← FastAPI app entry point
│   ├── agents/
│   │   ├── base_agent.py       ← All agents must inherit from this
│   │   ├── research_agent.py   ← Scout 🔍 (DuckDuckGo + Parallel.AI)
│   │   ├── outline_agent.py    ← Draft 📝 (Pydantic-validated JSON)
│   │   ├── writer_agent.py     ← Ink ✍️ (outline-aware, compliance check)
│   │   └── publisher_agent.py  ← Relay 📱 (WhatsApp delivery)
│   ├── orchestrator/
│   │   └── pipeline.py         ← Director 🎬 (PipelineContext state machine)
│   ├── api/v1/
│   │   ├── routes.py           ← All API endpoints
│   │   └── models.py           ← Pydantic request/response models
│   └── tests/                  ← All tests live here
│
├── frontend/
│   ├── index.html              ← Dashboard UI
│   ├── style.css               ← Dark mode glassmorphism design
│   └── app.js                  ← Pipeline API integration
│
└── .agent/workflows/
    ├── start-task.md           ← Run BEFORE writing code
    └── complete-task.md        ← Run AFTER writing code
```

---

## ⚙️ backend/config.py — Single Source of Truth

> **Critical rule:** Any value listed here must be read FROM here in the codebase. Never hardcode these values in routes, agents, or frontend.

```python
CONTENT_TYPES = ['post', 'blog', 'tutorial', 'listicle', 'newsletter', 'story']

STYLES = ['technical', 'educational', 'professional', 'friendly', 'inspirational', 'storytelling']

LENGTHS = ['short', 'medium', 'long']

CHANNELS = ['instagram', 'whatsapp', 'linkedin', 'email', 'blog']
# ⚠️ Twitter is NOT in this list. Do not add it to any dropdown or route.

CHANNEL_LENGTH_GUIDES = {
    'instagram': {'short': '50-100 words', 'medium': '100-150', 'long': '150-200'},
    'whatsapp':  {'short': '100-200 words', 'medium': '200-400', 'long': '400-600'},
    'linkedin':  {'short': '150-300 words', 'medium': '300-600', 'long': '600-1000'},
    'email':     {'short': '200-400 words', 'medium': '400-800', 'long': '800-1200'},
    'blog':      {'short': '300-500 words', 'medium': '600-1000', 'long': '1200-1800'},
}
```

---

## 🤖 Agent Development Rules

All agents **must**:
- Inherit from `BaseAgent` (`backend/agents/base_agent.py`)
- Use **dependency injection** — `LLMClient` is passed in, never created inside the agent
- Be **stateless** — no instance-level state persisted between requests
- Validate all inputs in `_validate_input()` before processing
- Use `self.logger` (inherited from `BaseAgent`) — never `print()`
- Have docstrings with `Args:`, `Returns:`, `Raises:` on every public method
- Have type hints on every function signature

**PipelineContext** (in `pipeline.py`) is the data contract between all agents:
- `research_data`, `research_sources` → from Scout
- `outline` → from Draft
- `article_title`, `article_content`, `word_count` → from Ink
- `errors` → non-fatal failures (pipeline continues)
- `trace_id` → 8-char unique ID for log correlation

---

## 🔒 Technical Decisions Already Made (Do Not Re-litigate)

| Decision | Why | Since |
|----------|-----|-------|
| `asyncio.timeout(300)` wraps full pipeline | Prevent infinite hangs | Sprint 2 |
| `Pydantic V2` `model_config = ConfigDict()` | V1 `class Config` is deprecated | Sprint 1 |
| `CORS allow_origins=["*"]` dev only | Must restrict before production | Sprint 4 backlog |
| Outline passed directly to WriterAgent (not JSON-dumped) | Clean data contract | Sprint 2 |
| Hybrid search provider with circuit breaker fallback | DuckDuckGo can fail | Sprint 2 |
| `pywhatkit` lazy-init | Don't open browser on every request | Sprint 4 backlog |
| API version = `"2.0.0"` | Matches Sprint 2 completion | Sprint 2 |

---

## 🏷️ Naming Conventions

| Item | Format | Example |
|------|--------|---------|
| Agent files | `snake_case_agent.py` | `research_agent.py` |
| Agent classes | `PascalCaseAgent` | `ResearchAgent` |
| Agent personas | Single noun | Scout, Draft, Ink, Relay, Director |
| Test files | `test_<module>.py` | `test_writer_agent.py` |
| Git branches | `<type>/task-<N>-<desc>` | `feat/task-15-sse-streaming` |
| Config constants | `ALL_CAPS` | `CONTENT_TYPES`, `CHANNEL_LENGTH_GUIDES` |
| API versions | Prefix `/api/v1/` | `/api/v1/pipeline` |

---

## 🚨 Known Issues — Sprint 3 Must Fix

From `TEAM-REVIEW.md` (sprint-3 backlog):

| # | File | Issue | Priority |
|---|------|-------|----------|
| 1 | `research_agent.py` | `search_provider.search()` is sync inside async — blocks event loop | 🔴 |
| 2 | `research_agent.py` | No timeout on search call — pipeline hangs if provider is slow | 🔴 |
| 3 | `outline_agent.py` | Prompt schema uses `{{}}` f-string escaping — verify it renders correctly | 🔴 |
| 4 | `frontend/app.js` | Markdown not rendered — headers/bullets show as raw `#`, `**`, `-` | 🟡 |
| 5 | `frontend/app.js` | No copy-to-clipboard button on article output | 🟡 |
| 6 | `frontend/app.js` | Only Scout stage animates — Draft and Ink show no progress | 🟡 |
| 7 | `main.py` | `allow_origins=["*"]` must be restricted before production | 🔴 |

---

## 📊 Current Sprint Progress

**Sprint 1 ✅ 7/7** · **Sprint 2 ✅ 7/7** · **Sprint 3 🔜 starts Mar 3** · **Sprint 4 🔜 starts Mar 17**

Always check `PROGRESS.md` for the current live task list.

---

## 📚 Further Reading

| Document | Purpose |
|----------|---------|
| [AI-TEAM-CHARTER.md](AI-TEAM-CHARTER.md) | Full code quality standards, checkpoint system, lessons learned |
| [PROGRESS.md](PROGRESS.md) | Current task status for all sprints |
| [TEAM-REVIEW.md](TEAM-REVIEW.md) | Full Sprint 2 code review with all findings |
| [GITHUB-SETUP.md](GITHUB-SETUP.md) | Git + GitHub CLI setup and reference |
| [.agent/workflows/start-task.md](.agent/workflows/start-task.md) | Step-by-step pre-task checklist |
| [.agent/workflows/complete-task.md](.agent/workflows/complete-task.md) | Step-by-step post-coding checklist |

---

*Last updated: 2026-02-23 | Sprint 2 complete | Sprint 3 starting Mar 3*
