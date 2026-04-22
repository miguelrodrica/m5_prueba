-- Fase 5 PostgreSQL: DDL del esquema estrella

CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE analytics.dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_city VARCHAR(50),
    customer_country VARCHAR(50)
);

CREATE TABLE analytics.dim_product (
    product_id INTEGER PRIMARY KEY,
    product_code VARCHAR(20) NOT NULL UNIQUE,
    category VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS analytics.dim_region (
    region_id SERIAL PRIMARY KEY,
    country VARCHAR(50) NOT NULL UNIQUE,
    continent VARCHAR(30),
    region VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    quarter SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics.fact_sales (
    sales_key SERIAL PRIMARY KEY,
    order_number INTEGER NOT NULL,
    date_id INTEGER NOT NULL REFERENCES analytics.dim_date(date_id),
    customer_id INTEGER NOT NULL REFERENCES analytics.dim_customer(customer_id),
    product_id INTEGER NOT NULL REFERENCES analytics.dim_product(product_id),
    region_id INTEGER NOT NULL REFERENCES analytics.dim_region(region_id),
    quantity_ordered INTEGER,
    price_each NUMERIC(12,2),
    sales NUMERIC(14,2),
    product_code VARCHAR(20),
    product_line VARCHAR(50),
    UNIQUE (order_number, customer_id, product_id, date_id)
);

CREATE TABLE IF NOT EXISTS analytics.stg_fact_sales (
    order_number INTEGER,
    order_date DATE,
    product_code VARCHAR(20),
    product_line VARCHAR(50),
    quantity_ordered INTEGER,
    price_each NUMERIC(12,2),
    sales NUMERIC(14,2),
    country VARCHAR(50),
    year SMALLINT,
    month SMALLINT,
    quarter SMALLINT,
    continent VARCHAR(30),
    region VARCHAR(50),
    customer_id INTEGER,
    product_id INTEGER,
    customer_name VARCHAR(100),
    customer_city VARCHAR(50),
    customer_country VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date_id ON analytics.fact_sales(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_id ON analytics.fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product_id ON analytics.fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_region_id ON analytics.fact_sales(region_id);