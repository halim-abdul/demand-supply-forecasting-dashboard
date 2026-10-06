from __future__ import annotations
import numpy as np
import pandas as pd


def robust_sales_anomalies(frame: pd.DataFrame, window: int = 28, z_threshold: float = 4.0) -> pd.DataFrame:
    out = frame.sort_values("ds").copy()
    median = out["y"].rolling(window, min_periods=7).median()
    mad = (out["y"] - median).abs().rolling(window, min_periods=7).median()
    robust_z = 0.6745 * (out["y"] - median) / mad.replace(0, np.nan)
    out["anomaly_score"] = robust_z.abs().fillna(0)
    out["is_anomaly"] = out["anomaly_score"] >= z_threshold
    return out
