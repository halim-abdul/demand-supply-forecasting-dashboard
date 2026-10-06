from __future__ import annotations

import streamlit as st

from auth import logout_button, require_login

st.set_page_config(page_title="Göttingen Supply AI", page_icon="📦", layout="wide")
require_login()
logout_button()

st.title("📦 Göttingen Supermarket — Demand & Supply Control Tower")
st.caption("Sales → contextual signals → demand forecast → supply balance → inventory decisions")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Market", "Göttingen")
c2.metric("Forecast horizon", "56 days")
c3.metric("Refresh target", "30 sec")
c4.metric("Region", "Lower Saxony")

st.subheader("Decision flow")
st.markdown(
    "**POS / e-commerce sale** → validation → daily demand → weather + holiday + event + "
    "population features → Prophet/ensemble → inbound supply balance → procurement alerts"
)

st.info(
    "Use the pages in the sidebar for live sales, forecasts, inventory risk, scenarios, "
    "and local demand signals."
)
