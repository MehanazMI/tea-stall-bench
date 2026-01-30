# 🗓️ Sprint Execution Plan - Tea Stall Bench

> **AI Agent Development Roadmap** with detailed checkpoints and validation criteria

---

## 📌 How to Use This Document

**For AI Agents:**
1. Find your current sprint
2. Read all tasks for that sprint
3. Execute tasks in order
4. Validate ALL checkpoints before proceeding
5. Report status daily

**For Lead:**
- Assign tasks from this plan
- Track checkpoint completion
- Review and approve each milestone

---

## 🏃 Sprint 1: Foundation (Week 1-2)

**Goal:** Single-agent content generator working end-to-end

**Success Criteria:**
- User can enter topic in web UI
- Backend generates article using Ollama
- Article displays in under 30 seconds
- No critical errors

---

### **Task 1.1: Project Setup**

**Assigned To:** Backend AI Agent  
**Time Estimate:** 2 hours  
**Dependencies:** None

**Checkpoints:**

1. ✅ **Create folder structure**
   ```
   tea-stall-bench/
   ├── backend/
   │   ├── agents/
   │   ├── orchestrator/
   │   ├── utils/
   │   ├── main.py
   │   └── requirements.txt
   └── frontend/
       ├── index.html
       ├── styles.css
       └── app.js
   ```
   **Validation:** All folders exist, can be seen in file explorer

2. ✅ **Create requirements.txt**
   ```
   fastapi==0.104.1
   uvicorn==0.24.0
   ollama==0.1.6
   pydantic==2.5.2
   python-dotenv==1.0.0
   ```
   **Validation:** File exists, dependencies listed

3. ✅ **Create .env.example**
   ```
   LLM_TYPE=ollama
   MODEL_NAME=llama3
   API_KEY=optional
   ```
   **Validation:** File created with sample config

4. ✅ **Initialize Git (if not done)**
   ```bash
   git add backend/ frontend/
   git commit -m "feat: initial project structure"
   git push
   ```
   **Validation:** Files on GitHub

**Deliverable:** Project structure ready for development

---

### **Task 1.2: Base Agent Class**

**Assigned To:** Backend AI Agent  
**Time Estimate:** 3 hours  
**Dependencies:** Task 1.1 complete

**Checkpoints:**

1. ✅ **Create base_agent.py**
   Location: `backend/agents/base_agent.py`
   **Validation:** File exists

2. ✅ **Implement BaseAgent class structure**
   ```python
   class BaseAgent:
       def __init__(self, name: str, llm_client):
           self.name = name
           self.llm_client = llm_client
       
       async def execute(self, input_data: dict) -> dict:
           raise NotImplementedError("Subclasses must implement execute()")
   ```
   **Validation:** Class can be instantiated

3. ✅ **Add logging capability**
   ```python
   import logging
   
   def __init__(self, name: str, llm_client):
       self.name = name
       self.llm_client = llm_client
       self.logger = logging.getLogger(f"Agent.{name}")
   ```
   **Validation:** Logs appear when agent runs

4. ✅ **Add error handling**
   ```python
   async def execute(self, input_data: dict) -> dict:
       try:
           self.logger.info(f"{self.name} starting execution")
           result = await self._execute_internal(input_data)
           self.logger.info(f"{self.name} completed successfully")
           return result
       except Exception as e:
           self.logger.error(f"{self.name} failed: {str(e)}")
           raise
   ```
   **Validation:** Errors are caught and logged

5. ✅ **Write docstrings**
   **Validation:** All methods have clear docstrings

6. ✅ **Write unit test**
   Create: `backend/tests/test_base_agent.py`
   Test: Can instantiate, logging works
   **Validation:** `pytest tests/test_base_agent.py` passes

7. ✅ **Commit**
   ```bash
   git add backend/agents/base_agent.py backend/tests/
   git commit -m "feat: implement BaseAgent class with logging and error handling"
   git push
   ```
   **Validation:** Code on GitHub

**Deliverable:** Working base agent class with tests

---

### **Task 1.3: LLM Client**

**Assigned To:** Backend AI Agent  
**Time Estimate:** 4 hours  
**Dependencies:** Task 1.1 complete

**Checkpoints:**

1. ✅ **Create llm_client.py**
   Location: `backend/utils/llm_client.py`

2. ✅ **Implement Ollama integration**
   ```python
   import ollama
   
   class LLMClient:
       def __init__(self, model="llama3"):
           self.model = model
           self.client = ollama.Client()
       
       async def generate(self, prompt: str) -> str:
           response = self.client.generate(
               model=self.model,
               prompt=prompt
           )
           return response['response']
   ```
   **Validation:** Can call Ollama and get response

3. ✅ **Test local Ollama connection**
   ```python
   # Test script
   client = LLMClient()
   result = await client.generate("Say hello")
   print(result)  # Should print hello message
   ```
   **Validation:** Ollama responds successfully

