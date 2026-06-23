# About This Project & the Analyst Behind It

## Why This Project Was Built

This is a portfolio project designed to reflect how a **senior data analyst in 2026** actually works —
not just writing queries, but architecting a full analytics pipeline that bridges BI tools, Python ML,
and AI-assisted development.

## Tools & Technologies Used

| Layer | Tool | Why |
|---|---|---|
| Database | PostgreSQL 15 | Acts as the single data lake / source of truth |
| ETL & Cleaning | Python + pandas | Repeatable, version-controlled data preparation |
| ML — Anomaly Detection | scikit-learn IsolationForest | Unsupervised; no labelled data required |
| ML — Forecasting | statsmodels SARIMA | Handles retail seasonality well |
| ML — Segmentation | Custom RFM scoring | Industry-standard customer segmentation |
| Visualisation | Tableau | Flexible, stakeholder-friendly dashboards |
| Advanced Analytics | Power BI + DAX | Finance-grade time intelligence measures |
| AI Assistance | GitHub Copilot, Claude, ChatGPT | 3× faster boilerplate; analyst reviews all output |

## What "AI-Augmented" Means Here

AI tools were used to:
- Generate boilerplate SQL and Python (reviewed and corrected by the analyst)
- Suggest DAX measure patterns (validated against Power BI documentation)
- Draft documentation first passes (then rewritten for clarity)

AI tools were **NOT** used to replace understanding. Every piece of code in this project
can be explained line by line by the analyst.

## How to Navigate This Project

1. **Non-technical reader?** → Read `docs/` folder only
2. **Want to see the SQL?** → `sql/` folder
3. **Want to see the Python?** → `notebooks/` folder (run in order 01 → 06)
4. **Want to see the DAX?** → `powerbi/dax/` folder
5. **Want to run the dashboard?** → Open `tableau/retail_dashboard.twbx`
