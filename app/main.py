"""
Enterprise FastAPI Application Entrypoint.
==============================================================================
Multi-Agent Business Operations Platform
==============================================================================
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.environment import get_active_environment, get_env_file_path
from app.core.exceptions import register_exception_handlers
from app.core.logging import log_startup_banner, setup_logging
from app.middlewares.process_time import ProcessTimeMiddleware
from app.middlewares.request_id import RequestIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    Handles startup configuration checks and graceful teardown.
    """
    settings = get_settings()
    active_env = get_active_environment()
    env_file = get_env_file_path(active_env)
    logger = setup_logging(settings.LOG_LEVEL, settings.DEBUG)

    # Display enterprise banner with active environment & file path
    log_startup_banner(
        app_name=settings.APP_NAME,
        app_version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        env_file_path=str(env_file),
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
        logger=logger,
    )

    logger.info(f"Initialized application in [{settings.APP_ENV.upper()}] mode successfully.")
    yield
    logger.info("Initiating graceful application shutdown.")


def create_application() -> FastAPI:
    """
    FastAPI Application Factory.
    Builds and configures the production-ready FastAPI instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Production Enterprise Backend for Multi-Agent Business Operations Platform",
        docs_url="/docs" if (settings.DEBUG or settings.is_development) else "/docs",
        redoc_url="/redoc" if (settings.DEBUG or settings.is_development) else None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # -------------------------------------------------------------------------
    # Register Middlewares (LIFO execution order)
    # -------------------------------------------------------------------------
    # Process latency benchmarking
    app.add_middleware(ProcessTimeMiddleware)

    # Distributed tracing request ID
    app.add_middleware(RequestIdMiddleware)

    # Cross-Origin Resource Sharing (CORS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------------------------------------------------------
    # Exception Handlers
    # -------------------------------------------------------------------------
    register_exception_handlers(app)

    # -------------------------------------------------------------------------
    # Routers
    # -------------------------------------------------------------------------
    app.include_router(api_v1_router, prefix="/api")

    # Root redirect to API documentation
    @app.get("/", include_in_schema=False)
    async def root_redirect():
        return RedirectResponse(url="/docs")

    return app


# Application singleton for ASGI servers (Uvicorn / Gunicorn)
app = create_application()
