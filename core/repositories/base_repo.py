import sqlite3
import pandas as pd
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../coach.db'))

def init_db():
    """Initialize the database schema if it hasn't been created yet."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    # Check if a fundamental table like 'accounts' exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
    if not cursor.fetchone():
        schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/schema.sql'))
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_script = f.read()
            cursor.executescript(schema_script)
            conn.commit()
    conn.close()

# Initialize DB when module loads
init_db()

def get_connection():
    """Establish connection to SQLite coach.db."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def execute_read_query(sql_string):
    """Execute a raw SELECT query and return a DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql_string, conn)
        return df
    finally:
        conn.close()

def execute_write_query(sql_string):
    """Execute a raw INSERT, UPDATE, or DELETE query."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.executescript(sql_string)
        conn.commit()
        return True, "Consulta ejecutada exitosamente."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()
