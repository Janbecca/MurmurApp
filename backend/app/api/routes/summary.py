from datetime import date
from fastapi import APIRouter, Depends
from app.api.deps import get_repo
from app.schemas.summaries import SummaryRequest, SummaryResponse, SummaryJSON

router = APIRouter(prefix="/api/summaries", tags=["summaries"])


@router.post("", response_model=SummaryResponse)
async def create_or_get_summary(payload: SummaryRequest, repo=Depends(get_repo)):
    start = date.fromisoformat(payload.period_start)
    end = date.fromisoformat(payload.period_end)

    cached = await repo.get_summary(start, end)
    if cached:
        return SummaryResponse(period_start=payload.period_start, period_end=payload.period_end, summary=cached)

    # TODO: 下一步用 SummaryService 调 Qwen 生成
    summary = SummaryJSON(
        title="（占位）本周期情绪概览",
        insights=["你有在持续记录，这是重要的一步。"],
    )
    await repo.save_summary(start, end, summary)
    return SummaryResponse(period_start=payload.period_start, period_end=payload.period_end, summary=summary)
