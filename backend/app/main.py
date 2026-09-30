from fastapi import FastAPI

app = FastAPI(
    title="AI Research Assistant API",
    descriptiono="Backend API for the AI Research Assistant",
    version="0.1.0",

)

@app.get("/health")
def health_check():
    return {"status": "healthy"}