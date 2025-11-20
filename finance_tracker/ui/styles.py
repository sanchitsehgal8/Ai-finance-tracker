import streamlit as st


def load_custom_css():
    css = """
    <style>
    .stApp { background-color: #f7f9fb; }
    .metric { font-weight: 600; }
    </style>
    """
    try:
        st.markdown(css, unsafe_allow_html=True)
    except Exception:
        pass
