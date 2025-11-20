import streamlit as st


def load_custom_css():
    """Inject custom CSS to apply a dark theme and improved UI styles.

    This uses stable Streamlit container classes where possible. Streamlit
    class names can change between versions — keep this file small and
    focused on generic selectors to remain robust.
    """
    css = """
    <style>
    /* App background and text */
    .stApp {
        background: #071021;
        color: #E6EEF8;
    }

    /* Page content container */
    .stApp .block-container {
        background: transparent;
        padding-top: 1rem;
        padding-left: 1.25rem;
        padding-right: 1.25rem;
        padding-bottom: 1.25rem;
    }

    /* Card-like panels */
    .card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.04);
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(2,6,23,0.6);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #071021 0%, #081828 100%);
        color: #E6EEF8;
    }
    section[data-testid="stSidebar"] .css-1d391kg {
        color: #E6EEF8;
    }

    /* Inputs */
    input, textarea, select {
        background: rgba(255,255,255,0.03) !important;
        color: #E6EEF8 !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 6px !important;
    }

    /* Buttons */
    button[kind="primary"], .stButton>button {
        background: linear-gradient(90deg, #0ea5a1 0%, #06b6d4 100%) !important;
        color: #061826 !important;
        font-weight: 600;
        border: none !important;
        box-shadow: 0 6px 18px rgba(3, 102, 110, 0.15);
    }

    /* Metrics */
    .stMetric {
        color: #E6EEF8;
    }
    .stMetricValue {
        color: #BFF0FF !important;
        font-weight: 700 !important;
    }

    /* Dataframe/table */
    .stDataFrame table {
        background: transparent !important;
        color: #E6EEF8 !important;
    }
    .stDataFrame thead th {
        color: #CFEFF8 !important;
    }

    /* Ensure text and headers contrast well */
    h1, h2, h3, h4, h5, h6 {
        color: #F1FAFF !important;
    }

    /* Make Plotly charts fit dark background better when rendered as SVG/HTML */
    .stPlotlyChart > div {
        background: transparent !important;
    }

    /* Small helpers */
    .muted { color: #94a3b8; }
    .spaced { margin-top: 8px; margin-bottom: 8px; }
    </style>
    """
    try:
        st.markdown(css, unsafe_allow_html=True)
    except Exception:
        # If Streamlit isn't available or markup injection fails, skip silently
        pass
