from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_local_events(path: str | Path) -> pd.DataFrame:
    events = pd.read_csv(path, parse_dates=["start_date", "end_date"])
    expanded: list[dict] = []
    for row in events.to_dict("records"):
        for ds in pd.date_range(row["start_date"], row["end_date"], freq="D"):
            expanded.append({
                "ds": ds,
                "event": row["event"],
                "event_category": row["category"],
                "event_lift": float(row["expected_footfall_lift"]),
            })
    if not expanded:
        return pd.DataFrame(columns=["ds", "event", "event_category", "event_lift"])
    return pd.DataFrame(expanded)
