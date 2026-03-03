from __future__ import annotations
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str

    model_config = {"json_schema_extra": {"example": {"status": "ok"}}}
