import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class SupabaseConfig:
    """Singleton Supabase client provider.

    Use `SupabaseConfig.get_client()` to obtain a configured `supabase.Client`.
    """

    _instance = None
    _client: Optional[Client] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if not url or not key:
                # Do not raise here to allow offline development; functions should handle missing client.
                cls._client = None
            else:
                cls._client = create_client(url, key)
        return cls._instance

    @classmethod
    def get_client(cls) -> Optional[Client]:
        if cls._client is None:
            cls()
        return cls._client
