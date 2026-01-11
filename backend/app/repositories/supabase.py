from datetime import date
from typing import List, Optional
import httpx
from app.core.settings import settings
from app.core.errors import AppError
from app.repositories.base import ThoughtRepository, SummaryRepository
from app.schemas.thoughts import ThoughtListItem, ThoughtAIResult
from app.schemas.enums import ReplyType
from app.schemas.summaries import SummaryJSON


class SupabaseRepo(ThoughtRepository, SummaryRepository):
    def __init__(self) -> None:
        if not settings.supabase_url or not settings.supabase_service_role_key:
            raise AppError("supabase_not_configured", "Supabase credentials missing", http_status=500)
        self.base_url = settings.supabase_url.rstrip("/") + "/rest/v1"
        self.key = settings.supabase_service_role_key
        self.thoughts_table = "thoughts"
        self.summaries_table = "summaries"

    def _headers(self) -> dict[str, str]:
        return {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    async def create_thought(self, content: str, response_type: ReplyType, ai: ThoughtAIResult) -> str:
        payload = {
            "content": content,
            "response_type": response_type.value,
            "reply_text": ai.reply_text,
            "topic_guess": ai.topic_guess,
            "mood_guess": ai.mood_guess,
            "mood_score": ai.mood_score,
            "context_guess": ai.context_guess,
        }
        url = f"{self.base_url}/{self.thoughts_table}"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, headers={**self._headers(), "Prefer": "return=representation"}, json=payload)
            if response.status_code >= 400:
                raise AppError("supabase_insert_failed", response.text, http_status=502)
            data = response.json()
        if not data:
            raise AppError("supabase_insert_failed", "Empty response", http_status=502)
        return data[0].get("id")

    async def list_thoughts(self, limit: int, offset: int) -> List[ThoughtListItem]:
        url = f"{self.base_url}/{self.thoughts_table}?select=*"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=self._headers(), params={"limit": limit, "offset": offset})
            if response.status_code >= 400:
                raise AppError("supabase_list_failed", response.text, http_status=502)
            data = response.json()
        return [ThoughtListItem.model_validate(item) for item in data]

    async def list_thoughts_in_period(self, start: date, end: date) -> List[ThoughtListItem]:
        url = f"{self.base_url}/{self.thoughts_table}?select=*"
        params = [
            ("created_at", f"gte.{start.isoformat()}T00:00:00Z"),
            ("created_at", f"lte.{end.isoformat()}T23:59:59Z"),
        ]
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=self._headers(), params=params)
            if response.status_code >= 400:
                raise AppError("supabase_list_failed", response.text, http_status=502)
            data = response.json()
        return [ThoughtListItem.model_validate(item) for item in data]

    async def get_summary(self, start: date, end: date) -> Optional[SummaryJSON]:
        url = f"{self.base_url}/{self.summaries_table}?select=*"
        params = {
            "period_start": f"eq.{start.isoformat()}",
            "period_end": f"eq.{end.isoformat()}",
            "limit": 1,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=self._headers(), params=params)
            if response.status_code >= 400:
                raise AppError("supabase_summary_failed", response.text, http_status=502)
            data = response.json()
        if not data:
            return None
        return SummaryJSON.model_validate(data[0]["summary_json"])

    async def save_summary(self, start: date, end: date, summary: SummaryJSON) -> None:
        payload = {
            "period_start": start.isoformat(),
            "period_end": end.isoformat(),
            "summary_json": summary.model_dump(),
        }
        url = f"{self.base_url}/{self.summaries_table}"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, headers={**self._headers(), "Prefer": "return=representation"}, json=payload)
            if response.status_code >= 400:
                raise AppError("supabase_summary_save_failed", response.text, http_status=502)
