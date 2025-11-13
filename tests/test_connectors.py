import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_list_connectors():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/connectors")
    assert resp.status_code == 200
    data = resp.json()
    assert "connectors" in data
    assert isinstance(data["connectors"], list)

@pytest.mark.asyncio
async def test_execute_git_connector(tmp_path):
    # create dummy repo directories
    (tmp_path / "repo1").mkdir()
    (tmp_path / "repo2").mkdir()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(f"/api/connectors/git/execute", json={"payload": {"root": str(tmp_path)}})
    assert resp.status_code == 200
    result = resp.json()["result"]
    assert set(result["repositories"]) == {"repo1", "repo2"}
