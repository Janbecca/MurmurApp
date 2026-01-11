from typing import Optional
from app.schemas.thoughts import ThoughtAIResult
from app.schemas.enums import ReplyType
from app.services.qwen_client import QwenClient


class ThoughtService:
    def __init__(self, repo) -> None:
        self.repo = repo
        self.qwen = QwenClient()

    async def generate_ai_result(self, content: str, response_type: Optional[ReplyType]) -> ThoughtAIResult:
        if self.qwen.is_configured():
            prompt = self._build_prompt(content, response_type)
            data = await self.qwen.generate_json(prompt)
            return ThoughtAIResult.model_validate(data)

        fallback_type = response_type or ReplyType.reflective
        return ThoughtAIResult(
            reply_text="我在，先把这件事放在这里。",
            topic_guess="general",
            mood_guess="neutral",
            mood_score=50,
            context_guess="other",
            response_type=fallback_type,
        )

    def _build_prompt(self, content: str, response_type: Optional[ReplyType]) -> str:
        type_hint = response_type.value if response_type else "auto"
        return (
            "你是一个情绪支持型助手，目标是低打断地接住用户碎碎念。\n"
            "请根据内容自动选择回应类型：reflective / clarifying / action / boundary。\n"
            "如果用户指定 response_type，则尽量遵循，否则自动判断。\n"
            "输出必须是严格 JSON，字段如下：\n"
            "reply_text (string, <=500)、topic_guess (string)、mood_guess (joy|sadness|anxiety|anger|calm|neutral)、"
            "mood_score (0-100)、context_guess (work|study|relationship|family|health|other)、"
            "response_type (reflective|clarifying|action|boundary)。\n\n"
            f"response_type_preference: {type_hint}\n"
            f"content: {content}"
        )
