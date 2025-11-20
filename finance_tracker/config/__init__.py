"""Config package for application settings and supabase config."""

from .supabase_config import SupabaseConfig
from .settings import SETTINGS

__all__ = ["SupabaseConfig", "SETTINGS"]
