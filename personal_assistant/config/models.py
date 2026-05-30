from google.adk.models.lite_llm import LiteLlm


LOCAL_MODEL_NAME = "ollama_chat/qwen2.5:7b"

LOCAL_MODEL = LiteLlm(model=LOCAL_MODEL_NAME)