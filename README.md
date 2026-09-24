# Retail Data Pipeline

End-to-end data engineering project that transforms retail sales data and loads it into a PostgreSQL data warehouse.

## Overview

This project implements an end-to-end data pipeline for retail sales data.

The pipeline processes 99,457 sales transactions using Python and Pandas before loading the transformed data into a PostgreSQL data warehouse running in Docker.

The warehouse uses a star schema designed to support analytical queries across customers, products and stores.

## Data Source

The project uses the **Different Store Sales** dataset from Kaggle.

The dataset contains retail sales transactions from different stores, including customer, product, store, pricing and payment information.

Dataset: [Different Store Sales – Kaggle](https://www.kaggle.com/datasets/kzmontage/sales-from-different-stores)

Place the downloaded CSV file in:

```text
data/01_raw/Different_stores_dataset.csv
```

## Tech Stack

- Python
- Pandas
- PostgreSQL
- Docker
- SQL
- Git / GitHub

## Pipeline

Raw CSV  
→ Python/Pandas transformation  
→ PostgreSQL  
→ Star schema  
→ Analytical SQL queries

## Data Warehouse

The warehouse consists of:

- `dim_date`
- `dim_customer`
- `dim_product`
- `dim_store`
- `fact_sales`

The fact table contains 99,457 sales transactions.

The loading process is designed to be rerunnable without creating duplicate sales records.

## Project Structure

```text
retail-data-pipeline/
├── data/
│   ├── 01_raw/                  # Raw source data
│   ├── 02_processed/            # Transformed data
│   └── 03_archive/              # Archived data
├── docker/
│   └── compose.yaml             # PostgreSQL container configuration
├── docs/                        # Project documentation
├── notebooks/
│   └── 01_explore_data.ipynb    # Data exploration and validation
├── sql/
│   ├── 01_create_schema.sql     # Creates the warehouse schema
│   └── 02_create_tables.sql     # Creates dimensions and fact table
├── src/
│   ├── transform.py             # Data transformation
│   └── load.py                  # Loads data into PostgreSQL
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run

### 1. Set up the Python environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Start PostgreSQL

Start the PostgreSQL container using Docker Compose:

```bash
docker compose -f docker/compose.yaml up -d
```

### 3. Create the warehouse schema and tables

Run the SQL scripts inside the PostgreSQL container:

```bash
docker exec -i retail_postgres psql -U retail_user -d retail_dw < sql/01_create_schema.sql
docker exec -i retail_postgres psql -U retail_user -d retail_dw < sql/02_create_tables.sql
```

### 4. Transform the data

Transform and prepare the raw dataset:

```bash
python src/transform.py
```

### 5. Load the data

Load the transformed data into the PostgreSQL data warehouse:

```bash
python src/load.py
```

### 6. Verify the load

Connect to PostgreSQL:

```bash
docker exec -it retail_postgres psql -U retail_user -d retail_dw
```

Verify that the sales data has been loaded:

```sql
SELECT COUNT(*) FROM warehouse.fact_sales;
```

The expected result is 99,457 rows.

## Future Improvements

Possible future improvements include:

- Move the data warehouse to Google BigQuery
- Automate the pipeline execution
- Add data quality checks and logging
- Add automated testing
- Create a dashboard in Looker Studio
- Explore orchestration for scheduled pipeline runs