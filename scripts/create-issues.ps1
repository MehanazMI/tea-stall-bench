# Create GitHub Issues for Tea Stall Bench - Sprint 1
# Run this script to automatically create all Sprint 1 issues

# Configuration
$repo = "MehanazMI/tea-stall-bench"
$token = $env:GITHUB_TOKEN  # Set your GitHub personal access token as environment variable

if (-not $token) {
    Write-Host "ERROR: Please set GITHUB_TOKEN environment variable" -ForegroundColor Red
    Write-Host "Get your token from: https://github.com/settings/tokens" -ForegroundColor Yellow
    Write-Host "Then run: `$env:GITHUB_TOKEN='your_token_here'" -ForegroundColor Yellow
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $token"
    "Accept" = "application/vnd.github+json"
}

$baseUrl = "https://api.github.com/repos/$repo/issues"

# Issue #1: Project Setup
$issue1 = @{
    title = "[Sprint 1] Project Setup"
    body = @"
Set up the initial project structure with all necessary folders and configuration files.

**Labels:** sprint-1, backend, setup, infrastructure  
**Assignee:** Backend AI Agent  
**Estimate:** 2 hours

## Checkpoints

- [ ] Create folder structure (backend/agents, backend/orchestrator, backend/utils, frontend)
- [ ] Create requirements.txt with FastAPI, Uvicorn, Ollama dependencies
- [ ] Create .env.example with LLM configuration template
- [ ] Initialize Git and commit initial structure
- [ ] Push to GitHub

## Acceptance Criteria
- All folders exist and are visible in repository
- requirements.txt has all necessary dependencies
- Code is committed and pushed to GitHub
"@
    labels = @("sprint-1", "backend", "setup")
} | ConvertTo-Json

# Issue #2: Base Agent Class
$issue2 = @{
    title = "[Sprint 1] Base Agent Class"
    body = @"
Create the foundational BaseAgent class that all AI agents will inherit from. Includes logging, error handling, and abstract execute method.

**Labels:** sprint-1, backend, core  
**Assignee:** Backend AI Agent  
**Estimate:** 3 hours  
**Dependencies:** Issue #1

## Checkpoints

- [ ] Create ``backend/agents/base_agent.py`` file
- [ ] Implement BaseAgent class with ``__init__`` method
- [ ] Add logging capability using Python logging module
- [ ] Implement error handling wrapper in execute method
- [ ] Write comprehensive docstrings for all methods
- [ ] Create unit test file ``backend/tests/test_base_agent.py``
- [ ] All tests pass
- [ ] Commit and push code

## Acceptance Criteria
- BaseAgent class can be instantiated
- Logging works and outputs to console
- Errors are caught and logged properly
- Tests pass: ``pytest backend/tests/test_base_agent.py``
"@
    labels = @("sprint-1", "backend", "core")
} | ConvertTo-Json

# Issue #3: LLM Client Integration
$issue3 = @{
    title = "[Sprint 1] LLM Client Integration"
    body = @"
Create LLM client that connects to Ollama for content generation. This is the core AI integration.

**Labels:** sprint-1, backend, llm  
**Assignee:** Backend AI Agent  
**Estimate:** 4 hours  
**Dependencies:** Issue #1

## Checkpoints

- [ ] Create ``backend/utils/llm_client.py`` file
- [ ] Implement LLMClient class with Ollama integration
- [ ] Test connection to local Ollama instance
- [ ] Implement generate() method with prompt input
- [ ] Add error handling for connection failures and timeouts
- [ ] Write docstrings and type hints
- [ ] Create unit tests for LLM client
- [ ] All tests pass
- [ ] Commit and push code

## Acceptance Criteria
- Can connect to Ollama successfully
- ``generate("Say hello")`` returns a response
- Errors are handled gracefully
- Tests pass

## Prerequisites
- Ollama installed locally (``ollama pull llama3``)
"@
    labels = @("sprint-1", "backend", "llm")
} | ConvertTo-Json

# Issue #4: Writer Agent
$issue4 = @{
    title = "[Sprint 1] Writer Agent Implementation"
    body = @"
Build the Writer Agent that generates articles from topics. First functional agent in the system.

**Labels:** sprint-1, backend, agent  
**Assignee:** Backend AI Agent  
**Estimate:** 4 hours  
**Dependencies:** Issue #2, Issue #3

## Checkpoints

- [ ] Create ``backend/agents/writer_agent.py`` file
- [ ] Implement WriterAgent class inheriting from BaseAgent
- [ ] Create effective prompt template for article generation
- [ ] Implement execute() method that takes topic and returns article
- [ ] Test with multiple topics (Python tips, meditation benefits, tea making)
- [ ] Add input validation (non-empty topic, reasonable length)
- [ ] Write unit tests for Writer Agent
- [ ] All tests pass
- [ ] Commit and push code

## Acceptance Criteria
- Input: ``{"topic": "Python tips for beginners"}``
- Output: Coherent 500-800 word article
- No crashes or unhandled errors
- Tests pass
"@
    labels = @("sprint-1", "backend", "agent")
} | ConvertTo-Json

