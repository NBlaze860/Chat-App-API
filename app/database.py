from supabase import create_client, Client
from app.config import settings

# Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

def get_supabase_client() -> Client:
    return supabase 