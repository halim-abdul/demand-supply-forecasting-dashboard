from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parents[2]


class MarketConfig(BaseModel):
    name: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float
    timezone: str = "Europe/Berlin"
    holiday_country: str = "DE"
    holiday_subdivision: str = "NI"
    currency: str = "EUR"
    default_store_id: str = "GOE-001"


class ForecastConfig(BaseModel):
    horizon_days: int = 56
    prophet_interval_width: float = 0.9
    seasonality_mode: str = "multiplicative"
    min_history_days: int = 90
    safety_stock_service_level: float = 0.95


class InventoryConfig(BaseModel):
    review_period_days: int = 1
    default_lead_time_days: int = 3
    min_days_cover: int = 2
    max_days_cover: int = 18


class AppConfig(BaseModel):
    market: MarketConfig
    forecast: ForecastConfig
    inventory: InventoryConfig
    realtime: dict[str, Any] = Field(default_factory=dict)
    weather: dict[str, Any] = Field(default_factory=dict)


class RuntimeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///demand_supply.db"
    redis_url: str | None = None
    n8n_webhook_url: str | None = None
    app_env: str = "development"


@lru_cache(maxsize=1)
def load_config(path: str | Path | None = None) -> AppConfig:
    cfg_path = Path(path) if path else ROOT / "config" / "goettingen.yaml"
    with cfg_path.open("r", encoding="utf-8") as handle:
        return AppConfig.model_validate(yaml.safe_load(handle))


@lru_cache(maxsize=1)
def runtime_settings() -> RuntimeSettings:
    return RuntimeSettings()
