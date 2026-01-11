from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = Field(default="murmur-backend", alias="APP_NAME")
    env: str = Field(default="dev", alias="ENV")
    debug: bool = Field(default=True, alias="DEBUG")

    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")

    # Qwen (DashScope)
    qwen_base_url: str = Field(default="https://dashscope.aliyuncs.com", alias="QWEN_BASE_URL")
    qwen_api_key: str = Field(default="", alias="QWEN_API_KEY")
    qwen_model: str = Field(default="qwen-plus", alias="QWEN_MODEL")
    qwen_timeout_seconds: int = Field(default=8, alias="QWEN_TIMEOUT_SECONDS")

    # Repo
    repo_mode: str = Field(default="in_memory", alias="REPO_MODE")

    # Supabase (optional)
    supabase_url: str = Field(default="", alias="SUPABASE_URL")
    supabase_service_role_key: str = Field(default="", alias="SUPABASE_SERVICE_ROLE_KEY")

    def parsed_cors_origins(self) -> List[str]:
        raw = (self.cors_origins or "").strip()
        if raw == "*" or raw == "":
            return ["*"]
        return [s.strip() for s in raw.split(",") if s.strip()]


settings = Settings()
