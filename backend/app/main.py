from fastapi import FastAPI

from app.routes.analysis import router as analysis_router
from app.routes.upload import router as upload_router
from app.routes.dashboard import router as dashboard_router

app = FastAPI(
    title="BizMind AI",
    version="1.0.0",
    description="AI-Powered Business Intelligence Platform"
)

app.include_router(analysis_router)
app.include_router(upload_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to BizMind AI",
        "status": "Running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "BizMind AI Backend"
    }