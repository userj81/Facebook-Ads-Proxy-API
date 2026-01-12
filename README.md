# Facebook Ads Proxy API

> **Proxy local seguro em Python para Meta Marketing API v24.0**

---

## 📖 O Que É?

Um servidor API local que funciona como intermediário entre suas aplicações (como o Claude Code Agent) e a Meta Marketing API (Facebook Ads).

### 🎯 Problema Que Resolve

Quando você usa IA/Agentes para interagir com o Facebook Ads, há um **problema de segurança**: o Agent precisa ter acesso às suas credenciais de API (Access Token) para fazer as chamadas.

**Sem o Proxy:**
```
Agent (IA) → Tem acesso direto à API Key → Meta API
            ⚠️ RISCO: Credenciais expostas para a IA
```

**Com o Proxy:**
```
Agent (IA) → Chama API local (sem credenciais) → Proxy (injeta credenciais) → Meta API
            ✅ SEGURO: Credenciais nunca saem do Proxy
```

---

## 🏗️ Como Funciona

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Agent                        │
│                                                             │
│  Decide o que fazer: criar campanha, buscar insights, etc   │
│                                                             │
│  Faz request LOCAL (sem ver credenciais):                  │
│  POST http://localhost:8080/facebook-ads/proxy             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  FACEBOOK ADS PROXY API                     │
│                   (Este projeto)                            │
│                                                             │
│  1. Recebe request do Agent                                │
│  2. Busca credenciais do .env (só o Proxy vê)              │
│  3. Faz chamada para Meta API com credencial               │
│  4. Salva histórico no SQLite                              │
│  5. Retorna resposta para o Agent                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Meta Marketing API v24.0                   │
│              https://graph.facebook.com/                    │
└─────────────────────────────────────────────────────────────┘
```

### O Agente Decide Tudo

O Proxy é **"burro"** propositalmente - ele apenas:
- Recebe a requisição (endpoint, método, body)
- Injeta a credencial
- Faz a chamada
- Retorna a resposta

**O Agent (Claude Code) decide:**
- Qual endpoint chamar
- Qual método usar (GET, POST, DELETE, etc.)
- Quais parâmetros enviar
- Como processar a resposta

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 🔐 **Credenciais Protegidas** | Chaves ficam no `.env`, nunca expostas para o Agent |
| 📊 **Histórico SQLite** | Todas as chamadas são registradas automaticamente |
| 🎲 **Porta Aleatória** | Evita conflitos com outros projetos (porta automática) |
| 📚 **Swagger UI** | Documentação interativa em `/docs` |
| ⚡ **Fast & Async** | Built com FastAPI, performance otimizada |
| 🛡️ **CORS Habilitado** | Aceita requisições de qualquer origem local |

---

## 🚀 Quick Start

### 1. Instalação

```bash
cd /Users/jairflores/Downloads/agents/facebook-ads-proxy

# Copiar template de credenciais
cp .env.example .env

# Editar .env com suas credenciais
nano .env  # ou seu editor preferido
```

### 2. Configurar Credenciais

Edite o arquivo `.env`:

```bash
# Seu Access Token da Meta (obtenha em: https://developers.facebook.com/tools/accesstoken/)
FACEBOOK_API_KEY=EAAxxxxxxxxxxxx...

# Seu Ad Account ID (formato: act_123456789)
FACEBOOK_ACCOUNT_ID=act_123456789

# Versão da API (v24.0 é a mais recente)
FACEBOOK_API_VERSION=v24.0

# Porta (0 = aleatória, ou especifique como 8080)
PROXY_PORT=0
```

### 3. Iniciar o Servidor

```bash
./start.sh
```

Você verá algo como:

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

---

## 📡 Endpoints Disponíveis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Health check básico |
| `/health` | GET | Status detalhado do servidor |
| `/facebook-ads/proxy` | POST | **Proxy principal** - faz chamadas para Meta API |
| `/facebook-ads/history` | GET | Retorna histórico de chamadas |
| `/facebook-ads/stats` | GET | Estatísticas de uso |
| `/docs` | GET | Documentação Swagger UI interativa |

---

## 💡 Como Usar

### Request Básico

```bash
curl -X POST http://localhost:XXXXX/facebook-ads/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/v24.0/act_123456/campaigns",
    "method": "GET"
  }'
