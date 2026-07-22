from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="BizMind AI",
    description="AI Business Intelligence Assistant",
    version="1.0"
)


app.include_router(router)


@app.get("/")
def home():

    return {
        "message": "BizMind AI Backend Running 🚀"
    }