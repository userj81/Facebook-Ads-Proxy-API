import httpx
from ..config import get_settings


class FacebookClient:
    """Cliente HTTP para Meta Marketing API"""

    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://graph.facebook.com"
        self.api_version = self.settings.facebook_api_version

    async def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        body: dict = None,
        params: dict = None,
    ) -> tuple[dict, int]:
        """
        Faz request para Meta API e retorna (response_data, status_code)

        Args:
            endpoint: Endpoint da API (ex: /v24.0/act_123456/campaigns)
            method: Método HTTP (GET, POST, DELETE, PUT, PATCH)
            body: Corpo da requisição (para POST, PUT, PATCH)
            params: Query params (para GET)

        Returns:
            Tuple com (dados da resposta, status_code)
        """
        url = f"{self.base_url}{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.settings.facebook_api_key}"
        }

        if method in ["POST", "PUT", "PATCH"]:
            headers["Content-Type"] = "application/json"

        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(
                    url, headers=headers, params=params, timeout=30.0
                )
            elif method == "POST":
                response = await client.post(
                    url, headers=headers, json=body, timeout=30.0
                )
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, timeout=30.0)
            elif method == "PUT":
                response = await client.put(
                    url, headers=headers, json=body, timeout=30.0
                )
            elif method == "PATCH":
                response = await client.patch(
                    url, headers=headers, json=body, timeout=30.0
                )
            else:
                raise ValueError(f"Unsupported method: {method}")

        # Tentar parsear JSON, se falhar retorna texto bruto
        try:
            data = response.json()
        except Exception:
            data = {"raw_response": response.text}

        return data, response.status_code
