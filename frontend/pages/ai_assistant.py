import os
import sys

import requests
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_config import API_BASE_URL
from ui import hero, inject_styles

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
inject_styles()

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

hero("AI Assistant", "Natural language inventory exploration and summary generation", "🤖")

query = st.text_area("Ask about assets, APIs, risk, or executive summaries")

if st.button("Generate Insight"):
    if not query:
        st.warning("Please enter a question or request.")
    else:
        asset_response = requests.get(f"{API_BASE_URL}/assets/", headers=headers, timeout=10)
        api_response = requests.get(f"{API_BASE_URL}/apis/", headers=headers, timeout=10)
        dashboard_response = requests.get(f"{API_BASE_URL}/dashboard/", headers=headers, timeout=10)

        if asset_response.status_code == 200 and api_response.status_code == 200 and dashboard_response.status_code == 200:
            asset_data = asset_response.json()
            api_data = api_response.json()
            dashboard_data = dashboard_response.json()

            st.markdown("### AI-Ready Summary")
            st.write(
                f"The environment contains {len(asset_data)} assets and {len(api_data)} APIs. "
                f"Criticality summary: {dashboard_data.get('risk_summary', {})}. "
                f"The inventory spans providers: {dashboard_data.get('assets_by_provider', {})}."
            )

            st.markdown("### Suggested Prompt for LLM Integration")
            st.code(
                f"Using this inventory data:\n"
                f"Assets: {asset_data}\n"
                f"APIs: {api_data}\n"
                f"Dashboard: {dashboard_data}\n"
                f"User query: {query}\n"
                f"Return a concise answer, risk summary, and executive-ready insights."
            )
        else:
            st.error("Unable to retrieve inventory data.")
