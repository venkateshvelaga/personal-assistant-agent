from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from personal_assistant.tools.task_tools import (
    create_task,
    list_tasks,
    complete_task,
)


task_agent = Agent(
    name="task_agent",
    #model="gemini-2.5-flash-lite",
    model=LiteLlm(model="ollama_chat/qwen2.5:7b"),
    description="Specialized agent responsible for task management.",
    instruction="""
You are a task management specialist.

Your responsibilities:
- create tasks
- list tasks
- complete tasks

Always use the provided tools when modifying or retrieving task data.

Do not claim a task was created, listed, or completed unless a tool was successfully called.
""",
    tools=[
        create_task,
        list_tasks,
        complete_task,
    ],
)