import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()
# Read correct environment variable names
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    # Provide an actionable error message; do not print the key.
    raise Exception(
        "Supabase credentials are missing or malformed.\n"
        "Please create a `.env` file (or set environment variables) with SUPABASE_URL and SUPABASE_KEY.\n"
        "You can copy `.env.example` and fill in your values, then restart the app."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase_client():
    return supabase

