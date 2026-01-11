from fastapi import APIRouter, Depends
from app.api.deps import get_repo
from app.schemas.thoughts import ThoughtCreateRequest, ThoughtCreateResponse, ThoughtListItem
from app.services.thought_service import ThoughtService

router = APIRouter(prefix="/api/thoughts", tags=["thoughts"])


@router.post("", response_model=ThoughtCreateResponse)
async def create_thought(payload: ThoughtCreateRequest, repo=Depends(get_repo)):
    service = ThoughtService(repo)
    ai = await service.generate_ai_result(payload.content, payload.response_type)
    tid = await repo.create_thought(
        content=payload.content,
        reply_type=payload.reply_type,
        response_type=ai.response_type,
        ai=ai,
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
        response_type=t.response_type,
    )


@router.get("", response_model=list[ThoughtListItem])
async def list_thoughts(limit: int = 50, offset: int = 0, repo=Depends(get_repo)):
    limit = max(1, min(limit, 200))
    offset = max(0, offset)
    return await repo.list_thoughts(limit=limit, offset=offset)
