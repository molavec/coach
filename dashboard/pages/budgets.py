import streamlit as st
from utils.db import load_pending_payments, load_budgets_vs_actual
from components.charts import plot_budget_vs_actual
from components.tables import render_pending_payments_table

pending_df = load_pending_payments()
budgets_df = load_budgets_vs_actual()

st.plotly_chart(plot_budget_vs_actual(budgets_df), use_container_width=True)
st.divider()
render_pending_payments_table(pending_df)
