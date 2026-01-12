# Facebook Ads Proxy API - Exemplos Práticos

> **Coleção de exemplos práticos para usar o Facebook Ads Proxy API**

---

## Índice

1. [Operações Básicas](#operações-básicas)
2. [Gerenciamento de Campanhas](#gerenciamento-de-campanhas)
3. [Ad Sets](#ad-sets)
4. [Anúncios](#anúncios)
5. [Insights e Relatórios](#insights-e-relatórios)
6. [Operações em Lote](#operações-em-lote)
7. [Scripts Úteis](#scripts-úteis)
8. [Integração com Python](#integração-com-python)

---

## Operações Básicas

### Health Check

Verifique se o proxy está rodando:

```bash
curl http://localhost:XXXXX/
```

**Resposta:**
```json
{
  "status": "ok",
  "service": "facebook-ads-proxy",
  "version": "1.0.0",
  "port": 63309
}
```

### Health Check Detalhado

```bash
curl http://localhost:XXXXX/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "service": "facebook-ads-proxy"
}
```

### Listar Campanhas (Básico)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456789/campaigns",
    "method": "GET"
  }'
```

### Listar Campanhas (Com Fields)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456789/campaigns",
    "method": "GET",
    "params": {
      "fields": "id,name,status,objective,daily_budget,lifetime_budget,start_time,stop_time",
      "limit": "20"
    }
  }'
```

### Filtrar Campanhas por Status

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456789/campaigns",
    "method": "GET",
    "params": {
      "fields": "id,name,status,objective",
      "filtering": [{"field": "status", "operator": "EQUAL", "value": "ACTIVE"}]
    }
  }'
```

---

## Gerenciamento de Campanhas

### Criar Campanha (Vendas)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456789/campaigns",
    "method": "POST",
    "body": {
      "name": "Black Friday 2026",
      "objective": "OUTCOME_SALES",
      "status": "PAUSED",
      "daily_budget": 50000,
      "special_ad_categories": []
    }
  }'
```

### Criar Campanha (Leads)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456789/campaigns",
    "method": "POST",
    "body": {
      "name": "Geração de Leads - Janeiro",
      "objective": "OUTCOME_LEADS",
      "status": "PAUSED",
      "daily_budget": 30000,
      "special_ad_categories": []
    }
  }'
```

### Criar Campanha (Tráfego)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456789/campaigns",
    "method": "POST",
    "body": {
      "name": "Tráfego Site - Blog",
      "objective": "OUTCOME_TRAFFIC",
      "status": "PAUSED",
      "daily_budget": 20000,
      "special_ad_categories": []
    }
  }'
```

### Atualizar Campanha

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630",
    "method": "PATCH",
    "body": {
      "daily_budget": 100000,
      "name": "Black Friday 2026 - Budget Aumentado"
    }
  }'
```

### Ativar Campanha

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630",
    "method": "PATCH",
    "body": {
      "status": "ACTIVE"
    }
  }'
```

### Pausar Campanha

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630",
    "method": "PATCH",
    "body": {
      "status": "PAUSED"
    }
  }'
```

### Deletar Campanha

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630",
    "method": "DELETE"
  }'
```

---

## Ad Sets

### Listar Ad Sets de uma Campanha

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630/adsets",
    "method": "GET",
    "params": {
      "fields": "id,name,status,daily_budget,targeting,optimization_goal",
      "limit": "50"
    }
  }'
```

### Criar Ad Set (Targeting Brasil)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630/adsets",
    "method": "POST",
    "body": {
      "name": "Ad Set - Brasil",
      "campaign_id": "23843663654630",
      "daily_budget": 20000,
      "optimization_goal": "OFFSITE_CONVERSIONS",
      "billing_event": "IMPRESSIONS",
      "targeting": {
        "geo_locations": {
          "countries": ["BR"]
        },
        "age_min": 18,
        "age_max": 65,
        "genders": [1, 2],
        "publisher_platforms": ["facebook", "instagram"],
        "device_platforms": ["mobile", "desktop"]
      },
      "status": "PAUSED"
    }
  }'
```

### Criar Ad Set (Targeting Específico)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630/adsets",
    "method": "POST",
    "body": {
      "name": "Ad Set - São Paulo - Mulheres 25-45",
      "campaign_id": "23843663654630",
      "daily_budget": 15000,
      "optimization_goal": "OFFSITE_CONVERSIONS",
      "billing_event": "IMPRESSIONS",
      "targeting": {
        "geo_locations": {
          "regions": [{"key": "3846"}],
          "country": "BR"
        },
        "age_min": 25,
        "age_max": 45,
        "genders": [2],
        "publisher_platforms": ["facebook", "instagram"],
        "device_platforms": ["mobile"]
      },
      "status": "PAUSED"
    }
  }'
```

### Criar Ad Set (Custom Audiences)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630/adsets",
    "method": "POST",
    "body": {
      "name": "Ad Set - Custom Audience",
      "campaign_id": "23843663654630",
      "daily_budget": 10000,
      "optimization_goal": "OFFSITE_CONVERSIONS",
      "billing_event": "IMPRESSIONS",
      "targeting": {
        "geo_locations": {
          "countries": ["BR"]
        },
        "age_min": 18,
        "custom_audiences": [{"id": "123456789"}],
        "publisher_platforms": ["facebook", "instagram"]
      },
      "status": "PAUSED"
    }
  }'
```

### Atualizar Budget do Ad Set

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654631",
    "method": "PATCH",
    "body": {
      "daily_budget": 50000
    }
  }'
