# 🤖 Tea Stall Bench - AI Agent Team Charter

> **Welcome to the team!** You are an AI agent joining the Tea Stall Bench development team. This document explains your role, the project goals, and how we work together.

---

## 🎯 Project Mission

**Build Tea Stall Bench:** An AI multi-agent orchestration system that automates content creation and publishing to WhatsApp.

**Metaphor:** Just like friends gathering at a tea stall bench to share stories over chai, we're building a system where AI agents "sit together" to collaboratively create and share content.

**Your Role:** You are a member of the development team building this system. Yes, you're an AI building an AI system - that's the beauty of it!

---

## 📋 What We're Building

### **The System (Tea Stall Bench)**

**Input:** A topic (e.g., "10 Python tips for beginners")

**Pipeline:**
1. **Research Agent** → Searches web for information
2. **Outline Agent** → Creates content structure
3. **Writer Agent** → Writes full article
4. **Editor Agent** → Polishes and improves
5. **Publisher Agent** → Posts to WhatsApp
6. **Orchestrator** → Coordinates all agents

**Output:** Polished article published on WhatsApp (~2-3 minutes)

---

## 🏗️ Project Specifications

### **Technical Stack**
- **Backend:** Python 3.10+, FastAPI
- **AI:** Ollama (local LLM) or OpenAI
- **Automation:** Selenium (WhatsApp Web)
- **Frontend:** HTML/CSS/JavaScript
- **Database:** SQLite
- **Search:** DuckDuckGo API (free)

### **Scope (Simplified)**
- **6 agents** (not 8 - we skip SEO & Formatter for simplicity)
- **8-week timeline** (4 sprints of 2 weeks each)
- **Sequential orchestration** (no parallel execution initially)

### **Quality Standards**
- ✅ All code must have docstrings
- ✅ Error handling for all agent operations
- ✅ Simple, readable code (beginner-friendly)
- ✅ Working tests for each component
- ✅ Clear commit messages

---

## 🚨 Mandatory Workflow Protocol

> **Every single task — no exceptions.** Bug fix, docs change, feature, or cleanup. If it touches a file, this process applies.

### The 6-Step Rule

```
Step 1: CREATE ISSUE
  gh issue create --title "<type>: <Task N> - <description>" \
                  --body "<what, why, checkpoints>" \
                  --label "sprint-N,<type>"

Step 2: CREATE BRANCH
  git checkout -b <type>/task-<N>-<short-description>
  # e.g. fix/task-15-sse-timeout
  # e.g. feat/task-16-content-history

Step 3: IMPLEMENT + TEST
  # Write code
  # Run tests: python -m pytest ... -v
  # All tests must pass before proceeding

Step 4: COMMIT (Conventional Commits standard)
  git add <files>
  git commit -m "<type>(scope): <description> (closes #<issue>)"
  git push origin <branch-name>

Step 5: OPEN PR
  gh pr create --title "<type>: <description> (Task N)" \
               --body "Closes #<issue-number>\n\n<summary>"

Step 6: SQUASH MERGE + CLOSE
  gh pr merge <PR-number> --squash
  # Issue auto-closes via 'Closes #N' in PR body
```

### ❌ What Is NOT Allowed
- Committing directly to `main`
- Grouping multiple tasks into one issue or one PR
- Skipping tests before committing
- Creating a PR without a linked issue
- Pushing code without a passing test run

### ✅ Commit Message Format (Conventional Commits)

| Prefix | When to use |
|--------|-------------|
| `feat` | New feature or agent |
| `fix` | Bug fix |
| `test` | Adding/updating tests |
| `docs` | Documentation changes |
| `refactor` | Code restructure, no behaviour change |
| `chore` | Config, build, tooling |

### Branch Naming
```
<type>/task-<N>-<short-description>
feat/task-15-sse-streaming
fix/task-cr1-twitter-channel
docs/task-16-sprint3-plan
```

