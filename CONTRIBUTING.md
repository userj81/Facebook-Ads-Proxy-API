# Contribuindo para Facebook Ads Proxy API

> **Obrigado por considerar contribuir com o Facebook Ads Proxy API!**

---

## Índice

1. [Como Contribuir](#como-contribuir)
2. [Setup do Ambiente de Desenvolvimento](#setup-do-ambiente-de-desenvolvimento)
3. [Padrões de Código](#padrões-de-código)
4. [Processo de Pull Request](#processo-de-pull-request)
5. [Reportando Bugs](#reportando-bugs)
6. [Sugerindo Funcionalidades](#sugerindo-funcionalidades)
7. [Documentação](#documentação)

---

## Como Contribuir

### Maneiras de Contribuir

Existem várias formas de contribuir com o projeto:

| Tipo | Descrição |
|------|-----------|
| 🐛 **Reportar Bugs** | Encontrou um problema? Reporte! |
| 💡 **Sugerir Funcionalidades** | Tem uma ideia? Compartilhe! |
| 📝 **Melhorar Documentação** | Ajude a deixar os docs mais claros |
| 🔧 **Enviar Código** | Corrija bugs ou adicione funcionalidades |
| 🧪 **Escrever Testes** | Aumente a cobertura de testes |
| 🎨 **Melhorar Design** | UX/UI, arquitetura, etc. |

---

## Setup do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.10 ou superior
- pip
- git
- Access Token da Meta API (para testes)

### Passo 1: Fork o Repositório

```bash
# No GitHub, clique em "Fork"
# Clone seu fork
git clone https://github.com/SEU_USUARIO/Facebook-Ads-Proxy-API.git
cd Facebook-Ads-Proxy-API
```

### Passo 2: Configure o Remoto

```bash
# Adiciona o repositório original como upstream
git remote add upstream https://github.com/userj81/Facebook-Ads-Proxy-API.git

# Verifica os remotos
git remote -v
```

### Passo 3: Crie Ambiente Virtual

```bash
# Cria ambiente virtual
python3 -m venv venv

# Ativa ambiente virtual
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### Passo 4: Instale Dependências

```bash
# Instala dependências
pip install -r requirements.txt

# (Opcional) Instala dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### Passo 5: Configure Credenciais de Teste

```bash
# Copia template
cp .env.example .env

# Edita com suas credenciais de teste
nano .env
```

### Passo 6: Execute o Servidor

```bash
python -m src.main
```

---

## Padrões de Código

### Estilo de Código

Seguimos as convenções do **PEP 8**:

```python
# ✅ Bom
def get_campaign(campaign_id: str) -> dict:
    """Retorna dados de uma campanha."""
    url = f"{base_url}/{campaign_id}"
    return requests.get(url).json()


# ❌ Ruim
def GetCampaign(id):
    url=base_url+'/'+id
    return requests.get(url).json()
```

### Type Hints

Use type hints para funções:

```python
from typing import Optional, Dict, Any

def create_campaign(
    name: str,
    objective: str,
    status: str = "PAUSED",
    budget: Optional[int] = None
) -> Dict[str, Any]:
    """Cria uma nova campanha."""
    # ...
```

### Docstrings

Use docstrings estilo Google:

```python
def get_insights(
    object_id: str,
    date_preset: str = "last_7d"
) -> dict:
    """Busca insights de um objeto.

    Args:
        object_id: ID do objeto (campaign, adset, ad).
        date_preset: Período predefinido (default: "last_7d").

    Returns:
        Dicionário com dados de insights.

    Raises:
        ValueError: Se object_id for inválido.
    """
    # ...
```

### Nomes de Variáveis

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Variáveis | snake_case | `campaign_id`, `daily_budget` |
| Constantes | UPPER_CASE | `MAX_RETRIES`, `BASE_URL` |
| Classes | PascalCase | `FacebookClient`, `HistoryService` |
| Funções | snake_case | `get_campaign()`, `create_adset()` |

---

## Processo de Pull Request

### 1. Crie uma Branch

```bash
# Atualiza master
git checkout main
git pull upstream main

# Cria branch para sua feature
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b fix/bug-descricao
```

### 2. Faça suas Mudanças

```bash
# Edite os arquivos
# ...

# Verifique mudanças
git status

# Adicione arquivos
git add .
# ou arquivos específicos
git add src/models/schemas.py
```

### 3. Commit suas Mudanças

```bash
# Commit com mensagem clara
git commit -m "feat: adiciona suporte a batch requests"
```

### Padrão de Mensagens de Commit

Use conventional commits:

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova funcionalidade | `feat: adiciona retry automático` |
| `fix` | Correção de bug | `fix: corrige erro de timeout` |
| `docs` | Mudanças na documentação | `docs: atualiza README.md` |
| `style` | Mudanças de estilo (formato) | `style: formata código com black` |
| `refactor` | Refatoração | `refactor: melhora estrutura de services` |
| `test` | Adiciona ou modifica testes | `test: adiciona testes para history service` |
| `chore` | Tarefas de build/config | `chore: atualiza requirements.txt` |

### 4. Push para seu Fork

```bash
git push origin feature/nova-funcionalidade
```

### 5. Abra Pull Request

1. Vá para: https://github.com/SEU_USUARIO/Facebook-Ads-Proxy-API
2. Clique em "Pull Requests" → "New Pull Request"
3. Preencha o template de PR

### Template de Pull Request

```markdown
## Descrição
Breve descrição das mudanças.

## Tipo de Mudança
- [ ] Bug fix (não quebrad changes)
- [ ] Nova feature (não quebrad changes)
- [ ] Breaking change (fix ou feature que quebrad changes)
- [ ] Documentação

## Testing
Como testar essas mudanças?
```

---

## Reportando Bugs

### Antes de Reportar

1. **Pesquise issues existentes**
   - Use a busca do GitHub
   - Verifique issues fechadas

2. **Verifique se é um bug do proxy ou da Meta API**
   - Teste diretamente na Meta API
   - Veja o status do proxy: `/health`

### Como Reportar

Use o template de bug report:

```markdown
## Descrição
Descrição clara e concisa do bug.

## Passos para Reproduzir
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

## Comportamento Esperado
O que você esperava que acontecesse.

## Comportamento Real
O que realmente aconteceu.

## Ambiente
- OS: [e.g. macOS 14.0]
- Python: [e.g. 3.11.0]
- Versão: [e.g. 1.0.0]

## Logs Relevantes
Cole logs aqui.
```

---

## Sugerindo Funcionalidades

### Antes de Sugerir

1. **Verifique se já existe**
   - Pesquise issues abertas
   - Verifique o roadmap

2. **Pense na utilidade geral**
   - A funcionalidade beneficia outros usuários?
   - É específica demais para um caso de uso?

### Como Sugerir

Use o template de feature request:

```markdown
## Descrição
Descrição clara da funcionalidade sugerida.

## Problema
Qual problema essa funcionalidade resolve?

## Solução Proposta
Como você imagina a solução?

## Alternativas
Quais alternativas você considerou?

## Contexto Adicional
Screenshots, exemplos, mocks, etc.
```

---

## Documentação

### Melhorando a Documentação

A documentação é tão importante quanto o código! Você pode ajudar:

| Tipo | Como Ajudar |
|------|-------------|
| **Correções** | Corrigir erros de gramática, ortografia |
| **Clarificações** | Explicar melhor conceitos confusos |
| **Exemplos** | Adicionar mais exemplos práticos |
| **Traduções** | Traduzir para outros idiomas |
| **Screenshots** | Adicionar capturas de tela |

### Arquivos de Documentação

| Arquivo | Propósito |
|---------|-----------|
| `README.md` | Visão geral e quick start |
| `GUIDE.md` | Guia detalhado de uso |
| `AGENTS.md` | Integração com Claude Code |
| `EXAMPLES.md` | Exemplos práticos |
| `CHANGELOG.md` | Registro de mudanças |
| `CONTRIBUTING.md` | Guia para contribuidores |

### Escrevendo Bons Docs

- **Seja claro e conciso**
- **Use exemplos** (código, curl, etc.)
- **Mantenha atualizado** (quando mudar código, atualize docs)
- **Use formatação** (markdown, tabelas, listas)

---

## Código de Conduta

### Se Respeitoso

- Respeite opiniões diferentes
- Seja construtivo nas críticas
- Aceite feedback com elegância
- Foque no que é melhor para a comunidade

### Não Aceitamos

- Harassment ou linguagem ofensiva
- Ataques pessoais
- Trolling ou comportamento disruptivo
- Comportamento inadequado profissional

---

## Obtenha Ajuda

### Canais de Ajuda

- **GitHub Issues**: Para bugs e features
- **GitHub Discussions**: Para dúvidas e conversas
- **Email**: Para questões privadas

### Antes de Pedir Ajuda

1. Leia a documentação
2. Pesquise issues existentes
3. Tente resolver sozinho
4. Prepare um exemplo mínimo reproduzível

---

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a **Licença MIT**.

---

## Reconhecimento

Contribuidores serão listados no README.md:

```markdown
## Contribuidores

- [@usuario1](https://github.com/usuario1) - Contribuição X
- [@usuario2](https://github.com/usuario2) - Contribuição Y
```

---

**Obrigado por contribuir! 🎉**

---

## Links Úteis

- **Repositório:** https://github.com/userj81/Facebook-Ads-Proxy-API
- **Issues:** https://github.com/userj81/Facebook-Ads-Proxy-API/issues
- **Discussions:** https://github.com/userj81/Facebook-Ads-Proxy-API/discussions
- **Meta API Docs:** https://developers.facebook.com/docs/marketing-api/
