from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from .external.events import load_local_events
from .external.holidays_de import lower_saxony_holidays


def calendar_features(dates: pd.Series) -> pd.DataFrame:
    ds = pd.to_datetime(dates)
    iso = ds.dt.isocalendar()
    return pd.DataFrame({
        "ds": ds,
        "dow": ds.dt.dayofweek,
        "week": iso.week.astype(int),
        "month": ds.dt.month,
        "quarter": ds.dt.quarter,
        "day_of_month": ds.dt.day,
        "is_weekend": ds.dt.dayofweek.isin([5, 6]).astype(int),
        "is_month_start": ds.dt.is_month_start.astype(int),
        "is_month_end": ds.dt.is_month_end.astype(int),
        "sin_dow": np.sin(2 * np.pi * ds.dt.dayofweek / 7),
        "cos_dow": np.cos(2 * np.pi * ds.dt.dayofweek / 7),
    })


def enrich_daily_sales(
    daily: pd.DataFrame,
    events_path: str | Path = "data/reference/goettingen_events_2026.csv",
    population_path: str | Path = "data/reference/goettingen_population_by_district.csv",
    weather: pd.DataFrame | None = None,
) -> pd.DataFrame:
    out = daily.copy()
    out["ds"] = pd.to_datetime(out["ds"])
    cal = calendar_features(out["ds"])
    for column in cal.columns.drop("ds"):
        out[column] = cal[column].to_numpy()

    holiday = lower_saxony_holidays(out["ds"].min(), out["ds"].max())
    out = out.merge(holiday, on="ds", how="left")
    out["is_public_holiday"] = out["is_public_holiday"].fillna(0).astype(int)
    out["holiday"] = out["holiday"].fillna("")

    events = load_local_events(events_path)
    out = out.merge(events, on="ds", how="left")
    out["event_lift"] = out["event_lift"].fillna(0.0)
    out["event"] = out["event"].fillna("")
    out["event_category"] = out["event_category"].fillna("")

    if weather is not None and not weather.empty:
        weather = weather.copy()
        weather["ds"] = pd.to_datetime(weather["ds"])
        out = out.merge(weather, on="ds", how="left")

    if "district" in out.columns:
        pop = pd.read_csv(population_path)
        pop["population_share"] = pop["population"] / pop["population"].sum()
        out = out.merge(pop[["district", "population", "population_share"]], on="district", how="left")
    return out
