import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()

SUPABASE_URL = os.getenv("https://utxhqgsshmggvesmflca.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0eGhxZ3NzaG1nZ3Zlc21mbGNhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2NjgwMjYsImV4cCI6MjA3OTI0NDAyNn0.STXxVLcK_hR-5XrRvLpGVpTYE0NaB_T-6XiJWJofqVs")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials are missing in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client():
    return supabase

print("URL:", os.getenv("SUPABASE_URL"))