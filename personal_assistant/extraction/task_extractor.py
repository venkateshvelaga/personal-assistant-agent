import re


def extract_task_fields(message: str) -> dict:
    text = message.strip()
    lower = text.lower()

    priority = "medium"
    if "high priority" in lower or "urgent" in lower:
        priority = "high"
    elif "low priority" in lower:
        priority = "low"

    due_date = ""
    for phrase in ["tomorrow", "today", "next week", "next month", "this month", "this evening", "in the evening"]:
        if phrase in lower:
            due_date = phrase
            break

    title = text

    cleanup_phrases = [
        "add a high priority task to",
        "add high priority task to",
        "add a low priority task to",
        "add low priority task to",
        "add a task to",
        "add task to",
        "create a task to",
        "create task to",
        "remind me to",
        "todo",
        "to-do",
        "high priority",
        "low priority",
        "urgent",
    ]

    for phrase in cleanup_phrases:
        title = re.sub(phrase, "", title, flags=re.IGNORECASE).strip()

    return {
        "title": title,
        "due_date": due_date,
        "priority": priority,
    }