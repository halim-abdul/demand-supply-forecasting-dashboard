# n8n automation

Three importable workflows are provided:

1. **Realtime Sales Ingestion** — POS/e-commerce webhook → validation → FastAPI sales endpoint.
2. **Forecast Refresh** — every six hours fetch Göttingen weather and request a 56-day forecast refresh.
3. **Inventory Risk Alerts** — scheduled health/risk polling and webhook alert fan-out.

The workflows are shipped inactive so credentials and target URLs can be reviewed before enabling them. In production, use n8n credential objects instead of embedding tokens, enable execution retention limits, and secure webhooks with authentication/signatures.

`docker compose up --build` starts PostgreSQL, Redis, API, dashboard and n8n. Import JSON workflows from `/workflows` in n8n and configure environment variables before activation.
