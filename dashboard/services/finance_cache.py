import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import core.repositories.finance_repo as finance_repo

@st.cache_data(ttl=30)
def load_accounts():
    return finance_repo.load_accounts()

def add_account(name, type_str, currency='CLP', balance=0.0, details=None):
    success, msg = finance_repo.add_account(name, type_str, currency, balance, details)
    if success:
        load_accounts.clear()
    return success, msg

@st.cache_data(ttl=30)
def load_categories():
    return finance_repo.load_categories()

def add_category(name, type_str, parent_id=None, is_essential=0):
    result = finance_repo.add_category(name, type_str, parent_id, is_essential)
    if result[0]:
        load_categories.clear()
    return result

@st.cache_data(ttl=30)
def load_transactions(limit=500):
    return finance_repo.load_transactions(limit)

def add_transaction(date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status='Completado', is_recurring=0, installments=1):
    success, msg = finance_repo.add_transaction(
        date_str, type_str, amount, currency, account_id, 
        destination_account_id, category_id, description, status, is_recurring, installments
    )
    if success:
        load_transactions.clear()
        load_accounts.clear()
        load_cash_flow_monthly.clear()
        load_budgets_vs_actual.clear()
    return success, msg

def delete_transaction(transaction_id):
    success, msg = finance_repo.delete_transaction(transaction_id)
    if success:
        load_transactions.clear()
        load_accounts.clear()
        load_cash_flow_monthly.clear()
        load_budgets_vs_actual.clear()
    return success, msg

def update_transaction(transaction_id, date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status='Completado', is_recurring=0, installments=1):
    success, msg = finance_repo.update_transaction(
        transaction_id, date_str, type_str, amount, currency, account_id, 
        destination_account_id, category_id, description, status, is_recurring, installments
    )
    if success:
        load_transactions.clear()
        load_accounts.clear()
        load_cash_flow_monthly.clear()
        load_budgets_vs_actual.clear()
    return success, msg

@st.cache_data(ttl=30)
def load_pending_payments():
    return finance_repo.load_pending_payments()

def add_pending_payment(title, type_str, amount, currency, due_date, account_id, category_id, status='Pendiente', counterparty=None, notes=None):
    result = finance_repo.add_pending_payment(title, type_str, amount, currency, due_date, account_id, category_id, status, counterparty, notes)
    if result[0]:
        load_pending_payments.clear()
    return result

@st.cache_data(ttl=30)
def load_budgets_vs_actual(period=None):
    return finance_repo.load_budgets_vs_actual(period)

def add_budget(period, category_id, allocated_amount, currency='CLP'):
    result = finance_repo.add_budget(period, category_id, allocated_amount, currency)
    if result[0]:
        load_budgets_vs_actual.clear()
    return result

@st.cache_data(ttl=30)
def load_cash_flow_monthly():
    return finance_repo.load_cash_flow_monthly()
