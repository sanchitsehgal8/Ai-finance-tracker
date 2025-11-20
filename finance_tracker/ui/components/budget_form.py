import streamlit as st
from services.budget_service import BudgetService


def render_budget_form():
    st.title("Budget Management")
    user_id = st.session_state.get('user_id')
    with st.form(key='budget_form'):
        category_id = st.text_input('Category ID (use category list)')
        monthly_limit = st.number_input('Monthly Limit', min_value=1.0)
        month = st.date_input('Month')
        submitted = st.form_submit_button('Save Budget')
        if submitted:
            if not category_id:
                st.error('Category ID required')
            else:
                svc = BudgetService()
                res = svc.set_budget(user_id, category_id, float(monthly_limit), month.isoformat())
                if res:
                    st.success('Budget saved')
                else:
                    st.error('Failed to save budget')
