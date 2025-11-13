# MCP API

Minimal FastAPI-based MCP service demonstrating a connector framework (git, database placeholder) with execution endpoint and health checks.

## Features
- Health endpoint `/api/health`
- List connectors `/api/connectors`
- Execute connector `/api/connectors/{name}/execute`
- Environment-driven enable/disable of connectors

## Quick Start
```bash
python -m pip install -e .[dev]
pytest -q
uvicorn app.main:app --reload
```

## Environment Variables
- `MCP_ENV` (default: development)
- `MCP_ENABLE_GIT` (default: true)
- `MCP_ENABLE_DB` (default: false)
- `MCP_GIT_ROOT` (default: /tmp/repos)
- `MCP_DATABASE_URL` (default: sqlite:///./mcp.db)

## Docker
```bash
docker build -t mcp-api:latest .
docker run -p 8000:8000 mcp-api:latest
```

## Connectors
Each connector implements `execute(payload)` returning a JSON-serializable result. Add new connectors under `app/connectors/` and register them in `registry.py` based on settings.