```

### Com Parâmetros

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

### Criar Campanha

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

### Buscar Insights

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

---

## 📦 Formato de Request/Response

### Request

```json
{
  "endpoint": "/v24.0/act_123456/campaigns",
  "method": "POST",
  "body": {
    "name": "Minha Campanha",
    "objective": "OUTCOME_SALES"
  },
  "params": {
    "fields": "id,name,status"
  }
}
```

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `endpoint` | string | ✅ Sim | Endpoint da Meta API (ex: `/v24.0/act_123456/campaigns`) |
| `method` | string | Não | Método HTTP (GET, POST, DELETE, PUT, PATCH). Default: `GET` |
| `body` | object | Não | Corpo da requisição (para POST, PUT, PATCH) |
| `params` | object | Não | Query parameters (para GET) |

### Response

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

| Campo | Descrição |
|-------|-----------|
| `success` | `true` se status < 400, `false` caso contrário |
| `data` | Dados retornados pela Meta API |
| `meta.timestamp` | Timestamp da resposta |
| `meta.request_id` | ID único da requisição (para rastreamento) |
| `meta.facebook_status` | Status code retornado pelo Facebook |
| `meta.duration_ms` | Tempo total da requisição em ms |

---

## 📊 Histórico de Chamadas

Todas as requisições são automaticamente salvas no SQLite.

### Via API

```bash
curl http://localhost:XXXXX/facebook-ads/history
```

Response:
```json
{
  "calls": [
    {
      "id": 1,
      "request_id": "req_abc12345",
      "timestamp": "2026-01-12T16:10:08.349323",
      "endpoint": "/v24.0/act_123456/campaigns",
      "method": "GET",
      "body_summary": "name=Black Friday",
      "response_status": 200,
      "duration_ms": 245.5,
      "created_at": "2026-01-12 20:10:08"
    }
  ]
}
```

### Via SQLite Direto

```bash
sqlite3 data/history.db

# Ver todas as chamadas
SELECT * FROM calls ORDER BY id DESC LIMIT 10;

# Ver apenas erros
SELECT * FROM calls WHERE response_status >= 400;

# Estatísticas
SELECT
  COUNT(*) as total,
  AVG(duration_ms) as avg_duration,
  SUM(CASE WHEN response_status >= 400 THEN 1 ELSE 0 END) as errors
FROM calls;
```

---

## 🤖 USANDO COM CLAUDE CODE AGENTS

Esta é a **forma mais poderosa** de usar o Facebook Ads Proxy API. Você tem agents especializados que automatizam tarefas complexas sem nunca expor suas credenciais.

---

### 🎯 O Que São Claude Code Agents?

**Agents** são especialistas automatizados que você pode "contratar" para fazer tarefas específicas. Eles:

- 🎯 **Entendem linguagem natural** - você pede em português
- 🔧 **Executam tarefas complexas** - criam campanhas, geram relatórios, etc.
- 🔐 **NUNCA veem suas credenciais** - usam este proxy como intermediário
- 📊 **Retornam resultados formatados** - relatórios prontos, insights, etc.

---

### 📋 Seus Agents Disponíveis

Você tem **2 agents** especializados em Facebook Ads:

#### 1. Facebook Ads Operator (Agent)
**Localização:** `~/.claude/agents/facebook-ads-agent/`

**O que faz:**
- ✅ Cria campanhas de anúncios
- ✅ Cria ad sets com targeting
- ✅ Cria e gerencia anúncios
- ✅ Pausa, atualiza ou deleta campanhas
- ✅ Monitora performance

**Exemplos de uso:**
```
"Cria uma campanha chamada 'Black Friday' com objetivo de vendas"
"Cria um ad set com budget de $500, targeting Brasil e maiores de 18"
"Me mostra o performance dos últimos 7 dias da campanha 123"
"Pausa a campanha 'Black Friday'"
```

---

#### 2. Facebook Ads Reports Generator (Agent)
**Localização:** `~/.claude/agents/facebook-ads-reports-agent/`

**O que faz:**
- ✅ Gera relatórios automáticos completos
- ✅ Analisa todas as campanhas, ad sets e ads
- ✅ Calcula métricas avançadas (ROI, ROAS, CPA, CTR)
- ✅ Identifica top performers e underperformers
- ✅ Gera recomendações acionáveis

**Exemplos de uso:**
```
"Gera relatório dos últimos 7 dias"
"Analisa em detalhe a campanha Black Friday"
"Compara últimos 7 dias com 7 dias anteriores"
"Quais são as campanhas com pior performance?"
```

---

### 🚀 Como Usar os Agents

#### Passo 1: Iniciar o Proxy

**PRIMEIRO**, sempre inicie o proxy:

```bash
cd /Users/jairflores/Downloads/agents/facebook-ads-proxy
./start.sh
```

Aguarde o mensagem com a porta (ex: `http://localhost:63309`).

