# Göttingen Demand–Supply Forecasting Dashboard

An end-to-end AI inventory decision platform for a supermarket/warehouse in **Göttingen, Lower Saxony, Germany**. The system turns POS sales into demand forecasts, combines calendar/weather/local-event/catchment signals, projects inbound supply, detects shortage/overstock risk, and exposes the results in a **login-protected Streamlit dashboard** with **n8n automation**.

## What is implemented

- Real-time POS / e-commerce sale ingestion through FastAPI and n8n webhooks
- PostgreSQL/SQLite persistence with typed Pydantic data contracts
- Daily SKU/store demand aggregation
- Prophet forecasting with weekly/yearly/monthly seasonality
- Seasonal-naive and moving-average baselines
- Rolling-origin backtesting with MAE, RMSE, WAPE and signed bias
- External regressors: Lower Saxony public holidays, promotions, Göttingen events, weather, district population/catchment
- Forecast ensembles, hierarchical reconciliation and robust anomaly detection
- Inventory logic: safety stock, reorder point, days cover, suggested order quantity
- Explicit inbound-supply projection and projected stock balance
- Shortage / healthy / overstock decision support
- Authenticated Streamlit control tower with real-time sales, forecasts, inventory risk, local signals and scenario lab
- Three importable n8n workflows for POS ingestion, forecast refresh and alerts
- Docker Compose stack: PostgreSQL + Redis + FastAPI + Streamlit + n8n
- 20 research notebooks from EDA to end-to-end operations
- Optional C++17 rolling-feature helper for high-volume extensions
- GitHub Actions CI and pytest tests

## System flow

```text
POS / E-commerce / ERP
        |
        v
 n8n realtime webhook
        |
        v
FastAPI /api/v1/sales ------> PostgreSQL/SQLite
        |                           |
        |                           v
        |                    daily SKU demand
        |                           |
        +---- weather / holidays / events / promotions / population
                                    |
                                    v
                         Prophet + baseline + ensemble
                                    |
                                    v
                         demand forecast + uncertainty
                                    |
          inventory + inbound POs --+--> projected supply balance
                                    |
                                    v
                     shortage / reorder / overstock
                          |                     |
                          v                     v
                Streamlit dashboard        n8n alerts
```

## Göttingen-specific signals

The default market configuration is centered on Göttingen (`51.5413, 9.9158`, timezone `Europe/Berlin`) and Lower Saxony (`DE-NI`). The project includes configurable district population reference data and a local-event table. Event uplift values are **priors for experimentation** and should be calibrated against observed POS residuals before production use.

Examples represented in the local calendar include the Göttinger Kultursommer and the Gänseliesel-Fest. The 2026 Göttinger Weihnachtsmarkt runs **23 November–29 December 2026** (closed 24–26 December); event files should be reviewed periodically because schedules change.

## Repository layout

```text
app/                    Streamlit login + dashboard pages
api/                    FastAPI realtime endpoints
config/                 Göttingen market/model settings
cpp/                    optional C++ rolling-feature extension
data/reference/         population + local event reference tables
docs/                   architecture, forecasting, automation, dashboard docs
n8n/workflows/           importable workflow JSON
notebooks/              20 research/analysis notebooks
scripts/                 demo-data and password utilities
src/demand_supply/      ingestion, features, forecasting, inventory/supply logic
tests/                   unit tests
```

## Quick start — Python

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python scripts/generate_demo_data.py
pytest -q
```

Start the API:

```bash
uvicorn api.main:app --reload --port 8000
```

Create a dashboard password hash:

```bash
python scripts/hash_password.py "change-this-password"
```

Copy the output to `DASHBOARD_PASSWORD_HASH`, set `DASHBOARD_USER`, then run:

```bash
streamlit run app/Home.py --server.port 8501
```

Open the Streamlit URL and log in. No plaintext password is committed to the repository.

## Quick start — full stack

```bash
cp .env.example .env
# set POSTGRES_PASSWORD, DASHBOARD_USER and DASHBOARD_PASSWORD_HASH
docker compose up --build
```

Services:

- Dashboard: `http://localhost:8501`
- FastAPI/OpenAPI: `http://localhost:8000/docs`
- n8n: `http://localhost:5678`

Import the JSON files under `n8n/workflows/` into n8n, inspect credentials/URLs, then activate them.

## Realtime sale example

```bash
curl -X POST http://localhost:8000/api/v1/sales \
  -H "Content-Type: application/json" \
  -d '{
    "event_id":"sale-10001",
    "timestamp":"2026-10-06T17:00:00+02:00",
    "store_id":"GOE-001",
    "product_id":"MILK-1L",
    "category":"dairy",
    "quantity":2,
    "unit_price":1.29,
    "district":"Weende",
    "promotion":false,
    "channel":"store"
  }'
```

## Demand vs. supply

Demand is the model forecast (`yhat`). Supply is represented by current on-hand inventory, open/inbound purchase quantities and lead-time arrival dates. `project_supply_balance(...)` creates the future stock trajectory:

```text
projected_stock[t] = projected_stock[t-1] + inbound_supply[t] - forecast_demand[t]
```

This lets the dashboard distinguish **high demand** from a true **stockout risk**. Procurement rules then use lead-time demand + safety stock to recommend orders.

## Research notebooks

The `notebooks/` directory contains 20 ordered notebooks:

1. data contracts
2. POS EDA
3. data quality/leakage
4. calendar + Lower Saxony holidays
5. weather effects
6. Göttingen events/festivals
7. district population/catchment
8. Prophet baseline
9. Prophet regressors
10. rolling backtests
11. inventory policy
12. safety stock/service level
13. shortage/overstock
14. scenario lab
15. hierarchical forecasting
16. ensemble forecasts
17. anomaly detection
18. realtime simulation
19. model monitoring
20. end-to-end demo

## Production notes

The repository ships reference/demo data, not private supermarket POS data. Before production use, connect actual POS/ERP/inventory feeds; persist historical weather; calibrate event effects; add supplier case packs, MOQs, delivery calendars, shelf/storage capacity and expiry/spoilage constraints; move authentication to OIDC/OAuth for multi-user access; terminate TLS at a reverse proxy; and monitor model + business KPIs.

Population is a contextual feature, not a deterministic demand target. Weather beyond the provider forecast horizon requires climatology or a longer-range provider. A forecasting model should not be promoted unless it beats the seasonal-naive baseline consistently in rolling validation.

## Branches used for the build

- `feature/data-pipeline`
- `feature/forecasting-engine`
- `feature/dashboard-auth`
- `feature/n8n-automation`
- `research/notebooks`

All five are merged into `main` through pull requests.

## License

See [LICENSE](LICENSE).
