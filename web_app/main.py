from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from personal_assistant.orchestration.agent_orchestrator import (
    handle_user_message_with_agents,
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
    result = await handle_user_message_with_agents(
        message=request.message,
        session_id=request.session_id,
    )

    return {
        "session_id": result["session_id"],
        "reply": result["reply"],
        "handled_by": result["handled_by"],
        "raw": result,
    }