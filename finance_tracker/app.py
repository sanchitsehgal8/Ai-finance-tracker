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
    page_title="Finance Tracker",
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

            def _extract_user_id(res):
                # Try multiple known shapes: dicts with 'data'/'user'/'session',
                # or objects with attributes like .user, .id
                if not res:
                    return None

                # Helper to pull id from an object/dict
                def _id_from(obj):
                    try:
                        if obj is None:
                            return None
                        if isinstance(obj, dict):
                            return obj.get('id') or obj.get('user_id') or (obj.get('user') or {}).get('id')
                        # object with attributes
                        if hasattr(obj, 'id'):
                            return getattr(obj, 'id')
                        if hasattr(obj, 'user') and hasattr(obj.user, 'id'):
                            return getattr(obj.user, 'id')
                        if hasattr(obj, 'user') and isinstance(getattr(obj, 'user'), dict):
                            return getattr(obj, 'user').get('id')
                    except Exception:
                        return None
                    return None

                # If dict-like wrapper
                if isinstance(res, dict):
                    # common supabase-py v2 shape: {'data': {...}, 'error': None}
                    data = res.get('data') or res.get('session') or res
                    # Try a few nested candidates
                    for candidate in (data, res.get('user'), res.get('session')):
                        uid = _id_from(candidate)
                        if uid:
                            return uid
                    return _id_from(res)

                # If object-like
                # check .user, .session, direct .id
                for attr in ('user', 'session'):
                    candidate = getattr(res, attr, None)
                    uid = _id_from(candidate)
                    if uid:
                        return uid
                return _id_from(res)

            user_id = _extract_user_id(result)

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
                st.info("Tip: the Supabase auth response was received — check the debug output above for the exact shape. If you signed up recently, the auth user exists but you may still need to create a profile row in `user_profiles`.")
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
        import os
        import uuid

        # Prefer an explicit DEV_USER_ID (set in .env) so local writes can reference a real Supabase user.
        dev_id = os.getenv('DEV_USER_ID')
        if not dev_id:
            # Generate a UUID to satisfy validation. Note: generated id may not exist in `auth.users`,
            # which can cause foreign-key errors on writes; set DEV_USER_ID to a real user id to avoid that.
            dev_id = str(uuid.uuid4())
            st.warning('DEV_USER_ID not set — using a generated UUID for dev session. DB writes may fail due to missing auth user.')

        st.session_state['authenticated'] = True
        st.session_state['user_id'] = dev_id
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




