import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
try:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully")
    else:
        supabase = None
        print("Supabase credentials not found, running without database")
except Exception as e:
    supabase = None
    print(f"Failed to initialize Supabase: {e}")

def get_supabase_client():
    """Get the Supabase client instance"""
    return supabase
