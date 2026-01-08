from typing import Dict, Any
from .base import BaseConnector, ExecutionResult
from .git import GitConnector
from .database import DatabaseConnector
from .warehouse import WarehouseConnector
from app.core.config import get_settings

class ConnectorRegistry:
    def __init__(self) -> None:
        self._connectors: Dict[str, BaseConnector] = {}
        self._initialized = False

    def initialize(self) -> None:
        if self._initialized:
            return
        settings = get_settings()
        if settings.enable_git_connector:
            self.register(GitConnector("git"))
        if settings.enable_database_connector:
            self.register(DatabaseConnector("database"))
        
        # Always register warehouse for now (or add a setting later)
        self.register(WarehouseConnector("warehouse"))
            
        self._initialized = True

    def register(self, connector: BaseConnector) -> None:
        self._connectors[connector.name] = connector

    def list_names(self):
        return list(self._connectors.keys())

    def execute(self, name: str, payload: Dict[str, Any]) -> ExecutionResult:
        if name not in self._connectors:
            raise ValueError(f"Connector '{name}' not found")
        return self._connectors[name].execute(payload)

_registry = ConnectorRegistry()

def get_registry() -> ConnectorRegistry:
    _registry.initialize()
    return _registry