4. ✅ **Add error handling**
   - Handle Ollama not running
   - Handle network errors
   - Handle timeout
   **Validation:** Errors are caught gracefully

5. ✅ **Write docstrings and type hints**
   **Validation:** Code is well-documented

6. ✅ **Write unit tests**
   Test: Connection, generation, error handling
   **Validation:** Tests pass

7. ✅ **Commit**
   **Validation:** Code on GitHub

**Deliverable:** Working LLM client that connects to Ollama

---

### **Task 1.4: Writer Agent**

**Assigned To:** Backend AI Agent  
**Time Estimate:** 4 hours  
**Dependencies:** Tasks 1.2, 1.3 complete

**Checkpoints:**

1. ✅ **Create writer_agent.py**
   Location: `backend/agents/writer_agent.py`

2. ✅ **Implement WriterAgent class**
   ```python
   from .base_agent import BaseAgent
   
   class WriterAgent(BaseAgent):
       def __init__(self, llm_client):
           super().__init__("Writer", llm_client)
       
       async def execute(self, input_data: dict) -> dict:
           topic = input_data.get("topic")
           # Generate article
   ```
   **Validation:** Class inherits from BaseAgent

3. ✅ **Create effective prompt**
   ```python
   prompt = f"""You are a skilled content writer. Write a comprehensive, 
   engaging article about: {topic}
   
   Requirements:
   - 500-800 words
   - Clear introduction and conclusion
   - Use examples where appropriate
   - Professional tone
   
   Article:"""
   ```
   **Validation:** Prompt generates good content

4. ✅ **Implement execute method**
   - Takes topic as input
   - Generates using LLM
   - Returns formatted article
   **Validation:** Generates coherent article

5. ✅ **Test with multiple topics**
   - "Python tips for beginners"
   - "Benefits of meditation"
   - "How to make tea"
   **Validation:** All generate good content

6. ✅ **Add validation**
   - Check topic is not empty
   - Check generated content length
   - Check for errors
   **Validation:** Invalid inputs handled

7. ✅ **Write tests**
   **Validation:** All tests pass

8. ✅ **Commit**
   **Validation:** Code on GitHub

**Deliverable:** Writer agent that generates articles from topics

---

### **Task 1.5: FastAPI Backend**

**Assigned To:** Backend AI Agent  
**Time Estimate:** 3 hours  
**Dependencies:** Task 1.4 complete

**Checkpoints:**

1. ✅ **Create main.py structure**
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   
   app = FastAPI(title="Tea Stall Bench API")
   
   # CORS setup
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
   **Validation:** App starts without errors

2. ✅ **Create /api/generate endpoint**
   ```python
   @app.post("/api/generate")
   async def generate_content(request: GenerateRequest):
       # Initialize writer agent
       # Generate content
       # Return result
   ```
   **Validation:** Endpoint exists

3. ✅ **Implement generation logic**
   ```python
   llm_client = LLMClient()
   writer = WriterAgent(llm_client)
   result = await writer.execute({"topic": request.topic})
   return {"content": result}
   ```
   **Validation:** Returns generated content

4. ✅ **Add request/response models**
   ```python
   from pydantic import BaseModel
   
   class GenerateRequest(BaseModel):
       topic: str
   
   class GenerateResponse(BaseModel):
       content: str
       status: str
   ```
   **Validation:** Models validate data

5. ✅ **Test with curl**
   ```bash
   curl -X POST http://localhost:8000/api/generate \
     -H "Content-Type: application/json" \
     -d '{"topic": "Python tips"}'
   ```
   **Validation:** Returns article JSON

6. ✅ **Add health check endpoint**
   ```python
   @app.get("/health")
   async def health_check():
       return {"status": "healthy"}
   ```
   **Validation:** Returns 200 OK

7. ✅ **Commit**
   **Validation:** Code on GitHub

**Deliverable:** Working FastAPI backend with generation endpoint

---

### **Task 1.6: Frontend UI**

**Assigned To:** Frontend AI Agent  
**Time Estimate:** 4 hours  
**Dependencies:** Task 1.5 complete

**Checkpoints:**

