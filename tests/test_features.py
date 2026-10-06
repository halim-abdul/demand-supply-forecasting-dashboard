import pandas as pd
from demand_supply.features import calendar_features


def test_calendar_features_weekend():
    frame = calendar_features(pd.Series(pd.to_datetime(["2026-10-03", "2026-10-05"])))
    assert frame["is_weekend"].tolist() == [1, 0]
    assert frame["dow"].tolist() == [5, 0]
