-- Fase 5 PostgreSQL: DDL del esquema estrella

CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_city TEXT,
    customer_country TEXT
);

CREATE TABLE IF NOT EXISTS analytics.dim_product (
    product_id INTEGER PRIMARY KEY,
    product_code TEXT NOT NULL UNIQUE,
    category TEXT
);

CREATE TABLE IF NOT EXISTS analytics.dim_region (
    region_id BIGSERIAL PRIMARY KEY,
    country TEXT NOT NULL UNIQUE,
    continent TEXT,
    region TEXT
);

CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    quarter SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics.fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,
    order_number INTEGER NOT NULL,
    date_id INTEGER NOT NULL REFERENCES analytics.dim_date(date_id),
    customer_id INTEGER NOT NULL REFERENCES analytics.dim_customer(customer_id),
    product_id INTEGER NOT NULL REFERENCES analytics.dim_product(product_id),
    region_id BIGINT NOT NULL REFERENCES analytics.dim_region(region_id),
    quantity_ordered INTEGER,
    price_each NUMERIC(12,2),
    sales NUMERIC(14,2),
    product_code TEXT,
    product_line TEXT,
    UNIQUE (order_number, customer_id, product_id, date_id)
);

CREATE TABLE IF NOT EXISTS analytics.stg_fact_sales (
    order_number INTEGER,
    order_date DATE,
    product_code TEXT,
    product_line TEXT,
    quantity_ordered INTEGER,
    price_each NUMERIC(12,2),
    sales NUMERIC(14,2),
    country TEXT,
    year SMALLINT,
    month SMALLINT,
    quarter SMALLINT,
    continent TEXT,
    region TEXT,
    customer_id INTEGER,
    product_id INTEGER,
    customer_name TEXT,
    customer_city TEXT,
    customer_country TEXT
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date_id ON analytics.fact_sales(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_id ON analytics.fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product_id ON analytics.fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_region_id ON analytics.fact_sales(region_id);