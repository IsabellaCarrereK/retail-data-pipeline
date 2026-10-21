
import pandas as pd


def validate_data(df):
    """Validate that the input data contains required information."""
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

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df[required_columns].isna().any().any():
        raise ValueError("Required columns contain missing values.")


def transform_data(df):
    """Transform retail sales data and calculate sales metrics."""
    df = df.copy()

    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    df["total_sales"] = (
        df["quantity"] * df["selling_price_per_unit"]
    )

    df["total_profit"] = (
        df["selling_price_per_unit"] - df["cost_price_per_unit"]
    ) * df["quantity"]

    return df


def main():
    """Run the retail data transformation pipeline."""
    input_path = "data/01_raw/Different_stores_dataset.csv"
    output_path = "data/02_processed/retail_sales_clean.csv"

    df = pd.read_csv(input_path)

    validate_data(df)

    df = transform_data(df)

    df.to_csv(output_path, index=False)

    print(f"Transformation completed: {len(df)} rows processed.")


if __name__ == "__main__":
    main()
