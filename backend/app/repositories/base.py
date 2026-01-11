from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from app.schemas.thoughts import ThoughtListItem, ThoughtAIResult
from app.schemas.enums import ReplyType
from app.schemas.summaries import SummaryJSON


class ThoughtRepository(ABC):
    @abstractmethod
    async def create_thought(
        self,
        content: str,
        response_type: ReplyType,
        ai: ThoughtAIResult,
    ) -> str:
        ...

    @abstractmethod
    async def list_thoughts(self, limit: int, offset: int) -> List[ThoughtListItem]:
        ...

    @abstractmethod
    async def list_thoughts_in_period(self, start: date, end: date) -> List[ThoughtListItem]:
        ...


class SummaryRepository(ABC):
    @abstractmethod
    async def get_summary(self, start: date, end: date) -> Optional[SummaryJSON]:
        ...

    @abstractmethod
    async def save_summary(self, start: date, end: date, summary: SummaryJSON) -> None:
        ...
