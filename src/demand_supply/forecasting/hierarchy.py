from __future__ import annotations
import pandas as pd


def reconcile_category_to_items(item_forecasts: pd.DataFrame, category_forecast: pd.DataFrame) -> pd.DataFrame:
    """Proportionally reconcile item forecasts to a category-level target per day."""
    items = item_forecasts.copy()
    cat = category_forecast[["ds", "category", "yhat"]].rename(columns={"yhat": "category_yhat"})
    items = items.merge(cat, on=["ds", "category"], how="left")
    denom = items.groupby(["ds", "category"])["yhat"].transform("sum")
    factor = items["category_yhat"] / denom.replace(0, pd.NA)
    items["yhat_reconciled"] = (items["yhat"] * factor.fillna(1.0)).clip(lower=0)
    return items
