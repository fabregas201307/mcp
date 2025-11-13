from abc import ABC, abstractmethod
from typing import Any, Dict

class ExecutionResult(Dict[str, Any]):
    pass

class BaseConnector(ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> ExecutionResult:
        """Execute a connector-specific action."""
        raise NotImplementedError
