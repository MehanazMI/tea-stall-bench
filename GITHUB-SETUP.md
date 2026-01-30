# GitHub Setup Guide

This document explains how to set up and maintain GitHub sync for the Agentic Post project.

---

## 🎯 Initial Setup (One-Time)

### Step 1: Create GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `agentic-post`
3. **Description:** AI Multi-Agent Content Orchestration System
4. **Visibility:** Public (or Private if you prefer)
5. **Do NOT initialize with README** (we already have one)
6. Click **Create repository**

### Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see setup instructions. Use these commands:

```bash
# Navigate to project directory
cd c:\Silambu\agentic-post

# Set your GitHub username and email (one-time configuration)
git config user.name "Your Name"
git config user.email "your-email@example.com"

# Add remote repository (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/agentic-post.git

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
git commit -m "Initial commit: Agentic Post project with documentation"

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
git remote set-url origin git@github.com:YOUR-USERNAME/agentic-post.git
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
- [ ] Can see files on github.com/YOUR-USERNAME/agentic-post
- [ ] README looks good with rendered diagrams
- [ ] Authentication working (token or SSH)

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
cd c:\Silambu\agentic-post
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

---

## 📊 Best Practices

### Commit Messages

✅ **Good:**
- `"Added Research Agent with DuckDuckGo integration"`
- `"Fixed WhatsApp authentication timeout issue"`
- `"Updated README with installation instructions"`

❌ **Bad:**
- `"Update"`
- `"Fixed bugs"`
- `"Changes"`

### When to Commit

- ✅ After completing a feature
- ✅ After fixing a bug
- ✅ Before switching tasks
- ✅ At the end of each day
- ✅ Before testing something risky

### Branching (Advanced)

For team projects, use branches:

```bash
# Create feature branch
git checkout -b feature/seo-agent

# Work on feature, commit changes
git add .
git commit -m "Added SEO agent"

# Push branch to GitHub
git push origin feature/seo-agent

# Create Pull Request on GitHub
# After review and merge, switch back to main
git checkout main
git pull origin main
```

---

## 🎓 Learning Resources

- **Git Basics:** https://git-scm.com/book/en/v2
- **GitHub Docs:** https://docs.github.com/en
- **Interactive Tutorial:** https://learngitbranching.js.org/

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
