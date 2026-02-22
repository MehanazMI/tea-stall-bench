# GitHub Setup Guide

This document explains how to set up and maintain GitHub sync for the Tea Stall Bench project.

> This guide covers both **basic Git setup** (for newcomers) and the **team workflow** that this project actually uses (Conventional Commits, GitHub CLI, sprint branches, PR process).

---

## 🎯 Initial Setup (One-Time)

### Step 1: Create GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `tea-stall-bench`
3. **Description:** AI Multi-Agent Content Orchestration System
4. **Visibility:** Public (or Private if you prefer)
5. **Do NOT initialize with README** (we already have one)
6. Click **Create repository**

### Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see setup instructions. Use these commands:

```bash
# Navigate to project directory
cd c:\Silambu\tea-stall-bench

# Set your GitHub username and email (one-time configuration)
git config user.name "Your Name"
git config user.email "your-email@example.com"

# Add remote repository (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/tea-stall-bench.git

# Verify remote is set
git remote -v
```

### Step 3: Create First Commit

```bash
# Check what files will be committed
git status

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: Tea Stall Bench project with documentation"

# Push to GitHub (main branch)
git push -u origin main
```

---

## 📝 Daily Workflow

### Making Changes and Committing

Every time you make changes to your project files:

```bash
# 1. Check what changed
git status

# 2. Stage specific files (or use . for all files)
git add filename.md
# Or stage everything:
git add .

# 3. Commit with a meaningful message
git commit -m "Description of what you changed"

# 4. Push to GitHub
git push
```

### Example Workflow

```bash
# After editing README-SIMPLIFIED.md
git add README-SIMPLIFIED.md
git commit -m "Improved ASCII diagram formatting"
git push

# After adding a new feature
git add backend/agents/new_agent.py
git commit -m "Added sentiment analysis agent"
git push
```

---

## 🖥️ GitHub CLI (gh) — Project Standard

### `git` vs `gh` — What's the difference?

| | `git` | `gh` |
|---|---|---|
| **What it is** | Core version control tool | GitHub's official CLI tool |
| **What it does** | Commits, branches, merges, diffs | Issues, PRs, labels, releases |
| **Talks to** | Local repo + remote via Git protocol | GitHub API (requires auth) |
| **Example** | `git commit`, `git push`, `git pull` | `gh pr create`, `gh issue close` |
| **Install** | Comes with Git | Separate install required |

> **Rule of thumb:** Use `git` to manage your **code changes**. Use `gh` to manage your **GitHub project** (issues, PRs, labels).

This project uses **both**. `gh` is required for the team workflow (creating issues, opening/merging PRs, applying sprint labels).

### Install

```powershell
# Windows (via winget)
winget install --id GitHub.cli

# Verify
gh --version
```

### Authenticate

```bash
gh auth login
# Choose: GitHub.com → HTTPS → Login with a web browser
```

### Common gh Commands

```bash
# Create an issue
gh issue create --title "Task 15: SSE Streaming" --body "Description..." --label "sprint-3,enhancement"

# Close an issue with a comment
gh issue close 15 --comment "Completed in PR #20"

# Create a pull request
gh pr create --title "feat: SSE streaming (Task 15)" --body "Description..."

# Merge (squash) a pull request
gh pr merge 20 --squash

# List open issues
gh issue list

# List open PRs
gh pr list

# Create a label
gh label create sprint-3 --description "Sprint 3 tasks" --color 0e8a16
```

---

## 🔄 Automatic Sync Setup (Optional)

### Option 1: VS Code Auto-Sync

If using VS Code:

1. Install **GitLens** extension
2. Go to Settings → Search "git auto fetch"
3. Enable **Git: Auto Fetch**
4. Enable **Git: Auto Stage**

### Option 2: Git Hooks (Advanced)

Create auto-commit on file save (use with caution):

```bash
# Create post-commit hook
echo '#!/bin/sh\ngit push origin main' > .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

⚠️ **Warning:** Auto-push can be dangerous if you make mistakes. Better to commit manually!

---

## 📦 What Gets Committed

### Included Files (in Git)
✅ All documentation (.md files)
✅ Source code (.py, .js, .html, .css)
✅ Configuration files (requirements.txt, etc.)
✅ Project structure files

### Excluded Files (via .gitignore)
❌ Virtual environment (`venv/`, `env/`)
❌ Python cache (`__pycache__/`, `*.pyc`)
❌ Database files (`*.db`, `*.sqlite`)
❌ API keys and secrets (`.env`)
❌ OS files (`.DS_Store`, `Thumbs.db`)
❌ IDE files (`.vscode/`, `.idea/`)

---

## 🛠️ Common Git Commands

### Checking Status

```bash
# See what changed
git status

