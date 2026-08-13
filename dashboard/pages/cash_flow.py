import streamlit as st
from utils.db import (
    load_accounts, load_transactions, load_cash_flow_monthly,
    load_categories, add_category
)
from components.kpis import render_financial_kpis
from components.charts import (
    plot_cash_flow_monthly, plot_category_distribution, plot_50_30_20_breakdown
)

accounts_df = load_accounts()
transactions_df = load_transactions(limit=1000)
cash_flow_df = load_cash_flow_monthly()
categories_df = load_categories()

cat_options = {row['name']: row['id'] for _, row in categories_df.iterrows()} if not categories_df.empty else {}

if accounts_df.empty and transactions_df.empty:
    st.info("👋 **¡Bienvenido a Coach!** Parece que tu base de datos está vacía. Utiliza el agente conversacional para registrar tus cuentas, ingresos y egresos iniciales.")


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

with st.expander("➕ Añadir Nueva Categoría", expanded=False):
    with st.form("add_category_form", clear_on_submit=True):
        c_name = st.text_input("Nombre de la Categoría", placeholder="Ej: Supermercado, Suscripciones")
        
        c1, c2 = st.columns(2)
        with c1:
            c_type = st.selectbox("Tipo de Flujo", ["Ingreso", "Egreso", "Inversión", "Transferencia"])
            c_essential = st.checkbox("¿Es un gasto/ingreso esencial? (Regla 50/30/20)")
        with c2:
            c_parent_name = st.selectbox("Categoría Padre (Opcional)", [""] + list(cat_options.keys()))
            
        c_submitted = st.form_submit_button("Guardar Categoría", use_container_width=True)
        if c_submitted:
            if not c_name.strip():
                st.error("El nombre de la categoría es requerido.")
            else:
                parent_id = cat_options[c_parent_name] if c_parent_name else None
                is_essential = 1 if c_essential else 0
                success, msg = add_category(c_name.strip(), c_type, parent_id, is_essential)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(f"Error: {msg}")
