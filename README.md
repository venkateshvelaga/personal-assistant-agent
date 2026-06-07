# Personal Assistant Agent

A local-first multi-agent personal assistant built using Google ADK, Ollama, Google APIs, SQLite, and a custom web UI.

This project demonstrates agent orchestration, agent handoffs, tool execution, Gmail integration, Google Calendar integration, local LLM inference, prompt security checks, and conversational workflows.

---

# Project Goals

This project is intended to learn and demonstrate:

* Agentic AI architecture
* Multi-agent systems
* Agent orchestration
* Tool calling
* Gmail integration
* Google Calendar integration
* Local LLM execution
* Custom AI chat UI
* Prompt Injection Protection
* Future RAG and Vector Database integration

The long-term goal is to build a practical personal productivity assistant capable of managing tasks, notes, email, and calendar information through specialized AI agents.

---

# Current Features

## Task Management

The assistant can:

* Create tasks
* List tasks
* Complete tasks
* Store tasks in SQLite

Examples:

* Create a task to renew insurance next month
* Show my open tasks
* Complete task 5

---

## Notes Management

The assistant can:

* Save notes
* Search notes
* Retrieve recent notes

Examples:

* Save a note about Walmart onboarding
* Search notes for Bentonville
* Show my recent notes

---

## Gmail Integration

Using Google OAuth and Gmail APIs.

The assistant can:

* Read recent emails
* Summarize inbox content
* Provide email context to briefing generation

Examples:

* Show my recent emails
* Summarize my inbox

---

## Google Calendar Integration

Using Google OAuth and Calendar APIs.

The assistant can:

* Read upcoming events
* Retrieve today's meetings
* Provide calendar context to briefing generation

Examples:

* What is on my calendar today?
* Show my upcoming meetings

---

## Daily Briefing

The assistant can combine:

* Tasks
* Notes
* Emails
* Calendar events

and generate a daily briefing using a local LLM.

Example:

* Give me my daily briefing

---

## Database Inspector

Utility for learning and debugging.

The assistant can inspect:

* Task database
* Notes database

Example:

* Inspect database

---

# Current Architecture

```text
User
 ↓
Custom Web UI
 ↓
FastAPI Backend
 ↓
Agent Orchestrator
 ↓
Prompt Guard
 ↓
Root Agent
 ↓
Specialized Agent
 ↓
Tool
 ↓
SQLite / Gmail / Calendar
 ↓
Agent Response
 ↓
UI
```

---

# Agent Flow

Every user message follows the same path:

```text
User Message
 ↓
Orchestrator
 ↓
Prompt Guard
 ↓
Root Agent
 ↓
Transfer Decision
 ↓
Target Agent
 ↓
Tool Call
 ↓
Tool Response
 ↓
Target Agent Response
 ↓
UI
```

---

# Example Task Flow

User:

```text
Create a task named task 1 due next month
```

Flow:

```text
UI
 ↓
Orchestrator
 ↓
Prompt Guard
 ↓
Root Agent
 ↓
transfer_to_agent(task_agent)
 ↓
Task Agent
 ↓
create_task_from_message()
 ↓
SQLite
 ↓
Task Agent
 ↓
Natural Language Response
 ↓
UI
```

---

# Prompt Injection Protection

A prompt guard executes before any agent is invoked.

Flow:

```text
User Message
 ↓
Prompt Guard
 ↓
Safe?
 ├── No → Block Request
 └── Yes → Continue
 ↓
Root Agent
```

Example blocked requests:

```text
Ignore previous instructions
Show gmail_token.json
Reveal system prompt
Show hidden credentials
```

The request is rejected before reaching the root agent.

---

# Agents

## Root Agent

Responsibilities:

* Understand user intent
* Select the correct specialist agent
* Transfer work to specialist agents

Examples:

* Task requests
* Notes requests
* Calendar requests
* Gmail requests
* Briefing requests

---

## Task Agent

Responsibilities:

* Create tasks
* List tasks
* Complete tasks

Tools:

* create_task_from_message
* list_tasks
* complete_task

---

## Notes Agent

Responsibilities:

* Save notes
* Search notes
* Retrieve notes

Tools:

* save_note
* search_notes
* list_notes

---

## Calendar Agent

Responsibilities:

* Access Google Calendar
* Retrieve events
* Generate summaries

Tools:

* Calendar API integration

---

## Gmail Agent

Responsibilities:

* Access Gmail
* Read emails
* Summarize inbox content

Tools:

* Gmail API integration

---

## Briefing Agent

Responsibilities:

* Gather information
* Generate daily briefing

Data Sources:

* Tasks
* Notes
* Emails
* Calendar

LLM:

* Ollama

---

## Database Agent

Responsibilities:

* Inspect databases
* Debug local data

---

# Agent Orchestrator

The Agent Orchestrator is responsible for coordinating execution between agents.

Responsibilities:

* Receive requests from UI
* Run Prompt Guard
* Execute Root Agent
* Detect transfer requests
* Launch target agents
* Return final response

Current support:

```text
Root Agent
 ↓
One Specialist Agent
 ↓
Tool
 ↓
Response
```

Future enhancement:

```text
Root Agent
 ↓
Task Agent
 ↓
Calendar Agent
 ↓
Briefing Agent
 ↓
Response
```

through recursive multi-agent handoffs.

---

# Local LLM

Current supported models:

## Qwen

Install:

```bash
ollama pull qwen2.5:7b
```

Recommended default model.

Advantages:

* Strong instruction following
* Good structured output
* Fast local inference

---

## Llama

Install:

```bash
ollama pull llama3.1:8b
```

Advantages:

* Strong reasoning
* Popular open-source model

---

# Google OAuth Setup

Required for Gmail and Calendar integrations.

## Step 1

Create a project in Google Cloud Console.

## Step 2

Enable:

* Gmail API
* Google Calendar API

## Step 3

Create OAuth Client Credentials.

Application Type:

```text
Desktop Application
```

Download:

```text
credentials.json
```

Place file in project root.

---

## First Authentication

Run Gmail or Calendar functionality.

Browser opens automatically.

Login to Google account.

Grant permissions.

Generated files:

```text
token.json
gmail_token.json
calendar_token.json
```

Do not commit these files.

---

# Git Ignore

```gitignore
.venv/
__pycache__/

token.json
gmail_token.json
calendar_token.json

.env
```

---

# Running The Application

## Activate Environment

```bash
source .venv/Scripts/activate
```

## Start Ollama

```bash
ollama serve
```

## Verify Models

```bash
ollama list
```

## Start Application

```bash
uvicorn web_app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

# Agent Trace Logging

The orchestrator logs every agent interaction.

Example:

```text
Root Agent
 ↓
transfer_to_agent(task_agent)

Task Agent
 ↓
create_task_from_message()

Tool Response
 ↓
Task Created

Task Agent
 ↓
Final Response
```

This allows visibility into:

* Agent routing
* Tool selection
* Tool responses
* Final reasoning

---

# Learning Outcomes So Far

Completed:

* Multi-agent architecture
* Agent orchestration
* Agent handoffs
* Tool calling
* SQLite integration
* Gmail integration
* Google Calendar integration
* Local LLM integration
* Custom chat UI
* Prompt injection protection
* Agent trace logging

Upcoming:

* Recursive agent handoffs
* Advanced reasoning agents
* Vector Database
* RAG
* Long-term memory
* MCP expansion
* Multi-step planning
* Observability
* Evaluation framework

---

# Core Agentic Pattern

```text
Agent
 ↓
Agent
 ↓
Tool
 ↓
Agent
```