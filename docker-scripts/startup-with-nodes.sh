#!/bin/bash

echo "🚀 Iniciando n8n con nodos de la comunidad..."

# Crear directorio de nodos si no existe
mkdir -p /home/node/.n8n/nodes

# Copiar nodos instalados desde temp si no existen
if [ ! -d "/home/node/.n8n/nodes/node_modules/n8n-nodes-tesseractjs" ]; then
    echo "📦 Copiando nodos de la comunidad..."
    cp -r /tmp/community-nodes/* /home/node/.n8n/nodes/
    chown -R node:node /home/node/.n8n/nodes
fi

echo "🎯 Iniciando n8n..."
# Ejecutar n8n con el comando original
exec gosu node tini -- /docker-entrypoint.sh "$@"