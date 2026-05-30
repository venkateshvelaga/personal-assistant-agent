from google.adk.agents import Agent

from personal_assistant.config.models import LOCAL_MODEL
from personal_assistant.tools.briefing_tools import generate_daily_briefing


briefing_agent = Agent(
    name="briefing_agent",
    model=LOCAL_MODEL,
    description="Specialized agent responsible for generating daily briefings from tasks and notes.",
    instruction="""
You are a daily briefing specialist.

Your responsibility is to generate a practical daily briefing using available tasks and notes.

When the user asks for:
- daily briefing
- plan my day
- what should I focus on
- summarize my day
- morning briefing

use the generate_daily_briefing tool.

Do not invent calendar or email information.
Only use available task and note data.
""",
    tools=[
        generate_daily_briefing,
    ],
)