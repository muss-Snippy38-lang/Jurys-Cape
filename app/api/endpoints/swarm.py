from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.services.swarm_orchestrator import swarm_orchestrator

router = APIRouter()

class NodeRegistration(BaseModel):
    role: str
    url: str

@router.post("/swarm/register")
async def register_node(data: NodeRegistration):
    """
    Called by the Colab node upon startup to register its Ngrok URL.
    """
    return swarm_orchestrator.register_node(data.role, data.url)

@router.get("/swarm/nodes")
async def list_nodes():
    return swarm_orchestrator.list_nodes()

@router.post("/swarm/dispatch/{role}")
async def dispatch_task(role: str, task_endpoint: str, payload: Dict[str, Any]):
    """
    Manually dispatch a task to a specific node. 
    'task_endpoint' should be the path on the worker node, e.g. '/ocr'
    """
    # ensure endpoint starts with /
    if not task_endpoint.startswith("/"):
        task_endpoint = "/" + task_endpoint
        
    try:
        result = await swarm_orchestrator.dispatch_task(role, task_endpoint, payload)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
