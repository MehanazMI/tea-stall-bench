---
description: mandatory pre-task checklist before writing any code
---

# 🚦 Start Task Workflow

> Run this BEFORE touching any file. No exceptions.

## Step 1: Read the project docs
// turbo
```powershell
# Confirm you have read (in this order):
# 1. AI-TEAM-CHARTER.md
# 2. PROGRESS.md
# 3. TEAM-REVIEW.md (if sprint just ended)
# If you have NOT read them in this session, read them now before continuing.
```

## Step 2: Find the next task number
// turbo
```powershell
gh issue list --label sprint-3 --state open
```

## Step 3: Create a GitHub issue FIRST
```powershell
gh issue create `
  --title "<type>: Task <N> - <short description>" `
  --body "## Goal`n<what and why>`n`n## Checkpoints`n- [ ] <step 1>`n- [ ] <step 2>`n- [ ] Tests pass`n- [ ] PR created`n`n## Success Criteria`n<how we know it is done>" `
  --label "sprint-3,<type>"
```
> ⛔ Do NOT proceed to Step 4 until the issue URL is confirmed.

## Step 4: Create a branch named after the task
```powershell
git checkout main
git pull origin main
git checkout -b <type>/task-<N>-<short-description>
# Examples:
#   feat/task-15-sse-streaming
#   fix/task-16-cors-lockdown
#   docs/task-17-sprint3-plan
```
> ⛔ Do NOT write any code while still on `main`.

## Step 5: Confirm checklist before coding
- [ ] Issue created and URL noted
- [ ] On correct branch (not `main`) — verify with `git branch`
- [ ] Checkpoints written in the issue
- [ ] `PROGRESS.md` shows this task as 🔄 IN PROGRESS

**Only after all boxes above are checked → start writing code.**
