from __future__ import annotations

import streamlit as st

from auth import logout_button, require_login

require_login()
logout_button()
st.title("🧪 What-if scenario lab")
weather = st.slider("Weather demand multiplier", 0.70, 1.50, 1.00, 0.01)
festival = st.slider("Festival/event multiplier", 0.80, 1.80, 1.00, 0.01)
promotion = st.slider("Promotion multiplier", 0.80, 2.00, 1.00, 0.01)
pop_growth = st.slider("Catchment population change", -0.10, 0.20, 0.00, 0.01)
combined = weather * festival * promotion * (1 + pop_growth)
st.metric("Combined scenario factor", f"{combined:.2f}×")
st.caption(
    "Use this as an exploratory stress factor; production forecasts should use calibrated "
    "regressors and observed data."
)