```

---

## Anúncios

### Listar Anúncios de um Ad Set

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654631/ads",
    "method": "GET",
    "params": {
      "fields": "id,name,status,creative,adset_id,campaign_id",
      "limit": "50"
    }
  }'
```

### Criar Criativo (Imagem)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456789/adcreatives",
    "method": "POST",
    "body": {
      "name": "Criativo - Black Friday",
      "object_story_spec": {
        "page_id": "123456789",
        "link_data": {
          "image_hash": "abcdef123456",
          "link": "https://example.com",
          "message": "Oferta imperdível!",
          "call_to_action": {"type": "SHOP_NOW"}
        }
      }
    }
  }'
```

### Criar Anúncio

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654631/ads",
    "method": "POST",
    "body": {
      "name": "Anúncio - Black Friday",
      "adset_id": "23843663654631",
      "creative": {"creative_id": "23843663654632"},
      "status": "PAUSED"
    }
  }'
```

### Criar Anúncio com Criativo Inline

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654631/ads",
    "method": "POST",
    "body": {
      "name": "Anúncio - Promoção",
      "adset_id": "23843663654631",
      "creative": {
        "object_story_spec": {
          "page_id": "123456789",
          "link_data": {
            "image_hash": "abcdef123456",
            "link": "https://example.com",
            "message": "Aproveite!",
            "call_to_action": {"type": "SHOP_NOW"}
          }
        }
      },
      "status": "PAUSED"
    }
  }'
```

---

## Insights e Relatórios

### Insights de Campanha (Últimos 7 Dias)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630/insights",
    "method": "GET",
    "params": {
      "date_preset": "last_7d",
      "fields": "impressions,clicks,spend,actions,action_values,cpc,cpm,ctr,frequency,reach"
    }
  }'
```

### Insights de Ad Set

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654631/insights",
    "method": "GET",
    "params": {
      "date_preset": "last_30d",
      "fields": "impressions,clicks,spend,actions,cpc,cpm,ctr"
    }
  }'
```

### Insights de Anúncio

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654633/insights",
    "method": "GET",
    "params": {
      "date_preset": "last_7d",
      "fields": "impressions,clicks,spend,actions"
    }
  }'
```

### Insights com Quebra por Dia

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630/insights",
    "method": "GET",
    "params": {
      "date_preset": "last_7d",
      "fields": "impressions,clicks,spend,actions",
      "time_increment": 1
    }
  }'
```

### Insights por Hora

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630/insights",
    "method": "GET",
    "params": {
      "date_preset": "last_7d",
      "fields": "impressions,clicks,spend",
      "time_increment": 1,
      "time_ranges": [{"since":"2026-01-01","until":"2026-01-07"}]
    }
  }'
```

### Insights com Nível de Account

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456789/insights",
    "method": "GET",
    "params": {
      "date_preset": "last_30d",
      "fields": "impressions,clicks,spend,actions,campaign_name",
      "level": "campaign",
      "limit": "50"
    }
  }'
