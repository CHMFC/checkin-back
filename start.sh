#!/bin/bash

# Script para executar o backend CheckIn

echo "🚀 Iniciando CheckIn Backend..."

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Verificar se as dependências estão instaladas
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
fi

# Verificar se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "⚙️ Criando arquivo .env..."
    cp env.example .env
    echo "⚠️ Configure o arquivo .env com suas credenciais do Supabase"
fi

echo "🔧 Configurações:"
echo "   - Host: 0.0.0.0"
echo "   - Port: 8000"
echo "   - Debug: True"
echo ""

echo "🌐 Iniciando servidor..."
echo "📖 Documentação: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""

# Executar o servidor
python run.py 