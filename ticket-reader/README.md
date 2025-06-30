# 🎫 Ticket Reader Agent

Sistema de N8N con **3 agentes especializados** para procesamiento OCR de tickets/recibos y almacenamiento en base de datos PostgreSQL.

## 🏗️ Arquitectura de 3 Agentes

### **🔍 Duplicate Checker Agent**
- **Responsabilidad**: Verificación exclusiva de duplicados
- **Prompt**: `duplicate_checker_agent.md`
- **Input**: JSON del ticket procesado
- **Output**: Lista de duplicados o autorización para insertar

### **💾 Data Insertion Agent**
- **Responsabilidad**: Inserción exclusiva de datos validados  
- **Prompt**: `data_insertion_agent.md`
- **Input**: JSON validado + autorización de inserción
- **Output**: Confirmación de inserción exitosa

### **🤖 Query Assistant Agent**
- **Responsabilidad**: Consultas analíticas e interacción con usuario
- **Prompt**: `query_assistant_agent.md`
- **Input**: Lenguaje natural del usuario
- **Output**: Análisis e insights en formato amigable

## 📁 Archivos del Sistema

### **Configuración de Agentes**
- `duplicate_checker_agent.md` - Prompt del agente verificador
- `data_insertion_agent.md` - Prompt del agente de inserción
- `query_assistant_agent.md` - Prompt del agente consultor
- `agent_architecture.md` - Documentación de la arquitectura
- `workflow_design.md` - Diseño detallado del flujo N8N

### **Sistema Legacy (Referencia)**
- `system_prompt.md` - Prompt del agente monolítico original
- `tables_descriptions.md` - Documentación de esquema de base de datos

### **Documentación Técnica**
- `session_architecture_summary.md` - Arquitectura de tablas por sesión
- `error_handling_strategy.md` - Estrategia de manejo inteligente de errores
- `descuentos_handling.md` - Manejo específico de descuentos/promociones
- `prompt_improvements.md` - Historial de mejoras al prompt

### **Ejemplos**
- `input_example.md` - Ejemplo de datos de entrada procesados

## 🚀 Cómo Usar

### **Opción 1: Sistema de 3 Agentes (Recomendado)**
1. **Crear 3 nodos AI Agent** en N8N
2. **Configurar prompts**:
   - Agent 1: Contenido de `duplicate_checker_agent.md`
   - Agent 2: Contenido de `data_insertion_agent.md` 
   - Agent 3: Contenido de `query_assistant_agent.md`
3. **Configurar flujo**: Seguir diseño en `workflow_design.md`
4. **Configurar credenciales**: Telegram, OpenAI, PostgreSQL
5. **Activar el flujo**: Sistema robusto anti-concurrencia

### **Opción 2: Sistema Legacy (Referencia)**
1. **Importar el flujo**: `ControlGastosEfectivoV2.json` en N8N
2. **Configurar credenciales**: Telegram, OpenAI, PostgreSQL
3. **Copiar system prompt**: Usar `system_prompt.md` en el nodo AI Agent
4. **Nota**: Puede tener problemas de concurrencia en verificación vs inserción

## 🔧 Características

### **Sistema de 3 Agentes (Nuevo)**
- **Separación de responsabilidades** - Cada agente tiene una función específica
- **Anti-concurrencia** - Elimina problemas de inserción prematura
- **Robustez** - Si un agente falla, no afecta a los otros
- **Mantenibilidad** - Prompts más simples y enfocados

### **Características Generales**
- **OCR inteligente** con GPT-4o para análisis preciso de tickets
- **Base de datos relacional** con PostgreSQL
- **Sesiones aisladas** por usuario de Telegram
- **Detección de duplicados** automática y robusta
- **Manejo de errores** inteligente con auto-diagnóstico
- **Análisis de gastos** con consultas en lenguaje natural

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