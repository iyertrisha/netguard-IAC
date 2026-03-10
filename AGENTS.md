## NetGuard Project Context
- Python 3.12, FastAPI microservices architecture
- All services live under services/ (api, parser, graph_engine, risk_scorer)
- Mohit owns services/risk_scorer/ (port 8003)
- Always run `pytest` after any change
- Use `httpx` for async HTTP calls between services
- All severity rules are deterministic first, LLM adjusts ±1
- LLM output must be JSON-mode structured
- Never hardcode API keys — use environment variables via python-dotenv
- Normalized resource JSON schema is owned by the parser service