# MCP Server

Standard MCP server implementation using FastMCP, demonstrating a connector framework (git, database placeholder).

## Features
- MCP Tools:
  - `list_git_repos`: List available git repositories.
  - `query_database`: Execute a database query.
- Environment-driven enable/disable of connectors

## Quick Start
```bash
python -m pip install -e .[dev]
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
docker build -t mcp-server:latest .
docker run -p 8000:8000 mcp-server:latest
```

## Client Example
See `examples/client.py` for how to connect to the server using the Python MCP SDK.

## Connectors
Each connector implements `execute(payload)` returning a JSON-serializable result. Add new connectors under `app/connectors/` and register them in `registry.py` based on settings.
