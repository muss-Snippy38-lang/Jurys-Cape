import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.services.swarm_orchestrator import swarm_orchestrator

client = TestClient(app)

def test_register_node():
    response = client.post("/api/v1/swarm/register", json={"role": "librarian", "url": "https://ngrok-url.com"})
    assert response.status_code == 200
    assert response.json()["url"] == "https://ngrok-url.com"
    
    # Check internal state
    node = swarm_orchestrator.get_node("librarian")
    assert node is not None
    assert node.url == "https://ngrok-url.com"

@pytest.mark.asyncio
async def test_dispatch_task_success():
    # Register node first
    swarm_orchestrator.register_node("librarian", "https://ngrok-url.com")
    
    # Mock httpx
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "ok"}
        
        result = await swarm_orchestrator.dispatch_task("librarian", "/ocr", {"file": "test.pdf"})
        assert result == {"status": "ok"}
        
        # Verify Headers
        call_kwargs = mock_post.call_args.kwargs
        assert "X-Swarm-Secret" in call_kwargs["headers"]

def test_dispatch_endpoint():
    # Register node
    client.post("/api/v1/swarm/register", json={"role": "judge", "url": "https://judge-url.com"})
    
    with patch("app.services.swarm_orchestrator.SwarmOrchestrator.dispatch_task", new_callable=AsyncMock) as mock_dispatch:
        mock_dispatch.return_value = {"verdict": "guilty"}
        
        response = client.post("/api/v1/swarm/dispatch/judge", params={"task_endpoint": "/adjudicate"}, json={"facts": []})
        assert response.status_code == 200
        assert response.json() == {"verdict": "guilty"}
