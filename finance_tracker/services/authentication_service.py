from typing import Optional
from config.supabase_config import SupabaseConfig


class AuthenticationService:
    """Authentication wrapper around Supabase Auth.

    Provides simple login/signup helpers that interact with the Supabase client.
    In production, add secure flow and error handling.
    """

    def __init__(self):
        self.client = SupabaseConfig.get_client()

    def sign_up(self, email: str, password: str) -> Optional[dict]:
        if not self.client:
            return None
        try:
            auth = self.client.auth.sign_up({'email': email, 'password': password})
            return auth.user if hasattr(auth, 'user') else None
        except Exception:
            return None

    def sign_in(self, email: str, password: str) -> Optional[dict]:
        if not self.client:
            return None
        try:
            session = self.client.auth.sign_in_with_password({'email': email, 'password': password})
            return session
        except Exception:
            return None
