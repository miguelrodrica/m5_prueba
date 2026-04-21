# Exploración de Datos (EDA) de Ventas
**Fecha:** 20 de abril de 2026

## Propósito
Documentar el análisis exploratorio y la limpieza aplicada al dataset de ventas `sales_data_sample.csv` usando el script [scripts/01_sales_eda.py](../scripts/01_sales_eda.py).

## Resumen del análisis

- Filas iniciales: 2,823
- Columnas originales: 25
- Filas finales guardadas: 2,823
- Columnas finales seleccionadas: 10
- Duplicados exactos: 0
- Países únicos: 19
- Productos únicos: 109
- Outliers en `sales` detectados con IQR: 81
- Rango temporal: 24 Feb 2003 → 6 May 2005

## Columnas conservadas

- `order_number`
- `order_date`
- `product_code`
- `quantity_ordered`
- `price_each`
- `sales`
- `country`
- `year`
- `month`
- `quarter`

## Limpieza aplicada

1. Carga del CSV original con `pandas.read_csv()`.
2. Exploración básica: forma, columnas, tipos, nulos, duplicados y estadísticas.
3. Conversión de `order_date` a formato datetime con `format='mixed'`.
4. Cálculo de outliers en `sales` usando el método IQR.
5. Creación de columnas derivadas: `year`, `month` y `quarter`.
6. Selección de columnas relevantes para análisis.
7. Exportación del dataset limpio a `data/processed/sales_cleaned.csv`.

## Decisiones tomadas

- No se eliminaron duplicados porque el dataset no tiene filas duplicadas exactas.
- No se eliminaron outliers porque parecen ventas válidas.
- Se trabajó sobre `sales_df_clean` para conservar el dataframe original intacto.
- Se redujo el dataset a columnas útiles para el análisis y el dashboard.

## Resultados clave

- El dataset final queda con 2,823 filas y 10 columnas.
- El archivo generado es `data/processed/sales_cleaned.csv`.
- La estructura queda lista para continuar con la integración de clientes, productos y regiones.
