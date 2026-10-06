from __future__ import annotations
import pandas as pd
import streamlit as st
from auth import require_login, logout_button

require_login(); logout_button()
st.title("🚨 Inventory risk")
file = st.file_uploader("Upload inventory plan CSV", type=["csv"])
if file:
    df = pd.read_csv(file)
    status = st.multiselect("Status", sorted(df.status.unique()), default=list(df.status.unique())) if "status" in df else []
    view = df[df.status.isin(status)] if status else df
    if "shortage_risk" in view:
        view = view.sort_values("shortage_risk", ascending=False)
    st.dataframe(view, use_container_width=True)
else:
    st.info("Shows reorder points, safety stock, recommended order quantities, days cover and shortage risk.")
