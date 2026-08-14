import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import core.repositories.projects_repo as projects_repo

@st.cache_data(ttl=30)
def load_projects_and_tasks():
    return projects_repo.load_projects_and_tasks()
