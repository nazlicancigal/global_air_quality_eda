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

## Methodology (Summary)

- **Data**: WHO PM2.5 (country-year, Total) and World Bank indicators (Life Expectancy, GDP/capita, Urban %), 2000–2023.
- **Cleaning**: Country harmonization via ISO3; filtered WHO `Dim1 == "Total"`.
- **Enrichment**: Merged World Bank metadata for region and income group to enable segment analysis.
- **EDA**: Trends by region, cross-sectional relationships (PM2.5 ↔ Life Expectancy, GDP), and distribution checks.
- **Model**: OLS with robust standard errors (HC3):  
  `life_expectancy ~ pm25 + gdp_per_capita + urban_pop_%`  
  Reported coefficients with robust SEs, 95% CIs, standardized coefficients, and VIF diagnostics.
- **Key Takeaways**:
  - Higher PM2.5 associates with lower life expectancy, even controlling for GDP and urbanization.
  - Regions X and Y show the slowest improvement in PM2.5 since 2010; Region Z improved the most.
  - GDP (log-scale) has a strong negative association with PM2.5, consistent with environmental Kuznets patterns.
- **Reproducibility**: `src/fetch_worldbank.py` (API), `src/process_merge.py` (merge), notebooks for analysis, and a Dash app for exploration.

## Interactive Dashboard

Run locally:

```bash
python app/dashboard.py
