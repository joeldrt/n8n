#!/bin/bash

echo "🚀 Iniciando n8n con nodos de la comunidad..."

# Asegurar que el directorio .n8n existe y tiene permisos correctos
mkdir -p /home/node/.n8n
chown -R node:node /home/node/.n8n

# Cambiar a usuario node para instalar nodos
su - node -c "/opt/install-community-nodes.sh"

echo "🎯 Iniciando n8n..."
# Ejecutar n8n con el comando original
exec gosu node tini -- /docker-entrypoint.sh "$@"