from __future__ import annotations

import httpx
import pandas as pd

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"


def fetch_goettingen_weather(latitude: float = 51.5413, longitude: float = 9.9158, forecast_days: int = 16) -> pd.DataFrame:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join([
            "temperature_2m_max", "temperature_2m_min", "precipitation_sum",
            "rain_sum", "snowfall_sum", "wind_speed_10m_max", "weather_code"
        ]),
        "timezone": "Europe/Berlin",
        "forecast_days": min(max(int(forecast_days), 1), 16),
    }
    response = httpx.get(OPEN_METEO, params=params, timeout=20.0)
    response.raise_for_status()
    daily = response.json()["daily"]
    frame = pd.DataFrame(daily).rename(columns={"time": "ds"})
    frame["ds"] = pd.to_datetime(frame["ds"])
    return frame
