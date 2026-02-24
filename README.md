# 🍵 Tea Stall Bench

> **Where AI Agents Gather to Brew Stories**

An AI multi-agent orchestration system that automates content creation and publishing. Like friends gathering at a tea stall bench to share stories, six specialized AI agents collaborate to research, write, edit, and publish engaging content automatically.

---

## 🎯 What Is This?

**Tea Stall Bench** demonstrates how multiple AI agents can work together in harmony to transform a simple topic into polished, published content on WhatsApp.

**The Metaphor:** Just as a tea stall bench is where people naturally gather to chat and share stories over chai, Tea Stall Bench is where AI agents "sit together" to collaboratively create and share content.

**Perfect for:**
- Learning AI agent orchestration
- Building practical automation tools
- Team projects with mixed experience levels
- Understanding multi-agent AI systems

---

## 🤖 The 6 Agents (Your AI Tea Stall Regulars)

**Pipeline Flow:**

```
┌─────────────┐
│ User Topic  │
└──────┬──────┘
       ↓
┌─────────────────┐
│  Orchestrator   │
└──────┬──────────┘
       ↓
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Research Agent  │ --> │ Outline Agent   │ --> │  Writer Agent   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                          ↓
                                                  ┌───────────────┐
                                                  │ Editor Agent  │
                                                  └───────┬───────┘
                                                          ↓
                                                  ┌──────────────────┐
                                                  │ Publisher Agent  │
                                                  └────────┬─────────┘
                                                           ↓
                                                     ┌──────────┐
                                                     │ WhatsApp │
                                                     └──────────┘
```

**Quick Version:** Topic → Research → Outline → Write → Edit → Publish → WhatsApp

| Agent | Persona | What They Do | Built In |
|-------|---------|-------------|----------|
| **Writer** | Ink ✍️ | Generates draft content | Sprint 1 ✅ |
| **Publisher** | Relay 📱 | Sends content to WhatsApp | Sprint 1 ✅ |
| **Research** | Scout 🔍 | Finds web information | Sprint 2 ✅ |
| **Outline** | Draft 📝 | Creates content structure | Sprint 2 ✅ |
| **Orchestrator** | Director 🎬 | Coordinates all agents | Sprint 2 ✅ |
| **Email/Telegram** | Relay 📱 | Multi-channel publishing | Sprint 4 🔜 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai/) (free local LLM)
- Chrome/Edge browser

### Installation

```bash
# Clone the repository
git clone https://github.com/MehanazMI/tea-stall-bench.git
cd tea-stall-bench

# Install dependencies
pip install -r backend/requirements.txt

# Get an LLM model
ollama pull llama3

# Run the app
python -m backend.main
```

Open `http://localhost:8000` in your browser and start brewing stories! ☕

---

## 💡 Example: How It Works

**Input:** "10 Python tips for beginners"

**What Happens:**
1. **Research Agent** → Searches web, finds Python resources
2. **Outline Agent** → Creates structure: Intro, 10 tips, Conclusion  
3. **Writer Agent** → Writes full article
4. **Editor Agent** → Polishes grammar, improves clarity
5. **Publisher Agent** → Posts to WhatsApp group

**Time:** ~2-3 minutes  
**Output:** Polished article ready to share! 📝

---

## 🛠️ Tech Stack

**Backend:** Python 3.10+, FastAPI, Ollama, Selenium  
**Frontend:** HTML/CSS/JavaScript, WebSocket  
**AI:** Ollama (local LLM) or OpenAI  
**Free Tools:** DuckDuckGo Search, SQLite

💰 **Cost:** $0/month with Ollama (or ~$3-5/month with OpenAI GPT-4)

---

## 📅 8-Week Build Timeline

| Sprint | Weeks | What You Build | Status |
|--------|-------|----------------|--------|
| **1** | 1-2 | Writer + Publisher + API | ✅ Done |
| **2** | 3-4 | Research → Outline → Write pipeline | ✅ Done |
| **3** | 5-6 | Real-time streaming + Content history | 🔜 Mar 3 |
| **4** | 7-8 | Multi-channel publishing + Analytics | 🔜 Mar 17 |

**Total:** 5 agents built, 8 weeks, team of 4+

---

## 👥 Beginner-Friendly Team Setup

This project is designed for **mixed-experience teams**!

**Recommended:**
- 1 Lead + 2 Experienced devs + 2-4 Beginners
- **Pair programming** throughout
- **Learning sessions** in every meeting
- **Simplified scope** for easier onboarding

📘 See [Beginner Team Plan](docs/beginner-team-plan.md) for 8-week guide

---

## 📚 Documentation

- **[Quick Start Guide](README-SIMPLIFIED.md)** - Get started in 5 minutes
- **[Implementation Plan](docs/implementation-plan.md)** - Complete technical architecture
- **[Beginner Team Plan](docs/beginner-team-plan.md)** - 8-week learning roadmap
- **[Advanced Team Plan](docs/advanced-team-plan.md)** - For experienced teams
- **[GitHub Setup](GITHUB-SETUP.md)** - Git workflow and sync guide

---

## 🎓 What You'll Learn

- ✅ Multi-agent AI orchestration
- ✅ Sequential vs parallel execution
- ✅ LLM integration (Ollama & OpenAI)
- ✅ Browser automation with Selenium
- ✅ Async Python programming
- ✅ FastAPI web development
- ✅ Real-world AI system design

---

## 🔮 Future Enhancements

After the core system works, consider:
- **SEO Agent** - Optimize content for search
- **Formatter Agent** - Smart message splitting
- **Translation Agent** - Multi-language content
- **Image Generator** - AI-generated thumbnails
- **Analytics** - Track engagement metrics

---

## 🤝 Contributing

Contributions welcome! This project is perfect for learning AI systems.

1. Fork the repo
2. Create a branch: `git checkout -b feat/task-N-description`
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/): `feat(scope): description`
4. Push and open a Pull Request via `gh pr create`

See [GITHUB-SETUP.md](GITHUB-SETUP.md) for the full team workflow.

---

## 📄 License

MIT License - Free to use and modify!

---

## 🙏 Acknowledgments

- **Ollama** - Making local LLMs accessible
- **FastAPI** - Amazing web framework
- **DuckDuckGo** - Free search API
- **The tea stall culture** - For inspiring this project's name! 🍵

---

<div align="center">

**Built with ❤️ and ☕**

*Where AI agents gather, stories are brewed*

⭐ Star this repo if you love the metaphor!

</div>
