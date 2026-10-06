from __future__ import annotations

import pandas as pd
import streamlit as st

from auth import logout_button, require_login

require_login()
logout_button()
st.title("🧾 Real-time sales")

try:
    from demand_supply.ingestion import load_sales

    df = load_sales()
except Exception as exc:
    st.warning(f"Database not initialized or unavailable: {exc}")
    df = pd.DataFrame()

if df.empty:
    st.info("No POS events yet. POST a SaleEvent JSON payload to /api/v1/sales.")
else:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    today = df[df["timestamp"].dt.date == df["timestamp"].max().date()]
    c1, c2, c3 = st.columns(3)
    c1.metric("Units today", int(today.quantity.sum()))
    c2.metric("Revenue today", f"€{(today.quantity * today.unit_price).sum():,.2f}")
    c3.metric("Transactions", len(today))
    st.dataframe(df.sort_values("timestamp", ascending=False).head(500), use_container_width=True)
