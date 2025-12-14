#!/bin/bash
# Script para build da imagem Docker

echo "🔨 Building PSI AI API Docker image..."

# Build da imagem
docker build -t psi-ai-api:latest .

if [ $? -eq 0 ]; then
    echo "✅ Build concluído com sucesso!"
    echo ""
    echo "Para executar localmente:"
    echo "  docker run -p 8000:8000 --env-file .env psi-ai-api:latest"
    echo ""
    echo "Ou use docker-compose:"
    echo "  docker-compose up -d"
else
    echo "❌ Erro no build"
    exit 1
fi
