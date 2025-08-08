from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.utils import standardize_country_names


def load_worldbank_all(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    pivot = df.pivot_table(
        index=["country", "iso3", "year"], columns="indicator", values="value"
    ).reset_index()
    return pivot


def load_who_pm25(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "country" not in df.columns:
        for c in df.columns:
            if df[c].dtype == "object":
                df = df.rename(columns={c: "country"})
                break
    if "year" not in df.columns:
        for c in df.columns:
            try:
                if df[c].astype(int).between(1950, 2100).any():
                    df = df.rename(columns={c: "year"})
                    break
            except Exception:
                pass
    for c in df.columns:
        if "pm" in c.lower() and "2.5" in c.lower().replace(" ", ""):
            df = df.rename(columns={c: "pm25"})
    df = standardize_country_names(df, "country")
    return df[["country", "iso3", "year", "pm25"]].dropna(subset=["iso3"])


def main(who_csv: str, wb_csv: str, outpath: str):
    wb = load_worldbank_all(wb_csv)
    who = load_who_pm25(who_csv)
    merged = wb.merge(who, on=["iso3", "year"], how="inner")
    Path(outpath).parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(outpath, index=False)
    print(f"Merged shape: {merged.shape}, saved to {outpath}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--who_csv", required=True)
    ap.add_argument("--wb_csv", default="data/external/worldbank_all.csv")
    ap.add_argument("--outpath", default="data/processed/merged_country_year.csv")
    args = ap.parse_args()
    main(args.who_csv, args.wb_csv, args.outpath)
