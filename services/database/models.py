"""
SQLAlchemy ORM models for the NetGuard database.

4 tables:
  - repositories: GitHub repos being analyzed
  - scans:        individual PR scan runs
  - graphs:       serialized graph snapshots (JSONB)
  - findings:     security findings from risk scoring
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship

from services.database.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Repository(Base):
    """A GitHub repository being monitored by NetGuard."""
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    url = Column(String(512), nullable=False)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    # Relationships
    scans = relationship("Scan", back_populates="repository", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Repository(id={self.id}, name='{self.name}')>"


class Scan(Base):
    """A single PR scan run against a repository."""
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    pr_number = Column(Integer, nullable=True)
    commit_sha = Column(String(40), nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    # Relationships
    repository = relationship("Repository", back_populates="scans")
    graphs = relationship("Graph", back_populates="scan", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="scan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scan(id={self.id}, pr={self.pr_number}, status='{self.status}')>"


class Graph(Base):
    """A serialized graph snapshot stored as JSONB."""
    __tablename__ = "graphs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    graph_type = Column(String(20), nullable=False)  # "base" or "head"
    graph_data = Column(JSON, nullable=False)  # Full D3-compatible JSON
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    # Relationships
    scan = relationship("Scan", back_populates="graphs")

    def __repr__(self):
        return f"<Graph(id={self.id}, type='{self.graph_type}')>"


class Finding(Base):
    """A security finding produced by the risk scorer."""
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    finding_type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)  # "critical", "high", "medium", "low"
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    # Relationships
    scan = relationship("Scan", back_populates="findings")

    def __repr__(self):
        return f"<Finding(id={self.id}, type='{self.finding_type}', severity='{self.severity}')>"
