FROM docker.n8n.io/n8nio/n8n:latest

# Cambiar a root para instalar dependencias
USER root

# Instalar herramientas básicas para procesamiento de imágenes
RUN apk update && apk add --no-cache \
    imagemagick \
    exiftool \
    file \
    bash \
    && rm -rf /var/cache/apk/*

# Crear directorio temporal para instalar nodos
WORKDIR /tmp/community-nodes

# Crear package.json inicial
RUN echo '{"name":"n8n-community-nodes","version":"1.0.0","description":"Community nodes for n8n","main":"index.js","dependencies":{}}' > package.json

# Instalar el nodo de la comunidad
RUN npm install n8n-nodes-tesseractjs --save

# Volver al directorio de trabajo original y usuario node
WORKDIR /data
USER node