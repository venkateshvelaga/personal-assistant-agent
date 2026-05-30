from google.adk.agents import Agent
from personal_assistant.config.models import LOCAL_MODEL

from personal_assistant.tools.notes_tools import (
    save_note,
    list_recent_notes,
    search_notes,
)


notes_agent = Agent(
    name="notes_agent",
    #model="gemini-2.5-flash-lite",
    model= LOCAL_MODEL,
    description="Specialized agent responsible for saving and searching notes.",
    instruction="""
You are a notes and lightweight memory specialist.

Your responsibilities:
- save notes
- list recent notes
- search notes by topic or content

Important routing boundary:
If the user says "add task", "create task", "todo", "to-do", "remind me", "complete task", "mark task", or "show tasks", do not save a note.
Instead, respond: "This is a task request. Please ask the root assistant to route this to the Task Agent."

Always use the provided tools when saving or retrieving notes.

Do not claim a note was saved or retrieved unless a tool was successfully called.
""",
    tools=[
        save_note,
        list_recent_notes,
        search_notes,
    ],
)