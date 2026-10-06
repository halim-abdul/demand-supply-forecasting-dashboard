from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st
from auth import require_login, logout_button

require_login(); logout_button()
st.title("🌦️ Göttingen local demand signals")

events_path = Path("data/reference/goettingen_events_2026.csv")
pop_path = Path("data/reference/goettingen_population_by_district.csv")
if events_path.exists():
    events = pd.read_csv(events_path)
    st.subheader("Festivals & occasions")
    st.dataframe(events, use_container_width=True)
if pop_path.exists():
    pop = pd.read_csv(pop_path)
    st.subheader("District population reference")
    st.bar_chart(pop.set_index("district")["population"])
    st.caption("Population is a contextual/catchment feature, not a deterministic demand target.")
