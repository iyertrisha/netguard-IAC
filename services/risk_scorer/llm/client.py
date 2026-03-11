"""
LLM client for enriching findings with AI explanations.
Currently MOCKED — returns realistic placeholder responses.
When LLM_API_KEY is set, this will call GPT-4o instead.
"""
import os
from typing import Optional
from ..schemas import Finding, Resource, GraphContext


def enrich_finding(
    finding: Finding,
    resource: Resource,
    graph_context: Optional[GraphContext] = None,
) -> Finding:
    """
    Enriches a rule-based finding with an AI explanation.
    - If LLM_API_KEY is set: calls GPT-4o (Phase 2 full implementation)
    - If not set: returns a mock enrichment so the pipeline works now
    """
    api_key = os.getenv("LLM_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        return _mock_enrich(finding, graph_context)

    # Real LLM call — will implement when API key is available
    return _mock_enrich(finding, graph_context)


def _mock_enrich(
    finding: Finding,
    graph_context: Optional[GraphContext] = None,
) -> Finding:
    """
    Returns a mock-enriched finding.
    Keeps existing explanation/remediation from the rule,
    and adds a mock confidence score.
    """
    newly_exposed = []
    if graph_context:
        newly_exposed = graph_context.newly_exposed

    is_new = finding.resource_id in newly_exposed

    # Return a new Finding with is_new set from graph context
    return Finding(
        resource_id=finding.resource_id,
        resource_type=finding.resource_type,
        finding_type=finding.finding_type,
        severity=finding.severity,
        explanation=finding.explanation + " [AI enrichment pending — LLM_API_KEY not set]",
        remediation=finding.remediation,
        confidence_score=0.90,
        is_new=is_new,
    )