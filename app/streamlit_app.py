import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Global Air Quality", layout="wide")

# Load data
DATA_PATH = "data/processed/enriched_country_year.csv"
d = pd.read_csv(DATA_PATH)

# Sidebar filters
st.sidebar.header("Filters")
regions = sorted(d["region"].dropna().unique())
income_groups = sorted(d["income_group"].dropna().unique())
years = sorted(d["year"].dropna().astype(int).unique())

region_sel = st.sidebar.multiselect("Region", regions, default=regions)
income_sel = st.sidebar.multiselect("Income Group", income_groups, default=income_groups)
year_sel = st.sidebar.slider(
    "Year", min_value=int(min(years)), max_value=int(max(years)), value=int(max(years))
)
logx = st.sidebar.checkbox("Log scale: GDP per Capita", value=True)

df = d[(d["region"].isin(region_sel)) & (d["income_group"].isin(income_sel))]
df_year = df[df["year"] == year_sel]

st.title("Global Air Quality Dashboard")

# Top KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Countries", f"{df_year['iso3'].nunique():,}")
col2.metric("Avg PM2.5 (µg/m³)", f"{df_year['pm25'].mean():.2f}")
col3.metric("Avg Life Expectancy", f"{df_year['life_expectancy_yrs'].mean():.1f} yrs")

# Scatter: GDP vs Life Expectancy
fig_scatter = px.scatter(
    df_year,
    x="gdp_per_capita_usd",
    y="life_expectancy_yrs",
    color="region",
    size="urban_pop_pct",
    hover_name="country",
    hover_data={
        "gdp_per_capita_usd": ":,.0f",
        "life_expectancy_yrs": ":.1f",
        "pm25": ":.2f",
        "income_group": True,
    },
    labels={
        "gdp_per_capita_usd": "GDP per Capita (USD)",
        "life_expectancy_yrs": "Life Expectancy (Years)",
        "urban_pop_pct": "Urban Pop. (%)",
        "pm25": "PM2.5 (µg/m³)",
    },
    title=f"Life Expectancy vs GDP per Capita — {year_sel}",
)
if logx:
    fig_scatter.update_xaxes(type="log")

# Line: PM2.5 over time by region
df_line = df.groupby(["year", "region"], as_index=False)["pm25"].mean()
fig_line = px.line(
    df_line,
    x="year",
    y="pm25",
    color="region",
    labels={"pm25": "Avg PM2.5 (µg/m³)", "year": "Year"},
    title="Average PM2.5 Over Time by Region",
)

# Layout
st.plotly_chart(fig_scatter, use_container_width=True)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("—")
st.caption(
    "Data: WHO PM2.5 (Total); World Bank indicators and metadata "
    "(Life Expectancy, GDP, Urbanization, Region, Income Group)."
)
