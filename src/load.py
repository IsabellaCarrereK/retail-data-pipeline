import os

import pandas as pd
import psycopg
from dotenv import load_dotenv


load_dotenv("docker/.env")


# Read transformed data
df = pd.read_csv("data/02_processed/retail_sales_clean.csv")

# Make sure invoice_date is treated as a date/time value
df["invoice_date"] = pd.to_datetime(df["invoice_date"])

print(df.head())
print(f"Rows to load: {len(df)}")


# Connect to PostgreSQL
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

print("Connected to PostgreSQL!")


with conn.cursor() as cur:

    # Load products
    products = df["category"].drop_duplicates()

    for category in products:
        cur.execute(
            """
            INSERT INTO warehouse.dim_product (category)
            VALUES (%s)
            ON CONFLICT (category) DO NOTHING;
            """,
            (category,)
        )

    # Load customers
    customers = df[
        ["customer_id", "gender", "age"]
    ].drop_duplicates()

    for _, customer in customers.iterrows():
        cur.execute(
            """
            INSERT INTO warehouse.dim_customer (
                customer_id,
                gender,
                age
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING;
            """,
            (
                customer["customer_id"],
                customer["gender"],
                customer["age"]
            )
        )

    # Load stores
    stores = df[
        ["shopping_mall", "state", "region"]
    ].drop_duplicates()

    for _, store in stores.iterrows():
        cur.execute(
            """
            INSERT INTO warehouse.dim_store (
                shopping_mall,
                state,
                region
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (shopping_mall, state) DO NOTHING;
            """,
            (
                store["shopping_mall"],
                store["state"],
                store["region"]
            )
        )

    # Load dates
    dates = df[["invoice_date"]].copy()
    dates["full_date"] = dates["invoice_date"].dt.date
    dates = dates[["full_date"]].drop_duplicates()

    for _, date_row in dates.iterrows():
        full_date = date_row["full_date"]
        date_key = int(full_date.strftime("%Y%m%d"))

        cur.execute(
            """
            INSERT INTO warehouse.dim_date (
                date_key,
                full_date,
                year,
                month,
                day
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (date_key) DO NOTHING;
            """,
            (
                date_key,
                full_date,
                full_date.year,
                full_date.month,
                full_date.day
            )
        )

    # Build lookup dictionaries
    cur.execute(
        """
        SELECT product_key, category
        FROM warehouse.dim_product;
        """
    )
    product_lookup = {
        category: product_key
        for product_key, category in cur.fetchall()
    }

    cur.execute(
        """
        SELECT customer_key, customer_id
        FROM warehouse.dim_customer;
        """
    )
    customer_lookup = {
        customer_id: customer_key
        for customer_key, customer_id in cur.fetchall()
    }

    cur.execute(
        """
        SELECT store_key, shopping_mall, state
        FROM warehouse.dim_store;
        """
    )
    store_lookup = {
        (shopping_mall, state): store_key
        for store_key, shopping_mall, state in cur.fetchall()
    }

    # Load fact table
    for _, row in df.iterrows():
        date_key = int(row["invoice_date"].strftime("%Y%m%d"))

        cur.execute(
            """
            INSERT INTO warehouse.fact_sales (
                date_key,
                customer_key,
                product_key,
                store_key,
                invoice_no,
                quantity,
                selling_price_per_unit,
                cost_price_per_unit,
                total_sales,
                total_profit,
                payment_method
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            );
            """,
            (
                date_key,
                customer_lookup[row["customer_id"]],
                product_lookup[row["category"]],
                store_lookup[(row["shopping_mall"], row["state"])],
                row["invoice_no"],
                row["quantity"],
                row["selling_price_per_unit"],
                row["cost_price_per_unit"],
                row["total_sales"],
                row["total_profit"],
                row["payment_method"]
            )
        )


# Save database changes
conn.commit()

print("All dimensions and fact_sales loaded!")

# Close database connection
conn.close()