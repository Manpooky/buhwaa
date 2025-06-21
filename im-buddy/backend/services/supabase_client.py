import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Create Supabase client
if SUPABASE_URL and SUPABASE_ANON_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        supabase = None
else:
    print("Supabase credentials not found in environment variables")
    supabase = None

def get_client():
    """
    Get the Supabase client instance
    
    Returns:
        Client: Supabase client instance
    """
    if not supabase:
        raise ValueError("Supabase client not initialized")
    return supabase

def fetch_data(table_name, query=None):
    """
    Fetch data from a Supabase table
    
    Args:
        table_name (str): Table to query
        query (dict): Optional query parameters
        
    Returns:
        dict: Query results
    """
    client = get_client()
    base_query = client.table(table_name).select("*")
    
    if query:
        # Apply filters if provided
        if "filter" in query:
            for column, value in query["filter"].items():
                base_query = base_query.eq(column, value)
        
        # Apply ordering if provided
        if "order" in query:
            base_query = base_query.order(query["order"])
        
        # Apply pagination if provided
        if "limit" in query:
            base_query = base_query.limit(query["limit"])
            
            if "offset" in query:
                base_query = base_query.offset(query["offset"])
    
    return base_query.execute() 