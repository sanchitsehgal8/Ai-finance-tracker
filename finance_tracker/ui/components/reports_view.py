import streamlit as st
from services.report_service import ReportService


def render_reports():
    st.title('Reports')
    user_id = st.session_state.get('user_id')
    svc = ReportService()
    option = st.selectbox('Report Type', ['Monthly', 'Yearly'])
    if option == 'Monthly':
        month = st.number_input('Month (1-12)', min_value=1, max_value=12, value=1)
        year = st.number_input('Year', min_value=2000, max_value=2100, value=2025)
        if st.button('Generate'):
            txns = []
            report = svc.generate_monthly(user_id, int(month), int(year), txns)
            st.json(report)
    else:
        year = st.number_input('Year', min_value=2000, max_value=2100, value=2025)
        if st.button('Generate'):
            txns = []
            report = svc.generate_yearly(user_id, int(year), txns)
            st.json(report)
