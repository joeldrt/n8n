#!/bin/bash

# image-processor.sh
# Script para procesar imágenes de tickets/recibos usando ImageMagick
# Uso: ./image-processor.sh <input_file> <output_file> [mode]

set -e  # Salir si hay error

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 <input_file> <output_file> [mode]"
    echo ""
    echo "Modes disponibles:"
    echo "  enhance    - Mejora contraste, brillo y nitidez"
    echo "  denoise    - Reduce ruido y suaviza imagen"
    echo "  ocr-prep   - Optimiza para OCR (escala grises, alto contraste)"
    echo "  auto       - Aplica secuencia automática de mejoras (default)"
    echo ""
    echo "Ejemplos:"
    echo "  $0 /workspace/input/ticket.jpg /workspace/output/enhanced.jpg auto"
    echo "  $0 /workspace/input/receipt.png /workspace/output/clean.png ocr-prep"
}

# Verificar argumentos
if [ $# -lt 2 ]; then
    echo "Error: Se requieren al menos 2 argumentos"
    show_help
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
MODE="${3:-auto}"

# Verificar que el archivo de entrada existe
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Archivo de entrada no encontrado: $INPUT_FILE"
    exit 1
fi

# Crear directorio de salida si no existe
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
mkdir -p "$OUTPUT_DIR"

# Verificar tipo de archivo
file_type=$(file -b --mime-type "$INPUT_FILE")
if [[ ! "$file_type" =~ ^image/ ]]; then
    echo "Error: El archivo no es una imagen válida: $file_type"
    exit 1
fi

echo "Procesando imagen..."
echo "  Entrada: $INPUT_FILE"
echo "  Salida: $OUTPUT_FILE"
echo "  Modo: $MODE"

# Aplicar procesamiento según el modo
case "$MODE" in
    "enhance")
        # Mejorar contraste, brillo y nitidez
        magick "$INPUT_FILE" \
            -contrast-stretch 2%x1% \
            -brightness-contrast 5x15 \
            -unsharp 0x1.5+1.5+0.02 \
            "$OUTPUT_FILE"
        ;;
    
    "denoise")
        # Reducir ruido y suavizar
        magick "$INPUT_FILE" \
            -despeckle \
            -blur 0x0.5 \
            -enhance \
            "$OUTPUT_FILE"
        ;;
    
    "ocr-prep")
        # Optimizar para OCR
        magick "$INPUT_FILE" \
            -colorspace Gray \
            -contrast-stretch 3%x2% \
            -normalize \
            -threshold 50% \
            -morphology close rectangle:1x1 \
            "$OUTPUT_FILE"
        ;;
    
    "auto")
        # Secuencia automática para tickets/recibos
        magick "$INPUT_FILE" \
            -colorspace Gray \
            -contrast-stretch 2%x1% \
            -brightness-contrast 10x20 \
            -unsharp 0x1+1+0.05 \
            -despeckle \
            -normalize \
            "$OUTPUT_FILE"
        ;;
    
    *)
        echo "Error: Modo no reconocido: $MODE"
        show_help
        exit 1
        ;;
esac

# Verificar que el archivo de salida se creó
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Error: No se pudo crear el archivo de salida"
    exit 1
fi

# Mostrar información del resultado
output_size=$(du -h "$OUTPUT_FILE" | cut -f1)
echo "✅ Imagen procesada exitosamente"
echo "  Tamaño: $output_size"
echo "  Ubicación: $OUTPUT_FILE"