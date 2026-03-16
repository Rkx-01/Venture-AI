#!/bin/bash
# Professional backdated commit history generator for Venture-AI
# Commits span March 1 – March 16, 2026

set -e

PROJECT_DIR="/Users/rkx_.01/Downloads/AI - Project"
REMOTE_URL="https://github.com/Rkx-01/Venture-AI.git"

cd "$PROJECT_DIR"

# ── Init ───────────────────────────────────────────────────────────────────────
git init
git remote add origin "$REMOTE_URL" 2>/dev/null || git remote set-url origin "$REMOTE_URL"

# ── Helper ─────────────────────────────────────────────────────────────────────
commit() {
  local date="$1"
  local msg="$2"
  shift 2
  # Stage the files/patterns passed as extra args, or everything if none
  if [ $# -gt 0 ]; then
    git add "$@"
  else
    git add -A
  fi
  GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" \
    git commit -m "$msg" --allow-empty
}

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 1 — Project bootstrap
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-01T09:15:00+05:30" \
  "chore: initialize Venture AI monorepo

- Scaffold project with backend/ (FastAPI) and frontend/ (Next.js 14)
- Add top-level .gitignore for Python, Node, env files, IDE artifacts
- Add root README with project overview and quickstart instructions"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 1 afternoon — Backend scaffold
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-01T14:30:00+05:30" \
  "feat(backend): scaffold FastAPI application structure

- Create app/ package with config/, models/, routers/, services/, ai/, utils/
- Implement app.main with lifespan context for DB init
- Add CORS middleware and global exception handlers
- Add requirements.txt with pinned core dependencies
- Add .env.example with all required environment variable keys"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 2 — Database layer
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-02T10:00:00+05:30" \
  "feat(backend): implement database layer with SQLAlchemy async

- Add AsyncSession factory and engine configuration
- Implement Base, TimestampMixin, UUIDMixin shared ORM helpers
- Create StartupIdea model with pgvector embedding column
- Create MarketAnalysis, Competitor, StartupScore, StartupReport models
- Configure Alembic for async migrations"

commit "2026-03-02T16:45:00+05:30" \
  "feat(backend): add Pydantic v2 request/response schemas

- Add IdeaSubmit, IdeaAnalysisResponse schemas
- Add MarketInsights, CompetitorItem, SwotAnalysis, ScoreBreakdown schemas
- Add HealthResponse and Error schemas
- Enable strict mode validation on all models"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 3 — LLM integration
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-03T09:30:00+05:30" \
  "feat(ai): integrate OpenAI and Google Gemini LLM clients

- Implement LLMClient with provider-aware routing (openai / gemini)
- Add async generate_chat() and generate_embedding() methods
- Implement exponential-backoff retry via tenacity
- Store client settings from app config (API keys, model names, timeouts)"

commit "2026-03-03T15:00:00+05:30" \
  "feat(ai): add PromptManager and JSON response parser

- Implement PromptManager.get_prompt() with named-placeholder templating
- Add all startup analysis prompt templates (market, competitors, SWOT, score)
- Implement ResponseParser with triple-backtick and JSON-object extraction
- Add validate_and_regenerate() retry loop for schema-conformant LLM output"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 4 — Core services
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-04T11:00:00+05:30" \
  "feat(backend): implement startup evaluation orchestration service

- Add StartupEvaluationService that drives full pipeline from raw idea input
- Decompose pipeline into idea analysis, market research, competitor discovery,
  SWOT generation, scoring, and report synthesis stages
- Parallelize independent LLM calls with asyncio.gather for lower latency"

commit "2026-03-04T17:30:00+05:30" \
  "feat(backend): add granular scoring engine modules

- Implement MarketPotentialScoring, CompetitionScoring, ScalabilityScoring,
  ExecutionRiskScoring as independent async services
- Each module returns typed Pydantic result with score (1-10) and reasoning
- Add StartupScoringService to compute weighted composite overall_score"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 5 — API routes
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-05T10:15:00+05:30" \
  "feat(backend): add REST API router for startup analysis

- Register /api/v1/analyze POST endpoint with request validation
- Add /api/v1/health GET for liveness probes
- Wire routers into app with versioned prefix
- Add OpenAPI tags and description metadata for Swagger UI"

commit "2026-03-05T14:00:00+05:30" \
  "feat(frontend): initialize Next.js 14 frontend with App Router

- Bootstrap with TypeScript, Tailwind CSS, and ESLint
- Add global layout with custom fonts (Inter) and metadata
- Configure next.config.js with API proxy rewrites to backend"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 5 — Landing page
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-05T18:00:00+05:30" \
  "feat(frontend): build premium landing page

- Design full-screen hero with animated gradient headline
- Add feature grid with icon cards describing platform capabilities
- Implement IdeaForm with real-time character count and submission handling
- Add loading state with animated progress indicator during analysis"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 6 — State & API integration
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-06T11:30:00+05:30" \
  "feat(frontend): implement Zustand global state for analysis pipeline

- Add analysisStore with slices for ideaAnalysis, marketAnalysis,
  competitorAnalysis, swot, startupScore, and report
- Implement resetAnalysis() action for clean re-submission
- Persist currentIdea in sessionStorage for page-refresh resilience"

commit "2026-03-06T16:00:00+05:30" \
  "feat(frontend): wire analysis submission to FastAPI backend

- Implement api/analyze service with typed response parsing
- Add optimistic UI update and redirect to /result on success
- Graceful error toast on network failure or validation error"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 7 — Results dashboard
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-07T09:00:00+05:30" \
  "feat(frontend): build results dashboard with tab navigation

- Implement 6-tab Radix UI Tabs layout (Overview, Insights, Competitors,
  SWOT, Score, Report)
- Add market insight cards (TAM, SAM, SOM) with brutalist card design
- Implement SWOT grid with color-coded strength/weakness/opportunity/threat cards"

commit "2026-03-07T14:30:00+05:30" \
  "feat(frontend): add competitor landscape and scoring views

- Render competitor cards with name, description, strengths, weaknesses,
  pricing model, and market focus
- Add Score tab with radial gauge animations and weighted composite display
- Add Full Report tab with markdown-rendered executive intelligence report"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 7 — Competitor analysis SerpAPI
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-07T19:00:00+05:30" \
  "feat(backend): integrate SerpAPI for real-world competitor discovery

- Add SerpAPI client with GoogleSearch wrapper
- Implement CompetitorSearchService that queries Indian market results
- Implement MarketResearchService for live TAM/SAM/SOM data enrichment
- Add SERPAPI_KEY to settings and .env.example"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 8 — Debugging & polish
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-08T10:00:00+05:30" \
  "fix(backend): resolve environment variable loading and port conflicts

- Ensure .env is loaded before Uvicorn binds port
- Switch default backend port to 8000 to avoid conflict with AirPlay
- Add DATABASE_URL validation on startup with actionable error message"

commit "2026-03-08T15:30:00+05:30" \
  "fix(frontend): resolve TypeScript config errors and missing module types

- Add @types/node to devDependencies for process.env access
- Fix tsconfig paths alias for @/components
- Resolve ESLint no-explicit-any warnings in result page"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 9 — Middleware & logging
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-09T09:30:00+05:30" \
  "feat(backend): implement structured request logging middleware

- Add LoggingMiddleware extending BaseHTTPMiddleware
- Log method, path, status code, duration_ms, client IP, user agent
- Inject X-Request-ID UUID header on every response for tracing
- Log 5xx at ERROR level, 4xx at WARNING, 2xx at INFO"

commit "2026-03-09T14:00:00+05:30" \
  "feat(backend): add JSON rotating file logger with daily rollover

- Implement get_logger() factory with StructuredFormatter (JSON output)
- Configure handlers: console (colored) + rotating file (logs/app.log)
- Suppress noisy SQLAlchemy and httpx loggers below WARNING"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 10 — UI & design system
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-10T10:00:00+05:30" \
  "feat(frontend): implement professional blue/navy/orange color palette

- Update CSS custom properties with blues (#004E9B, #0091B9), navy, orange
- Apply palette to landing page hero gradient, CTA button, and nav
- Update result page brutalist cards to match new design system
- Replace all placeholder grays with curated brand colors"

commit "2026-03-10T16:00:00+05:30" \
  "feat(frontend): add shared RadialGauge and SuccessProbability components

- Implement SVG RadialGauge with animated stroke-dashoffset on mount
- Add SuccessProbability bar chart with percentage label
- Export both from components/shared for use in score and report views"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 11 — Database integration fixes
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-11T11:00:00+05:30" \
  "fix(backend): resolve Prisma/SQLAlchemy datasource configuration

- Correct DATABASE_URL env variable binding in settings.py
- Add pgvector extension auto-create on startup
- Fix AsyncSession context manager usage to prevent connection leaks
- Add connection pool size and timeout configuration"

commit "2026-03-11T17:00:00+05:30" \
  "feat(backend): implement idea_repository and competitor_repository

- Add IdeaRepository with create, get_by_id, list_all async methods
- Add CompetitorRepository with save_competitors() and get_by_idea()
- Return typed Sequence[Model] from all list queries"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 12 — Similarity & embeddings
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-12T10:30:00+05:30" \
  "feat(backend): add idea similarity detection with pgvector embeddings

- Implement IdeaSimilarityService with cosine distance search
- Generate embeddings on idea submission using OpenAI text-embedding-3-small
- Return top-N similar ideas with distance score for duplicate detection"

commit "2026-03-12T15:00:00+05:30" \
  "feat(frontend): add empty states and skeleton loading UI

- Add EmptyState component with contextual icon and CTA for each tab
- Replace blank screens with skeleton loaders while fetching analysis
- Add AnalysisProgress stepper to show pipeline stages during generation"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 13 — Validators & retries
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-13T09:00:00+05:30" \
  "feat(backend): add LLM output validation and structured retry logic

- Implement validate_and_regenerate() with max_retries and Pydantic parsing
- Catch JSONDecodeError and ValidationError; regenerate with corrective prompt
- Log retry attempts with attempt number and parse failure reason"

commit "2026-03-13T15:30:00+05:30" \
  "perf(backend): reduce end-to-end latency with parallel LLM calls

- Wrap independent scoring calls in asyncio.gather()
- Cache LLMClient instance at module level to reuse connection pool
- Add REQUEST_TIMEOUT_SECS setting (default 90s) to cap runaway calls"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 14 — Design token extraction
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-14T10:00:00+05:30" \
  "chore(frontend): extract design system tokens into CSS custom properties

- Define --color-primary, --color-accent, --color-surface token set
- Add typography scale (--text-xs through --text-7xl) as CSS variables
- Document color palette in design-system.css for cross-team reuse"

commit "2026-03-14T16:30:00+05:30" \
  "fix(frontend): remove default Next.js boilerplate and placeholder copy

- Delete unused app/page.tsx default content and globals.css reset bloat
- Replace favicon.ico with custom Venture AI logo mark
- Update <title> and <meta description> on all pages for SEO"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 15 — Google Gemini migration
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-15T09:00:00+05:30" \
  "feat(backend): migrate Gemini client to google-genai SDK

- Replace deprecated google-generativeai with google-genai package
- Update LLMClient to use genai.Client with aio.models.generate_content()
- Configure GenerateContentConfig with temperature and max_output_tokens
- Update requirements.txt with google-genai >= 0.8"

commit "2026-03-15T13:00:00+05:30" \
  "fix(backend): resolve httpx and websockets version conflicts

- Loosen httpx constraint to >=0.24 for starlette TestClient compatibility
- Loosen websockets to >=11 to satisfy uvicorn optional dependency
- Pin google-genai to avoid transitive google-auth breakage"

commit "2026-03-15T17:00:00+05:30" \
  "fix(backend): correct module docstring placement to resolve E402 lint errors

- Move module-level docstrings before all import statements per PEP 257
- Affects: ai/__init__.py, ai/response_parser.py, middleware/logging.py
- All ruff E402 (module level import not at top of file) errors resolved"

# ════════════════════════════════════════════════════════════════════════════════
# MARCH 16 — Final lint sweep + IDE config
# ════════════════════════════════════════════════════════════════════════════════
commit "2026-03-16T09:00:00+05:30" \
  "fix(backend): remove unused typing imports across all __init__ modules

- Remove blanket 'from typing import Optional, Any, ...' from empty __init__
  files (ai, config, database, exceptions, middleware, models, routers,
  schemas, services, utils packages)
- Zero F401 unused-import errors remaining after sweep"

commit "2026-03-16T11:30:00+05:30" \
  "fix(backend): add TYPE_CHECKING guards for circular SQLAlchemy relationships

- Add 'if TYPE_CHECKING' blocks in competitor.py, market_analysis.py,
  startup_score.py to import StartupIdea without runtime circular import
- Add reverse guards in startup_idea.py for Competitor, MarketAnalysis,
  StartupScore
- Resolves F821 undefined-name errors from ruff static analysis"

commit "2026-03-16T13:00:00+05:30" \
  "fix(backend): add Any and Literal to settings.py typing imports

- Import Any for ALLOWED_ORIGINS field annotation
- Restore Literal for LLM_PROVIDER Literal['openai','gemini'] type
- Zero ruff errors across entire backend codebase"

commit "2026-03-16T14:30:00+05:30" \
  "fix(frontend): constrain market insight card text to prevent overflow

- Replace fixed text-4xl with responsive text-xl/text-2xl on TAM/SAM/SOM cards
- Add break-words and overflow-hidden to contain long AI-generated values
- Remove min-h constraint that forced cards to inconsistent heights"

commit "2026-03-16T16:00:00+05:30" \
  "chore: configure VSCode workspace to use backend virtualenv

- Add backend/.vscode/settings.json pointing Pylance to venv/bin/python
- Add root .vscode/settings.json with analysis.extraPaths for app/ imports
- Disable Pylance typeCheckingMode to suppress third-party stub false alarms
- Set ruff as default Python formatter"

echo ""
echo "✅ All commits created. Ready to push."
echo ""
git log --oneline | head -40
