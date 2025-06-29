#!/bin/bash

# Script para instalar nodos de la comunidad de n8n
# Específicamente: n8n-nodes-tesseractjs

set -e

echo "🔍 Verificando instalación de nodos de la comunidad..."

# Directorio donde n8n busca los nodos
N8N_USER_FOLDER="/home/node/.n8n"
NODES_DIR="$N8N_USER_FOLDER/nodes"

# Crear directorio de nodos si no existe
mkdir -p "$NODES_DIR"

# Función para verificar si un nodo está instalado
check_node_installed() {
    local node_name=$1
    if [ -d "$NODES_DIR/node_modules/$node_name" ]; then
        echo "✅ $node_name ya está instalado"
        return 0
    else
        echo "❌ $node_name no está instalado"
        return 1
    fi
}

# Función para instalar un nodo
install_node() {
    local node_name=$1
    echo "📦 Instalando $node_name..."
    
    cd "$NODES_DIR"
    
    # Inicializar package.json si no existe
    if [ ! -f "package.json" ]; then
        echo "📝 Creando package.json inicial..."
        cat > package.json << EOF
{
  "name": "n8n-community-nodes",
  "version": "1.0.0",
  "description": "Community nodes for n8n",
  "main": "index.js",
  "dependencies": {}
}
EOF
    fi
    
    # Instalar el nodo
    npm install "$node_name" --save
    
    echo "✅ $node_name instalado correctamente"
}

# Lista de nodos de la comunidad a instalar
COMMUNITY_NODES=(
    "n8n-nodes-tesseractjs"
)

# Verificar e instalar cada nodo
for node in "${COMMUNITY_NODES[@]}"; do
    if ! check_node_installed "$node"; then
        install_node "$node"
    fi
done

echo "🎉 Instalación de nodos de la comunidad completada"
echo "🔄 Reinicia n8n para que los nodos estén disponibles"