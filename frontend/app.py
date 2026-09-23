import os
import sys

import requests
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_config import API_BASE_URL, api_request, error_detail
from ui import hero, inject_styles


st.set_page_config(page_title="Secure Cloud Asset Inventory", page_icon="☁️", layout="wide")
inject_styles()


if "token" not in st.session_state:
    st.session_state.token = None


def login_user(username: str, password: str):
    response = api_request(
        "POST",
        "/auth/login",
        json_body={"username": username, "password": password},
    )
    if response is None:
        st.error("Cannot reach backend. It may still be starting; please try again.")
        return
    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["access_token"]
        st.session_state.user = data["user"]
        st.success("Logged in successfully")
        st.rerun()
    else:
        st.error(error_detail(response, "Login failed"))


if st.session_state.token is None:
    hero("Secure Cloud Asset & API Inventory Platform", "Enterprise asset and API lifecycle management made simple", "☁️")
    st.subheader("Sign in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            login_user(username, password)
    if st.button("Register Demo User"):
        payload = {
            "username": "demo_user",
            "email": "demo_user@example.com",
            "full_name": "Demo User",
            "password": "Demo@1234",
            "role_name": "User",
        }
        response = api_request("POST", "/auth/register", json_body=payload)
        if response is not None and response.status_code == 201:
            st.success("Demo user created. Try logging in.")
        else:
            st.error(error_detail(response, "Registration failed"))
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

hero("Secure Cloud Asset & API Inventory Platform", f"Welcome back, {st.session_state.user['username']}", "☁️")

with st.sidebar:
    st.write(f"User: {st.session_state.user['username']}")
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()

    st.page_link("app.py", label="Dashboard")
    st.page_link("pages/asset_inventory.py", label="Asset Inventory")
    st.page_link("pages/api_inventory.py", label="API Inventory")
    st.page_link("pages/ai_assistant.py", label="AI Assistant")


def api_get(path: str):
    response = api_request("GET", path, headers=headers)
    if response is None or response.status_code != 200:
        st.error(f"Request failed: {getattr(response, 'status_code', 'no response')} - {error_detail(response) if response else 'backend unreachable'}")
        return []
    return response.json()


dashboard = api_get("/dashboard/")
if dashboard:
    st.subheader("Dashboard Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assets", dashboard.get("total_assets", 0))
    col2.metric("Total APIs", dashboard.get("total_apis", 0))
    col3.metric("High Risk", dashboard.get("risk_summary", {}).get("high", 0))
    col4.metric("Medium Risk", dashboard.get("risk_summary", {}).get("medium", 0))

    st.write("Assets by Cloud Provider")
    st.bar_chart(dashboard.get("assets_by_provider", {}))

    st.write("Assets by Environment")
    st.bar_chart(dashboard.get("assets_by_environment", {}))

    st.write("APIs by Authentication Type")
    st.bar_chart(dashboard.get("apis_by_authentication_type", {}))
