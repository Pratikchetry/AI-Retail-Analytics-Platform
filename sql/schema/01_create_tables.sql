-- ============================================================
-- RETAIL REVENUE INTELLIGENCE — FINAL CORE SCHEMA
-- Based on corrected Online Retail II staging architecture
-- ============================================================

\c retail_db;

-- Optional cleanup for rebuilds during development
DROP TABLE IF EXISTS revenue_forecast CASCADE;
DROP TABLE IF EXISTS ml_anomaly_scores CASCADE;
DROP TABLE IF EXISTS ml_rfm_segments CASCADE;
DROP TABLE IF EXISTS fact_accounting_adjustments CASCADE;
DROP TABLE IF EXISTS fact_returns_cancellations CASCADE;
DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_country CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS schema_version CASCADE;
DROP SEQUENCE IF EXISTS dim_customer_customer_key_seq CASCADE;

-- ============================================================
-- SCHEMA VERSION
-- ============================================================

CREATE TABLE schema_version (
    version         VARCHAR(20) PRIMARY KEY,
    applied_at      TIMESTAMP DEFAULT NOW(),
    description     TEXT
);

INSERT INTO schema_version (version, description)
VALUES ('1.0', 'Initial corrected schema for Online Retail II staging layer');

-- ============================================================
-- DIMENSIONS
-- ============================================================

CREATE TABLE dim_date (
    date_key        DATE PRIMARY KEY,
    year            INT NOT NULL,
    quarter         INT NOT NULL,
    month           INT NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    week            INT NOT NULL,
    day_of_week     INT NOT NULL,
    day_name        VARCHAR(15) NOT NULL,
    is_weekend      BOOLEAN NOT NULL
);

CREATE TABLE dim_product (
    product_key      SERIAL PRIMARY KEY,
    stockcode        VARCHAR(50) NOT NULL UNIQUE,
    description      TEXT,
    is_merchandise   BOOLEAN NOT NULL DEFAULT TRUE,
    product_type     VARCHAR(50)
);

CREATE TABLE dim_customer (
    customer_key     INT PRIMARY KEY,
    customer_id      BIGINT UNIQUE NOT NULL,
    customer_segment VARCHAR(50)
);

CREATE TABLE dim_country (
    country_key      SERIAL PRIMARY KEY,
    country_name     TEXT NOT NULL UNIQUE
);

-- Insert explicit unknown customer row
INSERT INTO dim_customer (customer_key, customer_id, customer_segment)
VALUES (0, -1, 'Unknown');

-- Ensure future inserts use sequence values starting after 0
CREATE SEQUENCE IF NOT EXISTS dim_customer_customer_key_seq START 1;
ALTER TABLE dim_customer ALTER COLUMN customer_key SET DEFAULT nextval('dim_customer_customer_key_seq');
ALTER SEQUENCE dim_customer_customer_key_seq OWNED BY dim_customer.customer_key;
SELECT setval('dim_customer_customer_key_seq', COALESCE((SELECT MAX(customer_key) FROM dim_customer), 0) + 1, false);

-- ============================================================
-- FACT TABLES
-- ============================================================

CREATE TABLE fact_sales (
    sales_id         BIGSERIAL PRIMARY KEY,
    invoice          TEXT NOT NULL,
    order_date       DATE NOT NULL REFERENCES dim_date(date_key),
    product_key      INT NOT NULL REFERENCES dim_product(product_key),
    customer_key     INT NOT NULL REFERENCES dim_customer(customer_key),
    country_key      INT NOT NULL REFERENCES dim_country(country_key),
    quantity         INT NOT NULL,
    price            NUMERIC(14,4) NOT NULL,
    revenue          NUMERIC(16,4) NOT NULL
);

CREATE TABLE fact_returns_cancellations (
    return_id        BIGSERIAL PRIMARY KEY,
    invoice          TEXT NOT NULL,
    order_date       TIMESTAMP,
    stockcode        VARCHAR(50),
    description      TEXT,
    customer_id      BIGINT,
    country          TEXT,
    quantity         INT,
    price            NUMERIC(14,4)
);

CREATE TABLE fact_accounting_adjustments (
    adjustment_id    BIGSERIAL PRIMARY KEY,
    invoice          TEXT NOT NULL,
    order_date       TIMESTAMP,
    stockcode        VARCHAR(50),
    description      TEXT,
    customer_id      BIGINT,
    country          TEXT,
    quantity         INT,
    price            NUMERIC(16,4)
);

-- ============================================================
-- ANALYTICS / ML OUTPUT TABLES
-- ============================================================

CREATE TABLE ml_rfm_segments (
    customer_id      BIGINT PRIMARY KEY,
    recency          INT NOT NULL,
    frequency        INT NOT NULL,
    monetary         NUMERIC(16,4) NOT NULL,
    r_score          INT NOT NULL,
    f_score          INT NOT NULL,
    m_score          INT NOT NULL,
    rfm_score        VARCHAR(10) NOT NULL,
    rfm_total        INT NOT NULL,
    segment          VARCHAR(50) NOT NULL,
    scored_at        TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ml_anomaly_scores (
    order_date       DATE NOT NULL,
    country_name     TEXT,
    daily_revenue    NUMERIC(16,4) NOT NULL,
    daily_orders     INT NOT NULL,
    anomaly_score    NUMERIC(16,6) NOT NULL,
    is_anomaly       BOOLEAN NOT NULL,
    scored_at        TIMESTAMP DEFAULT NOW()
);

CREATE TABLE revenue_forecast (
    forecast_date      DATE PRIMARY KEY,
    forecast_revenue   NUMERIC(16,4) NOT NULL,
    model_name         TEXT,
    created_at         TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_fact_sales_invoice ON fact_sales(invoice);
CREATE INDEX idx_fact_sales_order_date ON fact_sales(order_date);
CREATE INDEX idx_fact_sales_product_key ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_customer_key ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_country_key ON fact_sales(country_key);

CREATE INDEX idx_returns_invoice ON fact_returns_cancellations(invoice);
CREATE INDEX idx_adjustments_invoice ON fact_accounting_adjustments(invoice);

CREATE INDEX idx_dim_product_stockcode ON dim_product(stockcode);
CREATE INDEX idx_dim_country_name ON dim_country(country_name);

CREATE INDEX idx_rfm_segment ON ml_rfm_segments(segment);
CREATE INDEX idx_anomaly_order_date ON ml_anomaly_scores(order_date);