# Issue #5: FastAPI Backend
$issue5 = @{
    title = "[Sprint 1] FastAPI Backend Setup"
    body = @"
Create FastAPI backend with endpoint for content generation. Exposes Writer Agent as an API.

**Labels:** sprint-1, backend, api  
**Assignee:** Backend AI Agent  
**Estimate:** 3 hours  
**Dependencies:** Issue #4

## Checkpoints

- [ ] Create ``backend/main.py`` with FastAPI app
- [ ] Configure CORS middleware for frontend access
- [ ] Create ``/api/generate`` POST endpoint
- [ ] Implement request/response Pydantic models
- [ ] Wire up Writer Agent to endpoint
- [ ] Add ``/health`` endpoint for status checks
- [ ] Test with ``curl`` command
- [ ] Backend starts without errors
- [ ] Commit and push code

## Acceptance Criteria
- ``uvicorn main:app --reload`` starts successfully
- ``curl -X POST localhost:8000/api/generate -d '{"topic":"test"}'`` returns article
- ``/health`` endpoint returns 200 OK
- CORS configured properly
"@
    labels = @("sprint-1", "backend", "api")
} | ConvertTo-Json

# Issue #6: Frontend UI
$issue6 = @{
    title = "[Sprint 1] Frontend Web UI"
    body = @"
Build beautiful web interface for Tea Stall Bench with topic input and article display.

**Labels:** sprint-1, frontend, ui  
**Assignee:** Frontend AI Agent  
**Estimate:** 4 hours  
**Dependencies:** Issue #5

## Checkpoints

- [ ] Create ``frontend/index.html`` with semantic structure
- [ ] Design tea stall themed UI in ``frontend/styles.css``
- [ ] Implement form for topic input
- [ ] Create JavaScript in ``frontend/app.js`` to call backend API
- [ ] Add loading indicator while content generates
- [ ] Display generated article with proper formatting
- [ ] Add error handling and display error messages
- [ ] Test end-to-end flow (input topic → display article)
- [ ] Commit and push code

## Acceptance Criteria
- Page loads and looks professional
- Can enter topic and click "Brew Story" button
- Article appears within 30 seconds
- Loading state is visible
- Errors are handled gracefully
"@
    labels = @("sprint-1", "frontend", "ui")
} | ConvertTo-Json

# Issue #7: Integration & Testing
$issue7 = @{
    title = "[Sprint 1] Integration & Testing"
    body = @"
End-to-end testing and Sprint 1 demo preparation. Verify all components work together.

**Labels:** sprint-1, testing, milestone  
**Assignee:** Testing AI Agent  
**Estimate:** 2 hours  
**Dependencies:** Issue #6

## Checkpoints

- [ ] Run all backend tests: ``pytest backend/tests/``
- [ ] Test full workflow: Frontend → Backend → LLM → Frontend
- [ ] Test with 5 different topics
- [ ] Verify performance (< 30 seconds per generation)
- [ ] Check all code is committed to GitHub
- [ ] Update README with "How to Run" instructions
- [ ] Record demo video or create screenshots
- [ ] Mark Sprint 1 complete in documentation

## Acceptance Criteria
- All tests pass
- End-to-end workflow works reliably
- Documentation is complete
- Demo ready to show
"@
    labels = @("sprint-1", "testing", "milestone")
} | ConvertTo-Json

# Create all issues
Write-Host "Creating Sprint 1 GitHub Issues..." -ForegroundColor Cyan

$issues = @($issue1, $issue2, $issue3, $issue4, $issue5, $issue6, $issue7)
$issueCount = 1

foreach ($issue in $issues) {
    Write-Host "Creating Issue #$issueCount..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri $baseUrl -Method Post -Headers $headers -Body $issue -ContentType "application/json"
        Write-Host "  ✅ Created: $($response.html_url)" -ForegroundColor Green
        $issueCount++
    } catch {
        Write-Host "  ❌ Failed to create issue: $_" -ForegroundColor Red
    }
}

Write-Host "`n✅ All Sprint 1 issues created!" -ForegroundColor Green
Write-Host "View them at: https://github.com/$repo/issues" -ForegroundColor Cyan
