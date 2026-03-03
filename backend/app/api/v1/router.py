from fastapi import APIRouter
from app.api.v1.endpoints.idea import router as idea_router

router = APIRouter()

# Register endpoint routers
# The prefix is handled either here or in main.py. 
# Based on instructions, we'll keep the prefix empty here.
router.include_router(idea_router, prefix="", tags=["Idea Analysis"])
