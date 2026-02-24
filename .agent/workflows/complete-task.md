---
description: mandatory post-coding checklist before marking a task done
---

# ✅ Complete Task Workflow

> Run this AFTER coding, BEFORE declaring a task done.

## Step 1: Run the full test suite — must be 0 failures
// turbo
```powershell
python -m pytest backend/tests/ -v --tb=short 2>&1 | Select-Object -Last 20
```
> ⛔ If ANY test fails — fix it. Do NOT open a PR with a failing test.

## Step 2: Commit (Conventional Commits format)
```powershell
git status   # check nothing unintended is staged
git add <specific files — NOT "git add .">
git commit -m "<type>(<scope>): <description> (closes #<issue-number>)"
git push origin <branch-name>
```

## Step 3: Open a Pull Request
```powershell
gh pr create `
  --title "<type>: <description> (Task <N>)" `
  --body "Closes #<issue-number>`n`n## Changes`n- <bullet per file changed>`n`n## Tests`n<X passing, 0 failing>"
```

## Step 4: Squash merge — issue auto-closes
```powershell
gh pr merge <PR-number> --squash
```

## Step 5: Update PROGRESS.md
- Mark the task row as `✅ DONE` with correct checkpoint count
- Commit the PROGRESS.md update directly on main (the only file allowed direct-to-main)

```powershell
git checkout main
git pull origin main
# edit PROGRESS.md
git add PROGRESS.md
git commit -m "chore(progress): mark Task <N> complete"
git push origin main
```

## Step 6: Confirm done
- [ ] All tests green
- [ ] PR merged (squash)
- [ ] Issue closed (auto via PR body)
- [ ] `PROGRESS.md` shows ✅ DONE
- [ ] Branch deleted (GitHub auto-deletes on squash merge)
