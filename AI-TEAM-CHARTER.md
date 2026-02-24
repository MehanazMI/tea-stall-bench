# 🤖 Tea Stall Bench — AI Agent Team Charter

> **This is the single source of truth for how this team works.**
> Read it before touching any file. Updated after Sprint 1 & Sprint 2 retrospectives.

---

## 🎯 Project Mission

Build **Tea Stall Bench**: an AI multi-agent system that takes a topic and outputs polished content published to WhatsApp (and more channels in Sprint 4).

**Metaphor:** Just as friends gather at a tea stall bench to share stories over chai, our AI agents "sit together" to collaboratively research, write, and share content.

---

## 🤖 The Six Agents (Team Members)

| Agent | Persona | Role | Added In |
|-------|---------|------|----------|
| Orchestrator | Director 🎬 | Coordinates the pipeline | Sprint 2 ✅ |
| Research Agent | Scout 🔍 | Web search + summarisation | Sprint 2 ✅ |
| Outline Agent | Draft 📝 | Structured content planning | Sprint 2 ✅ |
| Writer Agent | Ink ✍️ | Content generation | Sprint 1 ✅ |
| Publisher Agent | Relay 📱 | WhatsApp delivery | Sprint 1 ✅ |
| Multi-channel | Relay+ 📡 | Email, Telegram | Sprint 4 🔜 |

> ⚠️ **There is NO Editor Agent** in the current codebase. Do not document or reference one until it is built.

---

## 📅 Sprint Timeline

| Sprint | Weeks | Theme | Status |
|--------|-------|-------|--------|
| 1 | 1-2 | Foundation — BaseAgent, LLMClient, Writer, Publisher, FastAPI | ✅ Done |
| 2 | 3-4 | Multi-Agent Pipeline — Research → Outline → Write + Dashboard | ✅ Done |
| 3 | 5-6 | Quality & Real-Time — SSE, content history, resiliency | 🔜 Mar 3 |
| 4 | 7-8 | Production — Multi-channel, scheduling, analytics, Docker | 🔜 Mar 17 |

---

## 🚨 MANDATORY WORKFLOW — No Exceptions

> **Every task — no matter how small — must follow all 6 steps.**
> A direct commit to `main` is a process violation. A bundle of multiple tasks into one PR is a process violation.

### Step-by-Step

```
Step 1: CREATE GITHUB ISSUE (BEFORE writing any code)
─────────────────────────────────────────────────────
gh issue create \
  --title "<type>: Task <N> - <short description>" \
  --body "## Goal\n<what>\n\n## Checkpoints\n- [ ] ...\n\n## Success Criteria\n<how we know it's done>" \
  --label "sprint-<N>,<type>"

Example:
  gh issue create \
    --title "feat: Task 15 - SSE Pipeline Streaming" \
    --body "..." \
    --label "sprint-3,enhancement"

Step 2: CREATE A BRANCH (named after the task)
───────────────────────────────────────────────
git checkout -b <type>/task-<N>-<short-description>

Examples:
  feat/task-15-sse-streaming
  fix/task-cr1-twitter-channel
  docs/task-16-sprint3-plan
  test/task-17-resiliency-tests

Step 3: IMPLEMENT + ALL TESTS MUST PASS
─────────────────────────────────────────
# Write code
# Run: python -m pytest backend/tests/ -v
# STOP if any test fails — fix before proceeding

Step 4: COMMIT (Conventional Commits)
───────────────────────────────────────
git add <specific files — never "git add .">
git commit -m "<type>(scope): <description> (closes #<issue>)"
git push origin <branch>

Example:
  git commit -m "feat(pipeline): add SSE streaming endpoint (closes #22)"

Step 5: OPEN A PULL REQUEST
────────────────────────────
gh pr create \
  --title "<type>: <description> (Task <N>)" \
  --body "Closes #<issue-number>\n\n## Changes\n...\n\n## Tests\n<results>"

Step 6: SQUASH MERGE → ISSUE AUTO-CLOSES
──────────────────────────────────────────
gh pr merge <PR-number> --squash
# 'Closes #N' in PR body auto-closes the issue on merge
```

### ❌ What Is NEVER Allowed

