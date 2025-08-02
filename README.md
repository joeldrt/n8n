# 🚀 Plataforma N8N Local con Docker

## ¿Qué es esto?

Configuración completa de **n8n** (herramienta de automatización de flujos de trabajo) en tu computadora local usando Docker Compose, con base de datos PostgreSQL y capacidad de recibir webhooks desde internet usando túneles.

## 🎯 Propósito

- **Plataforma base**: Entorno completo de n8n para desarrollo de workflows
- **Base de datos**: PostgreSQL lista para usar en nodos de workflows
- **Conectividad externa**: Túneles para recibir webhooks desde internet
- **Nodos de la comunidad**: Incluye n8n-nodes-tesseractjs para OCR automáticamente

## 📁 Estructura del Proyecto

```
n8n/
├── docker-compose.yml          # Configuración de servicios
├── Dockerfile                  # Imagen personalizada con nodos de la comunidad
├── .env.example               # Plantilla de variables de entorno
├── docker-scripts/            # Scripts para construcción y configuración Docker
│   ├── install-community-nodes.sh
│   ├── startup-with-nodes.sh
│   └── startup.sh
├── runtime-scripts/           # Scripts ejecutables desde n8n workflows
│   ├── image-processor.sh
│   └── README.md
├── workspace/                 # Carpeta de trabajo compartida host ↔ contenedor
│   ├── input/                # Archivos de entrada
│   ├── output/               # Archivos procesados
│   └── temp/                 # Archivos temporales
├── ticket-reader/             # Workflow específico de procesamiento de tickets
│   ├── ControlGastosEfectivoV2.json
│   ├── system_prompt.md
│   └── [otros archivos del workflow]
└── README.md                  # Esta guía
```

## 🛠️ Componentes

- **n8n**: Automatiza tareas conectando diferentes servicios (usa SQLite internamente)
- **Nodos de la comunidad**: Incluye n8n-nodes-tesseractjs para OCR automáticamente
- **PostgreSQL**: Base de datos externa disponible para nodos de PostgreSQL en workflows
- **Docker Compose**: Orquesta múltiples contenedores (n8n + PostgreSQL)
- **Túnel**: Permite que servicios externos envíen datos a tu n8n local

## Requisitos

- Docker y Docker Compose instalados
- Conexión a internet
- 6GB RAM mínimo
- 5GB espacio libre

## Pasos Simples

### 1. Configurar Variables de Entorno

```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita el archivo .env con tu URL de ngrok (ver paso 2)
```

### 2. Configurar Túnel con ngrok

