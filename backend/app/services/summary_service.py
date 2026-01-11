from datetime import date
from app.schemas.summaries import SummaryJSON
from app.services.qwen_client import QwenClient


class SummaryService:
    def __init__(self, repo) -> None:
        self.repo = repo
        self.qwen = QwenClient()

    async def generate_summary(self, start: date, end: date) -> SummaryJSON:
        thoughts = await self.repo.list_thoughts_in_period(start, end)
        if self.qwen.is_configured() and thoughts:
            prompt = self._build_prompt(start.isoformat(), end.isoformat(), thoughts)
            data = await self.qwen.generate_json(prompt)
            return SummaryJSON.model_validate(data)

        title = "本周期情绪概览"
        insights = ["你有在持续记录，这是重要的一步。"]
        if not thoughts:
            insights.append("本周期还没有记录，先从一句话开始也很好。")
        return SummaryJSON(title=title, insights=insights)

    def _build_prompt(self, start: str, end: str, thoughts: list) -> str:
        items = [
            {
                "content": t.content,
                "created_at": t.created_at.isoformat(),
                "response_type": t.response_type.value,
                "topic_guess": t.topic_guess,
                "mood_guess": t.mood_guess.value,
                "context_guess": t.context_guess.value,
            }
            for t in thoughts
        ]
        return (
            "你是一个情绪分析助手，需要为一个周期生成总结 JSON。\n"
            "输出必须是严格 JSON，字段结构为 SummaryJSON：\n"
            "title, mood_trend[], mood_distribution[], top_triggers[], recurring_thoughts[], context_split[], insights[], suggestions[], persona_story。\n"
            "不确定时可以输出空数组，但必须包含 title 与 insights。\n\n"
            f"period_start: {start}\n"
            f"period_end: {end}\n"
            f"thoughts: {items}"
        )