1. ✅ **Create index.html structure**
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>Tea Stall Bench</title>
       <link rel="stylesheet" href="styles.css">
   </head>
   <body>
       <h1>🍵 Tea Stall Bench</h1>
       <p>Where AI Agents Brew Stories</p>
       <!-- Form here -->
       <script src="app.js"></script>
   </body>
   </html>
   ```
   **Validation:** HTML renders

2. ✅ **Create form for topic input**
   ```html
   <div class="input-container">
       <input type="text" id="topic" placeholder="Enter topic...">
       <button onclick="generateContent()">Brew Story ☕</button>
   </div>
   <div id="result"></div>
   ```
   **Validation:** Form is functional

3. ✅ **Style with CSS (styles.css)**
   - Modern, clean design
   - Responsive layout
   - Beautiful colors (tea stall theme!)
   - Smooth animations
   **Validation:** Looks professional

4. ✅ **Implement JavaScript (app.js)**
   ```javascript
   async function generateContent() {
       const topic = document.getElementById('topic').value;
       
       const response = await fetch('http://localhost:8000/api/generate', {
           method: 'POST',
           headers: {'Content-Type': 'application/json'},
           body: JSON.stringify({topic})
       });
       
       const data = await response.json();
       document.getElementById('result').innerHTML = data.content;
   }
   ```
   **Validation:** Calls backend successfully

5. ✅ **Add loading indicator**
   - Show spinner while generating
   - Disable button during generation
   **Validation:** UX is smooth

6. ✅ **Add error handling**
   - Show error message if generation fails
   - Validate topic input
   **Validation:** Errors displayed nicely

7. ✅ **Test end-to-end**
   - Start backend: `python main.py`
   - Open frontend: `index.html`
   - Enter topic, click generate
   - Article appears
   **Validation:** Full workflow works!

8. ✅ **Commit**
   **Validation:** Code on GitHub

**Deliverable:** Beautiful web UI that generates articles

---

### **Sprint 1 Milestone: MVP Demo**

**Requirements for Sprint Completion:**

1. ✅ **Demo Checklist:**
   - [ ] Backend starts without errors
   - [ ] Frontend loads in browser
   - [ ] Can enter topic
   - [ ] Article generates in < 30 seconds
   - [ ] Article is coherent and relevant
   - [ ] No crashes or errors
   - [ ] Code is on GitHub

2. ✅ **Documentation Updated:**
   - [ ] README has "How to Run" section
   - [ ] Sprint 1 marked complete in docs
   - [ ] Screenshots added (optional)

3. ✅ **All Tests Pass:**
   ```bash
   pytest backend/tests/
   ```

4. ✅ **Git Clean:**
   - All code committed
   - Pushed to GitHub
   - No uncommitted changes

**Sprint 1 Demo:** Record video showing topic → generated article

---

## 🏃 Sprint 2: Multi-Agent Pipeline (Week 3-4)

**Goal:** Research → Outline → Write pipeline working

**Success Criteria:**
- Research agent finds relevant info from web
- Outline agent creates logical structure
- Writer uses both to create better content
- Full pipeline completes in < 2 minutes

---

### **Task 2.1: Research Agent**

[Detailed checkpoints similar to above...]

### **Task 2.2: Outline Agent**

[Detailed checkpoints...]

### **Task 2.3: Orchestrator**

[Detailed checkpoints...]

---

## 📊 Checkpoint Validation Rules

### **What Constitutes a Valid Checkpoint?**

✅ **PASS Criteria:**
- Code runs without errors
- Meets functional requirements
- Tests pass (if applicable)
- Documented
- Committed to Git

❌ **FAIL Criteria:**
- Crashes/errors
- Doesn't meet requirements
- Tests fail
- Undocumented
- Not committed

### **Checkpoint Review Process:**

1. **Self-Check:** AI agent validates checkpoint
2. **Automated Test:** Run tests if available
3. **Manual Verification:** Run code, check output
4. **Document:** Mark checkbox as complete
5. **Commit:** Push to Git
6. **Report:** Update status to Lead

**Rule:** Cannot proceed to next checkpoint until current one passes!

---

## 🚦 Status Reporting Template

### **Daily Status Update:**

```markdown
**Date:** 2026-01-30
**Sprint:** Sprint 1
**Current Task:** Task 1.4 - Writer Agent
**AI Agent:** Backend Agent

**Today's Progress:**
- ✅ Checkpoint 1: Created writer_agent.py
- ✅ Checkpoint 2: Implemented WriterAgent class
- ✅ Checkpoint 3: Created effective prompt
- 🔄 Checkpoint 4: Implementing execute method (IN PROGRESS)

**Completed Checkpoints:** 3/8
**Blockers:** None
**Next Session:** Complete checkpoints 4-5

**Code Changes:**
- Added: backend/agents/writer_agent.py
- Modified: None
- Tests: 0/3 passing

**Questions/Notes:**
- Prompt generates good content for tech topics
- May need different prompt for creative topics
```

---

## ✅ Sprint 2-4 Plans

[To be detailed after Sprint 1 completion]

**Sprint 2 Preview:**
- Research Agent with DuckDuckGo
- Outline Agent with structure
- Enhanced Writer Agent
- Pipeline Orchestrator

**Sprint 3 Preview:**
- Editor Agent
- Error handling improvements
- Progress tracking UI
- Orchestrator enhancements

**Sprint 4 Preview:**
- Publisher Agent (Selenium)
- WhatsApp Web automation
- Database integration
- Complete system polish

---

**Ready to build?** Start with Sprint 1, Task 1.1! 🚀
