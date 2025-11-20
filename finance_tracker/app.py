import streamlit as st
from ui.components.sidebar import render_sidebar
from ui.components.dashboard import render_dashboard
from ui.components.transaction_form import render_transaction_form
from ui.components.budget_form import render_budget_form
from ui.components.reports_view import render_reports
from services.authentication_service import AuthenticationService
from ui.styles import load_custom_css

st.set_page_config(
    page_title="AI Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()


def render_login_page(auth_service: AuthenticationService):
    st.title("Welcome to AI Finance Tracker")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        if st.button('Sign in'):
            res = auth_service.sign_in(email, password)
            if res:
                st.session_state['authenticated'] = True
                st.session_state['user_id'] = 'mock-user'
                st.experimental_rerun()
            else:
                st.error('Sign in failed. Check credentials or Supabase configuration.')

    with col2:
        st.write('Or sign up')
        s_email = st.text_input('Signup Email', key='su_email')
        s_password = st.text_input('Signup Password', type='password', key='su_pass')
        if st.button('Sign up'):
            res = auth_service.sign_up(s_email, s_password)
            if res:
                st.success('Signup successful. Please sign in.')
            else:
                st.error('Signup failed. Check Supabase configuration.')


def main():
    auth_service = AuthenticationService()
    if not st.session_state.get('authenticated', False):
        render_login_page(auth_service)
        return

    page = render_sidebar()

    if page == "Dashboard":
        render_dashboard()
    elif page == "Add Transaction":
        render_transaction_form()
    elif page == "Budget Management":
        render_budget_form()
    elif page == "Reports":
        render_reports()


if __name__ == '__main__':
    main()
