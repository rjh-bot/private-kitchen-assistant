from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

from app.models.database import get_db
from app.models.user import User
from app.agent.react_agent import ReActAgent

router = APIRouter(prefix="/api/chat", tags=["chat"])
_agent: ReActAgent | None = None

def set_agent(agent: ReActAgent):
    global _agent
    _agent = agent

class ChatRequest(BaseModel):
    message: str
    user_id: int = 1

@router.post("/stream")
async def chat_stream(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    if not _agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")

    # 加载用户档案
    result = await db.execute(select(User).where(User.id == req.user_id))
    user = result.scalar_one_or_none()
    profile = {}
    if user:
        profile = {
            "goal": user.goal,
            "diet_preference": user.diet_preference,
            "allergies": user.allergies,
            "long_term_instructions": user.long_term_instructions,
            "weight": user.weight
        }

    async def event_generator():
        yield {"event": "start", "data": "assistant"}
        async for chunk in _agent.stream_run(req.message, profile):
            yield {"event": "message", "data": chunk}
        yield {"event": "done", "data": ""}

    return EventSourceResponse(event_generator())
