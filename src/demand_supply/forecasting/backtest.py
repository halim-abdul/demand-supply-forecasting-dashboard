from __future__ import annotations
import pandas as pd
from .metrics import mae, rmse, wape, bias
from .prophet_model import ProphetDemandModel


def rolling_backtest(frame: pd.DataFrame, horizon: int = 28, folds: int = 3) -> pd.DataFrame:
    data = frame.sort_values("ds").reset_index(drop=True)
    rows = []
    for fold in range(folds):
        test_end = len(data) - fold * horizon
        test_start = test_end - horizon
        train = data.iloc[:test_start]
        test = data.iloc[test_start:test_end]
        if len(train) < 60 or len(test) == 0:
            continue
        model = ProphetDemandModel().fit(train)
        pred = model.predict(test)
        rows.append({"fold": fold+1, "mae": mae(test.y, pred.yhat), "rmse": rmse(test.y, pred.yhat), "wape": wape(test.y, pred.yhat), "bias": bias(test.y, pred.yhat)})
    return pd.DataFrame(rows)
