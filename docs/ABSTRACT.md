# Project Abstract

## Retail Revenue Intelligence & Anomaly Detection

This project builds a retail analytics system from the **Online Retail II** dataset to understand how a retail business is performing, where its risks exist, and how its reporting should be structured for trustworthy decision-making.

The work began with raw data profiling of the original Excel workbook, followed by controlled cleaning and exploratory analysis. The raw data contained duplicates, returns, accounting-style adjustments, missing customer identifiers, and non-merchandise operational stock codes such as postage and manual entries. These issues meant the dataset could not be used directly for dashboards, SQL reporting, or modeling without first separating the different business behaviors inside it.

A cleaned staging layer was created to preserve only the permanent business-ready outputs needed for downstream work:
- `sales_main.csv`
- `returns_cancellations.csv`
- `accounting_adjustments.csv`
- `non_merchandise_codes.csv`

The cleaned sales staging dataset contains **1,007,914 valid sales rows** and **20,476,634.02** in total revenue. Exploratory analysis showed that the business is highly concentrated in the **United Kingdom**, which contributes **85.03%** of total revenue, and that revenue is strongly seasonal, with the highest months being **November**, **October**, and **December**. The analysis also showed that some high-revenue stock codes are not real merchandise, which means product reporting must distinguish between merchandise and operational/service entries to remain credible.

Customer-level exploration further showed that revenue is highly concentrated among a relatively small number of identifiable customers. This supports the later use of **RFM segmentation**, customer monitoring, and high-value customer analysis, but only on rows with valid customer identifiers.

The project is designed to use **PostgreSQL** as its central analytical data layer, with later integration into **Tableau** for dashboarding and **Power BI / DAX** as a companion analytics showcase. Future stages of the project include:
- PostgreSQL loading and reconciliation against benchmark totals
- SQL views for reporting
- RFM segmentation
- anomaly detection
- forecasting
- dashboard development
- later extension with **Rossmann Store Sales** and **NOAA weather data** for stronger time-series and external-factor analysis

Overall, this project is structured as a senior-level analytics workflow: profile first, clean with an audit trail, validate benchmark numbers, build a trustworthy data layer, and only then move into dashboards and modeling.