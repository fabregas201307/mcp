import os
from typing import Dict, Any
from .base import BaseConnector, ExecutionResult

class GitConnector(BaseConnector):
    def execute(self, payload: Dict[str, Any]) -> ExecutionResult:
        root = payload.get("root") or os.getenv("MCP_GIT_ROOT") or "/tmp/repos"
        repos = []
        if os.path.isdir(root):
            for entry in os.listdir(root):
                full = os.path.join(root, entry)
                if os.path.isdir(full):
                    repos.append(entry)
        return ExecutionResult({"connector": self.name, "root": root, "repositories": repos})