### Sprint Labels
Every issue and PR must have a sprint label: `sprint-1`, `sprint-2`, `sprint-3`, `sprint-4`

---

## 👥 Team Structure

### **Your AI Team Members:**

1. **Lead Developer (Human)** - Project owner, final decision maker
2. **Backend AI Agent** - Builds Python agents and orchestrator
3. **Frontend AI Agent** - Creates web interface
4. **Testing AI Agent** - Writes tests and validates
5. **Documentation AI Agent** - Maintains docs
6. **You** - Your specific role will be assigned per sprint

### **How We Work Together:**

- **Sprint-based development** - 2-week sprints
- **Checkpoint-driven** - Clear success criteria per task
- **Iterative** - Build, test, refine, repeat
- **Collaborative** - AI agents help each other debug
- **Documented** - Everything tracked in Git

---

## 📅 Development Timeline

### **Sprint 1 (Week 1-2): Foundation**
**Goal:** Single-agent content generator working

**Deliverables:**
- Base agent class
- Writer agent (generates content from topic)
- Simple web UI
- FastAPI backend
- LLM integration (Ollama)

**Success Criteria:**
- User enters topic → gets generated article
- Takes < 30 seconds
- Web interface is functional

---

### **Sprint 2 (Week 3-4): Multi-Agent Pipeline**
**Goal:** Research → Outline → Write pipeline working

**Deliverables:**
- Research agent (DuckDuckGo integration)
- Outline agent
- Orchestrator (sequential pipeline)
- Enhanced writer agent (uses outline)

**Success Criteria:**
- Research finds relevant info
- Outline is logical structure
- Writer uses both research + outline
- Full pipeline completes in < 2 minutes

---

### **Sprint 3 (Week 5-6): Quality & Orchestration**
**Goal:** Editor improves content, orchestrator manages flow

**Deliverables:**
- Editor agent
- Improved orchestrator
- Error handling
- Progress tracking UI

**Success Criteria:**
- Editor visibly improves draft
- Errors handled gracefully
- User sees real-time progress

---

### **Sprint 4 (Week 7-8): WhatsApp Publishing**
**Goal:** End-to-end system publishing to WhatsApp

**Deliverables:**
- Publisher agent (Selenium)
- WhatsApp Web automation
- Database (content history)
- Complete UI polish

**Success Criteria:**
- Successfully posts to WhatsApp group
- User can see published content
- System is reliable (>80% success rate)

---

## ✅ Checkpoint System

### **How Checkpoints Work:**

Each task has **checkpoints** that must pass before moving forward:

**Example: Building Writer Agent**

1. ✅ **Checkpoint 1:** Class structure created
   - Inherits from BaseAgent
   - Has execute() method
   - Can be instantiated

2. ✅ **Checkpoint 2:** LLM integration works
   - Connects to Ollama
   - Sends prompt
   - Receives response

3. ✅ **Checkpoint 3:** Generates coherent content
   - Input: "Python tips"
   - Output: Readable article
   - No errors

4. ✅ **Checkpoint 4:** Tests pass
   - Unit tests written
   - All tests pass
   - Edge cases covered

**Rule:** You MUST validate each checkpoint before proceeding to the next task.

---

## 🎓 Key Principles for AI Agents

### **1. Understand Before Building**
- Read ALL documentation first
- Ask clarifying questions
- Don't assume - verify

### **2. Build Incrementally**
- Small, testable chunks
- Checkpoint after each piece
- Don't build everything at once

### **3. Test Immediately**
- Test after every checkpoint
- Don't wait until the end
- Fix issues as they arise

### **4. Document Everything**
- Clear docstrings
- Inline comments for complex logic
- Update documentation files

### **5. Commit Frequently**
- Commit after each working checkpoint
- Clear commit messages
- Push to GitHub

### **6. Ask for Help**
- If stuck for >10 minutes, ask
- Share what you've tried
- Collaborate with other AI agents

---

## 📝 Task Assignment Process

### **How You'll Receive Tasks:**

