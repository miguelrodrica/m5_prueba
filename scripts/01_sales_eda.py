import pandas as pd

sales_data_path = "data/raw/sales_data_sample.csv"
sales_cleaned_path = "data/processed/sales_cleaned.csv"

sales_df = pd.read_csv(sales_data_path)
sales_df.columns = sales_df.columns.str.strip()

#EDA
print(f"Cantidad de filas y columnas inicial: {sales_df.shape}")
print(f"Nombres de las columnas: {sales_df.columns}")
print(f"Tipos de datos: {sales_df.dtypes}")

nulos = sales_df.isnull().sum()
if nulos.sum() > 0:
    print(f"Los nulos existentes son: {nulos[nulos > 0]}")
else:
    print("Sin valores nulos.")

print(f"Filas duplicadas totales: {sales_df.duplicated().sum()}")
print(f"Estadísticas descriptivas: {sales_df.describe()}")
print(f"Valores únicos de ORDERNUMBER: {sales_df['ORDERNUMBER'].nunique()}")
print(f"Valores únicos de PRODUCTCODE: {sales_df['PRODUCTCODE'].nunique()}")

#Limpiar y transformar
sales_df_clean = sales_df.copy()

sales_df_clean = sales_df_clean.rename(columns={
    'ORDERNUMBER': 'order_number',
    'ORDERDATE': 'order_date',
    'PRODUCTCODE': 'product_code',
    'PRODUCTLINE': 'product_line',
    'QUANTITYORDERED': 'quantity_ordered',
    'PRICEEACH': 'price_each',
    'SALES': 'sales',
    'COUNTRY': 'country'
})

sales_df_clean['order_date'] = pd.to_datetime(sales_df_clean['order_date'], format='mixed')

Q1 = sales_df_clean['sales'].quantile(0.25) # Revisar outliers en SALES
Q3 = sales_df_clean['sales'].quantile(0.75)
IQR = Q3 - Q1
outliers = ((sales_df_clean['sales'] < Q1 - 1.5*IQR) | (sales_df_clean['sales'] > Q3 + 1.5*IQR)).sum()
print(f"Outliers detectados (IQR): {outliers}")
print(f"SALES: min={sales_df_clean['sales'].min():.2f}, max={sales_df_clean['sales'].max():.2f}")

sales_df_clean['year'] = sales_df_clean['order_date'].dt.year
sales_df_clean['month'] = sales_df_clean['order_date'].dt.month
sales_df_clean['quarter'] = sales_df_clean['order_date'].dt.quarter

relevant_columns = [
    'order_number', 'order_date', 'product_code', 'product_line', 'quantity_ordered',
    'price_each', 'sales', 'country', 'year', 'month', 'quarter'
]
sales_df_clean = sales_df_clean[relevant_columns]

#Exportar el nuevo Dataset limpio y organizado
sales_df_clean.to_csv(sales_cleaned_path, index=False)