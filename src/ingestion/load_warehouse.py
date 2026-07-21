"""
Phase 0 — AI Retail Intelligence Platform
Real CSV -> Warehouse ingestion pipeline.

Replaces the mock seed_warehouse.py with an idempotent, validated loader:
  staging CSVs -> dimensions -> fact_sales -> analytics -> features

All DB access goes through the shared engine in src/utils/db.py.
"""

import os
import pandas as pd
from sqlalchemy import text

from src.utils.db import engine
from src.utils.logger import get_logger

log = get_logger(__name__)

STAGING_DIR = os.getenv("STAGING_DIR", "data/staging")

SCHEMA_BOOTSTRAP = [
    "sql/schema/01_create_tables.sql",
    "sql/schema/03_create_dim_holiday_uk.sql",
    "sql/seeds/03_seed_holiday_uk.sql",
]

# Analytics SQL files in strict dependency order.
ANALYTICS_PIPELINE = [
    "sql/analytics/01_customer_rfm_base.sql",
    "sql/analytics/02_customer_rfm_segmentation.sql",
    "sql/analytics/03_customer_segment_revenue.sql",
    "sql/analytics/04_customer_segment_profile.sql",
    "sql/analytics/05_update_customer_dimension.sql",
    "sql/analytics/06_revenue_monthly_summary.sql",
    "sql/analytics/07_revenue_seasonality.sql",
    "sql/analytics/08_revenue_growth_analysis.sql",
    "sql/analytics/09_yoy_revenue_analysis.sql",
    "sql/analytics/10_revenue_executive_summary.sql",
    "sql/analytics/11_product_revenue_analysis.sql",
    "sql/analytics/12_product_quantity_analysis.sql",
    "sql/analytics/13_product_revenue_contribution.sql",
    "sql/analytics/14_product_performance_matrix.sql",
    "sql/analytics/15_product_investment_analysis.sql",
    "sql/schema/04_create_feature_daily_enriched.sql",
    "sql/schema/05_create_feature_daily_model_input.sql",
    "sql/schema/06_create_ml_training_view.sql",
]


