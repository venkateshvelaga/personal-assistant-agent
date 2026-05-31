from personal_assistant.integrations.gmail_service import get_recent_emails


def list_recent_gmail_messages(max_results: int = 5) -> dict:
    """
    List recent Gmail inbox messages.

    This is read-only and does not send, delete, archive, or modify emails.

    Args:
        max_results: Maximum number of recent inbox messages to return.
    """
    return get_recent_emails(max_results)