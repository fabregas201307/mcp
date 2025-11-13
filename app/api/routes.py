from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from app.connectors.registry import get_registry

router = APIRouter(prefix="/api")

class ExecuteRequest(BaseModel):
    payload: Dict[str, Any] = {}

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/connectors")
def list_connectors():
    registry = get_registry()
    return {"connectors": registry.list_names()}

@router.post("/connectors/{name}/execute")
def execute_connector(name: str, req: ExecuteRequest):
    registry = get_registry()
    try:
        result = registry.execute(name, req.payload)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