def _read_staging(name: str) -> pd.DataFrame:
    path = os.path.join(STAGING_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Staging file not found: {path}")
    df = pd.read_csv(path, low_memory=False)
    log.info("Read %s: %d rows", name, len(df))
    return df


def _run_sql_file(path: str):
    """Execute a .sql file via SQLAlchemy, skipping psql-only directives."""
    if not os.path.exists(path):
        log.warning("SQL file missing, skipping: %s", path)
        return
    with open(path, "r", encoding="utf-8") as f:
        raw = "\n".join(
            line for line in f
            if not line.lstrip().startswith("\\")
        )
    statements = [
        s.strip() for s in raw.split(";")
        if s.strip() and not s.strip().startswith("\\")
    ]
    with engine.begin() as conn:
        for stmt in statements:
            if stmt:
                conn.execute(text(stmt))
    log.info("Executed %s", os.path.basename(path))


def bootstrap_schema():
    """Create the base warehouse tables needed by a fresh Docker database."""
    log.info("Bootstrapping core schema ...")
    for sql_file in SCHEMA_BOOTSTRAP:
        _run_sql_file(sql_file)


# ------------------------------------------------------------------
# STAGE 1 — validate staging data
# ------------------------------------------------------------------
def validate_staging(sales: pd.DataFrame) -> pd.DataFrame:
    log.info("Validating sales data ...")
    before = len(sales)
    sales = sales.dropna(subset=["stockcode", "invoice"]).copy()
    if "revenue" not in sales.columns:
        sales["revenue"] = sales["quantity"] * sales["price"]
    sales = sales[sales["revenue"] != 0]
    log.info("Validation: %d -> %d rows (dropped %d invalid)",
             before, len(sales), before - len(sales))
    return sales


# ------------------------------------------------------------------
# STAGE 2 — clear the whole warehouse in ONE statement.
# CASCADE handles the FKs atomically, so ordering is a non-issue.
# ------------------------------------------------------------------
def clear_warehouse():
    log.info("Clearing fact + dimension tables (CASCADE) ...")
    with engine.begin() as conn:
        conn.execute(text(
            "TRUNCATE TABLE fact_sales, dim_date, dim_country, "
            "dim_product, dim_customer RESTART IDENTITY CASCADE"
        ))
        # Re-seed the mandatory 'unknown customer' surrogate (key=0) so
        # fact rows with no customer_id can still resolve to a valid key.
        conn.execute(text(
            "INSERT INTO dim_customer (customer_key, customer_id, customer_segment) "
            "VALUES (0, -1, 'Unknown')"
        ))
    log.info("Warehouse cleared; unknown customer row re-seeded")


# ------------------------------------------------------------------
# STAGE 3 — build dimensions (vectorized, bulk to_sql)
# ------------------------------------------------------------------
def _dow(ts: pd.Series) -> pd.Series:
    """Postgres EXTRACT(DOW) convention: 0=Sunday .. 6=Saturday."""
    return (ts.dt.weekday + 1) % 7


def build_dimensions(sales: pd.DataFrame, non_merch: pd.DataFrame):
    log.info("Building dimensions ...")

    # ---- dim_date ----
    ts = pd.to_datetime(sales["invoicedate"], errors="coerce").dropna()
    dim_date = pd.DataFrame({
        "date_key": ts.dt.date,
        "year": ts.dt.year,
        "quarter": ts.dt.quarter,
        "material_month": ts.dt.month,  # placeholder, replaced below
        "month_name": ts.dt.strftime("%B"),
        "week": ts.dt.strftime("%V").astype(int),
        "day_of_week": _dow(ts).astype(int),
        "day_name": ts.dt.strftime("%A"),
        "is_weekend": _dow(ts).isin([0, 6]),
    })
    dim_date = dim_date.rename(columns={"material_month": "month"})
    dim_date = dim_date.drop_duplicates("date_key").sort_values("date_key")
    dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
    log.info("dim_date: %d dates", len(dim_date))

    # ---- dim_country ----
    dim_country = pd.DataFrame({
        "country_name": sorted(sales["country"].dropna().unique())
    })
    dim_country.to_sql("dim_country", engine, if_exists="append", index=False)
    log.info("dim_country: %d countries", len(dim_country))

    # ---- dim_product (merge merchandise flag) ----
    prods = sales[["stockcode", "description"]].drop_duplicates(subset=["stockcode"]).copy()
    prods["stockcode"] = prods["stockcode"].astype(str)
    non_merch_codes = set(non_merch["stockcode"].astype(str)) if not non_merch.empty else set()
    prods["is_merchandise"] = ~prods["stockcode"].isin(non_merch_codes)
    prods["product_type"] = prods["is_merchandise"].map({True: "merchandise", False: "non-merchandise"})
    prods.to_sql("dim_product", engine, if_exists="append", index=False)
    log.info("dim_product: %d products", len(prods))

    # ---- dim_customer (key=0 unknown row already re-seeded by clear_warehouse) ----
    cust_ids = sales[["customer_id"]].dropna().drop_duplicates()
    cust_ids["customer_id"] = cust_ids["customer_id"].astype(int)
    with engine.begin() as conn:
        for cid in cust_ids["customer_id"]:
            conn.execute(text(
                "INSERT INTO dim_customer (customer_id) VALUES (:cid) "
                "ON CONFLICT (customer_id) DO NOTHING"), {"cid": int(cid)})
    log.info("dim_customer: %d customers", len(cust_ids))


# ------------------------------------------------------------------
# STAGE 4 — load fact_sales (vectorized key resolution)
# ------------------------------------------------------------------
def load_fact_sales(sales: pd.DataFrame):
    log.info("Loading fact_sales ...")

    with engine.connect() as conn:
        date_keys = pd.read_sql(text("SELECT date_key::text FROM dim_date"), conn)
        country_map = pd.read_sql(text("SELECT country_name, country_key FROM dim_country"), conn)
        prod_map = pd.read_sql(text("SELECT stockcode, product_key FROM dim_product"), conn)
        cust_map = pd.read_sql(text("SELECT customer_id, customer_key FROM dim_customer"), conn)

    df = sales.copy()
    df["order_date"] = pd.to_datetime(df["invoicedate"], errors="coerce").dt.date.astype(str)
    df["stockcode"] = df["stockcode"].astype(str)
    df["customer_id"] = df["customer_id"].fillna(-1).astype(int)

    # CSV uses 'country'; dim_country uses 'country_name' — align them
    df = df.rename(columns={"country": "country_name"})

    valid_dates = set(date_keys["date_key"])
    before = len(df)

    df = df.merge(country_map, on="country_name", how="inner")
    df = df.merge(prod_map, on="stockcode", how="inner")
    df = df.merge(cust_map, on="customer_id", how="left")
    df["customer_key"] = df["customer_key"].fillna(0).astype(int)
    df = df[df["order_date"].isin(valid_dates)]
    dropped = before - len(df)

    fact = df[["invoice", "order_date", "product_key", "customer_key",
               "country_key", "quantity", "price", "revenue"]].copy()
    fact["invoice"] = fact["invoice"].astype(str)
    fact["quantity"] = pd.to_numeric(fact["quantity"], errors="coerce").fillna(0).astype(int)
    fact["price"] = pd.to_numeric(fact["price"], errors="coerce").fillna(0)
    fact["revenue"] = pd.to_numeric(fact["revenue"], errors="coerce").fillna(0)

    fact.to_sql("fact_sales", engine, if_exists="append", index=False, chunksize=10000)
    log.info("fact_sales: loaded %d rows (%d dropped for unresolved keys)", len(fact), dropped)


# ------------------------------------------------------------------
# STAGE 5 — rebuild analytics + features
# ------------------------------------------------------------------
def rebuild_analytics():
    log.info("Rebuilding analytics tables + feature tables (in dependency order) ...")
    for sql_file in ANALYTICS_PIPELINE:
        _run_sql_file(sql_file)


# ------------------------------------------------------------------
# ORCHESTRATOR
# ------------------------------------------------------------------
def run_full_ingestion():
    log.info("=" * 60)
    log.info("FULL WAREHOUSE INGESTION (real data)")
    log.info("=" * 60)

    sales = _read_staging("sales_main.csv")
    non_merch = _read_staging("non_merchandise_codes.csv")
    sales = validate_staging(sales)

    bootstrap_schema()                   # 0. create base tables for fresh databases
    clear_warehouse()                    # 1. wipe fact + dims atomically (CASCADE)
    build_dimensions(sales, non_merch)   # 2. rebuild dims (bulk)
    load_fact_sales(sales)               # 3. reload facts with resolved keys
    rebuild_analytics()                  # 4. analytics + features

    log.info("=" * 60)
    log.info("INGESTION COMPLETE")
    log.info("=" * 60)


if __name__ == "__main__":
    run_full_ingestion()