# See commit history
git log --oneline

# See differences
git diff
```

### Undoing Changes

```bash
# Discard changes to a file (before staging)
git checkout -- filename.md

# Unstage a file (after git add)
git reset HEAD filename.md

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - DANGEROUS!
git reset --hard HEAD~1
```

### Pulling Latest Changes

```bash
# Get latest from GitHub (if working on multiple machines)
git pull origin main
```

---

## 🔐 Authentication

### Option 1: Personal Access Token (Recommended)

1. **Generate Token:**
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click **Generate new token**
   - Select scopes: `repo` (full control)
   - Copy the token

2. **Use Token as Password:**
   ```bash
   # When prompted for password during git push, use the token
   Username: your-username
   Password: ghp_yourPersonalAccessToken123456
   ```

3. **Cache Credentials (Optional):**
   ```bash
   # Store credentials for 1 hour
   git config --global credential.helper cache
   ```

### Option 2: SSH Keys (Advanced)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Copy public key:
cat ~/.ssh/id_ed25519.pub

# Change remote to SSH
git remote set-url origin git@github.com:YOUR-USERNAME/tea-stall-bench.git
```

---

## 📋 Complete Setup Checklist

Use this checklist to verify your setup:

- [ ] GitHub repository created
- [ ] Local git repository initialized (`git init`)
- [ ] User name and email configured
- [ ] Remote origin added and verified (`git remote -v`)
- [ ] `.gitignore` file created
- [ ] Initial commit made
- [ ] Successfully pushed to GitHub (`git push -u origin main`)
- [ ] Can see files on github.com/YOUR-USERNAME/tea-stall-bench
- [ ] README looks good with rendered diagrams
- [ ] Authentication working (token or SSH)
- [ ] **GitHub CLI installed** (`gh --version`)
- [ ] **GitHub CLI authenticated** (`gh auth status`)
- [ ] **Sprint labels created** (`sprint-1`, `sprint-2`, `sprint-3`)

---

## 🚨 Troubleshooting

### Problem: "Permission denied"
**Solution:** 
- Check your GitHub username is correct
- Use Personal Access Token instead of password
- Or set up SSH keys

### Problem: "Failed to push"
**Solution:**
```bash
# Pull first, then push
git pull --rebase origin main
git push origin main
```

### Problem: "Not a git repository"
**Solution:**
```bash
# Make sure you're in the right directory
cd c:\Silambu\tea-stall-bench
git init
```

### Problem: "Large files rejected"
**Solution:**
```bash
# GitHub has 100MB file limit
# Check file sizes:
git ls-files --others | xargs du -h | sort -hr | head -20

# Remove large file from staging:
git reset HEAD large-file.db
```

### Problem: Merge conflict after squash-merge from GitHub
**Context:** When you `gh pr merge --squash`, GitHub rewrites the commits. If local `main` has different commits, pulling creates a conflict.

**Solution:**
```bash
# Option A: Accept the remote (squashed) version of the conflicted file
git checkout --theirs <conflicted-file>
git add <conflicted-file>
git commit -m "merge: resolve conflict with squashed PR #N"
git push origin main

# Option B: Abort and force-sync local to remote
git merge --abort
git reset --hard origin/main
```

> ⚠️ **Why this happens:** Squash merge creates a brand-new commit SHA on `main` that doesn't match the commits on your local feature branch. Always `git pull origin main` immediately after a squash merge.

### Problem: `gh` command not found on Windows
**Solution:**
```powershell
# Install via winget
winget install --id GitHub.cli

# Or via scoop
scoop install gh

# Restart your terminal after installing!
```

---

## 📊 Best Practices

### Conventional Commits — Project Standard

This project uses **Conventional Commits** format. Every commit message must follow this structure:

```
<type>(<scope>): <description>
```

| Type | When to use | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(writer): add outline-aware prompt injection` |
| `fix` | Bug fix | `fix(api): handle empty topic gracefully` |
| `test` | Adding tests | `test(writer): add compliance check tests` |
| `docs` | Documentation | `docs: update sprint 2 plan as completed` |
| `refactor` | Code reorganization | `refactor(config): centralize channel constants` |
| `chore` | Build/tooling | `chore: update requirements.txt` |
| `merge` | Merge commits | `merge: resolve conflict with squashed PR #14` |

