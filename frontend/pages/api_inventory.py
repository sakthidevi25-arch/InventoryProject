import os
import sys

import requests
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_config import API_BASE_URL, api_request, error_detail
from ui import hero, inject_styles

st.set_page_config(page_title="API Inventory", page_icon="🔌")
inject_styles()

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
ENVIRONMENTS = ["Development", "Test", "Production", "Staging"]
AUTH_TYPES = ["OAuth2", "API Key", "JWT", "mTLS", "None"]


def fetch_apis():
    response = api_request("GET", "/apis/", headers=headers)
    if response is None:
        st.error("Cannot reach backend. It may still be starting; please try again.")
        return []
    if response.status_code == 200:
        return response.json()
    st.error(f"Request failed: {response.status_code} - {error_detail(response)}")
    return []


def api_payload(api_name, api_path, http_method, application_name, owner, environment, authentication_type, version, description):
    return {
        "api_name": api_name,
        "api_path": api_path,
        "http_method": http_method,
        "application_name": application_name,
        "owner": owner,
        "environment": environment,
        "authentication_type": authentication_type,
        "version": version,
        "description": description,
    }


hero("API Inventory", "Create, update, and delete APIs from a single place", "🔌")

apis = fetch_apis()

tab_create, tab_manage = st.tabs(["Create API", "Update / Delete API"])

with tab_create:
    st.subheader("Create New API")
    with st.form("api_form"):
        api_name = st.text_input("API Name")
        api_path = st.text_input("API Path")
        http_method = st.selectbox("HTTP Method", METHODS)
        application_name = st.text_input("Application Name")
        owner = st.text_input("Owner")
        environment = st.selectbox("Environment", ENVIRONMENTS)
        authentication_type = st.selectbox("Authentication Type", AUTH_TYPES)
        version = st.text_input("Version")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create API")

    if submitted:
        payload = api_payload(api_name, api_path, http_method, application_name, owner, environment, authentication_type, version, description)
        response = api_request("POST", "/apis/", headers=headers, json_body=payload)
        if response is not None and response.status_code == 200:
            st.success("API created successfully")
            st.rerun()
        else:
            st.error(error_detail(response, "Failed to create API"))

with tab_manage:
    if not apis:
        st.info("No APIs available.")
    else:
        options = {f"{api['api_name']} ({api['http_method']} {api['api_path']})": api for api in apis}
        selected_label = st.selectbox("Select an API to manage", list(options.keys()))
        selected = options[selected_label]

        st.divider()
        st.subheader("Update API")
        with st.form("update_api_form"):
            api_name = st.text_input("API Name", value=selected.get("api_name", ""))
            api_path = st.text_input("API Path", value=selected.get("api_path", ""))
            http_method = st.selectbox("HTTP Method", METHODS, index=METHODS.index(selected.get("http_method")) if selected.get("http_method") in METHODS else 0)
            application_name = st.text_input("Application Name", value=selected.get("application_name", ""))
            owner = st.text_input("Owner", value=selected.get("owner", ""))
            environment = st.selectbox("Environment", ENVIRONMENTS, index=ENVIRONMENTS.index(selected.get("environment")) if selected.get("environment") in ENVIRONMENTS else 0)
            authentication_type = st.selectbox("Authentication Type", AUTH_TYPES, index=AUTH_TYPES.index(selected.get("authentication_type")) if selected.get("authentication_type") in AUTH_TYPES else 0)
            version = st.text_input("Version", value=selected.get("version", ""))
            description = st.text_area("Description", value=selected.get("description") or "")
            updated = st.form_submit_button("Update API")

        if updated:
            payload = api_payload(api_name, api_path, http_method, application_name, owner, environment, authentication_type, version, description)
            response = api_request("PUT", f"/apis/{selected['id']}", headers=headers, json_body=payload)
            if response is not None and response.status_code == 200:
                st.success("API updated successfully")
                st.rerun()
            else:
                st.error(error_detail(response, "Failed to update API"))

        st.divider()
        st.subheader("Delete API")
        confirm_delete = st.checkbox(f"I confirm deleting API '{selected['api_name']}'")
        if st.button("Delete API", type="primary", disabled=not confirm_delete):
            response = api_request("DELETE", f"/apis/{selected['id']}", headers=headers)
            if response is not None and response.status_code == 200:
                st.success("API deleted successfully")
                st.rerun()
            else:
                st.error(error_detail(response, "Failed to delete API"))

st.divider()
st.subheader("All APIs")
if apis:
    st.dataframe(apis)