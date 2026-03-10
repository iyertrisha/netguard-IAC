import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from services.graph_engine.models import (
    GraphBuildRequest,
    GraphBuildResponse,
    GraphDiffRequest,
    GraphDiffResponse,
)
from services.graph_engine.builder import build_graph
from services.graph_engine.differ import diff_graphs
from services.graph_engine.serializer import serialize_graph
from services.database.database import get_db, Base, engine
from services.database.models import Graph

load_dotenv()

# Create tables on startup (simple approach, replace with Alembic later)
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass  # DB may not be available in test/dev without Docker

app = FastAPI(
    title="NetGuard Graph Engine Service",
    description="Builds network topology graphs from normalized resources and performs PR-level graph diffing",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "graph_engine"}


@app.post("/graph/build", response_model=GraphBuildResponse)
def graph_build(request: GraphBuildRequest):
    """
    Build a directed network topology graph from a list of resources.

    Accepts normalized resources, returns D3-compatible JSON with
    nodes, edges, and metadata.
    """
    graph = build_graph(request.resources)
    return serialize_graph(graph)


@app.post("/graph/diff", response_model=GraphDiffResponse)
def graph_diff(request: GraphDiffRequest):
    """
    Compare two resource sets (base vs head) and return what changed.

    Builds a graph for each, diffs them, and returns added/removed
    nodes and edges.
    """
    base_graph = build_graph(request.base)
    head_graph = build_graph(request.head)
    return diff_graphs(base_graph, head_graph)


@app.post("/graph/store")
def graph_store(request: GraphBuildRequest, scan_id: int = 1, graph_type: str = "base", db: Session = Depends(get_db)):
    """
    Build a graph and persist it to the database as JSONB.
    """
    graph = build_graph(request.resources)
    data = serialize_graph(graph)

    db_graph = Graph(
        scan_id=scan_id,
        graph_type=graph_type,
        graph_data=data,
    )
    db.add(db_graph)
    db.commit()
    db.refresh(db_graph)

    return {"graph_id": db_graph.id, "graph_type": db_graph.graph_type, **data}


@app.get("/graph/{graph_id}")
def graph_get(graph_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a stored graph by ID.
    """
    db_graph = db.query(Graph).filter(Graph.id == graph_id).first()
    if not db_graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return {
        "graph_id": db_graph.id,
        "graph_type": db_graph.graph_type,
        "created_at": str(db_graph.created_at),
        **db_graph.graph_data,
    }
