import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="NetGuard API",
    description="Backend API — orchestrates Parser, Graph Engine, and Risk Scorer services",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "api"}
