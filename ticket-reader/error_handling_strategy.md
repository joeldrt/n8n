# Estrategia de Manejo Inteligente de Errores

## 🎯 Filosofía del Auto-Diagnóstico

En lugar de dar instrucciones específicas para cada posible error, le damos al agente **herramientas de diagnóstico** para que pueda resolver errores por sí mismo.

## 🔧 Herramientas de Diagnóstico Disponibles

### **1. getDbSchemaAndTablesList**
**Cuándo usar:** Error de tabla no encontrada
**Propósito:** Verificar qué tablas existen realmente
**Query:** `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'`

### **2. getTableDefinition** 
**Cuándo usar:** Error de columnas, restricciones o tipos de datos
**Propósito:** Obtener estructura exacta de una tabla específica
**Información que proporciona:**
- Nombres exactos de columnas
- Tipos de datos
- Restricciones NOT NULL
- Claves primarias y foráneas
- Valores por defecto

### **3. executeSqlQuery**
**Cuándo usar:** Para ejecutar queries una vez verificada la estructura
**Propósito:** Realizar las operaciones de base de datos

## 📋 Proceso de Auto-Corrección

### **Flujo Inteligente:**
```
1. Ejecutar query → ERROR
2. Analizar mensaje de error
3. Elegir herramienta de diagnóstico apropiada:
   - Tabla no existe → getDbSchemaAndTablesList
   - Columna no existe → getTableDefinition  
   - Restricción violada → getTableDefinition
4. Obtener información real de la base de datos
5. Corregir query basándose en datos reales
6. Informar al usuario sobre la corrección
7. Ejecutar query corregido
```

## 🚨 Ejemplos de Errores y Respuestas

### **Error: Tabla no encontrada**
```
Error: relation "receipts_12345" does not exist
↓
Acción: getDbSchemaAndTablesList
↓  
Descubrir: La tabla se llama "receipts_123456" 
↓
Corregir: Usar el nombre correcto
```

### **Error: Columna no existe**  
```
Error: column "business_name" does not exist
↓
Acción: getTableDefinition para esa tabla
↓
Descubrir: La columna se llama "store_name"
↓
Corregir: Usar el nombre correcto
```

### **Error: Restricción NOT NULL**
```
Error: null value in column "quantity" violates not-null constraint  
↓
Acción: getTableDefinition para receipt_items_SESSION_ID
↓
Descubrir: quantity es NOT NULL
↓
Corregir: Usar 1 en lugar de NULL para descuentos
```

## ✅ Beneficios de Esta Estrategia

### **1. Adaptabilidad:**
- El agente puede manejar cambios en la estructura de BD
- No depende de documentación que puede estar desactualizada
- Se adapta a diferentes configuraciones

### **2. Aprendizaje Dinámico:**
- Obtiene información real de la base de datos
- No asume estructuras basándose solo en documentación
- Verifica antes de ejecutar

### **3. Transparencia:**
- Informa al usuario sobre errores encontrados
- Explica qué corrección se aplicó
- Muestra el proceso de diagnóstico

### **4. Robustez:**
- Maneja errores inesperados
- Reduce fallos por cambios en la BD
- Autodiagnóstico y autocorrección

## 🎯 Mensaje Clave para el Agente

**"Si algo falla, no adivines - verifica la realidad usando las herramientas de diagnóstico"**

### **Antes (Enfoque Rígido):**
```
Error → Consultar documentación → Asumir solución
```

### **Después (Enfoque Inteligente):**
```  
Error → Diagnosticar con herramientas → Verificar realidad → Corregir basándose en datos reales
```

## 🔄 Implementación en el Prompt

La nueva sección **"MANEJO DE ERRORES EN QUERIES"** en el prompt incluye:

1. **Proceso paso a paso** para manejar errores
2. **Mapeo específico** de errores a herramientas
3. **Ejemplos concretos** de errores comunes
4. **Flujo recomendado** para diagnóstico

Esto hace que el agente sea **auto-suficiente** y **adaptable** a diferentes escenarios de error.