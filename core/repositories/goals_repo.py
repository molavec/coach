import pandas as pd
from core.repositories.base_repo import get_connection

def load_savings_goals():
    """Load savings goals and targets."""
    conn = get_connection()
    query = """
        SELECT 
            s.id, 
            s.name, 
            s.target_amount, 
            s.current_amount, 
            s.currency, 
            s.target_date, 
            s.status,
            a.name AS account_name
        FROM savings_goals s
        LEFT JOIN accounts a ON s.account_id = a.id
        ORDER BY s.id ASC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_savings_goal(name, target_amount, current_amount=0.0, currency='CLP', target_date=None, account_id=None, status='En Progreso'):
    """Insert a new savings goal."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO savings_goals (name, target_amount, current_amount, currency, target_date, account_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, float(target_amount), float(current_amount), currency, target_date, account_id, status))
        conn.commit()
        return True, "Meta de ahorro añadida exitosamente."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()
