from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socket
from .routes import proxy
from .models.schemas import HealthResponse

app = FastAPI(
    title="Facebook Ads Proxy API",
    description="Proxy local para Meta Marketing API v24.0",
    version="1.0.0",
)

# CORS para permitir requisições locais
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(proxy.router)


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check básico"""
    return HealthResponse(
        status="ok", service="facebook-ads-proxy", version="1.0.0", port=0
    )


@app.get("/health")
async def health():
    """Health check detalhado"""
    return {"status": "healthy", "service": "facebook-ads-proxy", "version": "1.0.0"}


def get_available_port():
    """
    Retorna uma porta disponível

    Usa socket para encontrar uma porta livre no sistema.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def main():
    """Inicia o servidor"""
    import uvicorn

    from .config import get_settings

    settings = get_settings()

    # Se PORT=0, usa porta aleatória
    if settings.proxy_port == 0:
        port = get_available_port()
    else:
        port = settings.proxy_port

    print(
        f"""
    ╔══════════════════════════════════════════════════════════╗
    ║     Facebook Ads Proxy API - Starting...                ║
    ╠══════════════════════════════════════════════════════════╣
    ║  URL:      http://localhost:{port}                       ║
    ║  Docs:    http://localhost:{port}/docs                   ║
    ║  Version: {settings.facebook_api_version}                 ║
    ╚══════════════════════════════════════════════════════════╝
    """
    )

    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=port,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    main()
