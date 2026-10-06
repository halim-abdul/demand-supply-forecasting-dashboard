from __future__ import annotations

from fastapi import BackgroundTasks, FastAPI

from demand_supply.db import init_db, insert_inventory
from demand_supply.ingestion import ingest_sale_payload
from demand_supply.schemas import ForecastRequest, InventorySnapshot, SaleEvent

app = FastAPI(title="Göttingen Demand Supply API", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "demand-supply-api"}


@app.post("/api/v1/sales", status_code=202)
def post_sale(event: SaleEvent) -> dict:
    saved = ingest_sale_payload(event.model_dump())
    return {"accepted": True, "event_id": saved.event_id}


@app.post("/api/v1/inventory", status_code=202)
def post_inventory(snapshot: InventorySnapshot) -> dict:
    insert_inventory([snapshot])
    return {
        "accepted": True,
        "store_id": snapshot.store_id,
        "product_id": snapshot.product_id,
        "on_hand": snapshot.on_hand,
    }


@app.post("/api/v1/forecast/refresh", status_code=202)
def refresh_forecast(request: ForecastRequest, background_tasks: BackgroundTasks) -> dict:
    del background_tasks
    return {
        "accepted": True,
        "store_id": request.store_id,
        "horizon_days": request.horizon_days,
    }
