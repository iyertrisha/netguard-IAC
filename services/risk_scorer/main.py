import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from .schemas import ScoreRequest, ScoreResponse, Severity
from .rules.rules import run_all_rules
from .llm.client import enrich_finding

load_dotenv()

app = FastAPI(
    title="NetGuard Risk Scorer Service",
    description="Scores security findings using rule-based checks augmented by AI explanations",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "risk_scorer"}


@app.post("/score", response_model=ScoreResponse)
async def score_resources(request: ScoreRequest):
    """
    Main endpoint — receives a list of resources (from the parser)
    and an optional graph context (from the graph engine).
    Returns all security findings with severity + AI explanations.
    """
    if not request.resources:
        raise HTTPException(status_code=400, detail="No resources provided.")

    all_findings = []

    for resource in request.resources:
        # Layer 1: run all 11 deterministic rules
        findings = run_all_rules(resource)

        # Layer 2: enrich each finding with LLM explanation
        for finding in findings:
            finding = enrich_finding(finding, resource, request.graph_context)
            all_findings.append(finding)

    # Build summary counts
    return ScoreResponse(
        findings=all_findings,
        total=len(all_findings),
        critical_count=sum(1 for f in all_findings if f.severity == Severity.CRITICAL),
        high_count=sum(1 for f in all_findings if f.severity == Severity.HIGH),
        medium_count=sum(1 for f in all_findings if f.severity == Severity.MEDIUM),
        low_count=sum(1 for f in all_findings if f.severity == Severity.LOW),
    )