✅ **Good:**
```
feat(writer): outline-aware prompt injection and compliance check (Task 13)
fix(research): fallback to DuckDuckGo when Parallel.AI times out
docs: mark Sprint 2 as 100% complete (7/7 tasks)
```

❌ **Bad:**
```
Update
Fixed bugs
Changes
```

---

### Branch Naming Convention

All branches follow this naming pattern:

```
<type>/task-<number>-<short-description>
```

| Type | Pattern | Example |
|------|---------|--------|
| New feature | `feat/task-N-description` | `feat/task-15-sse-streaming` |
| Refactor | `refactor/task-N-description` | `refactor/task-9-config` |
| Bug fix | `fix/task-N-description` | `fix/task-10-research-timeout` |
| Documentation | `docs/description` | `docs/sprint3-plan` |

```bash
# Create a task branch
git checkout -b feat/task-15-sse-streaming

# Push and set upstream
git push -u origin feat/task-15-sse-streaming
```

---

### Sprint Label System

Every issue and PR must be labeled with its sprint:

| Label | Description | Colour |
|-------|-------------|--------|
| `sprint-1` | Sprint 1 tasks | grey |
| `sprint-2` | Sprint 2 tasks | green |
| `sprint-3` | Sprint 3 tasks | green |
| `enhancement` | Feature additions | blue |
| `bug` | Bug reports | red |
| `frontend` | UI work | lime |

```bash
# Create missing sprint labels
gh label create sprint-3 --description "Sprint 3 tasks" --color 0e8a16
gh label create sprint-4 --description "Sprint 4 tasks" --color 0e8a16
```

---

### Full PR Workflow (Team Standard)

```bash
# 1. Create branch for your task
git checkout -b feat/task-15-sse-streaming

# 2. Make changes, commit with Conventional Commits
git add backend/api/v1/stream.py
git commit -m "feat(api): add SSE streaming endpoint (Task 15)"

# 3. Push branch
git push -u origin feat/task-15-sse-streaming

# 4. Create PR with gh CLI
gh pr create \
  --title "feat: SSE pipeline streaming (Task 15)" \
  --body "## Task 15 Changes
- Added /api/v1/pipeline/stream endpoint
- Yields stage events via Server-Sent Events
- Tests: 5 new tests passing" \
  --label "sprint-3,enhancement"

# 5. After review: squash merge
gh pr merge <PR-number> --squash

# 6. Close linked issue
gh issue close <issue-number> --comment "Completed in PR #<PR-number>"

# 7. Sync local main
git checkout main
git pull origin main
```

### When to Commit

- ✅ After completing a feature or checkpoint
- ✅ After fixing a bug
- ✅ Before switching tasks
- ✅ At the end of each work session
- ✅ Before testing something risky

---

## 🌐 Windows / PowerShell Tips

This project is developed on Windows. Here are gotchas specific to this environment:

### Use `cd` with quotes for paths with spaces
```powershell
cd 'c:\Silambu\tea-stall-bench'
```

### Pipeline output in PowerShell
```powershell
# Pipe stderr to stdout (needed for pytest output capture)
python -m pytest backend/tests/ -v 2>&1 | Select-Object -Last 30
```

### Line endings (CRLF vs LF)
Git may warn about CRLF. Configure once:
```bash
git config --global core.autocrlf true
```

### Run the API server
```powershell
# From project root:
python -m backend.main

# Or using uvicorn directly:
uvicorn backend.main:app --reload
```

### Activate virtual environment
```powershell
.\venv\Scripts\Activate.ps1
# If blocked:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎓 Learning Resources

- **Git Basics:** https://git-scm.com/book/en/v2
- **GitHub Docs:** https://docs.github.com/en
- **Interactive Tutorial:** https://learngitbranching.js.org/
- **GitHub CLI:** https://cli.github.com/manual/
- **Conventional Commits:** https://www.conventionalcommits.org/en/v1.0.0/

---

## 📝 Quick Reference Card

```bash
# Daily workflow
git status          # Check changes
git add .           # Stage all changes
git commit -m "msg" # Commit with message
git push            # Push to GitHub

# Check history
git log --oneline   # See commits
git diff            # See changes

# Undo (use carefully!)
git reset HEAD~1    # Undo last commit (keep changes)
git checkout -- .   # Discard all changes

# Sync with GitHub
git pull            # Get latest from GitHub
git push            # Send to GitHub
```

---

**Setup completed!** 🎉

Your project is now connected to GitHub. Every change you make can be committed and synced automatically!
