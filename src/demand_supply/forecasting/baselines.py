from __future__ import annotations
import numpy as np
import pandas as pd


def seasonal_naive(history: pd.DataFrame, horizon_days: int, season: int = 7) -> pd.DataFrame:
    data = history.sort_values("ds")
    if data.empty:
        raise ValueError("history is empty")
    last = pd.Timestamp(data["ds"].max())
    pattern = data["y"].tail(season).to_numpy(dtype=float)
    values = np.resize(pattern, horizon_days)
    return pd.DataFrame({"ds": pd.date_range(last + pd.Timedelta(days=1), periods=horizon_days), "yhat": values})


def moving_average(history: pd.DataFrame, horizon_days: int, window: int = 28) -> pd.DataFrame:
    data = history.sort_values("ds")
    level = float(data["y"].tail(window).mean())
    last = pd.Timestamp(data["ds"].max())
    return pd.DataFrame({"ds": pd.date_range(last + pd.Timedelta(days=1), periods=horizon_days), "yhat": level})
