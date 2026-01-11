from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.core.logging import setup_logging
from app.core.errors import AppError
from app.api.routes import all_routers
import logging

logger = logging.getLogger("app")


def create_app() -> FastAPI:
    setup_logging("DEBUG" if settings.debug else "INFO")

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
    )

    # CORS
    origins = settings.parsed_cors_origins()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if origins != ["*"] else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    for r in all_routers:
        app.include_router(r)

    # Error handler
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.warning("AppError %s: %s", exc.code, exc.message)
        return fastapi_json(
            status_code=exc.http_status,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    return app


def fastapi_json(status_code: int, content: dict):
    # 轻量封装，避免每次 import JSONResponse
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=status_code, content=content)


app = create_app()
