import os
import sys

import requests
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_config import API_BASE_URL
from ui import hero, inject_styles

st.set_page_config(page_title="Asset Inventory", page_icon="🖥️")
inject_styles()

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

CATEGORIES = [
    "Virtual Machines",
    "Containers",
    "Databases",
    "Storage Accounts",
    "API Gateways",
    "Serverless Functions",
]
PROVIDERS = ["AWS", "Azure", "GCP", "OCI", "Other"]
ENVIRONMENTS = ["Development", "Test", "Production", "Staging"]
CRITICALITIES = ["Low", "Medium", "High", "Critical"]


def fetch_assets():
    response = requests.get(f"{API_BASE_URL}/assets/", headers=headers, timeout=10)
    if response.status_code == 200:
        return response.json()
    st.error(f"Request failed: {response.status_code} - {response.text}")
    return []


def asset_payload(asset_id, asset_name, asset_category, cloud_provider, account_id, region, owner, environment, criticality, description):
    return {
        "asset_id": asset_id,
        "asset_name": asset_name,
        "asset_category": asset_category,
        "cloud_provider": cloud_provider,
        "account_id": account_id,
        "region": region,
        "owner": owner,
        "environment": environment,
        "criticality": criticality,
        "description": description,
    }


hero("Asset Inventory", "Create, update, and delete cloud assets from a single place", "🖥️")

assets = fetch_assets()

tab_create, tab_manage = st.tabs(["Create Asset", "Update / Delete Asset"])

with tab_create:
    st.subheader("Create New Asset")
    with st.form("asset_form"):
        asset_id = st.text_input("Asset ID")
        asset_name = st.text_input("Asset Name")
        asset_category = st.selectbox("Asset Category", CATEGORIES)
        cloud_provider = st.selectbox("Cloud Provider", PROVIDERS)
        account_id = st.text_input("Account ID")
        region = st.text_input("Region")
        owner = st.text_input("Owner")
        environment = st.selectbox("Environment", ENVIRONMENTS)
        criticality = st.selectbox("Criticality", CRITICALITIES)
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create Asset")

    if submitted:
        payload = asset_payload(asset_id, asset_name, asset_category, cloud_provider, account_id, region, owner, environment, criticality, description)
        response = requests.post(f"{API_BASE_URL}/assets/", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            st.success("Asset created successfully")
            st.rerun()
        else:
            st.error(response.text)

with tab_manage:
    if not assets:
        st.info("No assets available.")
    else:
        options = {f"{asset['asset_id']} - {asset['asset_name']}": asset for asset in assets}
        selected_label = st.selectbox("Select an asset to manage", list(options.keys()))
        selected = options[selected_label]

        st.divider()
        st.subheader("Update Asset")
        with st.form("update_asset_form"):
            asset_id = st.text_input("Asset ID", value=selected.get("asset_id", ""))
            asset_name = st.text_input("Asset Name", value=selected.get("asset_name", ""))
            asset_category = st.selectbox("Asset Category", CATEGORIES, index=CATEGORIES.index(selected.get("asset_category")) if selected.get("asset_category") in CATEGORIES else 0)
            cloud_provider = st.selectbox("Cloud Provider", PROVIDERS, index=PROVIDERS.index(selected.get("cloud_provider")) if selected.get("cloud_provider") in PROVIDERS else 0)
            account_id = st.text_input("Account ID", value=selected.get("account_id", ""))
            region = st.text_input("Region", value=selected.get("region", ""))
            owner = st.text_input("Owner", value=selected.get("owner", ""))
            environment = st.selectbox("Environment", ENVIRONMENTS, index=ENVIRONMENTS.index(selected.get("environment")) if selected.get("environment") in ENVIRONMENTS else 0)
            criticality = st.selectbox("Criticality", CRITICALITIES, index=CRITICALITIES.index(selected.get("criticality")) if selected.get("criticality") in CRITICALITIES else 0)
            description = st.text_area("Description", value=selected.get("description") or "")
            updated = st.form_submit_button("Update Asset")

        if updated:
            payload = asset_payload(asset_id, asset_name, asset_category, cloud_provider, account_id, region, owner, environment, criticality, description)
            response = requests.put(f"{API_BASE_URL}/assets/{selected['id']}", json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                st.success("Asset updated successfully")
                st.rerun()
            else:
                st.error(response.text)

        st.divider()
        st.subheader("Delete Asset")
        confirm_delete = st.checkbox(f"I confirm deleting asset '{selected['asset_id']}'")
        if st.button("Delete Asset", type="primary", disabled=not confirm_delete):
            response = requests.delete(f"{API_BASE_URL}/assets/{selected['id']}", headers=headers, timeout=10)
            if response.status_code == 200:
                st.success("Asset deleted successfully")
                st.rerun()
            else:
                st.error(response.text)

st.divider()
st.subheader("All Assets")
if assets:
    st.dataframe(assets)