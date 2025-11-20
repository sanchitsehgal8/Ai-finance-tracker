from typing import Optional
from config.supabase_config import SupabaseConfig


class DatabaseManager:
    """Simple wrapper for a Supabase client instance.

    This class provides a central place to obtain the Supabase client. It is
    intentionally thin since `SupabaseConfig` handles creation.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = SupabaseConfig.get_client()
        return cls._instance

    def get_client(self):
        """Return the underlying Supabase client (or None if not configured)."""
        return self.client
