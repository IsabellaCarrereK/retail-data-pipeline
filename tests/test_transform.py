
import pandas as pd
import pytest

from src.transform import transform_data, validate_data


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "invoice_no": ["INV001", "INV002"],
        "invoice_date": ["2025-01-01", "2025-01-02"],
        "customer_id": ["C001", "C002"],
        "quantity": [2, 3],
        "selling_price_per_unit": [100.0, 200.0],
        "cost_price_per_unit": [60.0, 150.0],
    })


def test_validate_data_accepts_valid_data(sample_data):
    validate_data(sample_data)


def test_validate_data_rejects_empty_dataframe():
    with pytest.raises(ValueError, match="Input data is empty"):
        validate_data(pd.DataFrame())


def test_validate_data_rejects_missing_column(sample_data):
    df = sample_data.drop(columns=["quantity"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_data(df)


def test_validate_data_rejects_null_values(sample_data):
    df = sample_data.copy()
    df.loc[0, "customer_id"] = None

    with pytest.raises(ValueError, match="Required columns contain missing values"):
        validate_data(df)


def test_transform_data_calculates_sales_and_profit(sample_data):
    result = transform_data(sample_data)

    assert result["total_sales"].tolist() == [200.0, 600.0]
    assert result["total_profit"].tolist() == [80.0, 150.0]


def test_transform_data_converts_invoice_date(sample_data):
    result = transform_data(sample_data)

    assert pd.api.types.is_datetime64_any_dtype(result["invoice_date"])


def test_transform_data_does_not_modify_original(sample_data):
    original = sample_data.copy(deep=True)

    transform_data(sample_data)

    pd.testing.assert_frame_equal(sample_data, original)
