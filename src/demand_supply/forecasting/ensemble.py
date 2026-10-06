from __future__ import annotations
import numpy as np
import pandas as pd


def inverse_error_weights(errors: dict[str, float], floor: float = 1e-6) -> dict[str, float]:
    inv = {k: 1.0 / max(float(v), floor) for k, v in errors.items()}
    total = sum(inv.values())
    return {k: v / total for k, v in inv.items()}


def blend_forecasts(forecasts: dict[str, pd.DataFrame], weights: dict[str, float]) -> pd.DataFrame:
    names = list(forecasts)
    if not names:
        raise ValueError("no forecasts supplied")
    base = forecasts[names[0]][["ds"]].copy()
    yhat = np.zeros(len(base), dtype=float)
    lower = np.zeros(len(base), dtype=float)
    upper = np.zeros(len(base), dtype=float)
    for name, frame in forecasts.items():
        w = float(weights.get(name, 0.0))
        yhat += w * frame["yhat"].to_numpy(float)
        lower += w * frame.get("yhat_lower", frame["yhat"]).to_numpy(float)
        upper += w * frame.get("yhat_upper", frame["yhat"]).to_numpy(float)
    base["yhat"] = np.clip(yhat, 0, None)
    base["yhat_lower"] = np.clip(lower, 0, None)
    base["yhat_upper"] = np.clip(upper, 0, None)
    return base
