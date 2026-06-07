from google.adk.models.lite_llm import LiteLlm


#LOCAL_MODEL_NAME = "ollama_chat/llama3.1:8b"
LOCAL_MODEL_NAME = "ollama_chat/qwen2.5:7b"

LOCAL_MODEL = LiteLlm(model=LOCAL_MODEL_NAME)


MODEL_COMPLETION_CONFIG = {
    "temperature": 0.2,
    "top_p": 0.9,
    "max_tokens": 1000,
}