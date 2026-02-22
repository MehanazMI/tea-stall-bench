# 🍵 Tea Stall Bench — AI Team Code Review

**Reviewed:** 2026-02-22 | **Sprint 2 Complete (14/14 tasks done)**

Each agent reviewed the files in their domain and flagged what can be improved. Issues are tagged **🔴 Important**, **🟡 Nice-to-have**, or **🟢 Future sprint**.

---

## 🔍 Scout (Research Agent) — `backend/agents/research_agent.py`

**Reviewed by:** Scout

### Findings

| # | Issue | Priority |
|---|-------|----------|
| 1 | `search_provider.search()` is called synchronously inside an `async` function — could block the event loop on slow searches | 🔴 Important |
| 2 | No timeout on the search call. If the provider hangs, the entire pipeline hangs indefinitely | 🔴 Important |
| 3 | `_extract_sources()` only catches lines starting with `"URL: "` — fragile if the search provider changes format | 🟡 Nice-to-have |
| 4 | The LLM prompt asks for an "Executive Summary" but the output is never validated to confirm those sections actually appear | 🟡 Nice-to-have |
| 5 | `verbose` flag is stored but never used in the code | 🟢 Future sprint |
| 6 | No caching — identical topic searches hit the web every single time | 🟢 Future sprint (Task 18) |

---

## 📝 Draft (Outline Agent) — `backend/agents/outline_agent.py`

**Reviewed by:** Draft

### Findings

| # | Issue | Priority |
|---|-------|----------|
| 1 | `max_retries = 2` is hardcoded — should be a configurable parameter or env variable | 🟡 Nice-to-have |
| 2 | On retry, the error text is *appended* to the original prompt, making it longer each time. Should replace, not append | 🟡 Nice-to-have |
| 3 | `_clean_json_string` only handles `` ```json `` and ` ``` ` blocks. Doesn't handle `json` prefix without backticks, which some LLMs output | 🟡 Nice-to-have |
| 4 | The prompt schema example uses Python f-string `{{}}` escaping — double-check this renders correctly when the prompt is sent to the LLM | 🔴 Important |
| 5 | `module-level logger` (`logger = logging.getLogger(__name__)`) is created **before** `OutlineAgent.__init__`, but agents also create one via `BaseAgent`. Two loggers for the same class | 🟡 Nice-to-have |
| 6 | No minimum section count check — a valid outline with 0 sections would pass Pydantic validation | 🟡 Nice-to-have |

---

## ✍️ Ink (Writer Agent) — `backend/agents/writer_agent.py`

**Reviewed by:** Ink

### Findings

| # | Issue | Priority |
|---|-------|----------|
| 1 | `_check_compliance()` uses regex on the LLM output to count sections — but compliance is binary (pass/fail). A **score** with reasoning would be more useful | 🟡 Nice-to-have |
| 2 | Temperature mapping is done inline per style — consider moving this to `config.py` so it's easy to tune without touching agent code | 🟡 Nice-to-have |
| 3 | `logging` and `json` are imported but `json` is never used in the current file (after the import fix) | 🟢 Future sprint |
| 4 | Writer's prompt includes both `channel` AND `length` guidance, but there's no validation that the generated word count actually falls in the expected range | 🟡 Nice-to-have |
| 5 | `_build_prompt()` injects the entire outline as text — for long outlines (8+ sections) this pushes the prompt near context limits for smaller models | 🟢 Future sprint |

---

## 📱 Relay (Publisher Agent) — `backend/agents/publisher_agent.py` + `backend/utils/whatsapp_client.py`

**Reviewed by:** Relay

### Findings

| # | Issue | Priority |
|---|-------|----------|
| 1 | `PublisherAgent` creates a `WhatsAppClient` in `__init__` — pywhatkit opens a browser process just by importing it. This means **every API request** that creates a Publisher agent initialises WhatsApp, even if publishing isn't needed | 🔴 Important |
| 2 | `format_content()` hard-cuts to 4000 chars and raises an error. It should **truncate gracefully** with a `...` suffix instead (or split into multiple messages) | 🟡 Nice-to-have |
| 3 | `send_message()` uses `datetime.now()` twice to calculate duration — these calls may capture slightly different times | 🟢 Future sprint |
| 4 | `PyWhatKit_DB.txt` is in the repo root — this is a pywhatkit log file that should be in `.gitignore` | 🔴 Important |
| 5 | The docstring says "Only WhatsApp is supported" — update to reflect the Sprint 4 plan (Email + Telegram) | 🟢 Future sprint |
| 6 | `send_with_review()` imports `webbrowser` and `urllib.parse` inside the function body — move to file-level imports | 🟡 Nice-to-have |

---

## 🎬 Director (Orchestrator) — `backend/orchestrator/pipeline.py`

**Reviewed by:** Director

### Findings

| # | Issue | Priority |
|---|-------|----------|
| 1 | `PipelineContext` docstring says "Immutable" but it's a regular Pydantic model — fields are mutated throughout the pipeline. Should say "state container" | 🟡 Nice-to-have |
| 2 | `started_at` and `completed_at` are stored as ISO strings — should be `datetime` objects with a serialiser so duration calculation is type-safe | 🟡 Nice-to-have |
| 3 | No **pipeline timeout** — if any agent hangs, the whole pipeline never returns a response | 🔴 Important |
| 4 | `trace_id` is only 8 characters (`[:8]`) — could collide in high-volume use, though fine for current scale | 🟢 Future sprint |
| 5 | Agents are created fresh in `Orchestrator.__init__` on every request via `Depends(get_llm_client)` — no agent pooling or reuse | 🟢 Future sprint |

