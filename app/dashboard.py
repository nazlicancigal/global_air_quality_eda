import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

# Load enriched data saved from the notebook
D_PATH = "data/processed/enriched_country_year.csv"
d = pd.read_csv(D_PATH)

# Basic cleanliness: ensure expected columns exist
required = {
    "iso3",
    "country",
    "year",
    "pm25",
    "life_expectancy_yrs",
    "gdp_per_capita_usd",
    "urban_pop_pct",
    "region",
    "income_group",
}
missing = required - set(d.columns)
if missing:
    raise ValueError(
        f"Missing columns in {D_PATH}: {missing}. Re-run the notebook"
        f" cell that saves the enriched dataset."
    )

# Build filter options
region_opts = [{"label": r, "value": r} for r in sorted(d["region"].dropna().unique())]
income_opts = [{"label": g, "value": g} for g in sorted(d["income_group"].dropna().unique())]
year_min, year_max = int(d["year"].min()), int(d["year"].max())

app = dash.Dash(__name__)
app.title = "Global Air Quality Dashboard"

app.layout = html.Div(
    [
        html.H1("Global Air Quality Dashboard", style={"textAlign": "center", "marginBottom": 8}),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Region"),
                        dcc.Dropdown(
                            region_opts, multi=True, id="region_dd", placeholder="All regions"
                        ),
                    ],
                    style={"flex": 1, "minWidth": 220, "marginRight": 12},
                ),
                html.Div(
                    [
                        html.Label("Income Group"),
                        dcc.Dropdown(
                            income_opts, multi=True, id="income_dd", placeholder="All income levels"
                        ),
                    ],
                    style={"flex": 1, "minWidth": 220, "marginRight": 12},
                ),
                html.Div(
                    [
                        html.Label("Year"),
                        dcc.Slider(
                            min=year_min,
                            max=year_max,
                            step=1,
                            value=year_max,
                            id="year_slider",
                            marks={int(y): str(int(y)) for y in sorted(d["year"].unique())[::2]},
                        ),
                    ],
                    style={"flex": 2, "minWidth": 300},
                ),
            ],
            style={"display": "flex", "gap": 8, "marginBottom": 12, "flexWrap": "wrap"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Checklist(
                            options=[{"label": " Log GDP scale", "value": "logx"}],
                            value=["logx"],
                            id="logx_ck",
                            style={"marginBottom": 8},
                        ),
                        dcc.Graph(id="scatter_main"),
                    ],
                    style={"flex": 1, "minWidth": 400},
                ),
            ],
            style={"display": "flex", "gap": 16, "flexWrap": "wrap"},
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Average PM2.5 by Region Over Time", style={"marginBottom": 0}),
                        dcc.Graph(id="line_region"),
                    ],
                    style={"flex": 1, "minWidth": 400},
                ),
            ],
            style={"display": "flex", "gap": 16, "flexWrap": "wrap", "marginTop": 8},
        ),
    ],
    style={"padding": 16},
)


@app.callback(
    Output("scatter_main", "figure"),
    Output("line_region", "figure"),
    Input("region_dd", "value"),
    Input("income_dd", "value"),
    Input("year_slider", "value"),
    Input("logx_ck", "value"),
)
def update(region_vals, income_vals, year_val, logx_vals):
    df = d.copy()

    # Filters
    if region_vals:
        df = df[df["region"].isin(region_vals)]
    if income_vals:
        df = df[df["income_group"].isin(income_vals)]

    # Year slice for scatter
    df_year = df[df["year"] == year_val]

    # Scatter: PM2.5 vs Life Expectancy (color: region, size: urban %, hover: country)
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
            "urban_pop_pct": ":.1f",
            "pm25": ":.2f",
            "region": True,
            "income_group": True,
        },
        labels={
            "gdp_per_capita_usd": "GDP per Capita (USD)",
            "life_expectancy_yrs": "Life Expectancy (Years)",
            "urban_pop_pct": "Urban Population (%)",
            "pm25": "PM2.5 (µg/m³)",
        },
        title=f"Life Expectancy vs GDP · Year {year_val}",
    )
    if "logx" in (logx_vals or []):
        fig_scatter.update_xaxes(type="log")

    # Add a trendline per region? Could be noisy; instead, keep it clean for interpretability.

    # Line: Avg PM2.5 over time by region
    df_line = df.groupby(["year", "region"], as_index=False)["pm25"].mean()
    fig_line = px.line(
        df_line,
        x="year",
        y="pm25",
        color="region",
        labels={"pm25": "Avg PM2.5 (µg/m³)", "year": "Year"},
        title="Average PM2.5 Over Time by Region",
    )

    # Styling tweaks
    fig_scatter.update_layout(legend_title_text="Region", margin=dict(l=10, r=10, t=60, b=10))
    fig_line.update_layout(legend_title_text="Region", margin=dict(l=10, r=10, t=60, b=10))

    return fig_scatter, fig_line


if __name__ == "__main__":
    app.run_server(debug=True)
