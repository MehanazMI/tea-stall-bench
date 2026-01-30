# Tea Stall Bench - Quick Start Guide

> **Where AI Agents Gather to Brew Stories** - Automated content creation and WhatsApp publishing

---

## 🎯 What Is This?

**Tea Stall Bench** uses 6 AI agents working together to:
1. Research a topic from the web
2. Create a content outline
3. Write a full article
4. Edit for quality
5. Publish to WhatsApp automatically

**Perfect for:** Learning AI agent orchestration while building something useful!

---

## 🤖 The 6 Agents

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

| Agent | What It Does | When Built |
|-------|-------------|-----------|
| **Writer** | Generates draft content | Sprint 1 (Week 1-2) |
| **Research** | Finds web information | Sprint 2 (Week 3-4) |
| **Outline** | Creates content structure | Sprint 2 (Week 3-4) |
| **Editor** | Improves quality | Sprint 3 (Week 5-6) |
| **Publisher** | Posts to WhatsApp | Sprint 4 (Week 7-8) |
| **Orchestrator** | Coordinates everything | Sprint 3 (Week 5-6) |

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.10+ & FastAPI
- Ollama (free local LLM) or OpenAI
- Selenium (WhatsApp automation)

**Frontend:**
- HTML/CSS/JavaScript
- WebSocket for real-time updates

**Free Tools:**
- DuckDuckGo Search (research)
- SQLite (database)

💰 **Cost:** $0/month with Ollama (or ~$3-5/month with OpenAI)

---

## 📂 Project Structure

```
tea-stall-bench/
├── backend/
│   ├── agents/
│   │   ├── writer_agent.py
│   │   ├── research_agent.py
│   │   ├── outline_agent.py
│   │   ├── editor_agent.py
│   │   └── publisher_agent.py
│   ├── orchestrator/
│   │   └── pipeline.py
│   └── main.py
├── frontend/
│   ├── index.html
│   └── app.js
└── README.md
```

---

## 🚀 Quick Setup

### 1. Install Python Dependencies
```bash
pip install fastapi ollama selenium
```

### 2. Install Ollama & Get a Model
```bash
# Download from https://ollama.ai
ollama pull llama3
```

### 3. Run the App
```bash
cd backend
python main.py
```

### 4. Open Browser
Navigate to `http://localhost:8000`

---

## 📅 8-Week Build Timeline

### Sprint 1 (Week 1-2): Basic Writer
- ✅ Single agent generates content
- ✅ Simple web UI
- **Learn:** Python, FastAPI, LLM basics

### Sprint 2 (Week 3-4): Multi-Agent Pipeline
- ✅ Add Research & Outline agents
- ✅ Sequential pipeline
- **Learn:** Agent coordination, JSON data

### Sprint 3 (Week 5-6): Quality & Orchestration
- ✅ Add Editor agent
- ✅ Build Orchestrator
- **Learn:** Python classes, orchestration patterns

### Sprint 4 (Week 7-8): WhatsApp Publishing
- ✅ Browser automation
- ✅ Publish to WhatsApp
- **Learn:** Selenium, deployment

---

## 👥 Team Setup (Beginner-Friendly)

**Recommended Team:**
- 1 Lead (you!)
- 2 Experienced developers
- 2-4 Beginners

**Strategy:**
- **Pair programming** (experienced + beginner)
- **Learning sessions** every meeting
- **Simplified scope** (6 agents, not 8)

📘 See [Beginner Team Plan](docs/beginner-team-plan.md) for detailed guide

---

## 💡 How It Works

### Simple Example:

**Input:** "10 Python tips for beginners"

**Pipeline:**
1. **Research Agent** → Searches web, finds top Python resources
2. **Outline Agent** → Creates structure: Intro, 10 tips, Conclusion
3. **Writer Agent** → Writes full article based on outline
4. **Editor Agent** → Fixes grammar, improves clarity
5. **Publisher Agent** → Posts to WhatsApp group

**Time:** ~2-3 minutes total

---

## 🎓 What You'll Learn

By building this, you'll understand:
- ✅ Multi-agent AI systems
- ✅ Sequential orchestration
- ✅ LLM integration (local & cloud)
- ✅ Browser automation
- ✅ Async Python programming
- ✅ FastAPI web development

---

## 🔧 Configuration

### Using Ollama (Free)
```python
# In llm_client.py
LLM_TYPE = "ollama"
MODEL = "llama3"
```

### Using OpenAI (Better Quality)
```python
# In llm_client.py
LLM_TYPE = "openai"
API_KEY = "your-api-key"
MODEL = "gpt-4"
```

---

## 📝 Usage Example

### Via Web UI:
1. Enter topic: "Best practices for Python testing"
2. Click "Generate"
3. Watch agents work in real-time
4. Preview content
5. Click "Publish to WhatsApp"

### Via API:
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python testing best practices"}'
```

---

## 🚨 Common Issues & Fixes

### Issue: LLM not responding
**Fix:** Make sure Ollama is running: `ollama serve`

### Issue: WhatsApp automation fails
**Fix:** Update ChromeDriver to match your Chrome version

### Issue: Slow generation
**Fix:** Switch to smaller model: `ollama pull mistral`

---

## 🎯 Success Metrics

**You've succeeded when:**
- ✅ Content generates in < 3 minutes
- ✅ All 6 agents work without errors
- ✅ WhatsApp publishing works reliably
- ✅ Team members understand orchestration

---

## 🔮 Future Ideas

After the basics work, consider adding:
- **SEO Agent** - Optimize for search engines
- **Formatter Agent** - Smart WhatsApp message splitting
- **Translation Agent** - Multi-language support
- **Image Generator** - AI-generated thumbnails
- **Analytics** - Track content performance

---

## 📚 Documentation

- **[Full Implementation Plan](docs/implementation-plan.md)** - Complete technical details
- **[Beginner Team Plan](docs/beginner-team-plan.md)** - 8-week learning guide with meetings
- **[Advanced Team Plan](docs/advanced-team-plan.md)** - For experienced teams

---

## 🤝 Contributing

This project is beginner-friendly! To contribute:
1. Fork the repo
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

---

## 📄 License

MIT License - Free to use and modify!

---

## 🙋 Need Help?

- **Issues:** Open a GitHub issue
- **Questions:** Check the full implementation plan
- **Learning:** Follow the beginner team plan

---

**Ready to build your AI orchestration system?** 🚀

Start with Sprint 1 and build incrementally. By Week 8, you'll have a working multi-agent system!
