from google.adk.agents import Agent

from personal_assistant.tools.task_tools import (
    create_task,
    list_tasks,
    complete_task,
)


root_agent = Agent(
    name="personal_assistant",
    model="gemini-2.5-flash-lite",
    description="A personal assistant agent for tasks, notes, and daily planning.",
    instruction="""
You are a helpful personal assistant.

You currently have task management tools.

When the user asks to create, list, or complete tasks, use the available tools.
Be concise and practical.

If the user asks for calendar, email, or notes features, explain that those are not implemented yet.
Do not pretend to save something unless a tool actually saved it.
""",
    tools=[
        create_task,
        list_tasks,
        complete_task,
    ],
)