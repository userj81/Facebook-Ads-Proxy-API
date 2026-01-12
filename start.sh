#!/bin/bash

cd "$(dirname "$0")"

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -q -r requirements.txt

# Verificar .env
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Arquivo .env não encontrado!"
    echo "   Copie .env.example para .env e configure suas credenciais:"
    echo "   cp .env.example .env"
    echo ""
    echo "   Depois edite o .env com suas credenciais:"
    echo "   - FACEBOOK_API_KEY=seu_access_token"
    echo "   - FACEBOOK_ACCOUNT_ID=act_123456789"
    echo ""
    exit 1
fi

# Iniciar API
echo ""
echo "🚀 Iniciando Facebook Ads Proxy API..."
echo ""
python -m src.main