```

---

## Operações em Lote

### Batch Request (Múltiplas Operações)

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0",
    "method": "POST",
    "batch": [
      {
        "method": "GET",
        "relative_url": "act_123456789/campaigns?fields=id,name,status&limit=10"
      },
      {
        "method": "GET",
        "relative_url": "act_123456789/campaigns?fields=id,name,status&limit=10&offset=10"
      }
    ]
  }'
```

### Pausar Múltiplas Campanhas

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0",
    "method": "POST",
    "batch": [
      {
        "method": "POST",
        "relative_url": "23843663654630",
        "body": "status=PAUSED"
      },
      {
        "method": "POST",
        "relative_url": "23843663654631",
        "body": "status=PAUSED"
      }
    ]
  }'
```

---

## Scripts Úteis

### Script: Função Helper

```bash
#!/bin/bash

# facebook_proxy_call.sh

PROXY_URL="http://localhost:8080"
ENDPOINT="$1"
METHOD="${2:-GET}"
BODY="$3"
PARAMS="$4"

# Construir request JSON
REQUEST_JSON="{\"endpoint\":\"$ENDPOINT\",\"method\":\"$METHOD\""

if [ -n "$BODY" ]; then
  REQUEST_JSON="$REQUEST_JSON,\"body\":$BODY"
fi

if [ -n "$PARAMS" ]; then
  REQUEST_JSON="$REQUEST_JSON,\"params\":$PARAMS"
fi

REQUEST_JSON="$REQUEST_JSON}"

# Chamar proxy
curl -s -X POST "$PROXY_URL/facebook-ads/proxy" \
  -H "Content-Type: application/json" \
  -d "$REQUEST_JSON" | jq '.'
```

**Uso:**
```bash
# Listar campanhas
./facebook_proxy_call.sh "/v24.0/act_123456789/campaigns" "GET"

# Criar campanha
./facebook_proxy_call.sh "/v24.0/act_123456789/campaigns" "POST" '{"name":"Test","objective":"OUTCOME_SALES"}'
```

### Script: Relatório Diário

```bash
#!/bin/bash

# daily_report.sh

PROXY_URL="http://localhost:8080"
ACCOUNT_ID="act_123456789"

echo "# Relatório Diário - $(date +%Y-%m-%d)"
echo ""
echo "## 📊 Campanhas Ativas"
echo ""

# Buscar campanhas ativas
CAMPAIGNS=$(curl -s -X POST "$PROXY_URL/facebook-ads/proxy" \
  -H "Content-Type: application/json" \
  -d "{
    \"endpoint\": \"/v24.0/$ACCOUNT_ID/campaigns\",
    \"method\": \"GET\",
    \"params\": {
      \"fields\": \"id,name,status\",
      \"filtering\": [{\"field\": \"status\", \"operator\": \"EQUAL\", \"value\": \"ACTIVE\"}]
    }
  }" | jq -r '.data.data[] | @base64')

for CAMPAIGN in $CAMPAIGNS; do
  _jq() {
    echo "${CAMPAIGN}" | base64 --decode | jq -r "${1}"
  }

  CAMPAIGN_ID=$(_jq '.id')
  CAMPAIGN_NAME=$(_jq '.name')

  echo "### $CAMPAIGN_NAME"

  # Buscar insights
  INSIGHTS=$(curl -s -X POST "$PROXY_URL/facebook-ads/proxy" \
    -H "Content-Type: application/json" \
    -d "{
      \"endpoint\": \"/v24.0/$CAMPAIGN_ID/insights\",
      \"method\": \"GET\",
      \"params\": {
        \"date_preset\": \"last_7d\",
        \"fields\": \"impressions,clicks,spend,actions\"
      }
    }" | jq '.data.data[0]')

  IMPRESSIONS=$(echo $INSIGHTS | jq -r '.impressions // "0"')
  CLICKS=$(echo $INSIGHTS | jq -r '.clicks // "0"')
  SPEND=$(echo $INSIGHTS | jq -r '.spend // "0"')

  echo "- Impressions: $IMPRESSIONS"
  echo "- Clicks: $CLICKS"
  echo "- Spend: \$$SPEND"
  echo ""
done
```

---

## Integração com Python

### Cliente Python Básico

```python
import requests
import json

