# Personal Assistant Agent

A local-first AI Personal Assistant built using Google ADK, Ollama, Qwen, SQLite, Gmail, Google Calendar, structured extraction, and a multi-agent architecture.

## Features

- Task Management
- Notes / Personal Memory
- Google Calendar Integration (Read Only)
- Gmail Integration (Read Only)
- AI Daily Briefing
- Database Inspector
- Prompt Injection Guard Foundation
- Local LLM (Qwen via Ollama)

## Architecture

```text
User
 ↓
ADK Web
 ↓
Root Agent
 ├── Task Agent
 ├── Notes Agent
 ├── Briefing Agent
 ├── Calendar Agent
 ├── Gmail Agent
 └── Database Agent
      ↓
      Tools
      ↓
SQLite
Google Calendar API
Gmail API
Ollama
Qwen
```

## Agents

### Root Agent
Routes requests to specialized agents.

### Task Agent
- Create tasks
- List tasks
- Complete tasks

### Notes Agent
- Save notes
- List notes
- Search notes

### Calendar Agent
- Read Google Calendar events

### Gmail Agent
- Read Gmail messages
- Summarize inbox

### Briefing Agent
Generates daily briefings using:
- Tasks
- Notes
- Calendar
- Gmail

### Database Agent
Provides:
- Task counts
- Note counts
- Recent records
- Database inspection

---

## Local Model Stack

```text
Google ADK
 ↓
LiteLLM
 ↓
Ollama
 ↓
Qwen 2.5 7B
```

Current model:

```text
ollama_chat/qwen2.5:7b
```

Ollama is the local model runner.
Qwen is the actual LLM.

---

## Persistence

SQLite database stores:

- Tasks
- Notes

Data survives:
- Laptop restart
- ADK restart
- Ollama restart

---

## Google OAuth Setup

### Create Google Cloud Project

Enable:

- Gmail API
- Google Calendar API

### Configure OAuth

1. Configure OAuth Consent Screen
2. Add yourself as Test User
3. Create OAuth Desktop Credentials
4. Download credentials JSON

Rename:

```text
credentials.json
```

Place in project root.

### First Login

Calendar access creates:

```text
token.json
```

Gmail access creates:

```text
gmail_token.json
```

Never commit:

```text
credentials.json
token.json
gmail_token.json
```

---

## Installation

### Clone

```bash
git clone <repo-url>
cd personal-assistant-agent
```

### Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### Install

```bash
pip install -r requirements.txt
```

### Install Ollama

```bash
ollama pull qwen2.5:7b
```

Verify:

```bash
ollama run qwen2.5:7b
```

### Start ADK

```bash
adk web
```

---

## Example Prompts

### Tasks

```text
Add a high priority task to renew insurance tomorrow
Show my open tasks
```

### Notes

```text
Remember that my insurance renewal is due next month
Show my notes
```

### Calendar

```text
What is on my calendar today?
```

### Gmail

```text
Summarize my inbox
```

### Briefing

```text
Give me my daily briefing
What should I focus on today?
```

### Database

```text
Show database stats
Inspect database
```

---

## Security

Current implementation:

```text
personal_assistant/security/prompt_guard.py
```

Capabilities:

- Detect common prompt injection attempts
- Detect attempts to reveal:
  - credentials.json
  - token.json
  - gmail_token.json
  - API keys
  - hidden instructions

Status:

- Implemented
- Tested
- Not yet wired into ADK request path

---

## Project Structure

```text
personal_assistant/
├── agent.py
├── agents/
├── tools/
├── integrations/
├── extraction/
├── db/
├── security/
└── config/
```

---

## Future Enhancements

- Weekly Briefing
- Unified Search
- Guard Agent
- Tool Authorization
- Audit Logging
- Custom UI
- Model Service Abstraction
- CI/CD
- Automated Tests

---

## Learning Outcomes

This project demonstrates:

- Agentic AI
- Google ADK
- Tool Calling
- Multi-Agent Systems
- Structured Extraction
- SQLite Persistence
- OAuth Integrations
- Gmail API
- Calendar API
- Local LLMs
- Ollama
- Prompt Injection Basics
