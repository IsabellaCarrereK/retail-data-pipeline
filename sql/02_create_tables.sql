CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouse.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL UNIQUE,
    gender VARCHAR(20),
    age INTEGER
);

CREATE TABLE IF NOT EXISTS warehouse.dim_product (
    product_key SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS warehouse.dim_store (
    store_key SERIAL PRIMARY KEY,
    shopping_mall VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    UNIQUE (shopping_mall, state)
);



CREATE TABLE IF NOT EXISTS warehouse.fact_sales (
    sales_key SERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    invoice_no VARCHAR(20) NOT NULL UNIQUE,
    quantity INTEGER NOT NULL,
    selling_price_per_unit NUMERIC(12, 2) NOT NULL,
    cost_price_per_unit NUMERIC(12, 3) NOT NULL,
    total_sales NUMERIC(14, 2) NOT NULL,
    total_profit NUMERIC(14, 3) NOT NULL,
    payment_method VARCHAR(50),
    
FOREIGN KEY (date_key) REFERENCES warehouse.dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES warehouse.dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES warehouse.dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES warehouse.dim_store(store_key)
);
