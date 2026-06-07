"""
Prometheus metrics for the Personal Assistant Agent.

This module centralizes all metric definitions so the rest of the
application can record observability data without knowing Prometheus details.
"""

from prometheus_client import Counter, Histogram


HTTP_REQUESTS_TOTAL = Counter(
    "assistant_http_requests_total",
    "Total HTTP chat requests received by the assistant.",
    ["endpoint", "method", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "assistant_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["endpoint", "method"],
)

AGENT_INVOCATIONS_TOTAL = Counter(
    "assistant_agent_invocations_total",
    "Total number of agent invocations.",
    ["agent_name"],
)

AGENT_DURATION_SECONDS = Histogram(
    "assistant_agent_duration_seconds",
    "Agent execution duration in seconds.",
    ["agent_name"],
)

AGENT_TRANSFERS_TOTAL = Counter(
    "assistant_agent_transfers_total",
    "Total number of agent transfer decisions.",
    ["from_agent", "to_agent"],
)

PROMPT_GUARD_BLOCKS_TOTAL = Counter(
    "assistant_prompt_guard_blocks_total",
    "Total number of requests blocked by prompt guard.",
)

ERRORS_TOTAL = Counter(
    "assistant_errors_total",
    "Total number of application errors.",
    ["component"],
)

LLM_CALLS_TOTAL = Counter(
    "assistant_llm_calls_total",
    "Total number of LLM calls.",
    ["model_name", "status"],
)

LLM_DURATION_SECONDS = Histogram(
    "assistant_llm_duration_seconds",
    "LLM call duration in seconds.",
    ["model_name"],
)

LLM_TOKENS_TOTAL = Counter(
    "assistant_llm_tokens_total",
    "Total LLM tokens used.",
    ["model_name", "token_type"],
)