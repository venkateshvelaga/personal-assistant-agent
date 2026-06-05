from google.adk.agents import Agent

from personal_assistant.config.models import LOCAL_MODEL
from personal_assistant.tools.database_tools import inspect_database


database_agent = Agent(
    name="database_agent",
    model=LOCAL_MODEL,
    description="Specialized agent responsible for inspecting local SQLite database state.",
    instruction="""
You are a database inspection specialist.

Your responsibility:
- Show database statistics
- Summarize current task and note counts
- Show recent task and note records

Use inspect_database when the user asks:
- show database stats
- inspect database
- what is stored
- how many tasks do I have
- how many notes do I have
- show recent database records

Do not modify data.
This agent is read-only.
""",
    tools=[
        inspect_database,
    ],
)