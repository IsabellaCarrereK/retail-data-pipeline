import pandas as pd

df = pd.read_csv("data/01_raw/Different_stores_dataset.csv")

# Validation
required_columns = [
    "invoice_no",
    "invoice_date",
    "customer_id",
    "quantity",
    "selling_price_per_unit",
    "cost_price_per_unit",
]

if df.empty:
    raise ValueError("Input data is empty.")

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

if df[required_columns].isna().any().any():
    raise ValueError("Required columns contain missing values.")

# Transformations
df["invoice_date"] = pd.to_datetime(df["invoice_date"])

df["total_sales"] = df["quantity"] * df["selling_price_per_unit"]

df["total_profit"] = (
    df["selling_price_per_unit"] - df["cost_price_per_unit"]
) * df["quantity"]

df.to_csv("data/02_processed/retail_sales_clean.csv", index=False)

