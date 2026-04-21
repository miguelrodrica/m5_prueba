import pandas as pd

products_path = "data/processed/products.csv"
product_map_path = "data/processed/product_mapping.csv"
sales_prod_path = "data/processed/sales_products.csv"

sales_path = "data/processed/sales_cleaned.csv"

sales_df = pd.read_csv(sales_path)

#Relación de códigod de producto y líneas o categorías de producto
codes = sales_df["product_code"].dropna().astype(str).str.strip()
codes = codes[codes != ""]
codes = codes.drop_duplicates().reset_index(drop=True)
cat_map = sales_df.drop_duplicates("product_code").set_index("product_code")["product_line"]

#Tabla de productos
prod_df = pd.DataFrame(
    {
        "product_id": range(1, len(codes) + 1),
        "product_code": codes,
        "category": codes.map(cat_map).fillna("Unknown"),
    }
)

#Relación entre ventas y productos
map_df = prod_df[["product_code", "product_id"]].copy()
sales_prod_df = sales_df.merge(map_df, on="product_code", how="left")

null_prod_count = int(sales_prod_df["product_id"].isna().sum())

#Guardar archivos CSV
prod_df.to_csv(products_path, index=False)
map_df.to_csv(product_map_path, index=False)
sales_prod_df.to_csv(sales_prod_path, index=False)

if null_prod_count > 0:
    print("Se detectaron ventas sin product_id. Revisa los códigos de producto de entrada.")