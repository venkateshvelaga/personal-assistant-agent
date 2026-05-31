from google.adk.agents import Agent

from personal_assistant.config.models import LOCAL_MODEL
from personal_assistant.tools.gmail_tools import list_recent_gmail_messages


gmail_agent = Agent(
    name="gmail_agent",
    model=LOCAL_MODEL,
    description="Specialized agent responsible for read-only Gmail inbox summaries.",
    instruction="""
You are a Gmail inbox specialist.

Your responsibility:
- List recent Gmail inbox messages.
- Summarize recent inbox messages at a high level.

Use list_recent_gmail_messages when the user asks:
- show recent emails
- show my inbox
- summarize my inbox
- recent Gmail messages
- what emails did I get

This is read-only. Do not send, delete, archive, or modify emails.
""",
    tools=[
        list_recent_gmail_messages,
    ],
)