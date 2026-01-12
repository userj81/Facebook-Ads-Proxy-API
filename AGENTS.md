# Facebook Ads Proxy API - Integração com Claude Code Agents

> **Guia completo para usar o Facebook Ads Proxy API com Claude Code Agents**

---

## Índice

1. [O que são Claude Code Agents](#o-que-são-claude-code-agents)
2. [Arquitetura da Integração](#arquitetura-da-integração)
3. [Agents Disponíveis](#agents-disponíveis)
4. [Instalação dos Agents](#instalação-dos-agents)
5. [Configuração](#configuração)
6. [Uso Prático](#uso-prático)
7. [Exemplos de Workflows](#exemplos-de-workflows)
8. [Troubleshooting](#troubleshooting)

---

## O que são Claude Code Agents

**Claude Code Agents** são especializações do Claude Code que automatizam tarefas específicas. Eles entendem linguagem natural e executam operações complexas de forma autônoma.

### Benefícios de Usar Agents

| Benefício | Descrição |
|-----------|-----------|
| 🎯 **Linguagem Natural** | Faça pedidos em português |
| 🔧 **Automação Completa** | Agents executam tarefas complexas |
| 🔐 **Segurança** | Nunca acessam suas credenciais |
| 📊 **Resultados Formatados** | Relatórios e insights prontos |
| ⚡ **Eficiência** | Executam múltiplas operações |

---

## Arquitetura da Integração

### Fluxo de Dados com Agents

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Agent                        │
│                                                             │
│  1. Entende pedido em linguagem natural                     │
│  2. Decide quais operações executar                         │
│  3. Descobre porta do proxy automaticamente                 │
│                                                             │
│  Faz request LOCAL (sem ver credenciais):                  │
│  POST http://localhost:PORTA/facebook-ads/proxy            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  FACEBOOK ADS PROXY API                     │
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
└─────────────────────────────────────────────────────────────┘
```

### Descoberta Automática de Porta

Os agents usam este script para descobrir a porta do proxy:

```bash
# Tenta descobrir pelo processo
PROXY_PORT=$(ps aux | grep "python -m src.main" | grep -v grep | sed -n 's/.*.*:\([0-9]*\) .*/\1/p' | head -1)

# Se não encontrar, tenta portas comuns
if [ -z "$PROXY_PORT" ]; then
  for port in 8080 8081 8082 8100 8200; do
    if curl -s http://localhost:$port/health > /dev/null 2>&1; then
      PROXY_PORT=$port
      break
    fi
  done
fi
```

---

## Agents Disponíveis

### 1. Facebook Ads Operator

**Localização:** `~/.claude/agents/facebook-ads-agent/`

**Versão:** 2.0 (Proxy-Enabled)

#### O que faz

- ✅ Cria campanhas de anúncios
- ✅ Cria ad sets com targeting
- ✅ Cria e gerencia anúncios
- ✅ Pausa, atualiza ou deleta campanhas
- ✅ Monitora performance
- ✅ Extrai insights e relatórios

#### Exemplos de Uso

```
"Cria uma campanha chamada 'Black Friday' com objetivo de vendas"
"Cria um ad set com budget de $500, targeting Brasil e maiores de 18"
"Me mostra o performance dos últimos 7 dias da campanha 123"
"Pausa a campanha 'Black Friday'"
"Ativa todas as campanhas pausadas"
```

#### Estrutura do Agent

```
~/.claude/agents/facebook-ads-agent/
├── Agent.md              # Definição principal do agent
├── README.md             # Documentação
├── setup-api.sh          # Script de setup
└── operations.json       # Registro de operações
```

---

### 2. Facebook Ads Reports Generator

**Localização:** `~/.claude/agents/facebook-ads-reports-agent/`

**Versão:** 2.0 (Proxy-Enabled)

#### O que faz

- ✅ Gera relatórios automáticos completos
- ✅ Analisa todas as campanhas, ad sets e ads
- ✅ Calcula métricas avançadas (ROI, ROAS, CPA, CTR)
- ✅ Identifica top performers e underperformers
- ✅ Gera recomendações acionáveis
- ✅ Compara períodos diferentes

#### Exemplos de Uso

```
"Gera relatório dos últimos 7 dias"
"Analisa em detalhe a campanha Black Friday"
"Compara últimos 7 dias com 7 dias anteriores"
"Quais são as campanhas com pior performance?"
"Me mostre os 5 anúncios com melhor CTR"
```

#### Estrutura do Agent

```
~/.claude/agents/facebook-ads-reports-agent/
├── Agent.md              # Definição principal do agent
├── README.md             # Documentação
├── generate-report.sh    # Script de geração
├── test-insights.sh      # Script de teste
└── operations.json       # Registro de operações
```

---

## Instalação dos Agents

### Pré-requisitos

1. **Claude Code instalado**
2. **Facebook Ads Proxy API configurado e rodando**
3. **Credenciais configuradas no .env do proxy**

### Passo 1: Verificar Proxy

```bash
cd /caminho/para/facebook-ads-proxy
./start.sh
```

### Passo 2: Adicionar Agents no Claude Code

Os agents devem ser colocados no diretório `~/.claude/agents/`. Você pode:

1. **Clonar do repositório** (se disponível)
2. **Criar manualmente** copiando os arquivos Agent.md

### Passo 3: Verificar Instalação

No Claude Code:

```bash
/agent list
```

Você deve ver:
- `facebook-ads-agent`
- `facebook-ads-reports-agent`

---

## Configuração

### Configuração do Proxy

Edite o arquivo `.env` do proxy:

```bash
# /caminho/para/facebook-ads-proxy/.env

FACEBOOK_API_KEY=EAAxxxxxxxxxxxx...
FACEBOOK_ACCOUNT_ID=act_123456789
FACEBOOK_API_VERSION=v24.0
PROXY_PORT=0  # Aleatória recomendado
```

### Configuração dos Agents

**Não é necessário configurar variáveis de ambiente!**

Os agents:
- Descobrem a porta do proxy automaticamente
- Usam apenas chamadas locais (localhost)
- Nunca acessam as credenciais diretamente

---

## Uso Prático

### Passo a Passo Completo

#### 1. Iniciar o Proxy

```bash
cd /Users/jairflores/Downloads/agents/facebook-ads-proxy
./start.sh
```

**Saída esperada:**
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

#### 2. Abrir o Claude Code

```bash
claude
```

#### 3. Fazer Pedidos em Linguagem Natural

**No Claude Code:**

```
Você: "Gera relatório dos últimos 7 dias"
```

**O Agent automaticamente:**
1. Descobre a porta do proxy (63309)
2. Lista todas as campanhas via proxy
3. Busca insights de cada campanha
4. Calcula métricas (ROI, ROAS, CPA)
5. Identifica top/bottom performers
6. Gera relatório markdown profissional
7. Salva em `~/.claude/reports/facebook-ads/`

#### 4. Resultado

```markdown
# Facebook Ads Report - 2026-01-13

## 📊 Overview
| Métrica | Valor |
|---------|-------|
| Total Spend | $5,234.56 |
| Impressions | 234,567 |
| Clicks | 12,345 |
| Conversions | 234 |
| CPC | $0.42 |
| ROI | 245% |

## 🏆 Top 5 Campanhas
1. Black Friday - ROI: 450%
2. Summer Sale - ROI: 320%
3. ...
```

---

## Exemplos de Workflows

### Workflow 1: Criar Campanha Completa

```
Você: "Cria uma campanha completa para Black Friday"

Claude Agent:
1. ✅ Cria a campanha (status: PAUSED)
   - ID: 23843663654630

2. ✅ Cria um ad set com targeting Brasil
   - ID: 23843663654631
   - Budget: $50/dia
   - Público: Brasil, 18-65 anos

3. ✅ Cria um criativo
   - ID: 23843663654632

4. ✅ Cria o anúncio
   - ID: 23843663654633
   - Status: PAUSED

5. 📋 Mostra resumo:
   "✅ Campanha criada com sucesso!"
   "📦 Campaign ID: 23843663654630"
   "⚠️ Status: PAUSED (para revisão)"
   "🚀 Para ativar, use:"
   "POST /facebook-ads/proxy {\"endpoint\": \"/v24.0/23843663654630\", \"method\": \"PATCH\", \"body\": {\"status\": \"ACTIVE\"}}"
```

---

### Workflow 2: Análise Comparativa

```
Você: "Compara esta semana com semana passada"

Claude Agent:
1. ✅ Busca insights dos últimos 7 dias
2. ✅ Busca insights de 7-14 dias atrás
3. ✅ Calcula diferenças
4. ✅ Gera relatório comparativo

📊 Resultado:
┌────────────────┬────────────┬────────────┬──────────┐
│ Métrica        │ Esta Semana│ Semana Pass│ Δ        │
├────────────────┼────────────┼────────────┼──────────┤
│ Spend          │ $1,234.56  │ $1,073.45  │ +15% 📈  │
│ Conversions    │ 89         │ 72         │ +24% 📈  │
│ CPA            │ $13.87     │ $14.91     │ -7% 📉   │
│ ROI            | 245%       │ 198%       │ +47% 📈  │
└────────────────┴────────────┴────────────┴──────────┘
```

---

### Workflow 3: Otimização Automática

```
Você: "Pausa todas as campanhas com ROI negativo"

Claude Agent:
1. ✅ Lista todas as campanhas ativas
2. ✅ Busca insights de cada uma (últimos 7 dias)
3. ✅ Calcula ROI de cada campanha
4. ✅ Identifica campanhas com ROI < 0
5. ✅ Confirma com usuário: "Encontrei 3 campanhas com ROI negativo. Deseja pausar?"
6. ✅ Pausa as campanhas confirmadas

📋 Relatório:
⚠️ Camp 1: "Test Campaign" - ROI: -45% → PAUSADO
⚠️ Camp 2: "Old Promo" - ROI: -12% → PAUSADO
⚠️ Camp 3: "Expired" - ROI: -8% → PAUSADO
```

---

## Troubleshooting

### Erro: "Proxy não encontrado"

**Sintoma:**
```
⚠️ Facebook Ads Proxy não está rodando!
```

**Solução:**
```bash
# Inicie o proxy
cd /caminho/para/facebook-ads-proxy
./start.sh
```

---

### Erro: "success: false" na resposta do proxy

**Causas comuns:**

1. **Token expirado**
   ```bash
   # Atualize o .env do proxy com novo token
   nano /caminho/para/facebook-ads-proxy/.env
   ```

2. **Permissões insuficientes**
   ```bash
   # Verifique se o token tem as permissões:
   # - ads_management
   # - ads_read
   # - read_insights
   ```

3. **Parâmetros inválidos**
   ```bash
   # Consulte a documentação da Meta API
   # Ou use a Skill "Meta Ads API v24.0 Reference"
   ```

---

### Erro: "Agent não responde"

**Solução:**
```bash
# 1. Verifique se o agent está ativo
/agent list

# 2. Verifique se o proxy está rodando
curl http://localhost:XXXXX/health

# 3. Verifique o histórico do proxy
curl http://localhost:XXXXX/facebook-ads/history
```

---

### Performance Lenta

**Sintoma:** Agent demora muito para responder

**Causas:**

1. **Muitas requisições**
   - O agent pode estar fazendo muitas chamadas
   - Meta API tem rate limit de 200 req/min

2. **Grande período de dados**
   - `lifetime` pode ser muito lento
   - Use `last_30d` ou menor

**Solução:**
```
# Em vez de:
"Gera relatório lifetime"

# Use:
"Gera relatório dos últimos 30 dias"
```

---

## Skills Relacionadas

Os agents usam **Skills** para consultar documentação:

| Skill | Descrição |
|-------|-----------|
| **Meta Ads API v24.0 Reference** | Documentação completa para criar campanhas, ad sets, anúncios |
| **Facebook Ads Reports Expert** | Referência de insights, métricas e relatórios |

As skills garantem que os agents sempre usem os endpoints corretos e parâmetros válidos.

---

## Referências

- **Proxy README:** [README.md](README.md)
- **Guia Completo:** [GUIDE.md](GUIDE.md)
- **Exemplos:** [EXAMPLES.md](EXAMPLES.md)
- **Meta API Docs:** https://developers.facebook.com/docs/marketing-api/
- **Claude Code Docs:** https://docs.anthropic.com/claude-code

---

**Versão:** 2.0 (Proxy-Enabled)
**API Meta:** v24.0
**Última atualização:** 2026-01-13
