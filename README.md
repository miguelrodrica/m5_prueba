# End-to-End Analytics Solution — Emausoft Case

This project was made for Riwi. It connects sales data, customers, products, and geography to answer business questions and build a star model in PostgreSQL.

---

## Table of Contents

- [Context](#context)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [How to Run](#how-to-run)
- [Output Files](#output-files)
- [Data Model](#data-model)
- [Business Questions](#business-questions)
- [Documentation](#documentation)

---

## Context

Emausoft is a SaaS company that helps small and medium businesses in Latin America manage their sales data. This project takes messy data from different sources and turns it into clear, useful information for making decisions.

---

## Requirements

- Python 3.14 or higher
- [UV Astral](https://docs.astral.sh/uv/) to manage the virtual environment
- PostgreSQL 14 or higher (only for the database step)
- Internet connection (needed for APIs in phases 2 and 3)

---

## Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd prueba_m5

# 2. Create and activate the virtual environment
uv venv .venv
source .venv/bin/activate

# 3. Install dependencies
uv sync
```

---

## Project Structure

```
prueba_m5/
├── data/
│   ├── raw/                        # Original files — do not modify
│   │   ├── sales_data_sample.csv
│   │   ├── customers.json          # Raw response from RandomUser API
│   │   └── countries.json          # Raw response from RestCountries API
│   ├── processed/                  # Output files from each phase
│   │   ├── sales_cleaned.csv
│   │   ├── customers_processed.csv
│   │   ├── country_regions.csv
│   │   ├── products.csv
│   │   ├── product_mapping.csv
│   │   ├── sales_enriched.csv
│   │   └── sales_products.csv
│   └── analytical/                 # Final integrated dataset
│       └── fact_table.csv
│
├── scripts/
│   ├── 01_sales_eda.py             # Phase 1: clean sales data
│   ├── 02_customers.py             # Phase 2: customers from API
│   ├── 03_regions.py               # Phase 3: geography from API
│   ├── 04_products.py              # Phase 4: products table
│   ├── 05_integration.py           # Phase 5: integration and fact table
│   ├── 06_dashboard.py             # Phase 6: dashboard and charts
│   ├── 07_postgres_schema.sql      # Star model DDL
│   └── 08_postgres_load.sql        # Load data to PostgreSQL
│
├── docs/
│   ├── execution_guide.md          # Step by step guide for each phase
│   ├── 01_sales_eda.md             # EDA findings
│   ├── design_decisions.md         # Technical decisions and reasons
│   └── business_recommendations.md # Business recommendations
│
├── output/
│   └── plots/                      # Charts made by the dashboard
│
├── pyproject.toml
└── README.md
```

---

## Data Sources

| Source | Type | Description |
|---|---|---|
| `sales_data_sample.csv` | CSV file | Sales transaction data — [Kaggle](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data) |
| randomuser.me API | REST API | 100 fake customers |
| restcountries.com API | REST API | Geographic data for 250 countries |
| Built from sales data | Derived | Products table made from sales |

> **Note:** The sales dataset has no customer names. Customers were assigned using random distribution with `random.seed(42)` so results are the same every time you run the script.

---

## How to Run

### Full pipeline (Phases 1 to 5)

Run the scripts in order from the root folder:

```bash
cd prueba_m5
source .venv/bin/activate

python scripts/01_sales_eda.py
python scripts/02_customers.py
python scripts/03_regions.py
python scripts/04_products.py
python scripts/05_integration.py
```

Each script runs alone and saves files in `data/processed/`.

### Dashboard

```bash
python scripts/06_dashboard.py
```

Charts are saved in `output/plots/`.

### PostgreSQL step (optional)

You need PostgreSQL installed and running:

```bash
# Create the database
creatdb miguel_prueba

# Create the star schema
psql -d miguel_prueba -f scripts/07_postgres_schema.sql

# Load the data
psql -d miguel_prueba -f scripts/08_postgres_load.sql
```

---

## Output Files

| File | Description |
|---|---|
| `data/processed/sales_cleaned.csv` | Clean and ready sales data |
| `data/processed/customers_processed.csv` | Customers from the API |
| `data/processed/country_regions.csv` | Geographic regions table |
| `data/processed/products.csv` | Products table |
| `data/processed/product_mapping.csv` | Map of product_code and product_id |
| `data/processed/sales_products.csv` | Sales with product_id |
| `data/processed/sales_enriched.csv` | Final integrated sales dataset |
| `data/analytical/fact_table.csv` | Final integrated dataset |

---

## Data Model

The star model in PostgreSQL looks like this:

```
                    ┌─────────────┐
                    │  dim_date   │
                    └──────┬──────┘
                           │
┌──────────────┐    ┌──────┴──────┐    ┌──────────────┐
│ dim_customer │────│  fact_sales │────│  dim_product │
└──────────────┘    └──────┬──────┘    └──────────────┘
                           │
                    ┌──────┴──────┐
                    │ dim_region  │
                    └─────────────┘
```

---

## Business Questions

The dashboard answers these questions:

**Descriptive**
1. How have sales changed over time?
2. Which countries or regions make the most money?
3. Which products sell the best?

**Diagnostic**

4. Which regions have low performance?
5. Which products have the least impact on sales?

**Analytical**

6. Which type of customers bring more value?
7. Is there a link between location and buying behavior?

**Decision**

8. What actions would you recommend to the business?

---

## Documentation

| Document | Content |
|---|---|
| `docs/execution_guide.md` | Step by step guide for each phase |
| `docs/01_sales_eda.md` | Findings from the exploratory analysis |
| `docs/design_decisions.md` | Technical decisions and why they were made |
| `docs/business_recommendations.md` | Strategic recommendations for the business |

---

## Technical Notes

- Files in `data/raw/` are never changed — they are the original source of truth.
- Each phase saves its own output file without overwriting previous ones.
- Country name fixes (`USA → United States`, `UK → United Kingdom`) are done in memory during phase 3, not in the original files.
- Customer assignment uses `random.seed(42)` so results are the same every time the script runs on any machine.