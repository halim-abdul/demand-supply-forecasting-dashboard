from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy import Boolean, DateTime, Float, Integer, MetaData, String, Table, Column, create_engine, insert
from sqlalchemy.engine import Engine

from .config import runtime_settings
from .schemas import SaleEvent

metadata = MetaData()

sales = Table(
    "sales",
    metadata,
    Column("event_id", String(96), primary_key=True),
    Column("timestamp", DateTime(timezone=True), nullable=False, index=True),
    Column("store_id", String(32), nullable=False, index=True),
    Column("product_id", String(64), nullable=False, index=True),
    Column("category", String(64), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Float, nullable=False),
    Column("district", String(64)),
    Column("promotion", Boolean, default=False),
    Column("channel", String(32), default="store"),
)

inventory = Table(
    "inventory",
    metadata,
    Column("timestamp", DateTime(timezone=True), primary_key=True),
    Column("store_id", String(32), primary_key=True),
    Column("product_id", String(64), primary_key=True),
    Column("on_hand", Integer, nullable=False),
    Column("on_order", Integer, nullable=False, default=0),
    Column("lead_time_days", Integer, nullable=False, default=3),
)


def get_engine(url: str | None = None) -> Engine:
    return create_engine(url or runtime_settings().database_url, future=True)


def init_db(engine: Engine | None = None) -> Engine:
    engine = engine or get_engine()
    metadata.create_all(engine)
    return engine


def insert_sales(events: Iterable[SaleEvent], engine: Engine | None = None) -> int:
    engine = engine or init_db()
    rows = [event.model_dump() for event in events]
    if not rows:
        return 0
    with engine.begin() as conn:
        conn.execute(insert(sales), rows)
    return len(rows)


def utcnow() -> datetime:
    return datetime.now().astimezone()
