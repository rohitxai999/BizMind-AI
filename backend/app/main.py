from fastapi import FastAPI
from app.routes.analysis import router as analysis_router
from app.routes.upload import router as upload_router

app = FastAPI(
    title="BizMind AI",
    version="1.0.0",
    description="AI-Powered Business Intelligence Platform"
)

app.include_router(analysis_router)
app.include_router(upload_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to BizMind AI",
        "status": "Running"
    }