#### Passo 2: Usar o Agent

No Claude Code, simplesmente converse em português:

```
Você: "Gera relatório dos últimos 7 dias"
```

O Agent automaticamente:
1. ✅ Descobre a porta do proxy
2. ✅ Lista todas as campanhas
3. ✅ Busca insights de cada uma
4. ✅ Calcula métricas (ROI, ROAS, CPA)
5. ✅ Identifica top/bottom performers
6. ✅ Gera relatório markdown profissional
7. ✅ Salva em `~/.claude/reports/facebook-ads/`

**Resultado:**
```markdown
# Facebook Ads Report - 2026-01-13

## 📊 Overview
| Total Spend | $5,234.56 |
| Conversions | 234 |
| ROI | 245% |

## 🏆 Top 5 Campanhas
1. Black Friday - ROI: 450%
2. Summer Sale - ROI: 320%
...

## 💡 Recomendações
- ✅ Black Friday: aumentar budget
- ❌ Test Campaign: pausar (0 conversões)
```

---

### 🎓 Exemplos Completos de Uso

#### Criar Campanha Completa

```
Você: "Cria uma campanha completa para Black Friday"

Claude Agent:
1. Cria a campanha (status: PAUSED)
2. Cria um ad set com targeting Brasil
3. Cria um criativo com imagem
4. Cria o anúncio
5. Mostra: "✅ Campanha criada! ID: 23843663654630"
   "Use este comando para ativar: ..."
```

---

#### Analisar Performance

```
Você: "Qual campanha está dando melhor ROI?"

Claude Agent:
1. Busca insights de todas as campanhas
2. Calcula ROI de cada uma
3. Mostra ranking completo:
   "🏆 Melhor ROI: Black Friday (450%)"
   "   Pior ROI: Test Campaign (0%)"
```

---

#### Relatório Comparativo

```
Você: "Compara esta semana com semana passada"

Claude Agent:
1. Busca insights dos últimos 7 dias
2. Busca insights de 7 dias atrás
3. Calcula diferenças
4. Gera relatório:
   "📈 Spend: +15%"
   "📈 Conversions: +23%"
   "📉 CPA: -8% (melhorou!)"
```

---

### 🔧 Skills Disponíveis

Seus agents usam **Skills** para consultar documentação da Meta API:

| Skill | Descrição |
|-------|-----------|
| **Meta Ads API v24.0 Reference** | Documentação completa para criar campanhas, ad sets, anúncios |
| **Facebook Ads Reports Expert** | Referência de insights, métricas e relatórios |

As skills garantem que os agents sempre usam os endpoints corretos e parâmetros válidos.

---

### 📖 Documentação Completa

Para mais detalhes sobre agents e skills, consulte:

**Guia Completo:** `~/.claude/docs/AGENTS-AND-SKILLS-GUIDE.md`

Este guia contém:
- Documentação completa de todos os agents
- Documentação completa de todas as skills
- Como configurar cada um
- Exemplos de uso avançados
- Troubleshooting

---

### ✅ Checklist de Uso

Antes de usar os agents:

1. **[ ] Proxy rodando?**
   ```bash
   cd /Users/jairflores/Downloads/agents/facebook-ads-proxy
   ./start.sh
   ```

