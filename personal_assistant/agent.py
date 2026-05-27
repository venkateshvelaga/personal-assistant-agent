from google.adk.agents import Agent


root_agent = Agent(
    name="personal_assistant",
    model="gemini-2.5-flash-lite",
    description="A simple personal assistant agent for tasks, notes, and daily planning.",
    instruction="""
You are a helpful personal assistant.

For now, you can explain your planned capabilities:
- manage tasks
- save and search notes
- help plan the day
- later connect to calendar and email

Be concise, practical, and honest.
If a capability is not implemented yet, say so clearly.
""",
)