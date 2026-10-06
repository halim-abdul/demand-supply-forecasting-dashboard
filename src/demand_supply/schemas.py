from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class SaleEvent(BaseModel):
    event_id: str
    timestamp: datetime
    store_id: str = "GOE-001"
    product_id: str
    category: str
    quantity: PositiveInt
    unit_price: PositiveFloat
    district: str | None = None
    promotion: bool = False
    channel: str = "store"


class InventorySnapshot(BaseModel):
    timestamp: datetime
    store_id: str = "GOE-001"
    product_id: str
    on_hand: int = Field(ge=0)
    on_order: int = Field(default=0, ge=0)
    lead_time_days: int = Field(default=3, ge=0)


class ForecastRequest(BaseModel):
    store_id: str = "GOE-001"
    product_ids: list[str] | None = None
    horizon_days: int = Field(default=28, ge=1, le=365)


class ForecastPoint(BaseModel):
    ds: datetime
    product_id: str
    yhat: float
    yhat_lower: float
    yhat_upper: float
    shortage_risk: float | None = None
