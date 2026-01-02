import os
from typing import Dict, Any
from .base import BaseConnector, ExecutionResult

class GitConnector(BaseConnector):
    def execute(self, payload: Dict[str, Any]) -> ExecutionResult:
        root = payload.get("root") or os.getenv("MCP_GIT_ROOT") or "/tmp/repos"
        action = payload.get("action", "list")

        if action == "list":
            repos = []
            if os.path.isdir(root):
                for entry in os.listdir(root):
                    full = os.path.join(root, entry)
                    if os.path.isdir(full):
                        repos.append(entry)
            return ExecutionResult({"connector": self.name, "root": root, "repositories": repos})
        
        elif action == "search":
            keyword = payload.get("keyword")
            if not keyword:
                raise ValueError("Keyword is required for search")
            
            results = []
            if os.path.isdir(root):
                for dirpath, dirnames, filenames in os.walk(root):
                    # Skip .git directories
                    if ".git" in dirnames:
                        dirnames.remove(".git")
                    
                    for filename in filenames:
                        # Only search python files for now as requested
                        if not filename.endswith(".py"):
                            continue
                            
                        full_path = os.path.join(dirpath, filename)
                        try:
                            with open(full_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                
                            # Search in filename or content
                            if keyword.lower() in filename.lower() or keyword.lower() in content.lower():
                                rel_path = os.path.relpath(full_path, root)
                                results.append({
                                    "path": rel_path,
                                    "content": content
                                })
                        except Exception:
                            # Skip files that can't be read
                            continue
                            
            return ExecutionResult({"connector": self.name, "results": results})

        else:
            raise ValueError(f"Unknown action: {action}")
