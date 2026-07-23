from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analysis import router as analysis_router


app = FastAPI(
    title="BizMind AI",
    version="1.0.0",
    description="Autonomous Multi-Agent Business Intelligence Platform"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(analysis_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to BizMind AI API",
        "status": "running",
        "version": "1.0.0"
    }