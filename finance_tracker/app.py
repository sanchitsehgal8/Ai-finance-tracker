import streamlit as st
from ui.components.sidebar import render_sidebar
from ui.components.dashboard import render_dashboard
from ui.components.transaction_form import render_transaction_form
from ui.components.budget_form import render_budget_form
from ui.components.reports_view import render_reports
from ui.components.group_expenses import render_group_panel
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
    """Render a single login/signup UI with a dev bypass for local testing.

    The dev bypass button sets `st.session_state['authenticated'] = True` and
    a `user_id` so you can explore the UI without Supabase configured.
    """
    st.title("🔐 AI Finance Tracker — Sign in")

    # Small debug toggle so you can inspect session state while developing
    if st.checkbox("Show session_state (debug)"):
        st.write(dict(st.session_state))

    # Primary sign-in form
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_signin = st.form_submit_button("Sign in")

    if submit_signin:
        try:
            result = auth_service.sign_in(email=email, password=password)
            st.write("Auth result (debug):", result)
            # Try to extract user id from common supabase response shapes
            user_id = None
            if isinstance(result, dict):
                # supabase-py v2 may return {'data': {...}, 'error': None}
                if 'data' in result and isinstance(result.get('data'), dict):
                    data = result.get('data')
                    user = data.get('user') or data.get('session') or data
                    if isinstance(user, dict):
                        user_id = user.get('id') or user.get('user_id')
                user_id = user_id or result.get('user', {}).get('id') or result.get('id') or result.get('user_id')
            else:
                user_id = getattr(result, 'user_id', None) or getattr(result, 'id', None)

            if user_id:
                st.session_state['authenticated'] = True
                st.session_state['user_id'] = user_id
                # Safely attempt to rerun; some Streamlit builds may not expose experimental_rerun
                try:
                    st.experimental_rerun()
                except AttributeError:
                    st.info('Authentication successful — please refresh the page to continue.')
            else:
                st.error("Sign-in failed or did not return a user id. Check logs and Supabase config.")
        except Exception as exc:
            st.error(f"Sign-in failed: {exc}")
            import logging
            logging.exception("Sign-in error")

    # Secondary: signup form
    with st.expander("Sign up (create account)"):
        s_email = st.text_input('Signup Email', key='su_email')
        s_password = st.text_input('Signup Password', type='password', key='su_pass')
        if st.button('Sign up', key='signup_btn'):
            res = auth_service.sign_up(s_email, s_password)
            if res:
                st.success('Signup successful. Please sign in.')
            else:
                st.error('Signup failed. Check Supabase configuration or logs.')

    # Prominent dev bypass for local development (remove before production)
    st.markdown("---")
    st.warning("Development only: use the bypass to skip authentication and explore the UI.")
    if st.button("Dev bypass: Continue as `dev-user`", key='dev_bypass'):
        st.session_state['authenticated'] = True
        st.session_state['user_id'] = "dev-user"
        try:
            st.experimental_rerun()
        except AttributeError:
            st.info('Dev bypass set — please refresh the page to continue.')

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
    elif page == "Groups":
        user_id = st.session_state.get('user_id')
        render_group_panel(user_id=user_id)


if __name__ == '__main__':
    main()




