from pydantic import BaseModel
from typing import Optional, Dict, Any


class ProxyRequest(BaseModel):
    """Request para o proxy da Meta API"""

    endpoint: str  # Ex: /v24.0/act_123456/campaigns
    method: str = "GET"  # GET, POST, DELETE, PUT, PATCH
    body: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, Any]] = None


class FacebookResponse(BaseModel):
    """Response padrão do proxy"""

    success: bool
    data: Dict[str, Any]
    meta: Dict[str, Any]


class HistoryEntry(BaseModel):
    """Entrada do histórico de chamadas"""

    id: int
    request_id: str
    timestamp: str
    endpoint: str
    method: str
    response_status: int
    duration_ms: float
    body_summary: Optional[str] = None


class HealthResponse(BaseModel):
    """Response do health check"""

    status: str
    service: str
    version: str
    port: int
