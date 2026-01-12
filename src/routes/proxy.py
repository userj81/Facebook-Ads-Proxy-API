from fastapi import APIRouter, HTTPException
import time
import json
from pathlib import Path
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


@router.get("/accounts")
async def get_accounts():
    """
    Retorna mapeamento de nomes de contas para IDs.

    Os agents podem usar este endpoint para descobrir o account_id
    correto baseado no nome da conta informado pelo usuário.
    """
    accounts_file = Path(__file__).parent.parent.parent / "accounts.json"

    if not accounts_file.exists():
        return {
            "accounts": {},
            "metadata": {
                "total": 0,
                "error": "accounts.json not found"
            }
        }

    with open(accounts_file, "r") as f:
        return json.load(f)


@router.get("/templates")
async def list_templates():
    """
    Lista todos os templates de campanha disponíveis.

    Os agents podem usar este endpoint para descobrir quais templates
    estão disponíveis para criar campanhas.
    """
    templates_dir = Path(__file__).parent.parent.parent / "templates"
    index_file = templates_dir / "index.json"

    if not index_file.exists():
        return {
            "templates": [],
            "metadata": {
                "total": 0,
                "error": "templates/index.json not found"
            }
        }

    with open(index_file, "r") as f:
        return json.load(f)


@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    """
    Retorna um template específico com o fluxo completo de criação.

    O template inclui todos os steps necessários para criar uma campanha
    completa (campaign → adset → creative → ad).
    """
    templates_dir = Path(__file__).parent.parent.parent / "templates"
    template_file = templates_dir / f"{template_id}.json"

    if not template_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Template '{template_id}' not found. Available templates: vendas_simple, lead_generation, trafego_whatsapp, engajamento_instagram"
        )

    with open(template_file, "r") as f:
        return json.load(f)
