import streamlit as st


def render_sidebar() -> str:
    st.sidebar.title("AI Finance Tracker")
    st.sidebar.markdown("Manage your personal finances with AI assistance.")
    page = st.sidebar.selectbox("Navigate", ["Dashboard", "Add Transaction", "Budget Management", "Reports"]) 
    return page
