"""
routers/api_router.py
---------------------
Top-level versioned API router.

This is the single file that main.py imports. It mounts each version
under /api/vN, making version isolation and deprecation trivial.

How to add a new version
-------------------------
1. Create a new package: routers/v2/__init__.py
2. Define a `v2_router = APIRouter()` there with all v2 routes
3. Import it here and call:
       api_router.include_router(v2_router, prefix="/v2")

That's it — all v2 endpoints are now live at /api/v2/*.
Old v1 routes remain completely untouched.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.routers.v1 import v1_router
from app.routers import evaluate_startup

# Root API router — mounted at /api in main.py
api_router = APIRouter(prefix="/api")

# ── Primary Root Routes ───────────────────────────────────────────────────
api_router.include_router(
    evaluate_startup.router,
    prefix="/evaluate-startup",
    tags=["Evaluate Startup"],
)

# ── v1 ────────────────────────────────────────────────────────────────────
api_router.include_router(v1_router, prefix="/v1")
