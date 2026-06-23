<div align="center">

# 🏪 Retail Revenue Intelligence & Anomaly Detection

### End-to-End Retail Analytics System
### PostgreSQL · XGBoost · SHAP · Tableau · Power BI · GCP · LangGraph · RAG AI Agent

<br>

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.9-336791?style=for-the-badge&logo=postgresql)
![Tableau](https://img.shields.io/badge/Tableau-11%20Dashboards-E97627?style=for-the-badge&logo=tableau)
![Power BI](https://img.shields.io/badge/Power%20BI-DAX%20Companion-F2C811?style=for-the-badge&logo=powerbi)
![XGBoost](https://img.shields.io/badge/XGBoost-V1%20%26%20V2-FF6600?style=for-the-badge)
![SHAP](https://img.shields.io/badge/SHAP-Explainability-8A2BE2?style=for-the-badge)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikitlearn)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=for-the-badge&logo=jupyter)

<br>

> Built on **1,067,371 raw transactions** — profiled, cleaned, warehoused,
> segmented, anomaly-scored, forecast, explained, and dashboarded
> across **11 Tableau dashboards** and **two model generations**.

</div>

---

## What This Project Answers

| Business Question | How Answered |
|---|---|
| What happened to revenue? | Revenue Intelligence dashboard — monthly trend, seasonality, YoY, MoM |
| Which products drive the business? | Product Intelligence dashboard — revenue, quantity, performance matrix, investment strategy |
| Which customers matter most? | RFM segmentation — 5,878 customers, 5 segments, retention action matrix |
| What was unusual? | IsolationForest anomaly detection — 139 anomalies across 18 countries |
| What will happen next? | XGBoost V2 — MAE £7,248, WAPE 14.4%, R² 0.63 |
| Why does the model predict what it predicts? | SHAP — feature-level attribution for every prediction |
| Did V2 improve over V1? | V1 vs V2 comparison — 5 of 6 metrics improved, MAE +40.87% |

---

## Project Status

| Phase | Status |
|---|---|
| Raw data profiling | ✅ Complete |
| Data cleaning with audit trail | ✅ Complete |
| Exploratory data analysis | ✅ Complete |
| PostgreSQL warehouse (validated) | ✅ Complete |
| SQL analytics layer (15 views) | ✅ Complete |
| RFM customer segmentation | ✅ Complete |
| IsolationForest anomaly detection | ✅ Complete |
| Revenue forecasting V1 — XGBoost + SHAP | ✅ Complete |
| Revenue forecasting V2 — enriched features | ✅ Complete |
| Tableau dashboards — 11 pages total | ✅ Complete |
| GitHub polish and public release | 📋 Next |
| GCP deployment — BigQuery + Cloud Run | 📋 Planned |
| FastAPI + Docker + CI/CD | 📋 Planned |
| RAG AI Agent — LangChain + LangGraph + Gemini | 📋 Planned |
| Voice Agent | 📋 Planned |

---

## Dataset

**Source:** Online Retail II — UCI Machine Learning Repository
**File:** `data/raw/online_retail_ii/online_retail_II.xlsx`
**MD5:** `ed54ccfc5d358481c399cc11d0a244be`
**Currency:** GBP (£) — all monetary values are British Pounds Sterling
**Period:** December 2009 — December 2011
**Geography:** 43 countries, UK-dominant wholesale retailer

---

## Key Results

### Revenue Overview
| Metric | Value |
|---|---|
| Total revenue | £20,476,634 |
| Average monthly revenue | £819,065 |
| Best month | November 2011 — £1,503,867 |
| Worst month | February 2011 — £522,546 |
| YoY growth (2010 vs 2011) | −0.13% |
| UK revenue share | 85.0% (£17,410,570) |

### Monthly Revenue — 2010 vs 2011 YoY
| Month | 2010 | 2011 | YoY % |
|---|---|---|---|
| Jan | £651,155 | £689,812 | +5.94% |
| Feb | £551,878 | £522,546 | −5.32% |
| Mar | £830,915 | £716,215 | −13.80% |
| Apr | £678,875 | £536,968 | −20.90% |
| May | £657,706 | £769,297 | +16.97% |
| Jun | £749,537 | £760,547 | +1.47% |
| Jul | £648,810 | £718,076 | +10.68% |
| Aug | £695,252 | £757,841 | +9.00% |
| Sep | £921,697 | £1,056,435 | +14.62% |
| Oct | £1,161,902 | £1,151,264 | −0.92% |
| Nov | £1,464,293 | £1,503,867 | +2.70% |
| Dec | £821,453 | £637,808 | −22.36% |

### Product Intelligence
**Top 5 by Revenue**
| Product | Revenue | Contribution % |
|---|---|---|
| REGENCY CAKESTAND 3 TIER | £330,590 | 1.68% |
| CREAM HANGING HEART T-LIGHT HOLDER | £257,725 | 1.31% |
| JUMBO BAG RED RETROSPOT | £182,681 | 0.93% |
| PAPER CRAFT, LITTLE BIRDIE | £168,470 | 0.86% |
| PARTY BUNTING | £148,318 | 0.75% |

**Top 5 by Quantity Sold**
| Product | Quantity |
|---|---|
| WORLD WAR 2 GLIDERS ASSTD DESIGNS | 106,139 |
| JUMBO BAG RED RETROSPOT | 96,757 |
| PACK OF 72 RETRO SPOT CAKE CASES | 94,884 |
| CREAM HANGING HEART T-LIGHT HOLDER | 94,203 |
| POPCORN HOLDER | 88,499 |

**Product Investment Strategy Distribution**
| Strategy | Products |
|---|---|
| Monitor | 3,172 |
| Invest More | 810 |
| Premium Focus | 371 |
| Marketing Opportunity | 371 |

**Product Performance Quadrants**
| Quadrant | Revenue | Quantity | Action |
|---|---|---|---|
| Superstar Products | High | High | Protect inventory, increase marketing |
| Premium Products | High | Lower | Premium positioning, cross-sell |
| Mass Market Products | Lower | High | Volume efficiency, margin review |
| Underperforming Products | Low | Low | Monitor or discontinue |

### Customer Segmentation
| Segment | Customers | Avg Value | Avg Purchases | Avg Days Inactive |
|---|---|---|---|---|
| Champions | 1,317 | £9,552 | 17.71 | 25.1 |
| Loyal Customers | 1,341 | £2,298 | 5.58 | 100.0 |
| Potential Loyalists | 968 | £907 | 3.00 | 173.1 |
| At Risk | 1,411 | £475 | 1.69 | 292.6 |
| Lost Customers | 841 | £198 | 1.04 | 515.0 |
| **Total** | **5,878** | — | — | — |

### Anomaly Detection
| Metric | Value |
|---|---|
| Countries scored | 18 of 43 |
| Total anomalies | 139 |
| High anomalies (positive spikes) | 117 (84.17%) |
| Low anomalies (demand drops) | 22 (15.83%) |

### Forecasting — V1 vs V2
| Metric | V1 | V2 | Improvement |
|---|---|---|---|
| MAE | £12,258 | £7,248 | **+40.87%** |
| RMSE | £20,764 | £15,641 | **+24.67%** |
| R² | 34.89% | 63.06% | **+80.72%** |
| WAPE | 24.38% | 14.41% | **+40.87%** |
| Spike-Day MAE | £42,755 | £29,408 | **+31.22%** |
| Bias | −8.54% | −9.08% | −6.29% |
| **Overall** | — | — | **V2 wins 5 of 6** |

---

## All 11 Tableau Dashboards

### V1 Dashboards (Original 4)
| # | Dashboard | Key Finding |
|---|---|---|
| 1 | Revenue Overview | £20.47M total, UK = 85%, Nov peak |
| 2 | RFM Customer Segmentation (V1) | Champions drive 67.89% of revenue |
| 3 | Forecast Performance (V1) | MAE £12,258, RMSE £20,764 |
| 4 | Anomaly Monitoring | 139 anomalies, 84% positive spikes |

### V2 Dashboards (New 7)
| # | Dashboard | Key Finding |
|---|---|---|
| 5 | Revenue Intelligence & Growth Analytics | YoY −0.13%, Nov best, Feb worst, MoM trends |
| 6 | Product Intelligence & Investment Strategy (P1) | Cakestand £330K top, 3,172 Monitor products |
| 7 | Product Intelligence & Investment Strategy (P2) | 4-quadrant performance matrix, contribution % |
| 8 | V1 vs V2 Forecast Performance | MAE +40.87%, R² +80.72% |
| 9 | Forecast Monitoring & Operations Intelligence | WAPE 14.4%, V2 error vs V1 error comparison |
| 10 | V2 Business Impact Analysis | £450,900 quarterly improvement |
| 11 | Customer Segmentation & Retention Intelligence | Champions £9,552, At Risk 1,411 customers |

---

## SQL Analytics Layer

15 analytics views built in PostgreSQL covering the full business intelligence stack:

```
sql/analytics/
├── 01_customer_rfm_base.sql
├── 02_customer_rfm_segmentation.sql
├── 03_customer_segment_revenue.sql
├── 04_customer_segment_profile.sql
├── 05_update_customer_dimension.sql
├── 06_revenue_monthly_summary.sql
├── 07_revenue_seasonality.sql
├── 08_monthly_growth_analysis.sql
├── 09_yoy_revenue_analysis.sql
├── 10_revenue_executive_summary.sql
├── 11_product_revenue_analysis.sql
├── 12_product_quantity_analysis.sql
├── 13_product_revenue_contribution.sql
├── 14_product_performance_matrix.sql
└── 15_product_investment_analysis.sql
```

---

## Architecture

```
Raw Excel (data/raw/)
        │
        ▼
01 — Data Profiling       ← observation only, profiling_summary.json
02 — Data Cleaning        ← cleaning_audit_log.csv, 4 staging CSVs
03 — EDA                  ← business findings documented
        │
        ▼
PostgreSQL retail_db      ← validated dimensional warehouse
  Dimensions: dim_date, dim_product (is_merchandise),
              dim_customer (Unknown surrogate),
              dim_country, dim_holiday_uk
  Facts: fact_sales, fact_returns, fact_adjustments
  ML: ml_rfm_segments, ml_anomaly_scores, revenue_forecast
  Features: feature_daily_enriched, feature_daily_model_input
  Analytics: 15 SQL views (revenue, product, customer, growth)
        │
        ├── 04 — RFM Segmentation
        ├── 05 — Anomaly Detection
        └── 06 — Forecasting (Baseline → SARIMA → V1 → V2 → SHAP)
        │
        ▼
Tableau (11 Dashboards)   Power BI / DAX (in progress)
        │
        ▼  [Planned]
GCP: BigQuery + Cloud Run
FastAPI + Docker + CI/CD
LangGraph RAG AI Agent + Voice Agent
```

---

## Project Structure

```
retail-revenue-intelligence/
│
├── data/
│   ├── raw/online_retail_ii/online_retail_II.xlsx
│   ├── staging/
│   │   ├── sales_main.csv
│   │   ├── returns_cancellations.csv
│   │   ├── accounting_adjustments.csv
│   │   └── non_merchandise_codes.csv
│   └── exports/
│
├── docs/
│   ├── ABSTRACT.md
│   ├── ABOUT_THE_ANALYST.md
│   ├── data_findings.md
│   ├── HOW_TO_READ_NOTEBOOKS.md
│   ├── TABLEAU_GUIDE.md
│   └── validation_benchmark.md
│
├── knowledge_base/
│   ├── project_findings/
│   │   ├── eda_findings.md
│   │   ├── rfm_findings.md
│   │   ├── anomaly_findings.md
│   │   ├── forecast_results.md
│   │   ├── business_impact_findings.md
│   │   ├── revenue_intelligence_findings.md
│   │   └── product_intelligence_findings.md
│   ├── data_context/
│   │   ├── data_dictionary.md
│   │   └── business_rules.md
│   └── model_documentation/
│       ├── model_limitations.md
│       └── v2_roadmap.md
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_rfm_segmentation.ipynb
│   ├── 05_anomaly_detection.ipynb
│   └── 06_forecasting.ipynb
│
├── outputs/reports/
│   ├── profiling_summary.json
│   ├── cleaning_audit_log.csv
│   └── forecast_summary_xgboost.json
│
├── sql/
│   ├── analytics/          ← 15 business intelligence views
│   ├── queries/            ← ad hoc analysis queries
│   ├── schema/             ← table definitions + holiday + feature tables
│   ├── seeds/              ← seed data + UK holiday seed
│   └── validation/         ← post-load validation queries
│
├── src/
│   ├── ml/isolation_forest.py
│   └── utils/db_loader.py
│
├── tableau/
│   ├── workbooks/          ← 11 .twb files
│   ├── screenshots/v1/     ← 4 V1 PNGs
│   ├── screenshots/v2/     ← 7 V2 PNGs
│   └── README.md
├── tests/test_data_quality.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Validation Benchmarks

| Metric | Value |
|---|---|
| Raw rows | 1,067,371 |
| Valid sales rows | 1,007,914 |
| Total revenue | £20,476,634.00 |
| Merchandise revenue | £19,701,497.66 |
| Unique customers | 5,942 |
| Forecasting series (continuous) | 739 rows |
| Holdout rows | 90 |
| V2 MAE | £7,248 |
| V2 RMSE | £15,641 |
| V2 WAPE | 14.41% |
| V2 R² | 0.631 |
| Total anomalies | 139 |
| SQL analytics views | 15 |
| Tableau dashboards | 11 |

---

## Notebooks Reading Order

| Notebook | Purpose |
|---|---|
| 01_data_understanding | Profiling — observation only |
| 02_data_cleaning | Cleaning with formal audit trail |
| 03_eda | EDA on staging data |
| 04_rfm_segmentation | RFM scoring + PostgreSQL write-back |
| 05_anomaly_detection | IsolationForest country-level scoring |
| 06_forecasting | Baseline → SARIMA → XGBoost V1 → V2 → SHAP |

---

## Key Architecture Decisions

| Decision | Reason |
|---|---|
| EDA before schema design | Discovered non-merchandise codes before committing to schema |
| No db_ready CSV layer | Column filtering in loader script, not duplicate files |
| Returns in separate fact table | Prevents silent revenue understatement |
| Country-level anomaly detection | Prevents UK volume dominating the anomaly budget |
| Holiday dimension seeded | Enables V2 forecasting and future promotional analysis |
| feature_daily_enriched table | Clean separation of ML feature engineering from raw warehouse |
| Same 90-day holdout for all models | Ensures fair V1 vs V2 comparison |

---

## Tech Stack

**Data & ML:** Python 3.12 · Pandas · NumPy · scikit-learn · XGBoost ·
LightGBM · statsmodels · SHAP · SQLAlchemy

**Database:** PostgreSQL 17.9

**BI:** Tableau Desktop

**Planned:** GCP (BigQuery · Cloud Storage · Cloud Run) · Docker ·
FastAPI · LangChain · LangGraph · Gemini 1.5 Flash · ChromaDB ·
Qdrant · CI/CD (GitHub Actions)

---

## Important Notes

1. **Currency:** All values are GBP (£).
2. **RFM correction:** An earlier dashboard version had inverted segment
   labels. The current version is correct — Champions show highest value
   (£9,552), highest frequency (17.71), lowest recency (25.1 days).
3. **YoY growth of −0.13%** is not a business failure. Revenue is nearly
   flat year-over-year while H2 2011 shows clear acceleration vs H2 2010.
   The negative figure is driven by the partial December 2011 series.
4. **Paper Craft Little Birdie** (£168,470, 1 order) is a single-invoice
   bulk purchase anomaly — not a recurring product line.

---

## Contact

**Built by:** Pratik Chetry
**LinkedIn:** [Your LinkedIn URL]
**GitHub:** [This repository URL]
**Tableau Public:** [Add after publishing]

Open to remote roles in Data Science, Analytics Engineering, ML Engineering.