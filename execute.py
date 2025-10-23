"""execute.py

Reads sales data from data.xlsx and outputs a small JSON summary to stdout.
Designed to run with Python 3.11+ and pandas 2.3.

Fixes included:
- Removed typo "revenew" and used the correct "revenue" column throughout.
- Corrected rolling 7-day computation by grouping per region and using a time-based rolling window.
- Made the code robust to missing values and ensures JSON-serializable output.
"""

import json
from typing import Any, Dict

import pandas as pd


def _safe_float(x: Any) -> Any:
    """Convert numeric values to float for JSON; return None for NaN/NA."""
    try:
        if pd.isna(x):
            return None
        return float(x)
    except Exception:
        return None


def main() -> None:
    # Read the data (Excel file). This will raise a clear error if file is missing.
    df = pd.read_excel("data.xlsx")

    # Ensure expected columns exist
    expected = {"date", "region", "product", "units", "price"}
    if not expected.issubset(set(df.columns.str.lower())):
        # Try normalizing column names to lower-case mapping if possible
        cols_map = {c: c.lower() for c in df.columns}
        df = df.rename(columns=cols_map)

    # Now required columns should exist (raises KeyError with informative message otherwise)
    if not expected.issubset(set(df.columns)):
        raise KeyError(
            f"Input must contain columns: {expected}. Found: {set(df.columns)}"
        )

    # Ensure types
    df["date"] = pd.to_datetime(df["date"])  # ensure datetime
    df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(0)
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)

    # Compute revenue (units * price)
    df["revenue"] = df["units"] * df["price"]

    # row_count
    row_count = int(len(df))

    # regions: count of distinct regions
    regions_count = int(df["region"].nunique())

    # top_n_products_by_revenue (n=3)
    n = 3
    top_products = (
        df.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(n)
    )
    top_products_list = [
        {"product": row["product"], "revenue": _safe_float(row["revenue"]) }
        for _, row in top_products.iterrows()
    ]

    # rolling_7d_revenue_by_region: for each region, last value of 7-day moving average of daily revenue
    daily_rev = (
        df.groupby(["region", "date"], as_index=False)["revenue"]
        .sum()
        .sort_values(["region", "date"])  # ensure sorted for rolling
    )

    rolling_summary: Dict[str, Any] = {}

    # For each region, compute a time-based 7-day rolling mean on daily revenue and capture the last value.
    for region, g in daily_rev.groupby("region"):
        # Ensure sorted by date and set index for time-based rolling
        g = g.sort_values("date").set_index("date")
        # Calculate 7-day rolling mean (time-based window)
        # Using rolling with a time offset string requires a DatetimeIndex
        rolling = g["revenue"].rolling("7D").mean()
        if len(rolling) == 0:
            last_val = None
        else:
            last_val = _safe_float(rolling.iloc[-1])
        rolling_summary[region] = last_val

    result = {
        "row_count": int(row_count),
        "regions": int(regions_count),
        "top_n_products_by_revenue": top_products_list,
        "rolling_7d_revenue_by_region": rolling_summary,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
