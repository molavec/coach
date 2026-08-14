import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import core.repositories.goals_repo as goals_repo

@st.cache_data(ttl=30)
def load_savings_goals():
    return goals_repo.load_savings_goals()

def add_savings_goal(name, target_amount, current_amount=0.0, currency='CLP', target_date=None, account_id=None, status='En Progreso'):
    result = goals_repo.add_savings_goal(name, target_amount, current_amount, currency, target_date, account_id, status)
    if result[0]:
        load_savings_goals.clear()
    return result
