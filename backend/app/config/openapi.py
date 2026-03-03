"""
config/openapi.py
-----------------
OpenAPI document configuration for the AI Startup Analyst API.

Contains:
  - Title, description, and version
  - Contact information
  - Tags metadata (used to group endpoints in the Swagger UI)
"""
from __future__ import annotations

from app.config.settings import get_settings

settings = get_settings()

DESCRIPTION = """
**AI Startup Analyst API** powers investor-grade market research, 
competitor analysis, and feasibility scoring for new startup ideas.

### Features
* **Idea Analysis**: Submit a raw startup idea to get structured feedback.
* **Market Research**: Generate regional and industry-specific market reports.
* **Competitor Tracking**: Identify and analyze existing competitors.

*This API uses asynchronous processing. Analysis endpoints return 202 Accepted 
with a job ID that can be polled for results.*
"""

TAGS_METADATA = [
    {
        "name": "Analyze Idea",
        "description": "Core endpoints for evaluating a raw startup idea.",
    },
    {
        "name": "Market Analysis",
        "description": "Endpoints dedicated to market sizing and trend research.",
    },
    {
        "name": "Health",
        "description": "Infrastructure health checks used by load balancers and container orchestrators.",
    },
]

def get_openapi_kwargs() -> dict:
    """Returns kwargs to unfold into the FastAPI constructor."""
    kwargs = {
        "title": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": DESCRIPTION,
        "openapi_tags": TAGS_METADATA,
        "contact": {
            "name": "AI Startup Analyst Team",
            "url": "https://startupanalyst.ai/support",
            "email": "api@startupanalyst.ai",
        },
    }
    
    if not settings.docs_enabled:
        kwargs["openapi_url"] = None
        
    return kwargs
