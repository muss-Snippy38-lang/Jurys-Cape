import httpx
import logging
import json
from pathlib import Path
from typing import Dict, Optional, Any
from pydantic import BaseModel
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SwarmOrchestrator")

NODES_FILE = Path("data/nodes.json")
NODES_FILE.parent.mkdir(exist_ok=True, parents=True)

class NodeInfo(BaseModel):
    role: str  # 'librarian', 'investigator', 'judge'
    url: str   # The NGROK public URL
    status: str = "active"

class SwarmOrchestrator:
    _nodes: Dict[str, NodeInfo] = {}

    def __init__(self):
        self._load_nodes()

    def _load_nodes(self):
        """Loads nodes from disk to survive restarts."""
        if NODES_FILE.exists():
            try:
                data = json.loads(NODES_FILE.read_text())
                for role, info in data.items():
                    self._nodes[role] = NodeInfo(**info)
                logger.info(f"Loaded {len(self._nodes)} nodes from persisted storage.")
            except Exception as e:
                logger.error(f"Failed to load nodes: {e}")

    def _save_nodes(self):
        """Persists nodes to disk."""
        try:
            data = {role: node.dict() for role, node in self._nodes.items()}
            NODES_FILE.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logger.error(f"Failed to save nodes: {e}")

    def register_node(self, role: str, url: str) -> Dict[str, str]:
        """Registers a Colab node with its current Ngrok URL."""
        # Clean URL
        if url.endswith("/"):
            url = url[:-1]
            
        self._nodes[role] = NodeInfo(role=role, url=url)
        self._save_nodes() # Persist!
        
        logger.info(f"Registered Node [{role}] at {url}")
        return {"status": "registered", "role": role, "url": url}

    def get_node(self, role: str) -> Optional[NodeInfo]:
        return self._nodes.get(role)

    def list_nodes(self):
        return self._nodes

    async def dispatch_task(self, role: str, endpoint: str, payload: Dict[str, Any], timeout: int = 60):
        """
        Forwards a request to the specific worker node.
        Adds the SWARM_SECRET to headers for security.
        """
        node = self.get_node(role)
        if not node:
            raise ValueError(f"Node for role '{role}' is not registered.")

        target_url = f"{node.url}{endpoint}"
        headers = {
            "X-Swarm-Secret": settings.SWARM_SECRET,
            "Content-Type": "application/json"
        }

        logger.info(f"Dispatching task to {role} ({target_url})...")
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(target_url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                logger.error(f"Connection error to {role}: {e}")
                raise ConnectionError(f"Failed to reach {role} node: {e}")
            except httpx.HTTPStatusError as e:
                logger.error(f"Error from {role}: {e.response.text}")
                raise ValueError(f"Node {role} returned error: {e.response.text}")

swarm_orchestrator = SwarmOrchestrator()
