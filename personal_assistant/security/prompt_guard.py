BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "override your instructions",
    "reveal system prompt",
    "show system prompt",
    "print system prompt",
    "show credentials",
    "show token",
    "gmail_token",
    "token.json",
    "credentials.json",
    ".env",
    "api key",
    "secret key",
]


def is_prompt_injection_attempt(message: str) -> bool:
    text = message.lower()

    return any(pattern in text for pattern in BLOCKED_PATTERNS)


def guard_user_message(message: str) -> dict:
    if is_prompt_injection_attempt(message):
        return {
            "allowed": False,
            "reason": "Potential prompt injection or secret access attempt detected.",
        }

    return {
        "allowed": True,
        "reason": "Message passed prompt guard.",
    }