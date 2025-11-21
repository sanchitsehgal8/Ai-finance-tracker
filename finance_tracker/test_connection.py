from database.supabase_client import supabase  # adjust if path different

def test_connection():
    try:
        response = supabase.table("user_profiles").select("*").limit(1).execute()

        print("🟢 Connected Successfully!")
        print("📄 Data returned:", response.data)
    except Exception as e:
        print("🔴 Connection failed!")
        print("Error:", e)

if __name__ == "__main__":
    test_connection()