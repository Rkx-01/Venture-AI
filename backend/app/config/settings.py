"""
config/settings.py
------------------
Centralised configuration for the AI Startup Analyst API.

All values are read from environment variables (or a .env file via
python-dotenv). Required fields have no default and will raise a clear
ValidationError at startup if missing — fast-fail beats silent misconfiguration.

Usage anywhere in the app:
    from app.config.settings import get_settings
    settings = get_settings()
"""
from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import List, Optional, Any, Literal

from pydantic import (
    Field,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------------------------------
# Enums — prevent typos in enum-like config values
# ---------------------------------------------------------------------------


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class VectorDBType(str, Enum):
    FAISS = "faiss"
    PINECONE = "pinecone"


# ---------------------------------------------------------------------------
# Settings model
# ---------------------------------------------------------------------------


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables / .env file.

    Fields marked with ... (Ellipsis) as default are REQUIRED.
    The app will refuse to start if they are missing.
    """

    model_config = SettingsConfigDict(
        # Load from .env if present; environment variables always take priority
        env_file=".env",
        env_file_encoding="utf-8",
        # Variable names are case-sensitive (APP_NAME ≠ app_name)
        case_sensitive=True,
        # Silently ignore unknown env vars — keeps the config clean
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application identity
    # ------------------------------------------------------------------
    APP_NAME: str = Field(
        default="AI Startup Analyst API",
        description="Human-readable name exposed in API docs and logs.",
    )
    APP_VERSION: str = Field(
        default="1.0.0",
        description="Semantic version of the API.",
    )
    ENVIRONMENT: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Runtime environment: development | staging | production | test",
    )

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000, ge=1, le=65535)

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    ALLOWED_ORIGINS: Any = Field(
        default=["http://localhost:3000"],
        description="List of origins allowed for CORS. Comma-separated in .env.",
    )

    USE_MOCK_DB: bool = Field(
        default=False,
        description="If True, the API will return mock data and bypass real DB calls.",
    )

    # ------------------------------------------------------------------
    # Database — REQUIRED
    # ------------------------------------------------------------------
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description=(
            "Full async-compatible PostgreSQL DSN. "
            "Example: postgresql+asyncpg://user:pass@host:5432/dbname"
        ),
    )

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------
    SECRET_KEY: SecretStr = Field(
        ...,
        description="Secret key used for JWT signing. Generate with: openssl rand -hex 32",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        ge=5,
        description="JWT access token lifetime in minutes.",
    )

    # ------------------------------------------------------------------
    # AI / LLM
    # ------------------------------------------------------------------
    LLM_PROVIDER: Literal["openai", "gemini"] = Field(
        default="gemini",
        description="LLM provider to use: 'openai' or 'gemini'.",
    )
    OPENAI_API_KEY: Optional[SecretStr] = Field(
        default=None,
        description="OpenAI API key. Required if LLM_PROVIDER is 'openai'.",
    )
    GEMINI_API_KEY: Optional[SecretStr] = Field(
        default=None,
        description="Google Gemini API key. Required if LLM_PROVIDER is 'gemini'.",
    )
    SERPAPI_KEY: Optional[SecretStr] = Field(
        default=None,
        description="SerpAPI key for real-time competitor search.",
    )

    # ------------------------------------------------------------------
    # Vector database — REQUIRED
    # ------------------------------------------------------------------
    VECTOR_DB_TYPE: VectorDBType = Field(
        ...,
        description="Vector store backend: 'faiss' (local) or 'pinecone' (cloud).",
    )

    # Pinecone — only required when VECTOR_DB_TYPE=pinecone
    PINECONE_API_KEY: Optional[SecretStr] = Field(
        default=None,
        description="Pinecone API key. Required only when VECTOR_DB_TYPE=pinecone.",
    )
    PINECONE_ENVIRONMENT: Optional[str] = Field(
        default=None,
        description="Pinecone cloud environment, e.g. 'us-east-1-aws'.",
    )

    # ------------------------------------------------------------------
    # External services
    # ------------------------------------------------------------------
    AI_ENGINE_URL: str = Field(
        default="http://localhost:8001",
        description="Internal URL of the AI engine microservice.",
    )

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: Optional[str]) -> Optional[str]:
        """Reject obvious placeholder values that ship in .env.example."""
        if v and ("user:password@" in v or v == ""):
            raise ValueError(
                "DATABASE_URL looks like an unfilled placeholder. "
                "Set a real PostgreSQL connection string, or leave it empty for No-DB mode."
            )
        return v

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def validate_allowed_origins(cls, v: Any) -> List[str]:
        """Support comma-separated strings or JSON arrays in .env."""
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    @model_validator(mode="after")
    def validate_provider_credentials(self) -> "Settings":
        """Ensure required keys for the selected LLM_PROVIDER are present."""
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("LLM_PROVIDER='openai' requires OPENAI_API_KEY")
        if self.LLM_PROVIDER == "gemini" and not self.GEMINI_API_KEY:
            raise ValueError("LLM_PROVIDER='gemini' requires GEMINI_API_KEY")
        
        # Pinecone validation
        if self.VECTOR_DB_TYPE == VectorDBType.PINECONE:
            missing = [
                name
                for name, val in [
                    ("PINECONE_API_KEY", self.PINECONE_API_KEY),
                    ("PINECONE_ENVIRONMENT", self.PINECONE_ENVIRONMENT),
                ]
                if not val
            ]
            if missing:
                raise ValueError(
                    f"VECTOR_DB_TYPE=pinecone requires: {', '.join(missing)}"
                )
        return self

    # ------------------------------------------------------------------
    # Computed helpers
    # ------------------------------------------------------------------

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == Environment.PRODUCTION

    @property
    def is_debug(self) -> bool:
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @property
    def docs_enabled(self) -> bool:
        """Swagger / ReDoc are only available in non-production environments."""
        return not self.is_production


# ---------------------------------------------------------------------------
# Singleton accessor — import this throughout the application
# ---------------------------------------------------------------------------


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    The cache is populated on first call; subsequent calls return the same
    object without re-reading the environment. Call `get_settings.cache_clear()`
    in tests to reset between test cases.
    """
    return Settings()
