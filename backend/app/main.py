from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.api.questions import router as questions_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Research Assistant API",
    description="Backend API for the AI Research Assistant",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(documents_router)
app.include_router(questions_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}