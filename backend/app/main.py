from fastapi import FastAPI

app = FastAPI(
    title="Team Pillbox API",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Team Pillbox API"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
