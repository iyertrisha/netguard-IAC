"""
LLM client for enriching findings with AI explanations.
- If LLM_API_KEY is set: calls GPT-4o with structured JSON output
- If not set: returns mock enrichment so pipeline works without a key
"""
import os
import json
import logging
from typing import Optional
from ..schemas import Finding, Resource, GraphContext, Severity
from .prompt_builder import build_finding_prompt

logger = logging.getLogger(__name__)

# Severity ladder for Â±1 confidence adjustments
_SEVERITY_LADDER = [Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]


def enrich_finding(
    finding: Finding,
    resource: Resource,
    graph_context: Optional[GraphContext] = None,
) -> Finding:
    """
    Enriches a rule-based finding with AI explanation.
    Automatically falls back to mock if no API key is set.
    """
    api_key = os.getenv("LLM_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        return _mock_enrich(finding, resource, graph_context)

    try:
        return _llm_enrich(finding, resource, graph_context, api_key)
    except Exception as e:
        logger.warning(f"LLM call failed for {finding.finding_type}: {e}. Falling back to mock.")
        return _mock_enrich(finding, resource, graph_context)


def _llm_enrich(
    finding: Finding,
    resource: Resource,
    graph_context: Optional[GraphContext],
    api_key: str,
) -> Finding:
    """Real GPT-4o call â€” only runs when LLM_API_KEY is set."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    prompt = build_finding_prompt(finding, resource, graph_context)

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user",   "content": prompt["user"]},
        ],
        max_tokens=600,
        temperature=0.2,
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    # Apply Â±1 severity adjustment
    adjusted_severity = _adjust_severity(
        finding.severity,
        data.get("confidence_adjustment", 0)
    )

    # is_new from graph context
    is_new = (
        resource.resource_id in graph_context.newly_exposed
        if graph_context else False
    )

    return Finding(
        resource_id=finding.resource_id,
        resource_type=finding.resource_type,
        finding_type=finding.finding_type,
        severity=adjusted_severity,
        explanation=data.get("explanation", finding.explanation),
        remediation=data.get("remediation", finding.remediation),
        confidence_score=_adjustment_to_confidence(data.get("confidence_adjustment", 0)),
        is_new=is_new,
    )


def _mock_enrich(
    finding: Finding,
    resource: Resource,
    graph_context: Optional[GraphContext] = None,
) -> Finding:
    """Mock enrichment â€” realistic placeholder when no API key is available."""
    is_new = (
        resource.resource_id in graph_context.newly_exposed
        if graph_context else False
    )
    return Finding(
        resource_id=finding.resource_id,
        resource_type=finding.resource_type,
        finding_type=finding.finding_type,
        severity=finding.severity,
        explanation=finding.explanation + " [AI enrichment pending â€” LLM_API_KEY not set]",
        remediation=finding.remediation,
        confidence_score=0.90,
        is_new=is_new,
    )


def _adjust_severity(current: Severity, adjustment: int) -> Severity:
    """Shifts severity up or down by 1 step. Never goes above CRITICAL or below LOW."""
    if adjustment == 0:
        return current
    idx = _SEVERITY_LADDER.index(current)
    new_idx = max(0, min(len(_SEVERITY_LADDER) - 1, idx + adjustment))
    return _SEVERITY_LADDER[new_idx]


def _adjustment_to_confidence(adjustment: int) -> float:
    """Converts adjustment to a confidence score."""
    return {-1: 0.60, 0: 0.90, 1: 0.95}.get(adjustment, 0.90)
