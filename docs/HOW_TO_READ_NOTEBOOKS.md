# How to Read the Jupyter Notebooks (Non-Technical Guide)

## What Is a Jupyter Notebook?

Think of it like a **Word document that also runs code**. It has two types of blocks:

- **Grey blocks (code cells)** — This is the actual Python code. You don't need to understand it.
- **White blocks (text cells)** — This explains what the code does, in plain English. Just read these.

## What Does Each Notebook Do?

| Notebook | What It Does | Time to Run |
|---|---|---|
| 01_data_cleaning | Loads raw data, fixes errors, sends to database | ~4 min |
| 02_eda | Creates charts showing patterns in the data | ~2 min |
| 03_rfm_segmentation | Groups customers into loyalty tiers | ~3 min |
| 04_anomaly_detection | Flags days with unusual revenue | ~5 min |
| 05_forecasting | Predicts next 90 days of revenue | ~8 min |
| 06_validation | Confirms all data is correct before sharing | ~1 min |

## To Run Them (Technical Users)

```bash
pip install -r requirements.txt
cp .env.example .env   # Fill in your PostgreSQL password
jupyter notebook notebooks/
```

Run them in order: 01 → 02 → 03 → 04 → 05 → 06

## If You Can't Run Code

Look at the `reports/outputs/` folder — all charts are saved there as PNG files.
You can view them without running anything.
