import streamlit as st
from utils.db import load_accounts, load_transactions, load_cash_flow_monthly
from components.kpis import render_financial_kpis
from components.charts import (
    plot_cash_flow_monthly, plot_category_distribution, plot_50_30_20_breakdown
)

accounts_df = load_accounts()
transactions_df = load_transactions(limit=1000)
cash_flow_df = load_cash_flow_monthly()

total_income = transactions_df[transactions_df['type'] == 'Ingreso']['amount'].sum() if not transactions_df.empty else 0
total_expense = transactions_df[transactions_df['type'] == 'Egreso']['amount'].sum() if not transactions_df.empty else 0
net_flow = total_income - total_expense
total_liquidity = accounts_df['balance'].sum() if not accounts_df.empty else 0
avg_monthly_expense = total_expense if total_expense > 0 else 1
runway_months = (total_liquidity / avg_monthly_expense) if avg_monthly_expense > 0 else 0

render_financial_kpis(total_income, total_expense, net_flow, total_liquidity, runway_months)
st.divider()

c1, c2 = st.columns([7, 5])
with c1:
    st.plotly_chart(plot_cash_flow_monthly(cash_flow_df), use_container_width=True)
with c2:
    st.plotly_chart(plot_category_distribution(transactions_df), use_container_width=True)

st.divider()
st.plotly_chart(plot_50_30_20_breakdown(transactions_df), use_container_width=True)
