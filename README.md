# Personal Assistant Agent

A local-first AI personal assistant built with Google ADK, Ollama/Qwen, SQLite, tools, sub-agents, structured extraction, and daily briefing generation.

---

# What This Project Demonstrates

This project demonstrates a practical agentic AI architecture:

* ADK root agent
* Specialist sub-agents
* Tool calling
* SQLite persistence
* Local LLM execution with Ollama
* Structured extraction
* Deterministic routing
* Daily briefing generation

---

# Current Architecture

```text
User
 ↓
ADK Web / CLI
 ↓
Root Agent
 ├── Task Agent
 ├── Notes Agent
 └── Briefing Agent
 ↓
Tools
 ├── Task Tools
 ├── Notes Tools
 └── Briefing Tools
 ↓
SQLite + Local Qwen Model
```

---

# Features

## Task Management

Supported capabilities:

* Create tasks
* List open tasks
* Complete tasks
* Extract task fields from natural language

Example:

```text
Add a high priority task to renew insurance tomorrow
```

Stored as:

```text
title: renew insurance tomorrow
due_date: tomorrow
priority: high
```

---

## Notes / Lightweight Memory

Supported capabilities:

* Save notes
* List recent notes
* Search notes
* Extract note topic and clean content

Example:

```text
Remember that my car insurance renewal is due next month
```

Stored as:

```text
topic: insurance
content: my car insurance renewal is due next month
```

---

## Daily Briefing

Supported capabilities:

* Collect open tasks
* Collect recent notes
* Generate a concise daily briefing using local Qwen

Example:

```text
Give me my daily briefing
```

---

# Local Model Setup

This project uses Ollama with Qwen 2.5 7B.

```text
ADK
 ↓
LiteLLM
 ↓
Ollama
 ↓
qwen2.5:7b
```

Configured model:

```text
ollama_chat/qwen2.5:7b
```

---

# Project Structure

```text
personal-assistant-agent/
│
├── personal_assistant/
│   ├── agent.py
│   │
│   ├── agents/
│   │   ├── task_agent.py
│   │   ├── notes_agent.py
│   │   └── briefing_agent.py
│   │
│   ├── config/
│   │   └── models.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── extraction/
│   │   ├── task_extractor.py
│   │   └── notes_extractor.py
│   │
│   ├── routing/
│   │   └── intent_router.py
│   │
│   └── tools/
│       ├── task_tools.py
│       ├── notes_tools.py
│       └── briefing_tools.py
│
├── data/
│   └── personal_assistant.db
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Setup

## 1. Create Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Install Ollama

Download and install:

```text
https://ollama.com
```

Pull model:

```bash
ollama pull qwen2.5:7b
```

Verify:

```bash
ollama run qwen2.5:7b
```

## 4. Run ADK Web

```bash
adk web
```

Open the local URL shown in the terminal.

---

# Example Prompts

```text
Add a high priority task to renew insurance tomorrow

Show my open tasks

Mark task 1 complete

Remember that my car insurance renewal is due next month

Show my recent notes

Search notes for insurance

Give me my daily briefing

What should I focus on today?
```

---

# Deterministic Router

The project also contains a deterministic router for routing experiments.

Example:

```bash
python -m personal_assistant.router_app \
"Remember that my insurance renewal is due next month"
```

This bypasses ADK routing and routes directly using intent classification.

---

# Data Persistence

Tasks and notes are stored in:

```text
data/personal_assistant.db
```

The database survives:

* Laptop restart
* ADK restart
* VS Code restart
* Ollama restart

The database is intentionally excluded from Git.

---

# Current Limitations

* ADK Web routing can occasionally remain inside the current active sub-agent.
* Calendar integration not implemented.
* Gmail integration not implemented.
* Custom UI not implemented.
* Database is local only.

---

# Roadmap

## Near-Term

1. Google Calendar Integration
2. Gmail Integration
3. Custom Web UI
4. Calendar-aware Daily Briefing
5. Gmail-aware Daily Briefing

## Medium-Term

1. Unified Model Service
2. Database Inspection Utility
3. Better Routing Controls
4. Weekly Summary Agent
5. Personal Knowledge Search

## Long-Term

1. RAG Support
2. Multi-user Support
3. Cloud Deployment
4. Mobile UI
5. CI/CD Pipeline

---

# Learning Goals

This project was built to learn:

* Agentic AI
* Google ADK
* Root Agent and Sub-Agent architecture
* Tool Calling
* Local LLMs
* Ollama
* LiteLLM
* SQLite
* Structured Extraction
* Deterministic Routing
* AI-generated Summaries

---

# Notes

Do not commit:

```text
.env
.venv/
personal_assistant/.adk/
data/*.db
```

These contain local environment configuration and runtime data.
