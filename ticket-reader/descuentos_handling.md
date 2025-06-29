# Manejo de Descuentos y Promociones

## 🚨 Problema Encontrado
El agente intentó insertar un descuento con `quantity = NULL`, lo cual viola la restricción NOT NULL de la columna `quantity`.

### Query que falló:
```sql
INSERT INTO public.receipt_items_8023719029 (...) 
VALUES (..., (1, 'PROMOCIONES', NULL, -78.00, -78.00, NULL, NULL));
```

### Error:
```
null value in column "quantity" of relation "receipt_items_8023719029" violates not-null constraint
```

## ✅ Solución Implementada

### **Regla Crítica para Descuentos:**
Para cualquier descuento, promoción o ajuste que aparezca en un ticket:

1. **quantity**: SIEMPRE usar `1` (nunca NULL)
2. **unit_price**: Usar el valor negativo del descuento
3. **total_price**: Usar el valor negativo del descuento  
4. **product_name**: Usar el nombre de la promoción
5. **category**: Puede ser `'Descuento'` o NULL

### **Query Correcto:**
```sql
INSERT INTO public.receipt_items_SESSION_ID (receipt_id, product_name, quantity, unit_price, total_price, category, product_code) 
VALUES (1, 'PROMOCIONES', 1, -78.00, -78.00, 'Descuento', NULL);
```

## 📋 Ejemplos de Casos Comunes

### **Descuento por promoción:**
```sql
VALUES (1, 'PROMOCIONES', 1, -78.00, -78.00, 'Descuento', NULL)
```

### **Descuento por cupón:**
```sql
VALUES (1, 'CUPON 10%', 1, -25.50, -25.50, 'Descuento', 'CUP001')
```

### **Descuento por membresía:**
```sql
VALUES (1, 'DESC. CLIENTE VIP', 1, -15.00, -15.00, 'Descuento', NULL)
```

### **Cashback o reembolso:**
```sql
VALUES (1, 'CASHBACK', 1, -12.75, -12.75, 'Reembolso', NULL)
```

## 🛠️ Cambios en el Prompt

### **Instrucciones Agregadas:**
1. **Documentación clara** sobre manejo de descuentos
2. **Ejemplo específico** de query correcto
3. **Regla crítica** en sección IMPORTANTE
4. **Clarificación** en definición de columnas

### **Mensaje Clave Agregado:**
```
**CRÍTICO**: Para descuentos/promociones NUNCA uses NULL en quantity - SIEMPRE usa 1
```

## 🔍 Validación de Datos

### **Campos que NO pueden ser NULL en receipt_items:**
- `product_name` (VARCHAR NOT NULL)
- `quantity` (DECIMAL NOT NULL) 
- `unit_price` (DECIMAL NOT NULL)
- `total_price` (DECIMAL NOT NULL)

### **Campos que SÍ pueden ser NULL:**
- `product_code` (VARCHAR)
- `category` (VARCHAR)
- `tax_rate` (DECIMAL)

## 🎯 Resultado Esperado

Con estos cambios, el agente ahora debe generar queries válidos para descuentos:

**Antes (FALLA):**
```sql
VALUES (1, 'PROMOCIONES', NULL, -78.00, -78.00, NULL, NULL)
```

**Después (FUNCIONA):**
```sql
VALUES (1, 'PROMOCIONES', 1, -78.00, -78.00, 'Descuento', NULL)
```

El prompt actualizado en `system_prompt.md` incluye todas estas instrucciones para evitar este error en el futuro.