import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="NetGuard Risk Scorer Service",
    description="Scores security findings using rule-based checks augmented by AI API calls for contextual explanations",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "risk_scorer"}
