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

| Agent | What They Do | Built In |
|-------|-------------|----------|
| **Writer** | Generates draft content | Sprint 1 (Week 1-2) |
| **Research** | Finds web information | Sprint 2 (Week 3-4) |
| **Outline** | Creates content structure | Sprint 2 (Week 3-4) |
| **Editor** | Improves quality | Sprint 3 (Week 5-6) |
| **Publisher** | Posts to WhatsApp | Sprint 4 (Week 7-8) |
| **Orchestrator** | Coordinates everything | Sprint 3 (Week 5-6) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai/) (free local LLM)
- Chrome/Edge browser

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/tea-stall-bench.git
cd tea-stall-bench

# Install dependencies
pip install fastapi ollama selenium

# Get an LLM model
ollama pull llama3

# Run the app
cd backend
python main.py
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

| Sprint | Weeks | What You Build | Agents |
|--------|-------|----------------|--------|
| **1** | 1-2 | Basic Writer | 1 |
| **2** | 3-4 | Multi-Agent Pipeline | 4 |
| **3** | 5-6 | Quality & Orchestration | 5 |
| **4** | 7-8 | WhatsApp Publishing | 6 |

**Total:** 6 agents, 8 weeks, 17 team meetings

---

## 👥 Beginner-Friendly Team Setup

This project is designed for **mixed-experience teams**!

**Recommended:**
- 1 Lead + 2 Experienced devs + 2-4 Beginners
- **Pair programming** throughout
- **Learning sessions** in every meeting
- **Simplified scope** for easier onboarding

📘 See [Beginner Team Plan](tea-stall-bench-beginner-team-plan.md) for 8-week guide

---

## 📚 Documentation

- **[Quick Start Guide](README-SIMPLIFIED.md)** - Get started in 5 minutes
- **[Implementation Plan](README.md)** - Complete technical architecture
- **[Beginner Team Plan](tea-stall-bench-beginner-team-plan.md)** - 8-week learning roadmap
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
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

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
