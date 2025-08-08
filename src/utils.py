from __future__ import annotations

import pandas as pd
import pycountry


def standardize_country_names(df: pd.DataFrame, country_col: str = "country") -> pd.DataFrame:
    """Attempt to standardize country names and add ISO3 codes."""
    df = df.copy()
    iso3 = []
    for name in df[country_col].astype(str):
        code = None
        try:
            c = pycountry.countries.search_fuzzy(name)[0]
            code = c.alpha_3
        except Exception:
            code = None
        iso3.append(code)
    df["iso3"] = iso3
    return df


def wide_to_long(df: pd.DataFrame, id_vars: list[str]) -> pd.DataFrame:
    year_cols = [c for c in df.columns if str(c).isdigit()]
    return df.melt(
        id_vars=id_vars, value_vars=year_cols, var_name="year", value_name="value"
    ).assign(year=lambda d: d["year"].astype(int))
