import pandas as pd
from core.repositories.base_repo import get_connection

def load_projects_and_tasks():
    """Load tasks and projects productivity data."""
    conn = get_connection()
    projects_df = pd.read_sql_query("SELECT * FROM projects", conn)
    tasks_df = pd.read_sql_query("""
        SELECT 
            t.id, t.title, t.project_id, p.name AS project_name, 
            t.estimated_time, t.actual_time, t.priority, t.status, 
            t.created_at, t.started_at, t.completed_at
        FROM tasks t
        LEFT JOIN projects p ON t.project_id = p.id
        ORDER BY t.created_at DESC;
    """, conn)
    conn.close()
    return projects_df, tasks_df
