# Database Schema Description

## Schema: public

### Table: receipts (Tickets/Recibos principales)
```sql
CREATE TABLE receipts (
    id SERIAL PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL,
    business_address TEXT,
    business_tax_id VARCHAR(50),
    receipt_number VARCHAR(100),
    receipt_date TIMESTAMP NOT NULL,
    payment_method VARCHAR(50),
    tax_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columnas:**
- `id`: ID único del ticket (PRIMARY KEY)
- `business_name`: Nombre del negocio/establecimiento (OBLIGATORIO)
- `business_address`: Dirección completa del negocio
- `business_tax_id`: RFC o ID fiscal del negocio
- `receipt_number`: Número de folio/ticket
- `receipt_date`: Fecha y hora del ticket (OBLIGATORIO)
- `payment_method`: Método de pago (Efectivo, Tarjeta, etc.)
- `tax_amount`: Monto de impuestos
- `total_amount`: Total del ticket (OBLIGATORIO)
- `created_at`: Timestamp de creación del registro

### Table: receipt_items (Productos/Items del ticket)
```sql
CREATE TABLE receipt_items (
    id SERIAL PRIMARY KEY,
    receipt_id INTEGER REFERENCES receipts(id) ON DELETE CASCADE,
    product_name VARCHAR(255) NOT NULL,
    product_code VARCHAR(100),
    category VARCHAR(100),
    quantity DECIMAL(10,3) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    tax_rate DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columnas:**
- `id`: ID único del item (PRIMARY KEY)
- `receipt_id`: ID del ticket al que pertenece (FOREIGN KEY a receipts.id)
- `product_name`: Nombre del producto (OBLIGATORIO)
- `product_code`: Código de barras o SKU del producto
- `category`: Categoría del producto (Lácteos, Panadería, etc.)
- `quantity`: Cantidad comprada (OBLIGATORIO)
- `unit_price`: Precio unitario (OBLIGATORIO)
- `total_price`: Precio total del producto (OBLIGATORIO)
- `tax_rate`: Tasa de impuesto aplicada
- `created_at`: Timestamp de creación del registro

## Relación entre tablas:
- Un `receipt` puede tener múltiples `receipt_items`
- La relación es 1:N (One-to-Many)
- `receipt_items.receipt_id` hace referencia a `receipts.id`

## Queries comunes de ejemplo:

### Insertar ticket completo:
```sql
-- 1. Insertar ticket principal
INSERT INTO receipts (business_name, total_amount, receipt_date, business_address, receipt_number, payment_method, tax_amount)
VALUES ('7 ELEVEN MEXICO SA DE CV', 375.00, '2025-06-27 14:03:39', 'AV.MUNICH 195-B COL.CUAUHTEMOC', '19856310340627202520339', 'Efectivo', 35.17)
RETURNING id;

-- 2. Insertar productos (usando el ID retornado del paso anterior)
INSERT INTO receipt_items (receipt_id, product_name, quantity, unit_price, total_price)
VALUES 
(1, '12PK MODEL REFRI 355ML', 1, 288.00, 288.00),
(1, 'SABRITAS PAPAS CRUJI', 1, 75.00, 75.00);
```

### Consultas de análisis:
```sql
-- Total gastado por negocio
SELECT business_name, SUM(total_amount) as total_spent
FROM receipts 
GROUP BY business_name 
ORDER BY total_spent DESC;

-- Productos más comprados
SELECT product_name, SUM(quantity) as total_quantity, AVG(unit_price) as avg_price
FROM receipt_items 
GROUP BY product_name 
ORDER BY total_quantity DESC;

-- Gastos por mes
SELECT DATE_TRUNC('month', receipt_date) as month, SUM(total_amount) as monthly_total
FROM receipts 
GROUP BY month 
ORDER BY month DESC;
```