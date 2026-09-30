from fastapi import FastAPI

from app.api.documents import router as documents_router


app = FastAPI(
    title="AI Research Assistant API",
    description="Backend API for the AI Research Assistant",
    version="0.1.0",
)

app.include_router(documents_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}