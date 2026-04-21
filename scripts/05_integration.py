import pandas as pd

sales_enriched_path = "data/processed/sales_enriched.csv"
sales_with_customers_path = "data/processed/sales_with_customers.csv"
sales_products_path = "data/processed/sales_products.csv"
customers_path = "data/processed/customers_processed.csv"
fact_table_path = "data/analytical/fact_table.csv"


#Cargar datasets
sales_df = pd.read_csv(sales_enriched_path)
customers_sales_df = pd.read_csv(sales_with_customers_path)
products_sales_df = pd.read_csv(sales_products_path)
customers_df = pd.read_csv(customers_path)

#Identificador para unir tablas por posición
sales_df["row_id"] = range(len(sales_df))
customers_sales_df["row_id"] = range(len(customers_sales_df))
products_sales_df["row_id"] = range(len(products_sales_df))

#Armando el dataset final
fact_df = sales_df.merge(
    customers_sales_df[["row_id", "customer_id"]],
    on="row_id",
    how="left"
)

fact_df = fact_df.merge(
    products_sales_df[["row_id", "product_id"]],
    on="row_id",
    how="left"
)

fact_df = fact_df.merge(
    customers_df,
    on="customer_id",
    how="left"
)

fact_df = fact_df.drop(columns=["row_id"])

print(f"Filas despues de integracion: {len(fact_df)}")
print(f"Columnas finales: {fact_df.shape[1]}")

#Guardar dataset final en {sales_enriched_path}
fact_df.to_csv(sales_enriched_path, index=False)

#Guardar fact table en {fact_table_path}
fact_df.to_csv(fact_table_path, index=False)