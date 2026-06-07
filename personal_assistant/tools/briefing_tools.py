import json

from litellm import completion

from personal_assistant.config.models import LOCAL_MODEL_NAME
from personal_assistant.config.models import MODEL_COMPLETION_CONFIG
from personal_assistant.tools.task_tools import list_tasks
from personal_assistant.tools.notes_tools import list_recent_notes
from personal_assistant.tools.gmail_tools import list_recent_gmail_messages
from personal_assistant.tools.calendar_tools import list_today_calendar_events

def collect_briefing_data() -> dict:
    """
    Collect task, note, calendar and Gmail information
    for a daily briefing.
    """

    tasks = list_tasks("open")
    notes = list_recent_notes(5)
    calendar = list_today_calendar_events()
    emails = list_recent_gmail_messages(5)

    return {
        "tasks": tasks,
        "notes": notes,
        "calendar": calendar,
        "emails": emails,
    }

def generate_daily_briefing() -> dict:
    """
    Generate a daily briefing using open tasks and recent notes.
    """
    briefing_data = collect_briefing_data()

    prompt = f"""
You are an executive personal assistant.

Create a concise but useful daily briefing.

Sections:

1. High Priority Tasks
2. Notes / Reminders
3. Calendar
4. Email Highlights
5. Suggested Focus

Rules:

- Highlight high priority tasks first.
- Mention anything due today, tomorrow,
  this evening, this month, or next month.
- Summarize calendar events if available.
- Summarize recent emails.
- Ignore obvious marketing emails unless
  they appear important.
- Do not invent information.
- Keep the briefing concise.
- End with Suggested Focus.

Data:

{json.dumps(briefing_data, indent=2)}
"""

    response = completion(
        model=LOCAL_MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        **MODEL_COMPLETION_CONFIG,
    )

    return {
        "status": "success",
        "briefing": response["choices"][0]["message"]["content"],
        "source_data": briefing_data,
    }