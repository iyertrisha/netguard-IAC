from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ── What we receive FROM the parser (Vinay's schema) ──────────────────────────

class Rule(BaseModel):
    port: Any          # string from Vinay ("22"), we normalise to int internally
    protocol: str
    cidr: str


class Resource(BaseModel):
    resource_id: str
    resource_type: str
    provider: str
    properties: Dict = {}
    inbound_rules: List[Rule] = []
    outbound_rules: List[Rule] = []
    tags: Dict = {}


# ── What we receive FROM the graph engine (Vineet's schema) ───────────────────

class GraphContext(BaseModel):
    nodes: List[Dict] = []
    edges: List[Dict] = []
    newly_exposed: List[str] = []
    exposure_delta: int = 0


# ── The request body for POST /score ──────────────────────────────────────────

class ScoreRequest(BaseModel):
    resources: List[Resource]
    graph_context: Optional[GraphContext] = None


# ── A single finding your service produces ────────────────────────────────────

class Finding(BaseModel):
    resource_id: str
    resource_type: str
    finding_type: str
    severity: Severity
    explanation: str
    remediation: str
    confidence_score: float = 1.0
    is_new: bool = False


# ── The response body for POST /score ─────────────────────────────────────────

class ScoreResponse(BaseModel):
    findings: List[Finding]
    total: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int