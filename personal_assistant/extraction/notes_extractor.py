import re


def extract_note_fields(message: str) -> dict:
    text = message.strip()

    content = text
    cleanup_phrases = [
        "remember that",
        "note that",
        "save this",
        "save note",
        "keep in mind that",
        "store this",
    ]

    for phrase in cleanup_phrases:
        content = re.sub(phrase, "", content, flags=re.IGNORECASE).strip()

    lower = content.lower()

    topic = "general"
    topic_keywords = {
        "insurance": ["insurance", "renewal", "premium"],
        "grocery": ["grocery", "groceries", "shopping"],
        "family": ["daughter", "wife", "brother", "family"],
        "health": ["doctor", "medicine", "health", "gym"],
        "finance": ["bill", "payment", "tax", "loan", "mortgage"],
    }

    for candidate_topic, keywords in topic_keywords.items():
        if any(keyword in lower for keyword in keywords):
            topic = candidate_topic
            break

    return {
        "topic": topic,
        "content": content,
    }