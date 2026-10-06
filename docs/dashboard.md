# Authenticated dashboard

Run the API with `uvicorn api.main:app --reload --port 8000` and Streamlit with `streamlit run app/Home.py --server.port 8501`.

Set `DASHBOARD_USER` and a bcrypt `DASHBOARD_PASSWORD_HASH` in the environment. Never commit plaintext passwords or Streamlit secrets. Every Streamlit page calls the login guard, so direct page navigation is blocked until authentication succeeds.

For internet deployment, terminate TLS at the platform/reverse proxy, put the API behind a private network where possible, use PostgreSQL instead of SQLite, rotate credentials, add rate limiting and switch to an identity provider (OIDC/OAuth) for multi-user production access.