class FacebookAdsProxyClient:
    def __init__(self, proxy_url="http://localhost:8080"):
        self.proxy_url = proxy_url

    def call(self, endpoint, method="GET", body=None, params=None):
        """Faz chamada via proxy"""
        url = f"{self.proxy_url}/facebook-ads/proxy"

        payload = {
            "endpoint": endpoint,
            "method": method
        }

        if body:
            payload["body"] = body
        if params:
            payload["params"] = params

        response = requests.post(url, json=payload)
        return response.json()

    def list_campaigns(self, account_id, fields=None):
        """Lista campanhas"""
        fields = fields or ["id", "name", "status", "objective"]
        return self.call(
            endpoint=f"/v24.0/{account_id}/campaigns",
            method="GET",
            params={"fields": ",".join(fields)}
        )

    def create_campaign(self, account_id, name, objective, status="PAUSED"):
        """Cria campanha"""
        return self.call(
            endpoint=f"/v24.0/{account_id}/campaigns",
            method="POST",
            body={
                "name": name,
                "objective": objective,
                "status": status,
                "special_ad_categories": []
            }
        )

    def get_insights(self, object_id, date_preset="last_7d"):
        """Busca insights"""
        return self.call(
            endpoint=f"/v24.0/{object_id}/insights",
            method="GET",
            params={
                "date_preset": date_preset,
                "fields": "impressions,clicks,spend,actions"
            }
        )

# Uso
client = FacebookAdsProxyClient()

# Listar campanhas
campaigns = client.list_campaigns("act_123456789")
print(json.dumps(campaigns, indent=2))

# Criar campanha
campaign = client.create_campaign(
    account_id="act_123456789",
    name="Nova Campanha",
    objective="OUTCOME_SALES"
)
print(json.dumps(campaign, indent=2))

# Buscar insights
insights = client.get_insights("23843663654630", date_preset="last_30d")
print(json.dumps(insights, indent=2))
```

### Cliente Python com Retry

```python
import requests
import time
from typing import Optional, Dict, Any

class FacebookAdsProxyClient:
    def __init__(
        self,
        proxy_url: str = "http://localhost:8080",
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.proxy_url = proxy_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def call(
        self,
        endpoint: str,
        method: str = "GET",
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Faz chamada via proxy com retry"""

        for attempt in range(self.max_retries):
            try:
                url = f"{self.proxy_url}/facebook-ads/proxy"
                payload = {"endpoint": endpoint, "method": method}

                if body:
                    payload["body"] = body
                if params:
                    payload["params"] = params

                response = requests.post(url, json=payload, timeout=30)
                response.raise_for_status()

                data = response.json()

                # Verificar sucesso da chamada
                if data.get("success", False):
                    return data.get("data", {})
                else:
                    print(f"API error: {data}")
                    return data

            except requests.exceptions.Timeout:
                print(f"Timeout na tentativa {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))
                else:
                    raise

            except requests.exceptions.RequestException as e:
                print(f"Erro na tentativa {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))
                else:
                    raise

        return {}
```

---

## Referências Rápidas

### Objetivos Disponíveis (v24.0)

| Objetivo | Descrição |
|----------|-----------|
| `OUTCOME_SALES` | Vendas |
| `OUTCOME_LEADS` | Leads |
| `OUTCOME_ENGAGEMENT` | Engajamento |
| `OUTCOME_AWARENESS` | Alcance |
| `OUTCOME_TRAFFIC` | Tráfego |
| `OUTCOME_APP_PROMOTION` | Promoção de App |

### Status Possíveis

| Status | Descrição |
|--------|-----------|
| `ACTIVE` | Ativo |
| `PAUSED` | Pausado |
| `ARCHIVED` | Arquivado |
| `DELETED` | Deletado |

### Campos Comuns de Insights

| Campo | Descrição |
|-------|-----------|
| `impressions` | Número de impressões |
| `clicks` | Número de cliques |
| `spend` | Valor gasto |
| `actions` | Ações de conversão |
| `cpc` | Custo por clique |
| `cpm` | Custo por mil |
| `ctr` | Taxa de cliques |
| `reach` | Alcance único |
| `frequency` | Frequência média |

---

**Para mais informações:**
- [GUIDE.md](GUIDE.md) - Guia completo de uso
- [AGENTS.md](AGENTS.md) - Integração com Claude Code
- [README.md](README.md) - Visão geral do projeto
- Meta Marketing API: https://developers.facebook.com/docs/marketing-api/
