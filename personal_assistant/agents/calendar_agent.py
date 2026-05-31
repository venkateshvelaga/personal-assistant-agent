from google.adk.agents import Agent

from personal_assistant.config.models import LOCAL_MODEL
from personal_assistant.tools.calendar_tools import list_today_calendar_events


calendar_agent = Agent(
    name="calendar_agent",
    model=LOCAL_MODEL,
    description="Specialized agent responsible for read-only Google Calendar queries.",
    instruction="""
You are a calendar specialist.

Your responsibility:
- Show today's upcoming Google Calendar events.

Use list_today_calendar_events when the user asks:
- what is on my calendar today
- show my calendar
- today's meetings
- today's events
- do I have anything today

This is read-only. Do not create, update, or delete calendar events.
""",
    tools=[
        list_today_calendar_events,
    ],
)