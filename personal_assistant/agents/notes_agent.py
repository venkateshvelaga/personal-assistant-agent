from google.adk.agents import Agent
from personal_assistant.config.models import LOCAL_MODEL

from personal_assistant.tools.notes_tools import (
    save_note_from_message,
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

Always use the provided tools when saving or retrieving notes.
When saving a note from user text, use save_note_from_message.
Use list_recent_notes to list notes.
Use search_notes to search notes.

Do not claim a note was saved or retrieved unless a tool was successfully called.
""",
    tools=[
        save_note_from_message,
        list_recent_notes,
        search_notes,
    ],
)