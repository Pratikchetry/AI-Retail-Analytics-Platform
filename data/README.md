# Data Layer Guide

## Purpose
This folder contains the project data layers for the Retail Revenue Intelligence project.

The structure is designed to separate:
- the untouched raw source
- the cleaned staging outputs used for database loading and analysis

---

## Folder structure

```text
data/
├── raw/
│   └── online_retail_ii/
│       └── online_retail_II.xlsx
└── staging/
    ├── sales_main.csv
    ├── returns_cancellations.csv
    ├── accounting_adjustments.csv
    └── non_merchandise_codes.csv