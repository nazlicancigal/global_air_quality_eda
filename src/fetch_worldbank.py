from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
import requests

BASE = "https://api.worldbank.org/v2/country/all/indicator/{ind}?format=json&per_page=20000&date={start}:{end}"


def fetch_indicator(ind: str, start: int, end: int) -> pd.DataFrame:
    url = BASE.format(ind=ind, start=start, end=end)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json()
    rows = data[1] if len(data) > 1 else []
    df = pd.json_normalize(rows)
    if df.empty:
        return pd.DataFrame(columns=["country", "iso3", "date", "value", "indicator"])
    df = df.rename(
        columns={
            "country.value": "country",
            "countryiso3code": "iso3",
            "date": "year",
            "value": "value",
        }
    )
    df["indicator"] = ind
    df["year"] = df["year"].astype(int)
    return df[["country", "iso3", "year", "value", "indicator"]]


def main(indicators: list[str], start: int, end: int, outdir: str):
    Path(outdir).mkdir(parents=True, exist_ok=True)
    frames = []
    for ind in indicators:
        print(f"Fetching {ind}...")
        df = fetch_indicator(ind, start, end)
        df.to_csv(Path(outdir) / f"worldbank_{ind}.csv", index=False)
        frames.append(df)
        time.sleep(0.5)
    all_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    all_df.to_csv(Path(outdir) / "worldbank_all.csv", index=False)
    print(f"Saved {len(all_df):,} rows to {Path(outdir)/'worldbank_all.csv'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--indicators", nargs="+", required=True)
    ap.add_argument("--start", type=int, default=2000)
    ap.add_argument("--end", type=int, default=2023)
    ap.add_argument("--outdir", default="data/external")
    args = ap.parse_args()
    main(args.indicators, args.start, args.end, args.outdir)
