from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger

from app.routes.analysis import router as analysis_router
from app.routes.upload import router as upload_router
from app.routes.dashboard import router as dashboard_router
from app.api.dashboard import router as executive_dashboard_router
from app.api.v1.router import api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Autonomous Business Intelligence & Decision Support Platform",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Versioned API Router (Day 15)
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

# Backward Compatibility - Legacy Top-Level Routes
app.include_router(analysis_router)
app.include_router(upload_router)
app.include_router(dashboard_router)
app.include_router(executive_dashboard_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to BizMind AI",
        "status": "Running",
        "version": settings.VERSION,
        "api_v1": f"{settings.API_V1_STR}/health",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }