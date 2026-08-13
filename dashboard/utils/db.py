import streamlit as st
import sys
import os

# Ensure the root directory is in sys.path so we can import core.db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import core.db as core_db

def get_connection():
    """Establish connection to SQLite coach.db."""
    return core_db.get_connection()

@st.cache_data(ttl=30)
def load_accounts():
    """Load active financial accounts and their current balances."""
    return core_db.load_accounts()

def add_account(name, type_str, currency='CLP', balance=0.0, details=None):
    """Add a new financial account."""
    success, msg = core_db.add_account(name, type_str, currency, balance, details)
    if success:
        load_accounts.clear()
    return success, msg

@st.cache_data(ttl=30)
def load_categories():
    """Load all financial categories."""
    return core_db.load_categories()

def add_category(name, type_str, parent_id=None, is_essential=0):
    result = core_db.add_category(name, type_str, parent_id, is_essential)
    if result[0]:
        load_categories.clear()
    return result

@st.cache_data(ttl=30)
def load_transactions(limit=500):
    """Load transactions joined with account and category names."""
    return core_db.load_transactions(limit)

@st.cache_data(ttl=30)
def load_pending_payments():
    """Load pending payments and receivables."""
    return core_db.load_pending_payments()

def add_pending_payment(title, type_str, amount, currency, due_date, account_id, category_id, status='Pendiente', counterparty=None, notes=None):
    result = core_db.add_pending_payment(title, type_str, amount, currency, due_date, account_id, category_id, status, counterparty, notes)
    if result[0]:
        load_pending_payments.clear()
    return result

@st.cache_data(ttl=30)
def load_savings_goals():
    """Load savings goals and targets."""
    return core_db.load_savings_goals()

def add_savings_goal(name, target_amount, current_amount=0.0, currency='CLP', target_date=None, account_id=None, status='En Progreso'):
    result = core_db.add_savings_goal(name, target_amount, current_amount, currency, target_date, account_id, status)
    if result[0]:
        load_savings_goals.clear()
    return result

@st.cache_data(ttl=30)
def load_budgets_vs_actual(period=None):
    """Compare monthly allocated budget vs actual expenses per category."""
    return core_db.load_budgets_vs_actual(period)

def add_budget(period, category_id, allocated_amount, currency='CLP'):
    result = core_db.add_budget(period, category_id, allocated_amount, currency)
    if result[0]:
        load_budgets_vs_actual.clear()
    return result

@st.cache_data(ttl=30)
def load_cash_flow_monthly():
    """Calculate monthly cash flow totals (Ingresos vs Egresos)."""
    return core_db.load_cash_flow_monthly()

@st.cache_data(ttl=30)
def load_projects_and_tasks():
    """Load tasks and projects productivity data."""
    return core_db.load_projects_and_tasks()

def add_transaction(date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status='Completado', is_recurring=0, installments=1):
    """Insert a new transaction and update relevant account balances."""
    success, msg = core_db.add_transaction(
        date_str, type_str, amount, currency, account_id, 
        destination_account_id, category_id, description, status, is_recurring, installments
    )
    if success:
        st.cache_data.clear()
    return success, msg

def delete_transaction(transaction_id):
    """Delete a transaction and revert its effect on account balances."""
    success, msg = core_db.delete_transaction(transaction_id)
    if success:
        st.cache_data.clear()
    return success, msg

def update_transaction(transaction_id, date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status='Completado', is_recurring=0, installments=1):
    """Update an existing transaction and adjust account balances accordingly."""
    success, msg = core_db.update_transaction(
        transaction_id, date_str, type_str, amount, currency, account_id, 
        destination_account_id, category_id, description, status, is_recurring, installments
    )
    if success:
        st.cache_data.clear()
    return success, msg
