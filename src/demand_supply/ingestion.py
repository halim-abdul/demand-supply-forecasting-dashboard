from __future__ import annotations

import pandas as pd
from sqlalchemy import select

from .db import get_engine, init_db, insert_sales, sales
from .schemas import SaleEvent


def ingest_sale_payload(payload: dict) -> SaleEvent:
    event = SaleEvent.model_validate(payload)
    insert_sales([event])
    return event


def load_sales(store_id: str | None = None) -> pd.DataFrame:
    engine = init_db(get_engine())
    query = select(sales)
    if store_id:
        query = query.where(sales.c.store_id == store_id)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)


def daily_product_sales(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["ds", "store_id", "product_id", "category", "y", "revenue"])
    data = frame.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
    data["ds"] = data["timestamp"].dt.tz_convert("Europe/Berlin").dt.tz_localize(None).dt.floor("D")
    data["revenue"] = data["quantity"] * data["unit_price"]
    group = ["ds", "store_id", "product_id", "category"]
    if "district" in data.columns:
        group.append("district")
    return data.groupby(group, dropna=False, as_index=False).agg(y=("quantity", "sum"), revenue=("revenue", "sum"))
