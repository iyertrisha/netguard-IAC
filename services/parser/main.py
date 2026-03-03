import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="NetGuard Parser Service",
    description="Parses Terraform (.tf) and Kubernetes (.yaml) IaC files into a normalized resource representation",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "parser"}