| Violation | Why |
|-----------|-----|
| Committing directly to `main` | Bypasses review, breaks history |
| Multiple tasks in one issue or PR | Untraceable, hard to revert |
| `git add .` without checking `git status` first | Risk of committing unintended files |
| Skipping tests before commit | Breaks the pipeline for everyone |
| Creating a PR without a linked issue | No tracking, no history |
| Moving to next checkpoint if current tests fail | Technical debt accumulates |

---

## ✅ Commit Message Format (Conventional Commits)

```
<type>(<scope>): <short description> (closes #<N>)
```

| Type | When to use |
|------|-------------|
| `feat` | New feature, new agent, new endpoint |
| `fix` | Bug fix |
| `test` | Adding or updating tests only |
| `docs` | Documentation changes only |
| `refactor` | Code restructure, no behaviour change |
| `chore` | Config, build, tooling, dependencies |
| `perf` | Performance improvement |

**Examples from Sprint 1 & 2:**
```
feat(agents): add WriterAgent with outline-aware prompts (closes #15)
fix(pipeline): add asyncio.timeout(300) hard limit (closes #21)
docs(charter): add mandatory workflow protocol (closes #21)
test(writer): add 14 tests for compliance checking (closes #18)
```

---

## 🏷️ Sprint Labels

Every issue and PR **must** have a sprint label:

```bash
# Create labels if they don't exist
gh label create sprint-3 --description "Sprint 3 tasks" --color 0e8a16
gh label create sprint-4 --description "Sprint 4 tasks" --color 1d76db
```

Available labels: `sprint-1` `sprint-2` `sprint-3` `sprint-4` `bug` `enhancement` `documentation`

---

## 🧪 Code Quality Standards

These were established in Sprint 1 and enforced from PR #8 onwards.

### Every File Must Have
- ✅ **Docstrings** on every class and method (`Args:`, `Returns:`, `Raises:`, `Example:`)
- ✅ **Type hints** on all function signatures (`Dict[str, Any]`, `Optional[str]`, etc.)
- ✅ **Input validation** — validate before processing, raise `ValueError` with a clear message
- ✅ **Error handling** — no bare `except:`, always catch specific exceptions
- ✅ **Structured logging** — use `self.logger` from `BaseAgent`, never `print()`

### Agent Development Rules (Established in Sprint 1)
- All agents **must inherit from `BaseAgent`**
- All agents use **dependency injection** — `LLMClient` is passed in, never created inside the agent
- All agents are **stateless** — no instance-level state between requests
- Validation belongs in `_validate_input()` or at the top of `_execute_internal()`
- Constants (`STYLES`, `CONTENT_TYPES`, etc.) live in `backend/config.py`, not hardcoded

