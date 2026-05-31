from personal_assistant.integrations.calendar_service import get_today_events


def list_today_calendar_events() -> dict:
    """
    List today's upcoming Google Calendar events.

    This is read-only and does not create, update, or delete calendar events.
    """
    return get_today_events()