from __future__ import annotations
import os
import bcrypt
import streamlit as st


def _credentials() -> tuple[str, str]:
    username = os.getenv("DASHBOARD_USER", "admin")
    hashed = os.getenv("DASHBOARD_PASSWORD_HASH", "")
    return username, hashed


def login_form() -> bool:
    if st.session_state.get("authenticated"):
        return True
    st.title("Göttingen Demand & Supply Control Tower")
    st.caption("Authorized supermarket operations access")
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in", use_container_width=True)
    if submitted:
        expected_user, hashed = _credentials()
        ok = username == expected_user and bool(hashed) and bcrypt.checkpw(password.encode(), hashed.encode())
        if ok:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        st.error("Invalid credentials or missing DASHBOARD_PASSWORD_HASH.")
    return False


def require_login() -> None:
    if not login_form():
        st.stop()


def logout_button() -> None:
    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.rerun()
