# Changelog

All notable changes to the Facebook Ads Proxy API project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Rate limiting configurável
- Suporte para múltiplas contas de anúncios
- Cache de respostas
- Métricas avançadas de uso

---

## [1.0.0] - 2026-01-13

### Added

#### Core Features
- **Proxy Server** - FastAPI server para Meta Marketing API v24.0
- **Credential Protection** - Credenciais isoladas em arquivo `.env`
- **Auto Port Discovery** - Porta aleatória automática para evitar conflitos
- **SQLite History** - Histórico automático de todas as chamadas
- **CORS Middleware** - Suporte a requisições de qualquer origem local
- **Swagger UI** - Documentação interativa em `/docs`

#### Endpoints
- `GET /` - Health check básico
- `GET /health` - Status detalhado do servidor
- `POST /facebook-ads/proxy` - **Proxy principal** para Meta API
- `GET /facebook-ads/history` - Histórico de chamadas
- `GET /facebook-ads/stats` - Estatísticas de uso

#### Configuration
- Suporte a `.env` com variáveis de ambiente
- Configuração de porta (aleatória ou fixa)
- Configuração de versão da API
- Template `.env.example` para fácil setup

#### Documentation
- **README.md** - Documentação principal com visão geral e quick start
- **GUIDE.md** - Guia detalhado de instalação e uso
- **AGENTS.md** - Documentação de integração com Claude Code Agents
- **EXAMPLES.md** - Exemplos práticos de uso da API
- **CHANGELOG.md** - Registro de mudanças (este arquivo)
- **CONTRIBUTING.md** - Guia para contribuidores

#### Scripts
- `start.sh` - Script para iniciar o servidor com setup automático

#### Claude Code Integration
- Suporte para **Facebook Ads Operator Agent** (v2.0)
- Suporte para **Facebook Ads Reports Generator Agent** (v2.0)
- Auto-descoberta de porta do proxy pelos agents
- Exemplos de uso com linguagem natural

#### Security
- `.env` no `.gitignore` (nunca commitado)
- Servidor roda apenas em `127.0.0.1` (localhost)
- Histórico salvo localmente (SQLite)
- Suporte a tokens de longa duração

---

## [0.1.0] - 2026-01-12

### Added
- Initial project structure
- FastAPI setup
- Basic proxy functionality
- SQLite integration

---

## Versões Future

### Roadmap

#### [1.1.0] - Planejado
- Batch requests API
- Retry automático com exponential backoff
- Timeout configurável por request
- Rate limiting configurável
- Métricas de performance avançadas

#### [1.2.0] - Planejado
- Webhook support
- Event streaming
- Real-time insights
- Multi-account support

#### [2.0.0] - Planejado
- Dashboard web UI
- User authentication
- Role-based access control
- API key management
- Usage analytics

---

## Tipos de Mudanças

- `Added` - Novas funcionalidades
- `Changed` - Mudanças em funcionalidades existentes
- `Deprecated` - Funcionalidades que serão removidas
- `Removed` - Funcionalidades removidas
- `Fixed` - Correções de bugs
- `Security` - Melhorias de segurança

---

## Links

- **Repositório:** https://github.com/userj81/Facebook-Ads-Proxy-API
- **Issues:** https://github.com/userj81/Facebook-Ads-Proxy-API/issues
- **Releases:** https://github.com/userj81/Facebook-Ads-Proxy-API/releases

---

**Meta API Version:** v24.0
**Python Version:** 3.10+
**Framework:** FastAPI
