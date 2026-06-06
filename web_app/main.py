from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from personal_assistant.routing.intent_router import Intent, classify_intent
from personal_assistant.security.prompt_guard import guard_user_message

from personal_assistant.tools.task_tools import (
    create_task_from_message,
    list_tasks,
    complete_task,
)
from personal_assistant.tools.notes_tools import (
    save_note_from_message,
    list_recent_notes,
    search_notes,
)
from personal_assistant.tools.briefing_tools import generate_daily_briefing
from personal_assistant.tools.calendar_tools import list_today_calendar_events
from personal_assistant.tools.gmail_tools import list_recent_gmail_messages
from personal_assistant.tools.database_tools import inspect_database


app = FastAPI(title="Personal Assistant Agent")

app.mount("/static", StaticFiles(directory="web_app/static"), name="static")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse("web_app/static/index.html")


@app.post("/chat")
def chat(request: ChatRequest):
    guard_result = guard_user_message(request.message)

    if not guard_result["allowed"]:
        return {
            "reply": "I blocked this request because it looks like a prompt injection or secret access attempt.",
            "raw": guard_result,
        }

    result = route_message(request.message)

    return {
        "reply": format_response(result),
        "raw": result,
    }


def route_message(message: str) -> dict:
    text = message.lower().strip()

    if "briefing" in text or "plan my day" in text or "focus on today" in text:
        return generate_daily_briefing()

    if "calendar" in text or "meeting" in text or "events" in text:
        return list_today_calendar_events()

    if "email" in text or "gmail" in text or "inbox" in text:
        return list_recent_gmail_messages(5)

    if "database" in text or "db stats" in text or "inspect database" in text:
        return inspect_database()

    intent = classify_intent(message)

    if intent == Intent.TASK:
        if "show" in text or "list" in text or "open tasks" in text:
            return list_tasks("open")

        if "complete" in text or "mark" in text:
            tasks = list_tasks("open").get("tasks", [])
            if not tasks:
                return {"status": "empty", "message": "No open tasks found."}

            latest_task_id = tasks[0]["id"]
            return complete_task(latest_task_id)

        return create_task_from_message(message)

    if intent == Intent.NOTE:
        if "show" in text or "list" in text or "recent notes" in text:
            return list_recent_notes()

        if "search notes" in text:
            query = message.replace("search notes", "").replace("for", "").strip()
            return search_notes(query)

        return save_note_from_message(message)

    return {
        "status": "unsupported",
        "message": "I can help with tasks, notes, daily briefing, calendar, Gmail, and database inspection.",
    }


def format_response(result: dict) -> str:
    if "briefing" in result:
        return result["briefing"]

    if "tasks" in result:
        tasks = result.get("tasks", [])
        if not tasks:
            return "No open tasks found."

        lines = ["Open tasks:"]
        for task in tasks:
            lines.append(
                f"- #{task['id']} {task['title']} "
                f"(priority: {task['priority']}, due: {task.get('due_date') or 'not set'})"
            )
        return "\n".join(lines)

    if "notes" in result:
        notes = result.get("notes", [])
        if not notes:
            return "No notes found."

        lines = ["Recent notes:"]
        for note in notes:
            lines.append(f"- [{note['topic']}] {note['content']}")
        return "\n".join(lines)

    if "events" in result:
        events = result.get("events", [])
        if not events:
            return "No calendar events found for today."

        lines = ["Today's calendar events:"]
        for event in events:
            lines.append(f"- {event['summary']} | start: {event['start']}")
        return "\n".join(lines)

    if "emails" in result:
        emails = result.get("emails", [])
        if not emails:
            return "No recent emails found."

        lines = ["Recent emails:"]
        for email in emails:
            lines.append(
                f"- From: {email['from']}\n"
                f"  Subject: {email['subject']}\n"
                f"  Snippet: {email['snippet']}"
            )
        return "\n\n".join(lines)

    if "tasks" in result and "notes" in result:
        return str(result)

    return result.get("message", str(result))