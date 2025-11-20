from abc import ABC
from typing import Optional
from config.supabase_config import SupabaseConfig


class BaseRepository(ABC):
    """Abstract base repository providing access to a Supabase client.

    Repositories should extend this class to use `self.client` for DB operations.
    """

    def __init__(self):
        self.client = SupabaseConfig.get_client()
