# 📁 Workspace Directory

Esta carpeta está mapeada entre el host y el contenedor de n8n para procesar archivos.

## 📂 Estructura

### `input/`
- Archivos de entrada que n8n guarda para procesar
- Imágenes de tickets/recibos antes de procesamiento

### `output/`
- Archivos procesados listos para usar
- Imágenes mejoradas después del procesamiento

### `temp/`
- Archivos temporales durante el procesamiento
- Se puede limpiar periódicamente

## 🔄 Flujo Típico

1. **N8N Write Binary File** → Guarda en `input/`
2. **N8N Execute Command** → Procesa de `input/` a `output/`
3. **N8N Read Binary File** → Lee desde `output/`

## 🐛 Debug

Desde el host puedes acceder a:
- `./workspace/input/` - Ver qué archivos está procesando n8n
- `./workspace/output/` - Verificar resultados del procesamiento
- `./workspace/temp/` - Inspeccionar archivos intermedios

## 🧹 Limpieza

```bash
# Limpiar archivos temporales
rm -rf ./workspace/temp/*

# Limpiar todo (cuidado!)
rm -rf ./workspace/input/* ./workspace/output/* ./workspace/temp/*
```