from __future__ import annotations
from statistics import NormalDist
import math
import pandas as pd


def safety_stock(daily_std: float, lead_time_days: int, service_level: float = 0.95) -> float:
    z = NormalDist().inv_cdf(service_level)
    return max(0.0, z * daily_std * math.sqrt(max(lead_time_days, 1)))


def inventory_plan(
    forecast: pd.DataFrame,
    on_hand: float,
    on_order: float = 0,
    lead_time_days: int = 3,
    daily_std: float = 0,
    service_level: float = 0.95,
    review_period_days: int = 1,
) -> dict:
    fc = forecast.sort_values("ds")
    lead_demand = float(fc.head(max(lead_time_days, 1))["yhat"].sum())
    ss = safety_stock(daily_std, lead_time_days, service_level)
    reorder_point = lead_demand + ss
    position = float(on_hand + on_order)
    review_demand = float(fc.head(lead_time_days + review_period_days)["yhat"].sum())
    target = review_demand + ss
    order_qty = max(0.0, target - position)
    avg_daily = max(float(fc.head(14)["yhat"].mean()), 1e-9)
    days_cover = position / avg_daily
    risk = max(0.0, min(1.0, (reorder_point-position) / max(reorder_point, 1e-9)))
    return {
        "inventory_position": round(position, 2), "lead_time_demand": round(lead_demand, 2),
        "safety_stock": round(ss, 2), "reorder_point": round(reorder_point, 2),
        "recommended_order_qty": round(order_qty, 2), "days_cover": round(days_cover, 2),
        "shortage_risk": round(risk, 4), "status": "SHORTAGE_RISK" if position < reorder_point else ("OVERSTOCK" if days_cover > 18 else "HEALTHY")
    }
