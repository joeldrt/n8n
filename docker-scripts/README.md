# 🐳 Docker Scripts

Scripts usados durante la construcción y configuración del contenedor Docker.

## 📝 Scripts Disponibles

### `install-community-nodes.sh`
- **Propósito**: Instala nodos de la comunidad durante build
- **Ejecución**: Durante construcción de imagen Docker
- **Modificación**: Editar para agregar nuevos nodos

### `startup-with-nodes.sh`
- **Propósito**: Script de inicio con nodos preinstalados
- **Ejecución**: Al iniciar el contenedor
- **Uso**: Configuración inicial automatizada

### `startup.sh`
- **Propósito**: Script de inicio básico
- **Ejecución**: Al iniciar el contenedor
- **Uso**: Configuración mínima

## ⚠️ Importante

Estos scripts se ejecutan en el **contexto Docker** durante:
- Construcción de la imagen (`docker build`)
- Inicio del contenedor (`docker run`)

**No son accesibles desde n8n workflows** - para eso usar `runtime-scripts/`