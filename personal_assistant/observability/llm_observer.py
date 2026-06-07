"""
LLM observability wrapper.

This module wraps LiteLLM calls so every LLM request records:
- call count
- duration
- token usage
- success/failure

All future direct LLM calls should go through this module instead of calling
litellm.completion directly.
"""

import time
from typing import Any

from litellm import completion

from personal_assistant.observability.metrics import (
    LLM_CALLS_TOTAL,
    LLM_DURATION_SECONDS,
    LLM_TOKENS_TOTAL,
)


def observed_completion(
    model: str,
    messages: list[dict[str, str]],
    **kwargs: Any,
) -> Any:
    """
    Call an LLM through LiteLLM and record Prometheus metrics.

    Args:
        model: LiteLLM model name, for example "ollama_chat/qwen2.5:7b".
        messages: Chat messages passed to the model.
        **kwargs: Additional model configuration such as temperature,
            top_p, and max_tokens.

    Returns:
        The raw LiteLLM response object.
    """
    start_time = time.perf_counter()

    try:
        response = completion(
            model=model,
            messages=messages,
            **kwargs,
        )

        LLM_CALLS_TOTAL.labels(
            model_name=model,
            status="success",
        ).inc()

        record_token_usage(model, response)

        return response

    except Exception:
        LLM_CALLS_TOTAL.labels(
            model_name=model,
            status="error",
        ).inc()
        raise

    finally:
        duration = time.perf_counter() - start_time

        LLM_DURATION_SECONDS.labels(
            model_name=model,
        ).observe(duration)


def record_token_usage(model: str, response: Any) -> None:
    """
    Extract token usage from LiteLLM response and record it.

    Some providers may not return token usage. In that case, this function
    safely does nothing.
    """
    usage = response.get("usage") if isinstance(response, dict) else getattr(response, "usage", None)

    if not usage:
        return

    prompt_tokens = get_usage_value(usage, "prompt_tokens")
    completion_tokens = get_usage_value(usage, "completion_tokens")
    total_tokens = get_usage_value(usage, "total_tokens")

    if prompt_tokens is not None:
        LLM_TOKENS_TOTAL.labels(
            model_name=model,
            token_type="prompt",
        ).inc(prompt_tokens)

    if completion_tokens is not None:
        LLM_TOKENS_TOTAL.labels(
            model_name=model,
            token_type="completion",
        ).inc(completion_tokens)

    if total_tokens is not None:
        LLM_TOKENS_TOTAL.labels(
            model_name=model,
            token_type="total",
        ).inc(total_tokens)


def get_usage_value(usage: Any, key: str) -> int | None:
    """
    Read token usage from either a dict-like or object-like usage structure.
    """
    if isinstance(usage, dict):
        return usage.get(key)

    return getattr(usage, key, None)