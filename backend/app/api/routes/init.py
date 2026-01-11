from .health import router as health_router
from .thoughts import router as thoughts_router
from .summaries import router as summaries_router

all_routers = [health_router, thoughts_router, summaries_router]
