import pandas as pd
import json
import random
import requests

customers_raw_path = "data/raw/customers.json"
customers_processed_path = "data/processed/customers_processed.csv"
sales_path = "data/processed/sales_cleaned.csv"
sales_with_customers_path = "data/processed/sales_with_customers.csv"

url = "https://randomuser.me/api/?results=100"

#Obtener respuesta de la API
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    users = data["results"]
    print(f"Usuarios obtenidos: {len(users)}")
except requests.exceptions.RequestException as error:
    print(f"Error al consumir la API: {error}")
    raise SystemExit(1)

#Guardar la respuesta en un JSON
with open(customers_raw_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

#Construir tabla de clientes
customers = []

for idx, user in enumerate(users, start=1):
    customer = {
        "customer_id": idx,
        "customer_name": f"{user['name']['first']} {user['name']['last']}".strip(),
        "customer_city": user["location"]["city"].strip(),
        "customer_country": user["location"]["country"].strip(),
    }
    customers.append(customer)

customers_df = pd.DataFrame(customers)

#Guardar dataset de clientes
customers_df.to_csv(customers_processed_path, index=False)

#Cargar ventas limpias para asignar cliente_id
sales_df = pd.read_csv(sales_path)
sales_df.columns = sales_df.columns.str.strip()

#Asignar cliente_id de forma aleatoria y reproducible
random.seed(42)
customer_ids = customers_df["customer_id"].tolist()
sales_df["customer_id"] = [random.choice(customer_ids) for _ in range(len(sales_df))]

#Guardar ventas con cliente_id
sales_df.to_csv(sales_with_customers_path, index=False)
