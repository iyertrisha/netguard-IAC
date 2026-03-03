import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="NetGuard Graph Engine Service",
    description="Builds network topology graphs from normalized resources and performs PR-level graph diffing",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "graph_engine"}
