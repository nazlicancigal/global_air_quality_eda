import pandas as pd

from src.utils import standardize_country_names


def test_standardize_country_names():
    df = pd.DataFrame({"country": ["Germany", "Türkiye", "United States"]})
    out = standardize_country_names(df, "country")
    assert "iso3" in out.columns
    assert out["iso3"].notna().all()
