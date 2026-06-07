import time 
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Response;
from pydantic import BaseModel

from personal_assistant.orchestration.agent_orchestrator import (
    handle_user_message_with_agents,
)

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from personal_assistant.observability.metrics import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    AGENT_INVOCATIONS_TOTAL,
    AGENT_DURATION_SECONDS,
    AGENT_TRANSFERS_TOTAL, 
    PROMPT_GUARD_BLOCKS_TOTAL,
    ERRORS_TOTAL,
)


app = FastAPI(title="Personal Assistant Agent")

app.mount("/static", StaticFiles(directory="web_app/static"), name="static")


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.get("/")
def home():
    return FileResponse("web_app/static/index.html")


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint used by the custom UI.

    This endpoint delegates AI execution to the agent orchestrator.
    Metrics are recorded here for HTTP-level observability.
    """
    start_time = time.perf_counter()

    try:
        result = await handle_user_message_with_agents(
            message=request.message,
            session_id=request.session_id,
        )

        HTTP_REQUESTS_TOTAL.labels(
            endpoint="/chat",
            method="POST",
            status="success",
        ).inc()

        return {
            "session_id": result["session_id"],
            "reply": result["reply"],
            "handled_by": result["handled_by"],
            "raw": result,
        }

    except Exception:
        ERRORS_TOTAL.labels(component="web_app.chat").inc()

        HTTP_REQUESTS_TOTAL.labels(
            endpoint="/chat",
            method="POST",
            status="error",
        ).inc()

        raise

    finally:
        duration = time.perf_counter() - start_time

        HTTP_REQUEST_DURATION_SECONDS.labels(
            endpoint="/chat",
            method="POST",
        ).observe(duration)


@app.get("/metrics")
def metrics():
    try:
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)
    except Exception as e:
        ERRORS_TOTAL.labels(component="metrics_endpoint").inc()
        return Response(content=str(e), status_code=500)