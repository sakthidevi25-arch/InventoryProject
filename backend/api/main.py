from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from backend.api.routes.api_routes import router as api_router
from backend.api.routes.asset_routes import router as asset_router
from backend.api.routes.auth_routes import router as auth_router
from backend.api.routes.dashboard_routes import router as dashboard_router
from backend.core.config import settings
from backend.core.logging_config import logger
from backend.database.init_db import init_db
from backend.seed_data import seed_data

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Secure Cloud Asset & API Inventory Management Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(asset_router)
app.include_router(api_router)
app.include_router(dashboard_router)

@app.on_event("startup")
def startup_event():
    logger.info("Application starting...")
    init_db()
    seed_data()


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
