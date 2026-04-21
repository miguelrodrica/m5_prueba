# Guía de Ejecución del Pipeline
**Actualizado:** 20 de abril de 2026

## Descripción General
Este proyecto construye una solución analítica end-to-end para Emausoft, siguiendo un pipeline modular de 6 fases.

## Estructura del Proyecto

```
prueba_m5/
├── data/
│   ├── raw/                    # Datos sin procesar
│   │   ├── sales_data_sample.csv
│   │   ├── customers.json      (generado en Fase 2)
│   │   └── countries.json      (generado en Fase 3)
│   ├── processed/              # Datos limpios e integrados
│   │   ├── sales_cleaned.csv
│   │   ├── customers_processed.csv
│   │   ├── products.csv
│   │   ├── country_regions.csv
│   │   ├── sales_with_customers.csv
│   │   ├── product_mapping.csv
│   │   ├── sales_products.csv
│   │   └── sales_enriched.csv
│   └── analytical/             # Dataset analítico final
│       └── fact_table.csv
├── scripts/
│   ├── 01_sales_eda.py             (Fase 1)
│   ├── 02_customers.py             (Fase 2)
│   ├── 03_regions.py               (Fase 3)
│   ├── 04_products.py              (Fase 4)
│   ├── 05_integration.py           (Fase 5)
│   ├── 07_postgres_schema.sql      (Subetapa PostgreSQL)
│   └── 08_postgres_load.sql        (Subetapa PostgreSQL)
├── docs/
│   ├── 01_sales_eda.md
│   ├── design_decisions.md
│   └── business_recommendations.md
└── pyproject.toml
```

## Instrucciones de Ejecución

### Requisitos Previos
```bash
cd /home/miguel/Documentos/prueba_m5
source .venv/bin/activate
```

### Instalación de Dependencias
```bash
uv add requests matplotlib plotly
```

## Fases del Pipeline

### FASE 1: Cargar y Limpiar Ventas
**Archivo:** `scripts/01_sales_eda.py`

```bash
python scripts/01_sales_eda.py
```

**Salida:** `data/processed/sales_cleaned.csv`

**Qué hace:**
- Carga CSV de Kaggle
- Exploración de datos (EDA)
- Limpieza: formatos, nulos, duplicados
- Crea columnas derivadas (año, mes, trimestre)

---

### FASE 2: Consumir API de Clientes
**Archivo:** `scripts/02_customers.py`

```bash
python scripts/02_customers.py
```

**Salida:** `data/processed/customers_processed.csv`

**Qué hace:**
- Consume API RandomUser (100 usuarios)
- Crea cliente_id numérico (1-100)
- Normaliza campos: nombre, ciudad, país
- Asigna cliente_id a ventas (lógica aleatoria con seed)

---

### FASE 3: Consumir API de Regiones
**Archivo:** `scripts/03_regions.py`

```bash
python scripts/03_regions.py
```

**Salida:** `data/processed/country_regions.csv`

**Qué hace:**
- Consume API RestCountries
- Extrae: país, continente, región
- Normaliza nombres de país

---

### FASE 4: Construir Tabla de Productos
**Archivo:** `scripts/04_products.py`

```bash
python scripts/04_products.py
```

**Salida:** 
- `data/processed/products.csv`
- `data/processed/product_mapping.csv`
- `data/processed/sales_products.csv`

**Qué hace:**
- Usa `data/processed/sales_cleaned.csv` como entrada
- Extrae `product_code` únicos de ventas
- Genera `product_id` numérico
- Crea mapeo `product_code -> product_id`
- Enriquece ventas con `product_id`

---

### FASE 5: Integración de Datos
**Archivo:** `scripts/05_integration.py`

```bash
python scripts/05_integration.py
```

**Salida:** `data/processed/sales_enriched.csv` + `data/analytical/fact_table.csv`

**Qué hace:**
- Parte desde ventas ya enriquecidas con geografía
- Agrega customer_id desde ventas con clientes
- Agrega product_id desde ventas con productos
- Agrega atributos de cliente (nombre, ciudad, país)
- Crea fact table final

#### Subetapa obligatoria: PostgreSQL (Esquema Estrella + DDL)
Esta subetapa es crítica y debe ejecutarse dentro de la Fase 5, antes del dashboard.

1. Crear base/esquema analítico en PostgreSQL.
2. Ejecutar DDL para construir el modelo estrella:
	- `dim_customer`
	- `dim_product`
	- `dim_region` (o `dim_geography`)
	- `dim_date` (recomendado)
	- `fact_sales`
   
	Comandos sugeridos:

	```bash
	creatdb miguel_prueba
	psql -d miguel_prueba -f scripts/07_postgres_schema.sql
	psql -d miguel_prueba -f scripts/08_postgres_load.sql
	```
3. Definir restricciones y optimización:
	- PK en cada dimensión
	- FK desde `fact_sales` hacia dimensiones
	- `NOT NULL` donde aplique
	- índices en claves de join (`customer_id`, `product_id`, `region_id`, `date_id`)
4. Cargar datos en orden:
	- primero dimensiones
	- luego `fact_sales`
5. Validar integridad:
	- conteos por tabla
	- claves huérfanas = 0
	- nulos en claves críticas = 0

> Nota: El CSV `fact_table.csv` sirve como staging/intermedio. El entregable de modelado debe existir también en PostgreSQL.

---

## Ejecutar Todo de una Vez

```bash
python scripts/01_sales_eda.py && \
python scripts/02_customers.py && \
python scripts/03_regions.py && \
python scripts/04_products.py && \
python scripts/05_integration.py && \
python scripts/06_dashboard.py
```

## Paso adicional obligatorio (después de Fase 5)

Ejecutar el DDL en PostgreSQL y cargar el esquema estrella antes de presentar resultados de negocio.

## Documentación

Después de ejecutar el pipeline, completar:
1. `docs/01_sales_eda.md` - Con hallazgos del análisis
2. `docs/design_decisions.md` - Justificaciones técnicas
3. `docs/business_recommendations.md` - Insights y acciones

## Troubleshooting

| Problema | Solución |
|----------|----------|
| Error API RandomUser | Verificar conexión a internet; si falla, usar datos cached |
| Error API RestCountries | Verificar conexión; pausa de 10s antes de reintentar |
| Desajuste de nombres de país | Revisar normalización en Fase 3; documentar en EDA |
| Valores nulos en joins | Esperado en campos geográficos; revisar en validación de Fase 5 |

---

**Última actualización:** 20 de abril de 2026
