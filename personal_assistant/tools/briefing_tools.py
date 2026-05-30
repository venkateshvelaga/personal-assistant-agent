import json

from litellm import completion

from personal_assistant.config.models import LOCAL_MODEL_NAME
from personal_assistant.tools.task_tools import list_tasks
from personal_assistant.tools.notes_tools import list_recent_notes


def collect_briefing_data() -> dict:
    """
    Collect task and note information for a daily briefing.
    """
    tasks = list_tasks("open")
    notes = list_recent_notes(5)

    return {
        "tasks": tasks,
        "notes": notes,
    }


def generate_daily_briefing() -> dict:
    """
    Generate a daily briefing using open tasks and recent notes.
    """
    briefing_data = collect_briefing_data()

    prompt = f"""
You are a practical personal assistant.

Create a concise daily briefing from the following data.

Rules:
- Focus on open tasks and recent notes.
- Highlight high priority tasks first.
- Mention anything due today, tomorrow, this evening, this month, or next month.
- Do not invent calendar or email information.
- Keep it useful and concise.

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
    )

    return {
        "status": "success",
        "briefing": response["choices"][0]["message"]["content"],
        "source_data": briefing_data,
    }