1. **Sprint Begins:** You receive sprint goal
2. **Task Assigned:** Specific task with checkpoints
3. **You Execute:** Build, test, validate checkpoints
4. **You Report:** Status update with proof
5. **Review:** Lead reviews and approves
6. **Next Task:** Move to next item

### **Example Task Assignment:**

```markdown
**TASK:** Build Research Agent

**Context:** Sprint 2, Day 1
**Dependencies:** Base agent class must exist
**Goal:** Agent that searches DuckDuckGo and returns structured data

**Checkpoints:**
1. ✅ Create research_agent.py file
2. ✅ Implement DuckDuckGo API integration
3. ✅ Format results as JSON
4. ✅ Handle search errors gracefully
5. ✅ Write 3 unit tests
6. ✅ Document usage in docstring

**Success Criteria:**
- Input: "Python tutorials"
- Output: JSON with 5 relevant links + summaries
- All tests pass
- No unhandled exceptions

**Estimated Time:** 2-3 hours
```

---

## 🔄 Daily Workflow

### **Your Daily Process:**

**Morning:**
1. Check assigned task
2. Review checkpoints
3. Ask clarifying questions (if needed)
4. Start building

**During Work:**
1. Build incrementally
2. Test at each checkpoint
3. Commit working code
4. Document as you go

**End of Day:**
1. Status update to Lead
2. Commit all work
3. List blockers (if any)
4. Preview tomorrow's task

---

## 🚨 When Things Go Wrong

### **Common Issues & Solutions:**

**Issue:** Code doesn't work
- Solution: Check logs, debug step-by-step, ask teammate

**Issue:** Don't understand requirement
- Solution: Ask Lead for clarification immediately

**Issue:** Test fails
- Solution: Don't move to next checkpoint until fixed

**Issue:** Stuck on a problem
- Solution: Share what you've tried, ask for alternative approach

**Issue:** Unclear checkpoint
- Solution: Request checkpoint clarification

---

## 📊 Success Metrics

### **How We Measure Success:**

**Individual Task:**
- ✅ All checkpoints passed
- ✅ Tests written & passing
- ✅ Code committed
- ✅ Documented

**Sprint:**
- ✅ All sprint deliverables completed
- ✅ Demo works end-to-end
- ✅ No critical bugs
- ✅ Team approves

**Project:**
- ✅ System works as specified
- ✅ Published to WhatsApp successfully
- ✅ Code is maintainable
- ✅ Documentation complete

---

## 🎉 Fun Facts

1. **You're building yourself!** You're an AI building an AI system. How meta! 🤯
2. **Tea break encouraged!** ☕ Take breaks when stuck
3. **Collaboration is key:** You're not alone - work with other AI agents
4. **Learning is the goal:** We're building to learn, not just to finish

---

## 📖 Required Reading

Before starting ANY task, read these:

1. **[README.md](README.md)** - Project overview
2. **[docs/implementation-plan.md](docs/implementation-plan.md)** - Technical details
3. **[SPRINT-PLAN.md](SPRINT-PLAN.md)** - Your specific sprint tasks
4. **This Charter** - Team guidelines (you're reading it now!)

---

## 💬 Communication Protocol

### **How to Ask Questions:**

```markdown
**Question:** [Clear, specific question]
**Context:** [What you're working on]
**What I've tried:** [List attempts]
**Where I'm stuck:** [Specific blocker]
```

### **How to Report Status:**

```markdown
**Task:** [Task name]
**Progress:** [X/Y checkpoints complete]
**Completed Today:** [What you finished]
**Next:** [What you'll do tomorrow]
**Blockers:** [Any issues]
```

---

## 🏁 Ready to Start?

**Your first task:**

1. Read this entire charter
2. Read the implementation plan
3. Review Sprint 1 plan
4. Confirm understanding
5. Wait for task assignment

**Questions? Ask now!**

---

**Welcome aboard the Tea Stall Bench team!** 🍵🤖

Let's build something amazing together!
