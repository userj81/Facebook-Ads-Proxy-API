from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do .env"""

    facebook_api_key: str
    facebook_api_version: str = "v24.0"
    proxy_port: int = 0  # 0 = porta aleatória

    # Nota: facebook_account_id não é mais necessário aqui
    # O account_id (act_XXXXXX) é passado dinamicamente no endpoint pelo agent

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações"""
    return Settings()
