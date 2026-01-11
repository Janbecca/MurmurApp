from functools import lru_cache
from app.core.settings import settings, Settings
from app.repositories.in_memory import InMemoryRepo
from app.repositories.supabase import SupabaseRepo


@lru_cache
def get_settings() -> Settings:
    return settings


@lru_cache
def get_repo():
    if settings.repo_mode == "supabase":
        return SupabaseRepo()
    return InMemoryRepo()
