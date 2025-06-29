# 🛠️ Runtime Scripts

Scripts ejecutables desde workflows de n8n usando nodos Execute Command.

## 📍 Ubicación en Contenedor
Estos scripts están montados en `/runtime-scripts/` dentro del contenedor de n8n.

## 📝 Scripts Disponibles

### `image-processor.sh`
Script principal para procesamiento de imágenes usando ImageMagick.

**Uso:**
```bash
/scripts/image-processor.sh <input_file> <output_file> [mode]
```

**Modos disponibles:**
- `enhance` - Mejora contraste, brillo y nitidez
- `denoise` - Reduce ruido y suaviza imagen
- `ocr-prep` - Optimiza para OCR (escala grises, alto contraste)
- `auto` - Secuencia automática de mejoras (default)

## 🎯 Uso desde N8N

### Execute Command Node
```bash
/runtime-scripts/image-processor.sh /workspace/input/ticket.jpg /workspace/output/enhanced.jpg auto
```

### Flujo Típico en N8N

1. **Write Binary File Node**
   - Input: imagen del telegram/webhook
   - Output: `/workspace/input/ticket_{{ $json.timestamp }}.jpg`

2. **Execute Command Node**
   - Command: `/runtime-scripts/image-processor.sh /workspace/input/ticket_{{ $json.timestamp }}.jpg /workspace/output/enhanced_{{ $json.timestamp }}.jpg auto`

3. **Read Binary File Node**
   - Input: `/workspace/output/enhanced_{{ $json.timestamp }}.jpg`
   - Output: imagen mejorada para OCR

## 📊 Ejemplos de Comandos

### Mejorar contraste para ticket borroso
```bash
/runtime-scripts/image-processor.sh /workspace/input/ticket.jpg /workspace/output/clear.jpg enhance
```

### Preparar para OCR (máxima legibilidad)
```bash
/runtime-scripts/image-processor.sh /workspace/input/receipt.png /workspace/output/ocr_ready.png ocr-prep
```

### Reducir ruido en imagen con mala calidad
```bash
/runtime-scripts/image-processor.sh /workspace/input/noisy.jpg /workspace/output/clean.jpg denoise
```

### Procesamiento automático (recomendado)
```bash
/runtime-scripts/image-processor.sh /workspace/input/ticket.jpg /workspace/output/processed.jpg auto
```

## 🔧 Personalización

Para crear scripts personalizados:
1. Crear nuevo script en `./runtime-scripts/` (host)
2. Usar ImageMagick (`magick` command)
3. Hacer ejecutable: `chmod +x script.sh`
4. Usar desde Execute Command en n8n: `/runtime-scripts/script.sh`

## 📋 Herramientas Disponibles

- **ImageMagick** (`magick`) - Procesamiento de imágenes
- **ExifTool** (`exiftool`) - Metadatos de imágenes
- **File** (`file`) - Identificación de tipos de archivo
- **Bash** - Shell scripting avanzado