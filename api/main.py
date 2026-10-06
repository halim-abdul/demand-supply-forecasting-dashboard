from __future__ import annotations
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from demand_supply.db import init_db
from demand_supply.ingestion import ingest_sale_payload
from demand_supply.schemas import SaleEvent, ForecastRequest

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

@app.post("/api/v1/forecast/refresh", status_code=202)
def refresh_forecast(request: ForecastRequest, background_tasks: BackgroundTasks) -> dict:
    # Hook point for a queue/worker or n8n callback. Long model jobs should not block POS ingestion.
    return {"accepted": True, "store_id": request.store_id, "horizon_days": request.horizon_days}
