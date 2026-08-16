import pandas as pd

df = pd.read_csv("data/01_raw/Different_stores_dataset.csv")

df["invoice_date"] = pd.to_datetime(df["invoice_date"])

df["total_sales"] = df["quantity"] * df["selling_price_per_unit"]

print(df.head())
print(df[["quantity", "selling_price_per_unit", "total_sales"]].head())

df.to_csv("data/02_processed/retail_sales_clean.csv", index=False)