**Paso 1**: Instalar ngrok
1. Ve a [ngrok.com](https://ngrok.com) y crea una cuenta gratuita
2. Descarga ngrok para tu sistema operativo
3. Copia tu token de autenticación y configúralo:
   ```bash
   ngrok config add-authtoken TU_TOKEN_AQUI
   ```

**Paso 2**: Ejecutar ngrok para obtener URL
```bash
ngrok http 5678
```

**Paso 3**: Actualizar archivo .env
Copia la URL HTTPS que ngrok muestra (ej: `https://abcd-1234.ngrok.io`) y actualiza el archivo `.env`:
```bash
WEBHOOK_URL=https://abcd-1234.ngrok.io
```

### 3. Crear Volumen de Docker

```bash
docker volume create postgres_data
docker volume create n8n_data
```

### 4. Levantar los Servicios

```bash
# Primera vez: construir imagen con nodos de la comunidad
docker compose up -d --build

# Arranques posteriores (sin rebuild)
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f

# Detener servicios
docker compose down
```

### 5. Acceder a n8n

Una vez que ambos servicios estén ejecutándose:

1. **Localmente**: http://localhost:5678
2. **Desde internet**: https://abcd-1234.ngrok.io (tu URL de ngrok)

**Primera vez**: n8n te pedirá crear un usuario admin en el primer acceso.

**¡Guarda la URL de ngrok!** Es tu puerta de entrada desde internet.

### 6. Usar la URL para Webhooks

1. En n8n, crea un nodo **Webhook**
2. Copia la URL generada que será similar a:
   ```
   https://abcd-1234.ngrok.io/webhook/tu-webhook-id
   ```
3. Usa esta URL en Google Forms, Typeform, o cualquier servicio externo

### 7. Probar el Webhook

1. Envía datos desde el servicio externo
2. Verifica que n8n recibe los datos
3. Usa nodos de **HTTP Request** para procesar la información

## Comandos Útiles

### Gestión de servicios:
```bash
# Levantar servicios en background
docker compose up -d

# Ver estado de servicios
docker compose ps

# Ver logs
docker compose logs -f n8n
docker compose logs -f postgres

# Detener servicios
docker compose down

# Reiniciar un servicio específico
docker compose restart n8n
```

### Acceso a PostgreSQL (para nodos de n8n):
```bash
# Conectar a PostgreSQL externa
docker compose exec postgres psql -U n8n -d n8n

# Crear bases de datos para workflows
docker compose exec postgres createdb -U n8n mi_base_datos

# Hacer backup de bases de datos
docker compose exec postgres pg_dump -U n8n mi_base_datos > backup.sql
```

### Configuración para nodos PostgreSQL en n8n:
- **Host**: `localhost` (desde tu máquina) o `postgres` (desde otros contenedores)
- **Puerto**: `5432`
- **Usuario**: `n8n`
- **Contraseña**: `n8n_password`
- **Base de datos**: `n8n` (o crear nuevas según necesites)

## Nodos de la Comunidad Incluidos

### n8n-nodes-tesseractjs
- **Funcionalidad**: OCR (Optical Character Recognition) usando Tesseract.js
- **Uso**: Extrae texto de imágenes automáticamente en workflows
- **Instalación**: Se instala automáticamente al construir la imagen Docker

## Herramientas de Procesamiento de Imágenes

### ImageMagick y herramientas shell
- **Funcionalidad**: Procesamiento de imágenes desde scripts shell
- **Uso**: Scripts ejecutables desde nodos Execute Command
- **Instalación**: Se instalan automáticamente al construir la imagen Docker
- **Herramientas incluidas**: 
  - `ImageMagick`: Para procesamiento y manipulación de imágenes
  - `ExifTool`: Para metadatos de imágenes
  - `File`: Para identificación de tipos de archivo
  - `Bash`: Shell avanzado para scripting

## Carpeta de Trabajo Compartida

### `/workspace` - Directorio compartido host ↔ contenedor
- **input/**: Archivos que n8n guarda para procesar
- **output/**: Archivos procesados listos para usar
- **temp/**: Archivos temporales durante procesamiento
- **Debug**: Acceso directo desde host en `./workspace/`

### Agregar más nodos de la comunidad
Para agregar más nodos, edita el archivo `docker-scripts/install-community-nodes.sh` y añade el nombre del paquete npm a la lista `COMMUNITY_NODES`.

### Limpieza (⚠️ borra todos los datos):
```bash
# Eliminar servicios y volúmenes
docker compose down -v

# Eliminar imágenes también
docker compose down -v --rmi all
```

## ⚠️ Importante

- El túnel es **SOLO para desarrollo y pruebas**
- **NO usar en producción** por seguridad
- Para producción, usar servidor público con dominio y SSL

## Solución de Problemas

### Si n8n no inicia:
1. Verifica que Docker esté corriendo
2. Asegúrate de que el puerto 5678 esté libre
3. Reinicia Docker Desktop

### Si ngrok no funciona:
1. Verifica que tu token de autenticación esté configurado correctamente
2. Asegúrate de que ngrok esté ejecutándose en otra terminal
3. Copia exactamente la URL HTTPS que muestra ngrok
4. No uses la URL HTTP, siempre usa HTTPS

### Si los webhooks siguen sin funcionar:
1. Verifica que hayas usado la variable `-e WEBHOOK_URL` al reiniciar n8n
2. La URL debe ser exactamente la que muestra ngrok
3. Reinicia completamente n8n después de obtener la URL de ngrok

### Si los webhooks no responden:
1. Verifica que usaste la URL completa del túnel
2. Asegúrate de que el nodo Webhook esté activado
3. Revisa los logs de n8n en la terminal

## Ejemplos de Flujos

### Flujo Básico
1. **Webhook** → recibe datos externos
2. **Set** → procesa/transforma datos  
3. **HTTP Request** → envía a otro servicio
4. **Email** → notifica resultados

### Flujo de Procesamiento de Imágenes
1. **Telegram/Webhook** → recibe imagen de ticket
2. **Write Binary File** → guarda en `/workspace/input/`
3. **Execute Command** → procesa imagen con script
4. **Read Binary File** → lee imagen mejorada
5. **OCR/Analysis** → extrae datos del ticket

## 🎫 Workflows Incluidos

### Ticket Reader Agent
En la carpeta `ticket-reader/` encontrarás un workflow completo para procesamiento OCR de tickets/recibos:
- Procesamiento inteligente de imágenes con GPT-4o
- **Nuevo**: Mejora de imágenes con scripts shell antes del OCR
- Almacenamiento estructurado en PostgreSQL
- Análisis de gastos y detección de duplicados
- Carpeta de trabajo compartida para debug
- Consulta la documentación específica en `ticket-reader/README.md`

### Scripts de Procesamiento
En la carpeta `runtime-scripts/` encontrarás herramientas para mejorar imágenes:
- `image-processor.sh` - Script principal con múltiples modos
- Mejora de contraste, reducción de ruido, optimización para OCR
- Ejecutables desde nodos Execute Command
- Consulta la documentación en `runtime-scripts/README.md`

## 📚 Próximos Pasos

Una vez que tengas n8n funcionando:

1. **Explora la plataforma**: Navega por los nodos disponibles
2. **Prueba el workflow incluido**: Importa y configura el Ticket Reader Agent
3. **Crea tus propios flujos**: Conecta servicios que uses frecuentemente
4. **Para producción**: Considera un servidor en la nube con dominio propio

---

**Fuente**: Tutorial basado en el artículo de Bonface Alfonce en Medium
