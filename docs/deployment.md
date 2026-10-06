# Website deployment runbook

The repository contains a login-protected Streamlit web UI and FastAPI backend. A public URL is not created automatically by GitHub; deploy the containers to your chosen host (VM, Kubernetes, Render, Railway, Fly.io, Azure, AWS, GCP, etc.) and point DNS/TLS at the dashboard/reverse proxy.

## Minimum production requirements

1. PostgreSQL instead of local SQLite.
2. TLS/HTTPS at the load balancer or reverse proxy.
3. Secret manager/environment variables for DB/password hashes and webhook secrets.
4. OIDC/OAuth/SSO for multi-user production use; the included bcrypt login is appropriate for a controlled demo/single-operator deployment.
5. Network-restrict PostgreSQL, Redis and n8n; only expose required HTTP services.
6. Add backups, monitoring, rate limiting and log retention.
7. Configure n8n webhook authentication/signature verification before accepting retailer POS traffic.

For a local demo, `docker compose up --build` is sufficient. For a hosted environment, build the same Docker image and run API and Streamlit as separate services sharing the same PostgreSQL database.
