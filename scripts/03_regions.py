import pandas as pd
import json
import requests

countries_raw_path = "data/raw/countries.json"
country_regions_path = "data/processed/country_regions.csv"
sales_path = "data/processed/sales_cleaned.csv"
sales_enriched_path = "data/processed/sales_enriched.csv"

url = "https://restcountries.com/v3.1/all?fields=name,continents,region"

# Consumir API
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(f"Países obtenidos: {len(data)}")
except requests.exceptions.RequestException as error:
    print(f"Error al consumir la API: {error}")
    raise SystemExit(1)

# Guardar respuesta cruda
with open(countries_raw_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

# Construir tabla de regiones
regions = []

for country in data:
    try:
        region = {
            "country": country.get("name", {}).get("common", "Unknown"),
            "continent": country.get("continents", ["Unknown"])[0],
            "region": country.get("region", "Unknown"),
        }
        regions.append(region)
    except Exception as error:
        print(f"Error procesando país: {error}")
        continue

regions_df = pd.DataFrame(regions)
# Guardar dataset de regiones
regions_df.to_csv(country_regions_path, index=False)

# Cargar ventas y normalizar países
sales_df = pd.read_csv(sales_path)
sales_df.columns = sales_df.columns.str.strip()

if "country" not in sales_df.columns:
    print("No se encontró la columna country en sales_cleaned.csv")
    raise SystemExit(1)

sales_df["country"] = sales_df["country"].replace({
    "USA": "United States",
    "UK": "United Kingdom"
})

# Join y guardar
sales_df = sales_df.merge(regions_df, on="country", how="left")
sales_df.to_csv(sales_enriched_path, index=False)
print(f"Ventas enriquecidas guardadas: {sales_df.shape[0]} filas, {sales_df.shape[1]} columnas")