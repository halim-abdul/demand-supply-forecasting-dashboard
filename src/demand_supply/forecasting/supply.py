from __future__ import annotations

import pandas as pd


def project_supply_balance(
    forecast: pd.DataFrame,
    on_hand: float,
    inbound: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Project stock using forecast demand and dated inbound purchase quantities.

    `forecast` requires ds/yhat. `inbound`, when supplied, requires ds/quantity.
    """
    out = forecast[["ds", "yhat"]].copy().sort_values("ds")
    out["ds"] = pd.to_datetime(out["ds"])
    if inbound is None or inbound.empty:
        supply = pd.DataFrame({"ds": out["ds"], "inbound_supply": 0.0})
    else:
        supply = inbound.copy()
        supply["ds"] = pd.to_datetime(supply["ds"])
        supply = (
            supply.groupby("ds", as_index=False)["quantity"]
            .sum()
            .rename(columns={"quantity": "inbound_supply"})
        )
    out = out.merge(supply, on="ds", how="left")
    out["inbound_supply"] = out["inbound_supply"].fillna(0.0)
    stock = float(on_hand)
    projected = []
    for row in out.itertuples(index=False):
        stock += float(row.inbound_supply) - float(row.yhat)
        projected.append(stock)
    out["projected_stock"] = projected
    out["projected_shortage"] = out["projected_stock"] < 0
    return out
