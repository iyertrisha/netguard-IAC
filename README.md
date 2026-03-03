# NetGuard IaC Analyzer

**Team 18** — Automated Network Security Analysis and Risk Scoring for Infrastructure-as-Code Pipelines

NetGuard scans Terraform and Kubernetes configurations during pull requests, builds network topology graphs, performs PR-level graph diffing, and scores security risk using AI. Critical findings hard-block PRs from merging.

---

## Architecture

| Service | Port | Description |
|---|---|---|
| Backend API | 8000 | Orchestrates all services, persists data, serves the frontend |
| Parser Service | 8001 | Parses `.tf` and `.yaml` IaC files into normalized resources |
| Graph Engine Service | 8002 | Builds topology graphs and performs PR-level graph diffing |
| Risk Scorer Service | 8003 | Rule-based + AI scoring of security findings |
| Frontend | 5173 | React + Vite dashboard with D3.js graph visualization |
| PostgreSQL | 5432 | Persistent storage for scans, graphs, and findings |

---

## Prerequisites

- Python 3.12+
- Node.js 18+ and npm
- Docker Desktop

---

## Local Development Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd mini-project
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Python virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate       # macOS / Linux
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 4. Run a service locally

```bash
# From the project root, with venv activated:
uvicorn services.api.main:app --port 8000 --reload
uvicorn services.parser.main:app --port 8001 --reload
uvicorn services.graph_engine.main:app --port 8002 --reload
uvicorn services.risk_scorer.main:app --port 8003 --reload
```

Verify any service is running:
```bash
curl http://localhost:8000/health
# {"status":"ok","service":"api"}
```

### 5. Run the frontend

```bash
cd frontend
npm run dev
# Open http://localhost:5173
```

---

## Docker Compose (Full Stack)

```bash
# Copy and fill in your .env
cp .env.example .env

# Build and start all 6 containers
docker-compose up --build

# Stop everything
docker-compose down
```

Services will be available at the same ports listed in the Architecture table above.

---

## Running Tests

```bash
source venv/bin/activate
pytest
```

---

## Project Structure

```
mini-project/
├── .github/workflows/netguard.yml   # GitHub Action — triggers on PR
├── services/
│   ├── api/                         # Backend API (FastAPI, port 8000)
│   ├── parser/                      # Parser Service (FastAPI, port 8001)
│   ├── graph_engine/                # Graph Engine Service (FastAPI, port 8002)
│   └── risk_scorer/                 # Risk Scorer Service (FastAPI, port 8003)
├── frontend/                        # React + Vite + D3.js (port 5173)
├── docker/                          # Dockerfiles for each service
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Implementation Phases

| Phase | Description | Status |
|---|---|---|
| 0 | Project structure, venv, Docker skeleton | Done |
| 1 | AWS + Kubernetes parsers, graph construction | Pending |
| 2 | Risk scoring engine + AI integration | Pending |
| 3 | Backend API orchestration + PostgreSQL | Pending |
| 4 | Frontend dashboard | Pending |
| 5 | GitHub Action CI gate | Pending |
| 6 | Benchmarking and demo polish | Pending |
