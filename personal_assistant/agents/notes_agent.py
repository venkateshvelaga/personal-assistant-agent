from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from personal_assistant.tools.notes_tools import (
    save_note,
    list_recent_notes,
    search_notes,
)


notes_agent = Agent(
    name="notes_agent",
    #model="gemini-2.5-flash-lite",
    model=LiteLlm(model="ollama_chat/qwen2.5:7b"),
    description="Specialized agent responsible for saving and searching notes.",
    instruction="""
You are a notes and lightweight memory specialist.

Your responsibilities:
- save notes
- list recent notes
- search notes by topic or content

Always use the provided tools when saving or retrieving notes.

Do not claim a note was saved or retrieved unless a tool was successfully called.
""",
    tools=[
        save_note,
        list_recent_notes,
        search_notes,
    ],
)