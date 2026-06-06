from enum import Enum


class Intent(str, Enum):
    TASK = "task"
    NOTE = "note"
    UNKNOWN = "unknown"


TASK_KEYWORDS = [
    "task",
    "todo",
    "to-do",
    "complete",
    "mark complete",
    "show tasks",
    "list tasks",
    "open tasks",
    "add task",
    "create task",
    "remind me",
]

NOTE_KEYWORDS = [
    "remember",
    "note that",
    "save note",
    "save this",
    "keep in mind",
    "store this",
    "show notes",
    "list notes",
    "recent notes",
    "search notes",
    "show my notes",
]


def classify_intent(message: str) -> Intent:
    text = message.lower().strip()

    if any(keyword in text for keyword in NOTE_KEYWORDS):
        return Intent.NOTE

    if any(keyword in text for keyword in TASK_KEYWORDS):
        return Intent.TASK

    return Intent.UNKNOWN