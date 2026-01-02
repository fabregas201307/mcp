import pytest
from app.connectors.registry import get_registry

def test_list_connectors():
    registry = get_registry()
    names = registry.list_names()
    assert isinstance(names, list)

def test_execute_git_connector(tmp_path):
    # create dummy repo directories
    (tmp_path / "repo1").mkdir()
    (tmp_path / "repo2").mkdir()
    
    registry = get_registry()
    # Ensure git connector is registered (it depends on settings)
    
    result = registry.execute("git", {"action": "list", "root": str(tmp_path)})
    assert set(result["repositories"]) == {"repo1", "repo2"}

def test_search_git_connector(tmp_path):
    # create dummy repo and file
    repo = tmp_path / "repo1"
    repo.mkdir()
    
    # File with keyword in content
    f1 = repo / "test_match.py"
    f1.write_text("def my_function():\n    pass", encoding="utf-8")
    
    # File with keyword in name
    f2 = repo / "function_helper.py"
    f2.write_text("x = 1", encoding="utf-8")
    
    # File with no match
    f3 = repo / "other.py"
    f3.write_text("x = 1", encoding="utf-8")
    
    registry = get_registry()
    
    # Search for "function"
    result = registry.execute("git", {"action": "search", "keyword": "function", "root": str(tmp_path)})
    
    paths = [r["path"] for r in result["results"]]
    assert "repo1/test_match.py" in paths
    assert "repo1/function_helper.py" in paths
    assert "repo1/other.py" not in paths
    
    # Verify content is returned
    for r in result["results"]:
        assert "content" in r
        assert isinstance(r["content"], str)
