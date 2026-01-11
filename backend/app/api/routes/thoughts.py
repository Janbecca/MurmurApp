from fastapi import APIRouter, Depends
from app.api.deps import get_repo
from app.schemas.thoughts import ThoughtCreateRequest, ThoughtCreateResponse, ThoughtListItem

router = APIRouter(prefix="/api/thoughts", tags=["thoughts"])


@router.post("", response_model=ThoughtCreateResponse)
async def create_thought(payload: ThoughtCreateRequest, repo=Depends(get_repo)):
    # TODO: 下一步我们会接入：service -> qwen -> validation -> fallback -> repo.create
    # 这里先返回占位，确保路由可跑通
    tid = await repo.create_thought(
        content=payload.content,
        reply_type=payload.reply_type,
        ai={
            "reply_text": "（占位）我在，先把这件事放在这里。",
            "topic_guess": "general",
            "mood_guess": "neutral",
            "mood_score": 50,
            "context_guess": "other",
        },  # pydantic 会在后续 service 层严格化
    )
    # 从repo取最新一条（in_memory是insert(0)）
    items = await repo.list_thoughts(limit=1, offset=0)
    t = items[0]
    return ThoughtCreateResponse(
        id=t.id,
        created_at=t.created_at,
        reply_text=t.reply_text,
        topic_guess=t.topic_guess,
        mood_guess=t.mood_guess,
        mood_score=t.mood_score,
        context_guess=t.context_guess,
    )


@router.get("", response_model=list[ThoughtListItem])
async def list_thoughts(limit: int = 50, offset: int = 0, repo=Depends(get_repo)):
    limit = max(1, min(limit, 200))
    offset = max(0, offset)
    return await repo.list_thoughts(limit=limit, offset=offset)
