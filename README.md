# **Global Air Quality: Trends & Health Impacts**  

*Advanced EDA, Statistical Modeling & Interactive Dashboard*

A high-standard, end-to-end exploratory data analysis investigating how ambient air pollution (PM2.5) relates to health outcomes (life expectancy), socio-economic indicators, and emissions across countries.

---

## **📌 Live Resources**

- **Interactive App:** [Streamlit Dashboard](https://nazlicancigal-global-air-quality-eda-appstreamlit-app-vahyfg.streamlit.app/)  
- **Analysis Notebook:** [`notebooks/01_eda.ipynb`](notebooks/01_eda.ipynb)

---

## **🔍 Why This Project?**

- Real-world **data sourcing** from APIs & official CSVs.
- Complex **data cleaning & merging** (multi-source harmonization).
- **Statistical reasoning** beyond plotting — robust regression with controls.
- **Interactive storytelling** via a public dashboard.
- Follows **CRISP-DM** and **production-grade repo hygiene**.

---

## **🗺 Project Plan (CRISP-DM)**

1. **Business Understanding** — Identify global and regional patterns linking air quality to life expectancy.
2. **Data Understanding** — WHO PM2.5, World Bank indicators (life expectancy, GDP, urbanization), CO₂.
3. **Data Preparation** — Country-code harmonization, missingness handling, normalization.
4. **Modeling** — OLS regression with robust SEs, standardized coefficients, VIF analysis.
5. **Evaluation** — Sanity checks, sensitivity analyses, model comparison (raw vs log GDP).
6. **Deployment** — Streamlit dashboard for exploration.

---

## **📊 Methodology Summary**

- **Data**: WHO PM2.5 (country-year, `Dim1 == "Total"`) + World Bank socio-economic indicators, 2000–2023.
- **Cleaning**: ISO3 harmonization, numeric coercion, duplicate handling.
- **Enrichment**: Added World Bank metadata for **region** and **income group**.
- **EDA**:
  - PM2.5 trends by **region** and **income group**.
  - Cross-sectional relationships (PM2.5 ↔ life expectancy, GDP).
  - Distribution and missingness checks.
- **Model**:
  - OLS regression:  
    `life_expectancy ~ pm25 + log_gdp_per_capita + urban_pop_%`
  - Robust SEs (HC3), standardized coefficients, 95% CIs, VIF diagnostics.
- **Reproducibility**: Automated data fetching & merging scripts (`src/`), documented pipeline.

---

## **📈 Key Findings**
>
> Replace `X`/`Y` with your actual results - this will require detailed analysis.

- A +1 µg/m³ increase in PM2.5 is associated with ≈ ***X.X years lower*** life expectancy (p < 0.01), controlling for GDP & urbanization.
- Log-GDP model outperforms raw GDP (ΔAIC = *X*; adj. R² = *Y*), showing better fit and interpretability.
- Regions **A/B** improved most since 2010; **Region C** shows slowest progress.
- GDP per capita (log scale) is strongly negatively associated with PM2.5, consistent with environmental Kuznets curve patterns.

---

## **🖥 Interactive Dashboard**

Run locally:

```bash
python app/dashboard.py
```

Or explore the [Streamlit live app](https://nazlicancigal-global-air-quality-eda-appstreamlit-app-vahyfg.streamlit.app/) with:

- Filters for **Region** and **Income Group**
- Year slider for historical exploration
- GDP vs Life Expectancy scatter (size: urbanization, color: region, hover: PM2.5)
- PM2.5 trends over time by region

---

## **⚙️ Getting Started**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Optional: install pre-commit hooks
pre-commit install
```

---

## **📂 Data Sources**

- WHO Global Ambient Air Pollution (PM2.5)
- World Bank API:
  - Life expectancy (`SP.DYN.LE00.IN`)
  - GDP per capita (`NY.GDP.PCAP.CD`)
  - Urban population % (`SP.URB.TOTL.IN.ZS`)
  - CO₂ per capita (`EN.ATM.CO2E.PC`)

---

## **🛠 Reproducible Commands**

```bash
# Fetch World Bank data
python src/fetch_worldbank.py --indicators SP.DYN.LE00.IN NY.GDP.PCAP.CD SP.URB.TOTL.IN.ZS EN.ATM.CO2E.PC --start 2000 --end 2023

# Merge with WHO PM2.5 (after placing file in data/external/)
python src/process_merge.py --who_csv data/external/who_pm25.csv

# Start JupyterLab for analysis
jupyter lab
```

---

## **📦 Deliverables**

- **Notebook:** Narrative EDA & regression analysis.
- **Figures:** Publication-quality PNGs in `reports/figures/`.
- **Dashboard:** Local Dash app & live Streamlit app.
- **Reports:** Regression tables, model comparison CSVs.

![CI](https://github.com/<you>/global-air-quality-eda/actions/workflows/ci.yaml/badge.svg)
[![codecov](https://codecov.io/gh/<you>/global-air-quality-eda/branch/main/graph/badge.svg)](https://codecov.io/gh/<you>/global-air-quality-eda)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
