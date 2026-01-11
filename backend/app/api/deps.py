from functools import lru_cache
from app.core.settings import settings, Settings
from app.repositories.in_memory import InMemoryRepo


@lru_cache
def get_settings() -> Settings:
    return settings


@lru_cache
def get_repo():
    # 后续：根据 settings.repo_mode 切换 supabase repo
    return InMemoryRepo()
