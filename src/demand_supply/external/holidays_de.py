from __future__ import annotations

from datetime import date
import pandas as pd
import holidays


def lower_saxony_holidays(start: str | date, end: str | date) -> pd.DataFrame:
    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    years = list(range(start_ts.year, end_ts.year + 1))
    calendar = holidays.Germany(years=years, subdiv="NI", language="de")
    rows = [
        {"ds": pd.Timestamp(day), "holiday": name, "is_public_holiday": 1}
        for day, name in calendar.items()
        if start_ts.date() <= day <= end_ts.date()
    ]
    return pd.DataFrame(rows, columns=["ds", "holiday", "is_public_holiday"])
