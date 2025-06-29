# 🎫 Ticket Reader Agent

Agente de N8N especializado en procesamiento OCR de tickets/recibos y almacenamiento en base de datos PostgreSQL.

## 📁 Archivos del Flujo

### **Flujo Principal**
- `ControlGastosEfectivoV2.json` - Workflow completo de N8N

### **Configuración del Agente**
- `system_prompt.md` - Prompt principal del agente IA
- `tables_descriptions.md` - Documentación de esquema de base de datos

### **Documentación Técnica**
- `session_architecture_summary.md` - Arquitectura de tablas por sesión
- `error_handling_strategy.md` - Estrategia de manejo inteligente de errores
- `descuentos_handling.md` - Manejo específico de descuentos/promociones
- `prompt_improvements.md` - Historial de mejoras al prompt

### **Ejemplos**
- `input_example.md` - Ejemplo de datos de entrada procesados

## 🚀 Cómo Usar

1. **Importar el flujo**: Importa `ControlGastosEfectivoV2.json` en N8N
2. **Configurar credenciales**: Telegram, OpenAI, PostgreSQL
3. **Copiar system prompt**: Usa el contenido de `system_prompt.md` en el nodo AI Agent
4. **Activar el flujo**: El bot estará listo para procesar tickets

## 🔧 Características

- **OCR inteligente** con GPT-4o para análisis preciso de tickets
- **Base de datos relacional** con PostgreSQL
- **Sesiones aisladas** por usuario de Telegram
- **Detección de duplicados** automática
- **Manejo de errores** inteligente con auto-diagnóstico
- **Análisis de gastos** con queries predefinidos

## 📊 Funcionalidades

- Procesamiento de imágenes de tickets
- Extracción automática de datos (negocio, productos, precios)
- Almacenamiento estructurado en base de datos
- Consultas de análisis (gastos por negocio, productos más comprados, etc.)
- Prevención de tickets duplicados
- Manejo correcto de descuentos y promociones

## 🛠️ Dependencias

- N8N con nodos LangChain
- PostgreSQL
- OpenAI API (GPT-4o y o3-mini)
- Telegram Bot API
- Nodos de la comunidad: Tesseract.js (opcional)