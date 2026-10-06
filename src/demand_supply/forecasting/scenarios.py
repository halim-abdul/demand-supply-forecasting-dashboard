from __future__ import annotations
import pandas as pd


def apply_scenario(
    future: pd.DataFrame,
    weather_multiplier: float = 1.0,
    festival_multiplier: float = 1.0,
    promotion_multiplier: float = 1.0,
    population_growth: float = 0.0,
) -> pd.DataFrame:
    out = future.copy()
    out["scenario_multiplier"] = weather_multiplier * festival_multiplier * promotion_multiplier * (1 + population_growth)
    if "event_lift" in out:
        out["event_lift"] = out["event_lift"].fillna(0) * festival_multiplier
    if "population_share" in out:
        out["population_share"] = out["population_share"].fillna(0) * (1 + population_growth)
    if "promotion" in out:
        out["promotion"] = out["promotion"].fillna(0) * promotion_multiplier
    return out
