from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PRODUCTS = {
    "MILK-1L": ("dairy", 72, 1.29),
    "BREAD-WHEAT": ("bakery", 58, 2.49),
    "BANANA-KG": ("produce", 64, 1.89),
    "WATER-6PK": ("beverages", 38, 3.99),
    "PASTA-500G": ("pantry", 31, 1.49),
    "EGGS-10": ("dairy", 43, 3.19),
    "ICECREAM": ("frozen", 21, 3.79),
    "SOUP": ("pantry", 18, 2.59),
}
DISTRICTS = [
    "Innenstadt",
    "Oststadt",
    "Suedstadt",
    "Weststadt",
    "Nordstadt",
    "Weende",
    "Geismar",
    "Grone",
]


def make_demo(start="2024-01-01", end="2026-12-31", seed=42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    dates = pd.date_range(start, end, freq="D")
    for ds in dates:
        dow = ds.dayofweek
        yearly = 1 + 0.10 * np.sin(2 * np.pi * ds.dayofyear / 365.25)
        weekend = 1.12 if dow in (4, 5) else (0.82 if dow == 6 else 1.0)
        christmas = 1.35 if ds.month == 12 and ds.day < 25 else 1.0
        summer = 1.22 if ds.month in (6, 7, 8) else 1.0
        for product, (category, base, price) in PRODUCTS.items():
            product_season = summer if product in ("WATER-6PK", "ICECREAM") else 1.0
            if product == "SOUP" and ds.month in (10, 11, 12, 1, 2):
                product_season = 1.2
            demand = max(1, base * yearly * weekend * christmas * product_season)
            qty = int(max(0, rng.normal(demand, max(2, demand * 0.12))))
            rows.append(
                {
                    "ds": ds,
                    "store_id": "GOE-001",
                    "product_id": product,
                    "category": category,
                    "district": rng.choice(DISTRICTS),
                    "y": qty,
                    "unit_price": price,
                    "promotion": bool(rng.random() < 0.06),
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/processed/demo_daily_sales.parquet")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    make_demo().to_parquet(output, index=False)
    print(f"wrote {output}")
