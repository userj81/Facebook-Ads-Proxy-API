# Facebook Ads Proxy API - Guia Completo

> **Guia detalhado para instalação, configuração e uso do Facebook Ads Proxy API**

---

## Índice

1. [Conceitos](#conceitos)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Primeiros Passos](#primeiros-passos)
5. [Uso Avançado](#uso-avançado)
6. [Integração com Claude Code](#integração-com-claude-code)
7. [Segurança](#segurança)
8. [Troubleshooting](#troubleshooting)

---

## Conceitos

### O que é o Facebook Ads Proxy API?

É um servidor API local em Python que atua como intermediário seguro entre suas aplicações e a Meta Marketing API (Facebook Ads).

### Por que usar um Proxy?

| Sem Proxy | Com Proxy |
|-----------|-----------|
| Credenciais expostas na aplicação | Credenciais isoladas no proxy |
| Difícil rastrear chamadas | Histórico automático completo |
| Aplicação depende de API específica | Abstração da API Meta |

### Fluxo de Dados

```
┌─────────────────┐
│  Sua Aplicação  │
│  (ou Agent)     │
└────────┬────────┘
         │ HTTP Request
         │ (sem credenciais)
         ▼
┌─────────────────────────────┐
│  Facebook Ads Proxy API     │
│  - localhost:PORTA          │
│  - Injeta credenciais       │
│  - Salva histórico         │
└────────┬────────────────────┘
         │ HTTPS Request
         │ (com credenciais)
         ▼
┌─────────────────────────────┐
│  Meta Marketing API v24.0   │
│  graph.facebook.com         │
└─────────────────────────────┘
```

---

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Access Token da Meta API
- Ad Account ID

### Passo 1: Clone ou Download

```bash
# Se clonando do GitHub
git clone https://github.com/userj81/Facebook-Ads-Proxy-API.git
cd Facebook-Ads-Proxy-API

# Ou se já tem os arquivos
cd /caminho/para/facebook-ads-proxy
```

### Passo 2: Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# No macOS/Linux:
source venv/bin/activate

# No Windows:
# venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Credenciais

```bash
# Copiar template
cp .env.example .env

# Editar com suas credenciais
nano .env
```

---

## Configuração

### Arquivo .env

```bash
# Access Token da Meta (OBRIGATÓRIO)
FACEBOOK_API_KEY=EAAxxxxxxxxxxxx...

# Ad Account ID (OBRIGATÓRIO)
FACEBOOK_ACCOUNT_ID=act_123456789

# Versão da API (opcional, padrão: v24.0)
FACEBOOK_API_VERSION=v24.0

# Porta do servidor (0 = aleatória, ou especifique)
PROXY_PORT=0
```

### Obtendo o Access Token

1. Acesse: https://developers.facebook.com/tools/accesstoken/
2. Selecione seu App
3. Selecione a Ad Account
4. Copie o token gerado

### Obtendo o Ad Account ID

1. Acesse: https://business.facebook.com/ads/manager
2. Selecione a conta de anúncios
3. O ID está na URL: `act_123456789`

---

## Primeiros Passos

### Iniciando o Servidor

```bash
# Usando o script start.sh
./start.sh

# Ou manualmente
python -m src.main
```

### Saída Esperada

```
╔══════════════════════════════════════════════════════════╗
║     Facebook Ads Proxy API - Starting...                ║
╠══════════════════════════════════════════════════════════╣
║  URL:      http://localhost:63309                        ║
║  Docs:    http://localhost:63309/docs                    ║
║  Version: v24.0                                          ║
║  Account: act_123456789                                  ║
╚══════════════════════════════════════════════════════════╝
```

### Teste de Saúde

```bash
curl http://localhost:63309/
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "service": "facebook-ads-proxy",
  "version": "1.0.0",
  "port": 63309
}
```

### Acessar Documentação Swagger

Abra no navegador: `http://localhost:63309/docs`

---

## Uso Avançado

### Estrutura da Request

```json
{
  "endpoint": "/v24.0/act_123456/campaigns",
  "method": "POST",
  "body": {
    "name": "Minha Campanha",
    "objective": "OUTCOME_SALES",
    "status": "PAUSED"
  },
  "params": {
    "fields": "id,name,status"
  }
}
```

### Campos da Request

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `endpoint` | string | ✅ Sim | Caminho completo da Meta API |
| `method` | string | ❌ Não | GET, POST, DELETE, PUT, PATCH (default: GET) |
| `body` | object | ❌ Não | Dados para POST/PUT/PATCH |
| `params` | object | ❌ Não | Query parameters para GET |

### Estrutura da Response

```json
{
  "success": true,
  "data": {
    "id": "23843663654630"
  },
  "meta": {
    "timestamp": 1736686808.352,
    "request_id": "req_abc12345",
    "facebook_status": 200,
    "duration_ms": 245.5
  }
}
```

### Exemplos de Uso

#### Listar Campanhas

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456/campaigns",
    "method": "GET",
    "params": {
      "fields": "id,name,status,objective",
      "limit": "10"
    }
  }'
```

#### Criar Campanha

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456/campaigns",
    "method": "POST",
    "body": {
      "name": "Black Friday 2026",
      "objective": "OUTCOME_SALES",
      "status": "PAUSED",
      "special_ad_categories": []
    }
  }'
```

#### Buscar Insights

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630/insights",
    "method": "GET",
    "params": {
      "date_preset": "last_7d",
      "fields": "impressions,clicks,spend,actions"
    }
  }'
```

#### Atualizar Campanha

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

#### Deletar Campanha

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/23843663654630",
    "method": "DELETE"
  }'
```

### Endpoints do Proxy

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Health check básico |
| `/health` | GET | Status detalhado |
| `/facebook-ads/proxy` | POST | Proxy principal para Meta API |
| `/facebook-ads/history` | GET | Histórico de chamadas |
| `/facebook-ads/stats` | GET | Estatísticas de uso |
| `/docs` | GET | Documentação Swagger UI |

---

## Integração com Claude Code

### O que são Claude Code Agents?

Agents são especializações do Claude Code que automatizam tarefas específicas. Eles usam este proxy para interagir com o Facebook Ads sem nunca ter acesso às suas credenciais.

### Agentes Disponíveis

#### Facebook Ads Operator
- Cria e gerencia campanhas
- Configura ad sets
- Gerencia anúncios
- Monitora performance

#### Facebook Ads Reports Generator
- Gera relatórios automáticos
- Calcula métricas (ROI, ROAS, CPA)
- Identifica top performers
- Gera recomendações

### Instalando os Agents

Os agents são instalados no diretório `~/.claude/agents/`. Consulte o arquivo [AGENTS.md](AGENTS.md) para instruções detalhadas.

### Usando com Agents

1. **Inicie o proxy:**
   ```bash
   cd /caminho/para/facebook-ads-proxy
   ./start.sh
   ```

2. **No Claude Code, faça pedidos em linguagem natural:**
   ```
   "Gera relatório dos últimos 7 dias"
   "Cria uma campanha para Black Friday"
   "Qual campanha tem melhor ROI?"
   ```

O agent automaticamente:
- Descobre a porta do proxy
- Faz as chamadas necessárias
- Processa os dados
- Retorna o resultado formatado

---

## Segurança

### Boas Práticas

| Prática | Descrição |
|---------|-----------|
| ✅ Nunca commitar .env | Arquivo está no .gitignore |
| ✅ Usar localhost apenas | Servidor roda em 127.0.0.1 |
| ✅ Rotacionar tokens | Atualize tokens regularmente |
| ✅ Monitorar histórico | Revise /facebook-ads/history |
| ✅ Limitar permissões | Token deve ter permissões mínimas |

### Permissões do Token

O Access Token deve ter apenas as permissões necessárias:

- `ads_management` - Gerenciar campanhas
- `ads_read` - Ler dados de anúncios
- `read_insights` - Acessar insights

### Protegendo o .env

O arquivo `.env` já está no `.gitignore`, mas verifique:

```bash
# Verificar .gitignore
cat .gitignore

# Deve conter:
# .env
# *.db
# venv/
```

---

## Troubleshooting

### Erro: "Invalid OAuth access token"

**Causa:** Token expirado ou inválido

**Solução:**
1. Acesse: https://developers.facebook.com/tools/accesstoken/
2. Gere novo token
3. Atualize `FACEBOOK_API_KEY` no `.env`
4. Reinicie o servidor

### Erro: "Port already in use"

**Causa:** Porta já está em uso

**Solução:**
1. Edite `.env`
2. Mude `PROXY_PORT=0` para `PROXY_PORT=8080` (ou outra porta)
3. Reinicie o servidor

### Erro: "Connection refused"

**Causa:** Servidor não está rodando

**Solução:**
```bash
# Verificar se está rodando
ps aux | grep "python -m src.main"

# Se não estiver, inicie
./start.sh
```

### Erro: "Module not found"

**Causa:** Dependências não instaladas

**Solução:**
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Database locked"

**Causa:** Múltiplas tentativas de escrita no SQLite

**Solução:**
```bash
# Deletar banco de dados (opcional)
rm data/history.db

# Reiniciar servidor (será recriado)
./start.sh
```

### Logs de Erro

Para ver logs detalhados:

```bash
# Rodar com verbose
python -m src.main --log-level debug
```

---

## Próximos Passos

1. Leia [EXAMPLES.md](EXAMPLES.md) para mais exemplos práticos
2. Consulte [AGENTS.md](AGENTS.md) para integração com Claude Code
3. Acesse a documentação da Meta API: https://developers.facebook.com/docs/marketing-api/

---

**Versão:** 1.0.0
**API Meta:** v24.0
**Python:** 3.10+

Para mais informações, visite: https://github.com/userj81/Facebook-Ads-Proxy-API
