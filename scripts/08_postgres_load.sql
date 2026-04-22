-- Fase 5 PostgreSQL: carga del esquema estrella desde CSV (DBeaver)
-- Ejecutar conectado a la base miguel_prueba.

BEGIN;

TRUNCATE TABLE analytics.fact_sales RESTART IDENTITY;
TRUNCATE TABLE analytics.dim_date;
TRUNCATE TABLE analytics.dim_region RESTART IDENTITY;
TRUNCATE TABLE analytics.dim_product;
TRUNCATE TABLE analytics.dim_customer;
TRUNCATE TABLE analytics.stg_fact_sales;

COPY analytics.stg_fact_sales (
    order_number,
    order_date,
    product_code,
    product_line,
    quantity_ordered,
    price_each,
    sales,
    country,
    year,
    month,
    quarter,
    continent,
    region,
    customer_id,
    product_id,
    customer_name,
    customer_city,
    customer_country
)
FROM '/home/miguel/Documentos/prueba_m5/data/analytical/fact_table.csv'
WITH (FORMAT csv, HEADER true);

INSERT INTO analytics.dim_customer (customer_id, customer_name, customer_city, customer_country)
SELECT DISTINCT
    customer_id,
    customer_name,
    customer_city,
    customer_country
FROM analytics.stg_fact_sales
WHERE customer_id IS NOT NULL;

INSERT INTO analytics.dim_product (product_id, product_code, category)
SELECT DISTINCT
    product_id,
    product_code,
    product_line
FROM analytics.stg_fact_sales
WHERE product_id IS NOT NULL
  AND product_code IS NOT NULL;

INSERT INTO analytics.dim_region (country, continent, region)
SELECT DISTINCT
    country,
    continent,
    region
FROM analytics.stg_fact_sales
WHERE country IS NOT NULL;

INSERT INTO analytics.dim_date (date_id, full_date, year, month, quarter)
SELECT DISTINCT
    TO_CHAR(order_date, 'YYYYMMDD')::INTEGER AS date_id,
    order_date AS full_date,
    year,
    month,
    quarter
FROM analytics.stg_fact_sales
WHERE order_date IS NOT NULL;

INSERT INTO analytics.fact_sales (
    order_number,
    date_id,
    customer_id,
    product_id,
    region_id,
    quantity_ordered,
    price_each,
    sales,
    product_code,
    product_line
)
SELECT
    s.order_number,
    TO_CHAR(s.order_date, 'YYYYMMDD')::INTEGER AS date_id,
    s.customer_id,
    s.product_id,
    r.region_id,
    s.quantity_ordered,
    s.price_each,
    s.sales,
    s.product_code,
    s.product_line
FROM analytics.stg_fact_sales s
JOIN analytics.dim_region r
  ON r.country = s.country
WHERE s.order_number IS NOT NULL
  AND s.order_date IS NOT NULL
  AND s.customer_id IS NOT NULL
  AND s.product_id IS NOT NULL;

COMMIT;

-- Validaciones basicas
SELECT 'dim_customer' AS table_name, COUNT(*) AS rows FROM analytics.dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*) FROM analytics.dim_product
UNION ALL
SELECT 'dim_region', COUNT(*) FROM analytics.dim_region
UNION ALL
SELECT 'dim_date', COUNT(*) FROM analytics.dim_date
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM analytics.fact_sales;

SELECT
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) AS null_product_id,
    SUM(CASE WHEN date_id IS NULL THEN 1 ELSE 0 END) AS null_date_id,
    SUM(CASE WHEN region_id IS NULL THEN 1 ELSE 0 END) AS null_region_id
FROM analytics.fact_sales;