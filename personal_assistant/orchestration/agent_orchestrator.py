import re
import uuid

from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from personal_assistant.agent import root_agent
from personal_assistant.agents.task_agent import task_agent
from personal_assistant.agents.notes_agent import notes_agent
from personal_assistant.agents.briefing_agent import briefing_agent
from personal_assistant.agents.calendar_agent import calendar_agent
from personal_assistant.agents.gmail_agent import gmail_agent
from personal_assistant.agents.database_agent import database_agent


APP_NAME = "personal_assistant_custom_ui"
USER_ID = "local_user"

session_service = InMemorySessionService()

AGENTS = {
    "root": root_agent,
    "task_agent": task_agent,
    "notes_agent": notes_agent,
    "briefing_agent": briefing_agent,
    "calendar_agent": calendar_agent,
    "gmail_agent": gmail_agent,
    "database_agent": database_agent,
}

RUNNERS = {
    name: Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    for name, agent in AGENTS.items()
}


async def handle_user_message_with_agents(
    message: str,
    session_id: str | None = None,
) -> dict:
    """
    End-to-end agentic orchestration.

    1. Ask root agent what to do.
    2. If root asks to transfer, run target agent.
    3. Target agent calls its tools.
    4. Return final response.
    """

    session_id = session_id or str(uuid.uuid4())

    root_result = await run_agent(
        agent_name="root",
        message=message,
        session_id=session_id,
    )

    transfer_agent = extract_transfer_agent(root_result["text"])

    if transfer_agent and transfer_agent in RUNNERS:
        target_result = await run_agent(
            agent_name=transfer_agent,
            message=message,
            session_id=session_id,
        )

        return {
            "session_id": session_id,
            "handled_by": transfer_agent,
            "root_trace": root_result,
            "final_trace": target_result,
            "reply": target_result["text"],
        }

    return {
        "session_id": session_id,
        "handled_by": "root",
        "root_trace": root_result,
        "final_trace": root_result,
        "reply": root_result["text"],
    }


async def run_agent(agent_name: str, message: str, session_id: str) -> dict:
    await ensure_session(session_id)

    content = types.Content(
        role="user",
        parts=[types.Part(text=message)],
    )

    events = []

    async for event in RUNNERS[agent_name].run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        events.append(event)

    text = extract_last_text(events)

    log_events(agent_name, events)

    return {
        "agent": agent_name,
        "text": text,
        "event_count": len(events),
    }


async def ensure_session(session_id: str) -> None:
    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
    except Exception:
        pass


def extract_transfer_agent(text: str) -> str | None:
    if not text:
        return None

    patterns = [
        r'transfer_to_agent\("([^"]+)"\)',
        r"transfer_to_agent\('([^']+)'\)",
        r'"agent_name"\s*:\s*"([^"]+)"',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return None


def extract_last_text(events) -> str:
    texts = []

    for event in events:
        if not event.content or not event.content.parts:
            continue

        for part in event.content.parts:
            text = getattr(part, "text", None)
            if text:
                cleaned = text.strip()
                if cleaned:
                    texts.append(cleaned)

    return texts[-1] if texts else ""


def log_events(agent_name: str, events) -> None:
    print(f"\n========== AGENT TRACE: {agent_name} ==========")

    for index, event in enumerate(events, start=1):
        print(f"\n--- Event {index} ---")
        print(f"Author: {getattr(event, 'author', None)}")
        print(f"Final response: {event.is_final_response()}")

        if event.content and event.content.parts:
            for part in event.content.parts:
                text = getattr(part, "text", None)
                function_call = getattr(part, "function_call", None)
                function_response = getattr(part, "function_response", None)

                if text:
                    print(f"Text: {text}")

                if function_call:
                    print(f"Function call: {function_call}")

                if function_response:
                    print(f"Function response: {function_response}")

    print(f"\n========== END TRACE: {agent_name} ==========\n")