### Test Standards (From PR #10 Code Review)
- **Test/code ratio target: ≥ 1.0** (PR #10 achieved 1.08 — the benchmark)
- Tests must cover: initialization, validation, happy path, error paths, edge cases
- Use `AsyncMock` for async agent tests
- Test names must be descriptive: `test_execute_with_empty_topic_raises_value_error`
- Organised into test classes by feature area
- **100% of tests must pass before any PR is opened**

### PR Merge Checklist (from PR #10 review)
Before opening any PR:
- [ ] All tests passing (`pytest -v`)
- [ ] No merge conflicts with `main`
- [ ] Docstrings complete on all new functions
- [ ] Type hints on all signatures
- [ ] No `print()` statements — use logger
- [ ] `git status` clean (no unintended files)
- [ ] `PROGRESS.md` updated with task status
- [ ] Issue number in commit message

---

## 📋 Checkpoint System

Every task has numbered checkpoints. **You cannot skip a checkpoint or move forward if one fails.**

**Example (from Task 4 — Writer Agent):**
1. ✅ Create `writer_agent.py` file
2. ✅ Implement `WriterAgent` class inheriting from `BaseAgent`
3. ✅ Add content generation logic using LLMClient
4. ✅ Add writing prompts and templates
5. ✅ Support different content types
6. ✅ Write comprehensive docstrings
7. ✅ Create unit tests (22 tests)
8. ✅ All tests pass
9. ✅ Commit, push, create PR

**Rule:** Checkpoint 9 (commit + PR) never happens unless checkpoints 1–8 are all green.

---

## 📊 PROGRESS.md — Always Update

After every merged PR, update `PROGRESS.md`:

```markdown
| TaskN | Task Name | ✅ DONE | AgentPersona | X/X checkpoints |
```

The `PROGRESS.md` is the project's public status board. It must always reflect reality.

---

## 🏗️ Technical Architecture (Locked from Sprint 2)

### Pipeline Flow
```
User Topic
    ↓
Director (Orchestrator / pipeline.py)
    ↓
Scout (ResearchAgent) → findings
    ↓
Draft (OutlineAgent) → structured outline
    ↓
Ink (WriterAgent) → article with compliance check
    ↓
[Sprint 4] Relay (PublisherAgent) → WhatsApp / Email / Telegram
```

### Data Contract (PipelineContext)
All data flows through `PipelineContext` (Pydantic model):
- `research_data`, `research_sources` — from Scout
- `outline` — from Draft
- `article_title`, `article_content`, `word_count` — from Ink
- `errors` — non-fatal failures (pipeline continues)
- `trace_id` — 8-char unique ID for log correlation

### Key Technical Decisions Made
| Decision | Reason | Sprint |
|----------|---------|--------|
| `asyncio.timeout(300)` on full pipeline | Prevent infinite hangs | Sprint 2 CR |
| Outline passed directly (not JSON-dumped) to WriterAgent | Clean data contract | Sprint 2 |
| Hybrid search provider with circuit breaker | DuckDuckGo can fail | Sprint 2 |
| `Pydantic V2` `model_config = ConfigDict()` | V1 `class Config` deprecated | Sprint 1 |
| Channels list from `config.py` (not hardcoded in routes) | Single source of truth | Sprint 2 CR |
| `pywhatkit` lazy-init (don't import on startup) | Avoids browser on every request | Backlog |
| `CORS allow_origins=["*"]` for dev only | Must restrict before production | Sprint 4 |

---

## 🔤 Naming Conventions

| Thing | Convention | Example |
|-------|-----------|---------|
| Agent files | `snake_case_agent.py` | `research_agent.py` |
| Agent classes | `PascalCaseAgent` | `ResearchAgent` |
| Agent personas | Noun, single word | Scout, Draft, Ink, Relay, Director |
| Test files | `test_<module>.py` | `test_writer_agent.py` |
| Branches | `<type>/task-<N>-<desc>` | `feat/task-15-sse-streaming` |
| Config constants | `ALL_CAPS` | `CONTENT_TYPES`, `CHANNEL_LENGTH_GUIDES` |

---

## 🚨 Lessons Learned (From Sprint 1 & Sprint 2 Retrospectives)

These are real mistakes made during the project. Learn from them.

| Sprint | Mistake | Correct Approach |
|--------|---------|-----------------|
| Sprint 1 | PR title used wrong format — had to be fixed after creation | Always follow Conventional Commits before creating the PR |
| Sprint 1 | `README.md` referenced `Editor Agent` that doesn't exist | Only document agents that are actually built |
| Sprint 1 | `health_check()` version was wrong (`1.0.0` not `2.0.0`) | Version must be synced in `main.py` AND `health_check()` |
| Sprint 2 | All 6 critical fixes committed directly to `main` in one commit | Each fix = its own issue + branch + PR |
| Sprint 2 | `get_channels()` route only listed WhatsApp, not all 5 channels in config | Backend always reads from `config.py` as single source of truth |
| Sprint 2 | `Twitter` channel in frontend but not in `config.py` | Frontend dropdowns must exactly match `config.py` CHANNELS |
| Sprint 2 | `PyWhatKit_DB.txt` was in the repo (pywhatkit log file) | It's in `.gitignore` — always check `.gitignore` before first run |

---

## 📚 Required Reading Before Any Task

1. **This Charter** — you're reading it
2. **[README.md](README.md)** — project overview and current state
3. **[PROGRESS.md](PROGRESS.md)** — what's done, what's next
4. **[GITHUB-SETUP.md](GITHUB-SETUP.md)** — full git + gh CLI workflow detail
5. **[docs/sprint3_implementation_plan.md](docs/sprint3_implementation_plan.md)** — Sprint 3 tasks

---

## 💬 Status Reporting Format

After every completed task checkpoint, report:

```
Task: <Task name>
Progress: <X/Y> checkpoints
Completed: <what you did>
Tests: <X passing, 0 failing>
Next: <next checkpoint>
Blockers: None / <describe>
```

---

*Charter last updated: 2026-02-23 — reflects Sprint 1 & Sprint 2 history.*
*All agents must read and follow this document. No exceptions.*
