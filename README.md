# Retail Data Pipeline

End-to-end data engineering project that transforms retail sales data and loads it into a PostgreSQL data warehouse.

## Overview

The pipeline processes a retail sales dataset containing 99,457 transactions. 
Python and Pandas are used to transform the raw data before loading it into a PostgreSQL data warehouse running in Docker.

The warehouse uses a star schema designed for analytical queries.

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
│   ├── 01_raw/              # Raw source data
│   ├── 02_processed/        # Transformed data
│   └── 03_archive/          # Archived data
├── docker/
│   └── compose.yaml         # PostgreSQL container configuration
├── docs/                    # Project documentation
├── notebooks/
│   └── 01_explore_data.ipynb # Data exploration and validation
├── sql/
│   ├── 01_create_schema.sql # Creates the warehouse schema
│   └── 02_create_tables.sql # Creates dimensions and fact table
├── src/
│   ├── transform.py         # Data transformation
│   └── load.py              # Loads data into PostgreSQL
├── .gitignore
└── README.md
```





## Future Improvements


```text
Possible future improvements include:

- Move the data warehouse to Google BigQuery
- Automate the pipeline execution
- Add data quality checks and logging
- Add automated testing
- Create a dashboard in Looker Studio
- Explore orchestration for scheduled pipeline runs
```