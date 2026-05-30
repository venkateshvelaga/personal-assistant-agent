from google.adk.agents import Agent
from personal_assistant.config.models import LOCAL_MODEL

from personal_assistant.tools.task_tools import (
    create_task_from_message,
    list_tasks,
    complete_task,
)


task_agent = Agent(
    name="task_agent",
    #model="gemini-2.5-flash-lite",
    model= LOCAL_MODEL,
    description="Specialized agent responsible for task management.",
    instruction="""
You are a task management specialist.

Your responsibilities:
- create tasks
- list tasks
- complete tasks

Always use the provided tools when modifying or retrieving task data.
When creating a task from user text, use create_task_from_message.
Use list_tasks to list tasks.
Use complete_task to complete tasks.

Do not claim a task was created, listed, or completed unless a tool was successfully called.
""",
    tools=[
        create_task_from_message,
        list_tasks,
        complete_task,
    ],
)