2. **[ ] Credenciais configuradas?**
   ```bash
   # Edite o .env do proxy com suas credenciais reais
   nano .env
   ```

3. **[ ] Agent adicionado?**
   ```
   No Claude Code, o agent deve estar ativo automaticamente
   ```

4. **[ ] Faça seu pedido em português!**
   ```
   "Gera relatório dos últimos 30 dias"
   "Cria campanha para Natal"
   "Qual ad set está com pior CTR?"
   ```

---

## 🛠️ Troubleshooting

### Erro: "Arquivo .env não encontrado"

```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

### Erro: "Invalid OAuth access token"

Seu `FACEBOOK_API_KEY` expirou ou é inválido. Gere um novo token em:
https://developers.facebook.com/tools/accesstoken/

### Erro: "Port already in use"

Mude `PROXY_PORT=0` para uma porta específica no `.env`:
```bash
PROXY_PORT=8080
```

### Erro: "Proxy não encontrado" (no Agent)

**Solução:**
```bash
# Inicie o proxy primeiro
cd /Users/jairflores/Downloads/agents/facebook-ads-proxy
./start.sh
```

### Verificar se o servidor está rodando

```bash
# Health check
curl http://localhost:XXXXX/

# Ou ver documentação
# Abra no navegador: http://localhost:XXXXX/docs
```

---

## 📁 Estrutura do Projeto

```
facebook-ads-proxy/
├── src/
│   ├── main.py              # Entry point, FastAPI app
│   ├── config.py            # Carrega configurações do .env
│   ├── models/
│   │   └── schemas.py       # Pydantic models (Request/Response)
│   ├── routes/
│   │   └── proxy.py         # Endpoints da API
│   └── services/
│       ├── facebook_client.py  # Cliente HTTP para Meta API
│       └── history.py          # Serviço de histórico SQLite
├── data/
│   └── history.db           # SQLite (criado automaticamente)
├── venv/                    # Virtual environment Python
├── .env                     # Credenciais (NÃO commitar)
├── .env.example             # Template de credenciais
├── .gitignore               # Ignora .env, *.db, venv
├── requirements.txt         # Dependências Python
├── start.sh                 # Script para iniciar a API
└── README.md                # Esta documentação
```

---

## 📚 Documentação Completa

Além deste README, o projeto possui documentação detalhada:

| Arquivo | Descrição |
|---------|-----------|
| **[GUIDE.md](GUIDE.md)** | 📖 Guia completo de instalação, configuração e uso |
| **[AGENTS.md](AGENTS.md)** | 🤖 Integração com Claude Code Agents |
| **[EXAMPLES.md](EXAMPLES.md)** | 💡 Exemplos práticos (curl, Python scripts) |
| **[CHANGELOG.md](CHANGELOG.md)** | 📝 Histórico de versões e roadmap |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | 🤝 Guia para contribuidores |

### 📖 Guia Rápido

- **Novo no projeto?** Comece pelo [GUIDE.md](GUIDE.md)
- **Usando Claude Code?** Veja [AGENTS.md](AGENTS.md)
- **Precisa de exemplos?** Consulte [EXAMPLES.md](EXAMPLES.md)
- **Quer contribuir?** Leia [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🔐 Segurança

- ✅ Credenciais **nunca** são expostas para o Agent
- ✅ `.env` está no `.gitignore` (não vai para o Git)
- ✅ Servidor roda apenas em `127.0.0.1` (localhost)
- ✅ Histórico salvo localmente (SQLite)

---

## 📝 Licença

MIT

---

## 🤝 Contribuindo

Este é um projeto privado para automação de Facebook Ads. Sinta-se livre para adaptar para suas necessidades.

---

## 📞 Links Úteis

- **GitHub:** https://github.com/userj81/Facebook-Ads-Proxy-API
- **Guia de Agents/Skills:** `~/.claude/docs/AGENTS-AND-SKILLS-GUIDE.md`
- **Meta API Docs:** https://developers.facebook.com/docs/marketing-api/

---

**Versão:** 1.0.0
**API Meta:** v24.0
**Python:** 3.10+
