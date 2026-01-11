import uuid
from datetime import datetime, date
from typing import List, Optional
from app.repositories.base import ThoughtRepository, SummaryRepository
from app.schemas.thoughts import ThoughtListItem, ThoughtAIResult
from app.schemas.enums import ReplyType
from app.schemas.summaries import SummaryJSON


class InMemoryRepo(ThoughtRepository, SummaryRepository):
    def __init__(self) -> None:
        self._thoughts: List[ThoughtListItem] = []
        self._summaries: dict[str, SummaryJSON] = {}

    async def create_thought(self, content: str, reply_type: ReplyType, ai: ThoughtAIResult) -> str:
        tid = str(uuid.uuid4())
        item = ThoughtListItem(
            id=tid,
            content=content,
            created_at=datetime.utcnow(),
            reply_type=reply_type,
            reply_text=ai.reply_text,
            topic_guess=ai.topic_guess,
            mood_guess=ai.mood_guess,
            mood_score=ai.mood_score,
            context_guess=ai.context_guess,
        )
        self._thoughts.insert(0, item)
        return tid

    async def list_thoughts(self, limit: int, offset: int) -> List[ThoughtListItem]:
        return self._thoughts[offset : offset + limit]

    async def list_thoughts_in_period(self, start: date, end: date) -> List[ThoughtListItem]:
        # end: inclusive
        def in_range(dt: datetime) -> bool:
            d = dt.date()
            return start <= d <= end

        return [t for t in self._thoughts if in_range(t.created_at)]

    async def get_summary(self, start: date, end: date) -> Optional[SummaryJSON]:
        return self._summaries.get(f"{start.isoformat()}__{end.isoformat()}")

    async def save_summary(self, start: date, end: date, summary: SummaryJSON) -> None:
        self._summaries[f"{start.isoformat()}__{end.isoformat()}"] = summary
