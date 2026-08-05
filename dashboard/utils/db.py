import sqlite3
import pandas as pd
import streamlit as st
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../coach.db'))

def get_connection():
    """Establish connection to SQLite coach.db."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_data(ttl=30)
def load_accounts():
    """Load active financial accounts and their current balances."""
    conn = get_connection()
    query = """
        SELECT id, name, type, currency, balance, is_active, updated_at
        FROM accounts
        WHERE is_active = 1
        ORDER BY balance DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@st.cache_data(ttl=30)
def load_categories():
    """Load all financial categories."""
    conn = get_connection()
    query = """
        SELECT id, name, type, parent_id, is_essential
        FROM categories
        ORDER BY type, name;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@st.cache_data(ttl=30)
def load_transactions(limit=500):
    """Load transactions joined with account and category names."""
    conn = get_connection()
    query = f"""
        SELECT 
            t.id, 
            t.date, 
            t.type, 
            t.amount, 
            t.currency, 
            t.description,
            a.name AS account_name,
            da.name AS destination_account_name,
            c.name AS category_name,
            c.is_essential,
            t.status,
            t.is_recurring
        FROM transactions t
        LEFT JOIN accounts a ON t.account_id = a.id
        LEFT JOIN accounts da ON t.destination_account_id = da.id
        LEFT JOIN categories c ON t.category_id = c.id
        ORDER BY t.date DESC, t.id DESC
        LIMIT {limit};
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@st.cache_data(ttl=30)
def load_pending_payments():
    """Load pending payments and receivables."""
    conn = get_connection()
    query = """
        SELECT 
            p.id, 
            p.title, 
            p.type, 
            p.amount, 
            p.currency, 
            p.due_date, 
            p.status, 
            p.counterparty, 
            p.paid_date,
            p.notes,
            a.name AS account_name,
            c.name AS category_name
        FROM pending_payments p
        LEFT JOIN accounts a ON p.account_id = a.id
        LEFT JOIN categories c ON p.category_id = c.id
        ORDER BY p.due_date ASC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@st.cache_data(ttl=30)
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

@st.cache_data(ttl=30)
def load_budgets_vs_actual(period=None):
    """Compare monthly allocated budget vs actual expenses per category."""
    conn = get_connection()
    where_clause = f"WHERE b.period = '{period}'" if period else ""
    query = f"""
        SELECT 
            b.id,
            b.period,
            c.name AS category_name,
            c.is_essential,
            b.allocated_amount,
            b.currency,
            COALESCE(SUM(t.amount), 0) AS actual_amount
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
        LEFT JOIN transactions t ON t.category_id = c.id 
            AND strftime('%Y-%m', t.date) = b.period
            AND t.type = 'Egreso'
        {where_clause}
        GROUP BY b.id, b.period, c.name, c.is_essential, b.allocated_amount, b.currency;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@st.cache_data(ttl=30)
def load_cash_flow_monthly():
    """Calculate monthly cash flow totals (Ingresos vs Egresos)."""
    conn = get_connection()
    query = """
        SELECT 
            strftime('%Y-%m', date) AS month,
            SUM(CASE WHEN type = 'Ingreso' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type = 'Egreso' THEN amount ELSE 0 END) AS total_expenses,
            SUM(CASE WHEN type = 'Ingreso' THEN amount ELSE -amount END) AS net_flow
        FROM transactions
        WHERE type IN ('Ingreso', 'Egreso')
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month ASC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@st.cache_data(ttl=30)
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

def add_transaction(date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status='Completado', is_recurring=0):
    """Insert a new transaction and update relevant account balances."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO transactions (
                date, type, amount, currency, account_id, destination_account_id, category_id, description, status, is_recurring
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date_str, type_str, float(amount), currency, account_id, destination_account_id, category_id, description, status, int(is_recurring)))

        if type_str == 'Egreso':
            cursor.execute("""
                UPDATE accounts 
                SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (float(amount), account_id))
        elif type_str == 'Ingreso':
            cursor.execute("""
                UPDATE accounts 
                SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (float(amount), account_id))
        elif type_str == 'Transferencia':
            cursor.execute("""
                UPDATE accounts 
                SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (float(amount), account_id))
            if destination_account_id:
                cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (float(amount), destination_account_id))

        conn.commit()
        st.cache_data.clear()
        return True, "Transacción registrada exitosamente."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def delete_transaction(transaction_id):
    """Delete a transaction and revert its effect on account balances."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT type, amount, account_id, destination_account_id FROM transactions WHERE id = ?", (transaction_id,))
        tx = cursor.fetchone()
        if not tx:
            return False, "La transacción especificada no existe."

        t_type = tx['type']
        amount = float(tx['amount'])
        account_id = tx['account_id']
        dest_account_id = tx['destination_account_id']

        if t_type == 'Egreso':
            cursor.execute("""
                UPDATE accounts 
                SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (amount, account_id))
        elif t_type == 'Ingreso':
            cursor.execute("""
                UPDATE accounts 
                SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (amount, account_id))
        elif t_type == 'Transferencia':
            cursor.execute("""
                UPDATE accounts 
                SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (amount, account_id))
            if dest_account_id:
                cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (amount, dest_account_id))

        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        st.cache_data.clear()
        return True, "Transacción eliminada exitosamente y saldo de cuenta actualizado."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def update_transaction(transaction_id, date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status='Completado', is_recurring=0):
    """Update an existing transaction and adjust account balances accordingly."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT type, amount, account_id, destination_account_id FROM transactions WHERE id = ?", (transaction_id,))
        old_tx = cursor.fetchone()
        if not old_tx:
            return False, "La transacción a actualizar no existe."

        old_type = old_tx['type']
        old_amount = float(old_tx['amount'])
        old_account_id = old_tx['account_id']
        old_dest_account_id = old_tx['destination_account_id']

        # Revert old balance effect
        if old_type == 'Egreso':
            cursor.execute("UPDATE accounts SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (old_amount, old_account_id))
        elif old_type == 'Ingreso':
            cursor.execute("UPDATE accounts SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (old_amount, old_account_id))
        elif old_type == 'Transferencia':
            cursor.execute("UPDATE accounts SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (old_amount, old_account_id))
            if old_dest_account_id:
                cursor.execute("UPDATE accounts SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (old_amount, old_dest_account_id))

        # Apply new balance effect
        amount = float(amount)
        if type_str == 'Egreso':
            cursor.execute("UPDATE accounts SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (amount, account_id))
        elif type_str == 'Ingreso':
            cursor.execute("UPDATE accounts SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (amount, account_id))
        elif type_str == 'Transferencia':
            cursor.execute("UPDATE accounts SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (amount, account_id))
            if destination_account_id:
                cursor.execute("UPDATE accounts SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (amount, destination_account_id))

        # Update transactions record
        cursor.execute("""
            UPDATE transactions
            SET date = ?, type = ?, amount = ?, currency = ?, account_id = ?, destination_account_id = ?, category_id = ?, description = ?, status = ?, is_recurring = ?
            WHERE id = ?
        """, (date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status, int(is_recurring), transaction_id))

        conn.commit()
        st.cache_data.clear()
        return True, "Transacción actualizada exitosamente."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