---

## 🎨 Polish (Frontend) — `frontend/index.html`, `app.js`, `style.css`

**Reviewed by:** Polish

### Findings

| # | Issue | Priority |
|---|-------|----------|
| 1 | The `channel` dropdown in `index.html` includes `twitter` as an option, but `twitter` is NOT in `config.py`'s `CHANNELS` or `CHANNEL_LENGTH_GUIDES` — the backend will silently ignore it | 🔴 Important |
| 2 | `app.js` only animates the Scout stage to "active" immediately, but Draft and Ink show no activity indicator while the pipeline runs. User sees no feedback for 5-10 min after Scout | 🟡 Nice-to-have |
| 3 | `article_content` is rendered with `.textContent` — markdown in the article (headers, bold, bullets) is shown as raw `#`, `**`, `-` characters. Should render markdown | 🟡 Nice-to-have |
| 4 | No **copy to clipboard** button on the article output panel | 🟡 Nice-to-have |
| 5 | The `content_type` is hardcoded to `'blog'` in the fetch call — the form has no `content_type` selector so it's always blog regardless of channel picked | 🟡 Nice-to-have |
| 6 | Footer still says `Sprint 2` — should be updated as new sprints ship | 🟢 Future sprint |
| 7 | No page favicon — the browser tab shows a blank icon | 🟢 Future sprint |

---

## 🧠 Brew (Backend Infrastructure) — `main.py`, `routes.py`, `config.py`

**Reviewed by:** Brew

### Findings

| # | Issue | Priority |
|---|-------|----------|
| 1 | `allow_origins=["*"]` in CORS middleware is fine for development but **must be restricted before going to production** | 🔴 Important |
| 2 | `routes.py` — `get_channels()` only returns WhatsApp in the hardcoded list, but `config.py` has Instagram, LinkedIn, Email, Blog | 🔴 Important (inconsistency) |
| 3 | `health_check()` returns `version="1.0.0"` but the app's declared version is `"2.0.0"` — mismatch | 🟡 Nice-to-have |
| 4 | `config.py` has no env-var loading (`os.environ` / `python-dotenv`) — env-specific settings like model names or API keys should live in `.env`, not hardcoded | 🟡 Nice-to-have |
| 5 | Every request creates a new `LLMClient()` via `Depends(get_llm_client)` — no singleton. This is fine for Ollama but would be expensive for paid APIs | 🟢 Future sprint |
| 6 | `Screenshot 2026-02-18 220408.png` in repo root should be moved to `docs/screenshots/` or removed | 🟢 Future sprint |

---

## 📚 Docs & Project Files

**Reviewed by:** Whole Team

| # | Issue | Priority |
|---|-------|----------|
| 1 | `README.md` shows **Editor Agent** in the pipeline diagram and table, but no Editor agent exists in the code | 🔴 Important |
| 2 | `README.md` says Publisher was built in "Sprint 4 (Week 7-8)" — but it was actually built in Sprint 1 | 🔴 Important |
| 3 | `README.md` install command says `pip install fastapi ollama selenium` — missing `pywhatkit`, `duckduckgo-search`, `pydantic`, `uvicorn`, `pytest` etc. Should point to `requirements.txt` | 🔴 Important |
| 4 | `README.md` clone URL still has `YOUR-USERNAME` placeholder | 🟡 Nice-to-have |
| 5 | `SPRINT-PLAN.md` and `docs/implementation-plan.md` overlap heavily with `PROGRESS.md` — some consolidation would reduce confusion | 🟢 Future sprint |
| 6 | `.gitignore` should include `PyWhatKit_DB.txt`, `outputs/`, and `*.png` screenshots | 🔴 Important |

---

## 🎯 Priority Summary

### Fix Now (Sprint 3 Kickoff)
1. 🔴 `PyWhatKit_DB.txt` added to `.gitignore`
2. 🔴 `README.md` — fix agent table (no Editor agent), fix clone URL, point to `requirements.txt`
3. 🔴 `index.html` — remove `twitter` from channel dropdown (not in backend)
4. 🔴 `routes.py` — `get_channels()` should return all channels from `config.py`
5. 🔴 `health_check()` — fix version number (1.0.0 → 2.0.0)
6. 🔴 Add pipeline timeout in `Orchestrator`

### Sprint 3 Backlog
- Add `asyncio.timeout` wrapper to search calls in `ResearchAgent`
- Render markdown in article output panel
- Add "Copy to clipboard" button
- Fix CORS origins before production deploy
- Progressive stage animation (all three stages animate)

### Sprint 4 Backlog
- `WhatsAppClient` lazy-init (don't create on every request)
- `config.py` env-var loading
- Agent pooling / reuse
- Truncate-with-ellipsis on WhatsApp content > 4000 chars

---

*All agents reviewed their domains objectively. Issues listed reflect direct reading of source files, not assumptions.*
