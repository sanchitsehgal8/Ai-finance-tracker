import streamlit as st
from services.report_service import ReportService
from services.transaction_service import TransactionService


def render_reports():
    st.title('Reports')
    user_id = st.session_state.get('user_id')
    if not user_id:
        st.error('No user signed in — please sign in to view reports.')
        return

    svc = ReportService()
    tx_svc = TransactionService()

    option = st.selectbox('Report Type', ['Monthly', 'Yearly'])
    if option == 'Monthly':
        month = st.number_input('Month (1-12)', min_value=1, max_value=12, value=1)
        year = st.number_input('Year', min_value=2000, max_value=2100, value=2025)
        if st.button('Generate'):
            # Fetch recent transactions for the user and normalize fields for reporting
            txns = tx_svc.get_recent_transactions(user_id, limit=1000) or []
            for t in txns:
                # normalize category name into `category` key expected by report generator
                if not t.get('category'):
                    cat = t.get('categories')
                    if isinstance(cat, dict):
                        t['category'] = cat.get('name')
                    else:
                        t['category'] = None
            st.info(f'Using {len(txns)} transactions for report generation')
            report = svc.generate_monthly(user_id, int(month), int(year), txns)
            st.json(report)
    else:
        year = st.number_input('Year', min_value=2000, max_value=2100, value=2025)
        if st.button('Generate'):
            txns = tx_svc.get_recent_transactions(user_id, limit=5000) or []
            for t in txns:
                if not t.get('category'):
                    cat = t.get('categories')
                    if isinstance(cat, dict):
                        t['category'] = cat.get('name')
                    else:
                        t['category'] = None
            st.info(f'Using {len(txns)} transactions for report generation')
            report = svc.generate_yearly(user_id, int(year), txns)
            st.json(report)
