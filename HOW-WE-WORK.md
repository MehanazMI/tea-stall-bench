# 🍵 How We Work — Tea Stall Bench

> A plain-English guide for anyone wondering *"how does this project stay organized and up-to-date?"*

---

## The Big Picture

We're building an AI-powered writing tool called **Tea Stall Bench**. It researches topics, creates outlines, and writes articles — automatically.

The project is built by a developer working together with an **AI coding assistant** (think of it as a very capable co-programmer). Here's what makes our workflow special: **the AI doesn't just write code — it also keeps all the project's tracking documents up-to-date automatically.**

---

## 📁 Where Everything Lives

All project files live in two places:

| Place | What's there | How to see it |
|-------|-------------|---------------|
| **Local computer** | Code files, documents | The `c:\Silambu\tea-stall-bench` folder |
| **GitHub** | A copy of everything, with full history | [github.com/MehanazMI/tea-stall-bench](https://github.com/MehanazMI/tea-stall-bench) |

Think of **GitHub** like Google Drive for code — it stores every version of every file, so you can always see what changed and when.

---

## 🤖 What the AI Does Automatically

When a new feature is built, the AI handles all of this **without being asked**:

```
Developer says: "Build the outline agent"
        ↓
AI writes the code
        ↓
AI runs all tests to verify it works
        ↓
AI updates PROGRESS.md (marks the task ✅ DONE)
        ↓
AI updates the sprint plan document
        ↓
AI creates a GitHub Issue for the task
        ↓
AI creates a Pull Request with a description of the changes
        ↓
AI merges the code into the main codebase
        ↓
AI closes the GitHub Issue with a comment
        ↓
AI pushes everything to GitHub
```

This means the project's documentation is **always accurate** — it reflects exactly what has been built, not what we planned to build.

---

## 📊 How to Check Progress

### Option 1: PROGRESS.md (Simplest)
Open [PROGRESS.md on GitHub](https://github.com/MehanazMI/tea-stall-bench/blob/main/PROGRESS.md).

It shows:
- Which sprint we're on
- Which tasks are done ✅, in progress 🔄, or not started ⬜
- A visual progress bar using 🍵 emoji

### Option 2: GitHub Issues (Most Detail)
Go to the [Issues tab on GitHub](https://github.com/MehanazMI/tea-stall-bench/issues?q=is%3Aissue).

Each task has its own issue with:
- A description of what was built
- A checklist of sub-tasks (checkpoints)
- A comment when it was completed

Filter by sprint: click a label like `sprint-2` to see only Sprint 2 tasks.

### Option 3: GitHub Commits (Full History)
Go to [Commits on GitHub](https://github.com/MehanazMI/tea-stall-bench/commits/main).

Every change ever made is listed here with a message explaining what changed and why.

---

## 🗓️ How Sprints Work

The project is divided into **sprints** — 2-week chunks of focused work:

| Sprint | Theme | Status |
|--------|-------|--------|
| **Sprint 1** (Week 1-2) | Foundation: basic writer + API | ✅ Done |
| **Sprint 2** (Week 3-4) | Research → Outline → Write pipeline | ✅ Done |
| **Sprint 3** (Week 5-6) | Real-time streaming + content history | 📅 Starting Mar 3 |
| **Sprint 4** (Week 7-8) | Publishing + scheduling + analytics | 📅 Starting Mar 17 |

At the **end of each sprint**, the AI automatically:
- Marks all completed tasks in `PROGRESS.md`
- Updates the sprint plan document in `docs/`
- Creates a "Sprint X Complete" issue on GitHub and closes it

---

## 🔀 What's a "Pull Request"?

A **Pull Request (PR)** is how code changes are officially recorded.

Think of it like a **tracked change in Microsoft Word** — you can see exactly what was added or removed, and it only becomes permanent after it's reviewed and accepted.

On our [Pull Requests page](https://github.com/MehanazMI/tea-stall-bench/pulls?q=is%3Apr+is%3Aclosed), you can see every feature that was merged, when, and what it contained.

---

## 📝 Which Documents Are Auto-Updated?

| Document | What it tracks | Updated by |
|----------|---------------|-----------|
| `PROGRESS.md` | Sprint progress, task status, milestones | AI (after each task) |
| `docs/sprint2_implementation_plan.md` | Detailed steps for Sprint 2 | AI (marks steps done) |
| `docs/sprint3_implementation_plan.md` | Plan for Sprint 3 | AI (created before sprint) |
| `CHANGELOG.md` *(coming Sprint 3)* | User-facing list of new features | AI (after each PR) |
| GitHub Issues | Per-task tracking with checkpoints | AI (created + closed) |

---

## 💬 Questions?

| Question | Answer |
|----------|--------|
| *"How do I know the code actually works?"* | Every task has automated tests. The AI runs them before committing. |
| *"What if something breaks?"* | The AI logs errors and adds them to the issue. Tests prevent broken code from being merged. |
| *"Can I suggest a feature?"* | Yes — just say so and it becomes a new task in the next sprint. |
| *"How long does each feature take?"* | Each task has a time estimate in the sprint plan (usually 3-6 hours). |

---

## ✏️ Tips for Editing Documents

If you ever update a document like `PROGRESS.md` yourself, here's how to add the icons and symbols:

**On Windows** — press **`Win + .`** (Windows key + period) to open the emoji picker. Search by name, e.g. type "tea" to find 🍵.

**Quick reference — icons used in this project:**

| Emoji | Meaning in docs |
|-------|----------------|
| 🍵 | One completed sprint task (progress bar) |
| ✅ | Task done |
| 🔄 | Task in progress |
| ⬜ | Task not started |
| ⚠️ | Warning or blocker |
| 🎉 | Sprint milestone celebration |

You can also search for any emoji by name at [emojipedia.org](https://emojipedia.org) — click one to copy it, then paste directly into the document.

---

*Last updated: 2026-02-22*
