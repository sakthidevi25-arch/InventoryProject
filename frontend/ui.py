import streamlit as st

STYLES = """
<style>
    :root {
        --primary: #7C4DFF;
        --primary-dark: #6A3FD6;
        --primary-light: #9E77FF;
        --accent: #B39DDB;
        --bg-main: #F8F5FF;
        --bg-card: #FFFFFF;
        --bg-soft: #EFE9FA;
        --text-main: #2B1B4D;
        --text-soft: #6A5B8C;
        --border: #D9CCF0;
    }

    /* App background */
    .stApp {
        background: var(--bg-main);
        color: var(--text-main);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #EAE0FA 0%, #F6F2FF 100%);
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] a,
    [data-testid="stSidebar"] .stPageLink {
        color: var(--text-main);
    }
    [data-testid="stSidebar"] .stPageLink:hover {
        color: var(--primary);
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: var(--primary-dark) !important;
        font-weight: 700 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--bg-soft);
        border-radius: 999px;
        padding: 0.4rem;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
        color: var(--text-soft);
        border: none;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(124, 77, 255, 0.35);
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid var(--border);
        background: #FFFFFF;
        color: var(--primary-dark);
        font-weight: 600;
        padding: 0.55rem 1.2rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: var(--primary);
        color: var(--primary);
        box-shadow: 0 4px 12px rgba(124, 77, 255, 0.2);
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        color: #FFFFFF;
        border: none;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 18px rgba(124, 77, 255, 0.4);
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"]:disabled {
        background: #D8CBF5;
        color: #FFFFFF;
        box-shadow: none;
        transform: none;
    }

    /* Form controls */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid var(--border);
        background: #FFFFFF;
        color: var(--text-main);
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(124, 77, 255, 0.15);
    }
    [data-testid="stSelectbox"] > div > div {
        border-radius: 12px;
        border: 1px solid var(--border);
        background: #FFFFFF;
    }

    /* Dataframe / data editor */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    /* Cards */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 4px 16px rgba(124, 77, 255, 0.08);
    }
    div[data-testid="stMetricLabel"] {
        color: var(--text-soft);
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        color: var(--primary-dark);
        font-weight: 700;
    }

    /* Info / success / warning messages */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid var(--border);
        background: #FFFFFF;
    }

    /* Expander */
    [data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        background: #FFFFFF;
    }

    /* Links */
    a {
        color: var(--primary);
    }

    /* Generic utility classes */
    .purple-hero {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        border-radius: 18px;
        padding: 1.6rem 2rem;
        color: #FFFFFF;
        box-shadow: 0 8px 28px rgba(124, 77, 255, 0.35);
        margin-bottom: 1.5rem;
    }
    .purple-hero h1 {
        color: #FFFFFF !important;
        margin: 0;
        font-size: 2rem;
    }
    .purple-hero p {
        color: rgba(255, 255, 255, 0.9) !important;
        margin: 0.25rem 0 0 0;
        font-size: 1.05rem;
    }
    .purple-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-left: 6px solid var(--primary);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 4px 16px rgba(124, 77, 255, 0.08);
    }
    .section-title {
        color: var(--primary-dark);
        font-weight: 700;
        font-size: 1.35rem;
        margin: 1rem 0 0.5rem 0;
    }
</style>
"""


def inject_styles():
    st.markdown(STYLES, unsafe_allow_html=True)


def hero(title: str, subtitle: str = "", emoji: str = ""):
    emoji_html = f"{emoji} " if emoji else ""
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="purple-hero"><h1>{emoji_html}{title}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )