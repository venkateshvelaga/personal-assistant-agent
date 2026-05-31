# Personal Assistant Agent

A local-first AI Personal Assistant built using Google ADK, Ollama, Qwen, SQLite, Gmail, Google Calendar, and a multi-agent architecture.

---

# Project Goal

The goal of this project is to learn practical Agentic AI development by building a real personal assistant that can:

* Manage tasks
* Store personal notes
* Generate AI-powered daily briefings
* Read Google Calendar events
* Read Gmail inbox messages
* Run entirely on a local LLM

The project is intentionally designed to demonstrate:

* Multi-Agent Systems
* Tool Calling
* Structured Extraction
* Local LLM Integration
* Persistence
* External API Integrations

---

# Current Capabilities

## Task Management

The assistant can:

* Create tasks from natural language
* Extract priority automatically
* Extract due dates automatically
* List open tasks
* Mark tasks completed

Examples:

```text
Add a high priority task to renew insurance tomorrow

Show my open tasks

Mark my insurance task complete
```

---

## Notes / Personal Memory

The assistant can:

* Save notes from natural language
* Automatically identify note topics
* Search notes
* List recent notes

Examples:

```text
Remember that my car insurance renewal is due next month

Show my notes

Search notes for insurance
```

---

## Google Calendar Integration

The assistant can:

* Authenticate with Google Calendar
* Read today's events
* Summarize calendar schedule

Examples:

```text
What is on my calendar today?

Show today's meetings
```

Authentication uses OAuth Desktop Application flow.

Calendar access is currently read-only.

---

## Gmail Integration

The assistant can:

* Authenticate with Gmail
* Read recent inbox messages
* Summarize inbox activity

Examples:

```text
Show my recent emails

Summarize my inbox
```

Authentication uses OAuth Desktop Application flow.

Gmail access is currently read-only.

---

## AI Daily Briefing

The assistant generates a personalized daily briefing using:

* Open Tasks
* Personal Notes
* Calendar Events
* Gmail Messages

Examples:

```text
Give me my daily briefing

What should I focus on today?
```

Example output:

```text
High Priority Tasks
- Renew insurance tomorrow

Calendar
- Director Sync at 10:00 AM

Email Highlights
- Google Security Alert
- Citadel Job Alert

Suggested Focus
- Renew insurance
- Review security alert
```

---

# Architecture

## High-Level Architecture

```text
User
 ↓
ADK Root Agent
 ├── Task Agent
 ├── Notes Agent
 ├── Calendar Agent
 ├── Gmail Agent
 └── Briefing Agent
      ↓
      Tools
      ↓
SQLite
Google Calendar
Gmail
Ollama/Qwen
```

---

# Agents

## Root Agent

Responsibilities:

* Understand user intent
* Route requests
* Delegate to specialized agents

---

## Task Agent

Responsibilities:

* Create tasks
* List tasks
* Complete tasks

Uses:

```text
task_tools.py
```

---

## Notes Agent

Responsibilities:

* Save notes
* Search notes
* List notes

Uses:

```text
notes_tools.py
```

---

## Calendar Agent

Responsibilities:

* Read Google Calendar
* Summarize today's events

Uses:

```text
calendar_tools.py
calendar_service.py
```

---

## Gmail Agent

Responsibilities:

* Read Gmail inbox
* Summarize recent emails

Uses:

```text
gmail_tools.py
gmail_service.py
```

---

## Briefing Agent

Responsibilities:

Generate a unified daily briefing.

Uses:

```text
task_tools
notes_tools
calendar_tools
gmail_tools
```

The briefing agent aggregates data from multiple sources and then uses Qwen to create a concise summary.

---

# Structured Extraction

Instead of storing raw user input, the system extracts structured data.

Example:

Input:

```text
Add a high priority task to renew insurance tomorrow
```

Extracted:

```json
{
  "title": "renew insurance",
  "priority": "high",
  "due_date": "tomorrow"
}
```

This improves consistency and enables better AI summaries.

---

# Local LLM Setup

This project uses:

```text
Ollama
+
Qwen 2.5 7B
```

Model:

```text
ollama_chat/qwen2.5:7b
```

Flow:

```text
ADK
 ↓
LiteLLM
 ↓
Ollama
 ↓
Qwen
```

No cloud LLM is required.

---

# Persistence

Tasks and notes are stored in SQLite.

Database:

```text
personal_assistant.db
```

Data survives:

* Laptop restart
* ADK restart
* Ollama restart

---

# Project Structure

```text
personal_assistant/
│
├── agent.py
│
├── agents/
│   ├── task_agent.py
│   ├── notes_agent.py
│   ├── calendar_agent.py
│   ├── gmail_agent.py
│   └── briefing_agent.py
│
├── tools/
│   ├── task_tools.py
│   ├── notes_tools.py
│   ├── calendar_tools.py
│   ├── gmail_tools.py
│   └── briefing_tools.py
│
├── integrations/
│   ├── calendar_service.py
│   └── gmail_service.py
│
├── extraction/
│   ├── task_extractor.py
│   └── notes_extractor.py
│
├── db/
│   └── database.py
│
└── config/
    └── models.py
```

---

# Running the Project

Activate environment:

```bash
source .venv/Scripts/activate
```

Start ADK:

```bash
adk web
```

Open:

```text
http://localhost:8000
```

---

# Future Enhancements

Planned improvements:

* Weekly Briefing Agent
* Unified Search Agent
* Better Agent-to-Agent Collaboration
* Custom Web UI
* Model Service Abstraction
* Database Inspector Tool
* RAG-based Knowledge Search
* Mobile Interface

---

# Learning Outcomes

This project demonstrates:

* Agentic AI
* ADK Multi-Agent Design
* Tool Calling
* Local LLMs
* Ollama
* LiteLLM
* OAuth Integrations
* SQLite Persistence
* Structured Extraction
* AI-Powered Summarization

---

Built as a hands-on project to understand how modern AI assistants are architected end-to-end.
