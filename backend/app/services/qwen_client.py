import json
from typing import Any
import httpx
from app.core.settings import settings
from app.core.errors import AppError


class QwenClient:
    def __init__(self) -> None:
        self.base_url = settings.qwen_base_url.rstrip("/")
        self.api_key = settings.qwen_api_key
        self.model = settings.qwen_model
        self.timeout = settings.qwen_timeout_seconds

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def generate_json(self, prompt: str) -> dict[str, Any]:
        if not self.is_configured():
            raise AppError("qwen_not_configured", "Qwen API key not configured", http_status=500)

        url = f"{self.base_url}/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "input": {
                "prompt": prompt,
            },
            "parameters": {
                "result_format": "message",
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code >= 400:
                raise AppError("qwen_request_failed", response.text, http_status=502)
            data = response.json()

        try:
            content = data["output"]["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise AppError("qwen_response_invalid", "Unexpected Qwen response format", http_status=502) from exc

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise AppError("qwen_json_invalid", "Qwen response is not valid JSON", http_status=502) from exc
