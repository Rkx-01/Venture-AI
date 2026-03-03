from __future__ import annotations
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.openapi import get_openapi_kwargs
from app.config.settings import get_settings
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limiter import RateLimitMiddleware
from app.routers.api_router import api_router
from app.api.v1.router import router as api_v1_router
from app.routers.v1.health import router as health_router
from app.utils.logger import get_logger, setup_logging

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info(
        "%s v%s starting | env=%s",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT.value,
    )
    yield
    # --- Shutdown ---
    logger.info("%s shutting down gracefully.", settings.APP_NAME)


def create_app() -> FastAPI:
    """Application factory — builds and configures the FastAPI instance."""
    setup_logging()
    app = FastAPI(
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
        lifespan=lifespan,
        **get_openapi_kwargs(),
    )

    # Middleware is executed bottom-up (last added is outermost).
    # app.add_middleware(LoggingMiddleware)
    # app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
    
    # CORS configuration - Set to extremely permissive for cross-platform deployment
    # Since we use JWT in headers (not cookies), allow_credentials=False is safer and more compatible.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    logger.info("CORS configured with wildcard origins for maximum compatibility.")

    # --- Routers ---
    # Health check lives outside versioning (infrastructure concern, not API feature)
    app.include_router(health_router, tags=["Health"])
    # All versioned API routes — /api/v1/*, /api/v2/* etc.
    app.include_router(api_router)
    app.include_router(api_v1_router, prefix="/api/v1")

    # --- Exception handlers ---
    register_exception_handlers(app)

    return app


app = create_app()
