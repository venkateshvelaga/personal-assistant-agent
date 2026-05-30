import sys

from dotenv import load_dotenv

from personal_assistant.routing.intent_router import Intent, classify_intent
from personal_assistant.tools.task_tools import create_task, list_tasks, complete_task
from personal_assistant.tools.notes_tools import save_note, list_recent_notes, search_notes
from personal_assistant.extraction.task_extractor import extract_task_fields
from personal_assistant.extraction.notes_extractor import extract_note_fields

load_dotenv()


def handle_message(message: str) -> dict:
    intent = classify_intent(message)

    if intent == Intent.TASK:
        text = message.lower()

        if "show" in text or "list" in text or "open tasks" in text:
            return list_tasks("open")

        if "complete" in text or "mark" in text:
            # Simple first version: complete latest open task if no ID parsing yet
            tasks = list_tasks("open").get("tasks", [])
            if not tasks:
                return {"status": "empty", "message": "No open tasks found."}

            latest_task_id = tasks[0]["id"]
            return complete_task(latest_task_id)

        # Simple first version: create task using full message as title
        fields = extract_task_fields(message)
        return create_task(
            title=fields["title"],
            due_date=fields["due_date"],
            priority=fields["priority"],
)

    if intent == Intent.NOTE:
        text = message.lower()

        if "show" in text or "list" in text or "recent notes" in text:
            return list_recent_notes()

        if "search notes" in text:
            query = message.replace("search notes", "").replace("for", "").strip()
            return search_notes(query)

        fields = extract_note_fields(message)
        return save_note(
            topic=fields["topic"],
            content=fields["content"],
)

    return {
        "status": "unsupported",
        "message": "I do not have that capability yet. I can currently manage tasks and notes.",
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m personal_assistant.router_app \"your message\"")
        sys.exit(1)

    user_message = " ".join(sys.argv[1:])
    result = handle_message(user_message)
    print(result)