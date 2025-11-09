from supabase import create_client
from config import Config
from datetime import datetime

# Initialize Supabase client
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def log_project_run(project_title, ceo_decision, ceo_reason, operations_status):
    """Insert a new company run record into Supabase project_history."""
    try:
        data = {
            "project_title": project_title,
            "ceo_decision": ceo_decision,
            "ceo_reason": ceo_reason,
            "operations_status": operations_status,
            "timestamp": datetime.utcnow().isoformat()
        }
        response = supabase.table("project_history").insert(data).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def fetch_project_history():
    """Fetch all company project runs from Supabase."""
    try:
        response = (
            supabase.table("project_history")
            .select("*")
            .order("timestamp", desc=True)
            .execute()
        )
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
