# Global Air Quality: Trends & Health Impacts (Advanced EDA & Storytelling)

A high-standard, end-to-end exploratory data analysis investigating how ambient air pollution (e.g., PM2.5) relates to health outcomes (e.g., life expectancy), socio-economics, and emissions across countries.

## Why this project?

- Showcases data sourcing, cleaning, merging across APIs/CSVs
- Demonstrates statistical reasoning and robust EDA
- Produces interactive storytelling (Dash)
- Follows CRISP-DM and production-grade repo hygiene

## Project Plan (CRISP-DM)

1. **Business Understanding** — What country-level patterns link air quality and health?
2. **Data Understanding** — WHO air quality, World Bank indicators (life expectancy, GDP, urbanization), CO2.
3. **Data Preparation** — Country-code harmonization, outliers, missingness, normalization.
4. **Modeling (lite)** — Inference (OLS/robust), partial correlations; *no heavy ML* needed.
5. **Evaluation** — Sanity checks, sensitivity analyses.
6. **Deployment** — Dash storytelling app + static report.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt

# Pre-commit hooks
pre-commit install
```

## Data Sources (to download/fetch)

- WHO air quality (PM2.5) — CSV (manual download)
- World Bank Indicators via API:
  - Life expectancy (SP.DYN.LE00.IN)
  - GDP per capita (NY.GDP.PCAP.CD)
  - Urban population % (SP.URB.TOTL.IN.ZS)
  - CO2 per capita (EN.ATM.CO2E.PC)

## Reproducible Commands

```bash
python src/fetch_worldbank.py --indicators SP.DYN.LE00.IN NY.GDP.PCAP.CD SP.URB.TOTL.IN.ZS EN.ATM.CO2E.PC --start 2000 --end 2023
python src/process_merge.py --who_csv data/external/who_pm25.csv
jupyter lab
```

## Deliverables

- notebooks/01_eda.ipynb — Narrative EDA
- reports/air_quality_story.md — Long-form writeup
- app/ (optional) — Dash app
- Figures in reports/figures/
