# Arquitectura de Tablas por Sesión - Resumen

## 🎯 Problema Solucionado
- **Antes**: Todas las sesiones compartían las mismas tablas `receipts` y `receipt_items`
- **Ahora**: Cada usuario tiene sus propias tablas `receipts_[USER_ID]` y `receipt_items_[USER_ID]`

## 🏗️ Nueva Arquitectura

### **Naming Convention:**
- **Tickets**: `public.receipts_[SESSION_ID]`
- **Productos**: `public.receipt_items_[SESSION_ID]`
- **SESSION_ID**: Corresponde al `user_id` de Telegram (`{{ $json.message.from.id }}`)

### **Ejemplo de Tablas:**
```sql
-- Usuario con ID 12345
receipts_12345
receipt_items_12345

-- Usuario con ID 67890  
receipts_67890
receipt_items_67890
```

## 🔄 Flujo Automatizado

### **PASO 0 - Inicialización (SIEMPRE):**
```sql
-- 1. Verificar si existen las tablas
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('receipts_SESSION_ID', 'receipt_items_SESSION_ID');

-- 2. Crear tabla receipts si no existe
CREATE TABLE IF NOT EXISTS public.receipts_SESSION_ID (id SERIAL PRIMARY KEY, business_name VARCHAR(255) NOT NULL, business_address TEXT, business_tax_id VARCHAR(50), receipt_number VARCHAR(100), receipt_date TIMESTAMP NOT NULL, payment_method VARCHAR(50), tax_amount DECIMAL(10,2), total_amount DECIMAL(10,2) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- 3. Crear tabla receipt_items si no existe
CREATE TABLE IF NOT EXISTS public.receipt_items_SESSION_ID (id SERIAL PRIMARY KEY, receipt_id INTEGER REFERENCES public.receipts_SESSION_ID(id) ON DELETE CASCADE, product_name VARCHAR(255) NOT NULL, product_code VARCHAR(100), category VARCHAR(100), quantity DECIMAL(10,3) NOT NULL, unit_price DECIMAL(10,2) NOT NULL, total_price DECIMAL(10,2) NOT NULL, tax_rate DECIMAL(5,2), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```

## 📝 Configuración de Memory Node

### **Table Name Dinámico:**
En el nodo Memory de N8N, configurar:
- **Table Name**: `chat_memory_{{ $json.message.from.id }}`
- **Session Key**: `{{ $json.message.from.id }}`

Esto asegura que:
- Cada usuario tenga su propia memoria
- Cada usuario tenga sus propias tablas de tickets
- No se mezclen los datos entre usuarios

## 🔧 Cambios en el Prompt

### **Instrucciones Críticas Agregadas:**
1. **Inicialización obligatoria** al inicio de cada conversación
2. **Reemplazo automático** de SESSION_ID con user_id real
3. **Queries actualizados** para usar nombres de tabla con sufijo
4. **Verificación de duplicados** por sesión individual

### **Ejemplo de Query Transformado:**
```sql
-- ANTES (compartido):
SELECT * FROM public.receipts WHERE business_name = 'Soriana';

-- AHORA (por sesión):
SELECT * FROM public.receipts_12345 WHERE business_name = 'Soriana';
```

## ✅ Beneficios

### **Aislamiento de Datos:**
- Cada usuario ve solo sus propios tickets
- No hay interferencia entre usuarios
- Análisis independientes por usuario

### **Escalabilidad:**
- Soporta múltiples usuarios simultáneos
- Cada sesión es completamente independiente
- Memoria y datos separados por usuario

### **Seguridad:**
- Un usuario no puede acceder a datos de otro
- Aislamiento completo a nivel de base de datos
- Privacidad garantizada

## 🚀 Implementación

1. **Copiar** el prompt actualizado de `system_prompt.md`
2. **Configurar** el Memory node con table name dinámico
3. **Probar** con diferentes usuarios de Telegram
4. **Verificar** que se crean tablas separadas por usuario

¡El agente ahora maneja correctamente múltiples usuarios con datos completamente aislados!