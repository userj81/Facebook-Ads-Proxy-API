from fastapi import APIRouter, HTTPException
import time
from ..models.schemas import ProxyRequest, FacebookResponse
from ..services.facebook_client import FacebookClient
from ..services.history import HistoryService

router = APIRouter(prefix="/facebook-ads", tags=["facebook-ads"])
fb_client = FacebookClient()
history = HistoryService()


@router.post("/proxy", response_model=FacebookResponse)
async def proxy_request(request: ProxyRequest):
    """
    Endpoint principal - proxy para Meta API

    Recebe uma requisição e a repassa para a Meta Marketing API
    com as credenciais configuradas, salvando o histórico.
    """
    start_time = time.time()

    # Resumo do body para histórico (não salva dados sensíveis completos)
    body_summary = None
    if request.body:
        if "name" in request.body:
            body_summary = f"name={request.body.get('name')}"
        elif "message" in request.body:
            body_summary = f"message={request.body.get('message')[:50]}"
        else:
            body_summary = f"keys={list(request.body.keys())}"

    # Fazer request para Facebook
    try:
        data, status_code = await fb_client.make_request(
            endpoint=request.endpoint,
            method=request.method,
            body=request.body,
            params=request.params,
        )
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        history.save_call(
            endpoint=request.endpoint,
            method=request.method,
            response_status=500,
            duration_ms=duration_ms,
            body_summary=f"ERROR: {str(e)}",
        )
        raise HTTPException(status_code=500, detail=str(e))

    duration_ms = (time.time() - start_time) * 1000

    # Salvar no histórico
    request_id = history.save_call(
        endpoint=request.endpoint,
        method=request.method,
        response_status=status_code,
        duration_ms=duration_ms,
        body_summary=body_summary,
    )

    return FacebookResponse(
        success=status_code < 400,
        data=data,
        meta={
            "timestamp": time.time(),
            "request_id": request_id,
            "facebook_status": status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )


@router.get("/history")
async def get_history(limit: int = 50):
    """Retorna histórico de chamadas"""
    return {"calls": history.get_history(limit)}


@router.get("/stats")
async def get_stats():
    """Retorna estatísticas de uso"""
    return history.get_stats()
