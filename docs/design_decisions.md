# Decisiones de Diseño
**Fecha:** 20 de abril de 2026

## Descripción General
Este documento justifica las decisiones técnicas tomadas en la construcción de la solución analítica para Emausoft.

## 1. Estructura de Datos

### Tablas Principales
1. **ventas** (fact table)
   - Contiene transacciones con todas las dimensiones enriquecidas
   - Relacionada con clientes (cliente_id), productos (producto_id), geografía (país/continente)

2. **clientes** (dimensión)
   - Generada desde API RandomUser
   - 100 clientes únicos con cliente_id numérico

3. **productos** (dimensión)
    - Derivada de `product_code` únicos en ventas
    - Mapeo 1:1 `product_code -> product_id`

4. **regiones** (dimensión)
   - Enriquecimiento geográfico desde API RestCountries
    - Contiene: país, continente, región

## 2. Lógica de Asignación de Clientes

### Decisión: Asignación Aleatoria
- **Justificación:** El dataset de ventas no contiene información de clientes explícita. Se asignó aleatoriamente (con seed=42 para reproducibilidad) para demostrar la integración.
- **Alternativas consideradas:**
  - Asignación por país (requeriría validación de cobertura)
  - Distribución uniforme
  - Simulación histórica

## 3. Normalización de Datos

### Nombres de País
- Se normalizarán automáticamente durante el join de regiones
- Si hay desajustes, se documentarán en el reporte

### Formatos de Fecha
- Conversión a datetime estándar (YYYY-MM-DD)
- Extracción de año, mes, trimestre para análisis temporal

## 4. Pipeline de Integración

```
sales_cleaned.csv
    ↓
+ customer_id (desde customers) → sales_with_customers.csv
    ↓
+ product_id (desde products) → sales_products.csv
    ↓
+ continent, region (from country regions) → sales_enriched.csv
    ↓
FACT TABLE (analytical/fact_table.csv)
```

## 5. Métricas Clave

- **Ingresos Totales (sales):** suma de ventas
- **Número de Órdenes:** `order_number` único
- **Ticket Promedio:** ingresos / número de órdenes
- **Volumen:** `quantity_ordered`
- **Segmentación:** por país, continente, producto, cliente, período temporal

## 6. Rol de PostgreSQL en la Solución

### Decisión: CSV como staging + PostgreSQL como capa final
- **Justificación:** El pipeline en Python prepara y valida los datos de forma incremental, mientras PostgreSQL centraliza el modelo analítico final para consultas, integridad y escalabilidad.
- **Implementación aplicada:**
    - `data/analytical/fact_table.csv` se usa como staging final.
    - `scripts/07_postgres_schema.sql` crea el esquema estrella.
    - `scripts/08_postgres_load.sql` carga dimensiones y tabla de hechos.

### Modelo estrella definido
- **Dimensiones:** `dim_customer`, `dim_product`, `dim_region`, `dim_date`
- **Hechos:** `fact_sales`
- **Criterios técnicos:**
    - Claves primarias por dimensión.
    - Claves foráneas en `fact_sales`.
    - Índices en claves de join para mejorar rendimiento.
    - Validación de nulos en claves críticas tras la carga.

---
**Nota:** Las decisiones se adaptarán según los hallazgos del EDA.
