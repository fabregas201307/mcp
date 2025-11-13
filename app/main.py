from fastapi import FastAPI
from app.api.routes import router
from app.core.config import get_settings

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="MCP API", version="0.1.0", docs_url="/docs")
    app.include_router(router)

    @app.get("/")
    def root():
        return {"service": "mcp", "environment": settings.environment}

    return app

app = create_app()
