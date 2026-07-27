import streamlit as st
import pandas as pd
import datetime

from utils.db import (
    load_accounts, load_transactions, load_pending_payments,
    load_savings_goals, load_budgets_vs_actual, load_cash_flow_monthly,
    load_projects_and_tasks
)
from utils.excel_exporter import generate_excel_report
from components.kpis import render_financial_kpis, render_task_kpis
from components.charts import (
    plot_cash_flow_monthly, plot_category_distribution,
    plot_50_30_20_breakdown, plot_account_balances,
    plot_budget_vs_actual, plot_tasks_status
)
from components.tables import render_pending_payments_table, render_savings_goals_table

# Configure Streamlit page layout and theme
st.set_page_config(
    page_title="Coach Dashboard — Finanzas & Productividad",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("📊 Coach Dashboard — Finanzas & Productividad")
st.caption("Sistema de gestión estratégica de finanzas personales y ejecución de proyectos.")

# Sidebar Filters
st.sidebar.header("🔍 Filtros & Ajustes")
if st.sidebar.button("🔄 Recargar Datos"):
    st.cache_data.clear()
    st.rerun()

# Load Data
accounts_df = load_accounts()
transactions_df = load_transactions(limit=1000)
pending_df = load_pending_payments()
savings_df = load_savings_goals()
budgets_df = load_budgets_vs_actual()
cash_flow_df = load_cash_flow_monthly()
projects_df, tasks_df = load_projects_and_tasks()

# Global Financial Calculations
total_income = transactions_df[transactions_df['type'] == 'Ingreso']['amount'].sum() if not transactions_df.empty else 0
total_expense = transactions_df[transactions_df['type'] == 'Egreso']['amount'].sum() if not transactions_df.empty else 0
net_flow = total_income - total_expense
total_liquidity = accounts_df['balance'].sum() if not accounts_df.empty else 0

# Runway calculation (Monthly average expense)
avg_monthly_expense = total_expense if total_expense > 0 else 1
runway_months = (total_liquidity / avg_monthly_expense) if avg_monthly_expense > 0 else 0

# Main Tabs Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Flujo de Caja & Resumen", 
    "🛡️ Patrimonio & Cuentas", 
    "🚨 Presupuestos & Pendientes", 
    "🎯 Productividad (Coach)",
    "📥 Exportar a Excel"
])

# -----------------------------------------------------------------------------
# TAB 1: Flujo de Caja & Resumen Financiero
# -----------------------------------------------------------------------------
with tab1:
    st.header("💰 Resumen Financiero")
    render_financial_kpis(total_income, total_expense, net_flow, total_liquidity, runway_months)
    st.divider()

    c1, c2 = st.columns([7, 5])
    with c1:
        st.plotly_chart(plot_cash_flow_monthly(cash_flow_df), use_container_width=True)
    with c2:
        st.plotly_chart(plot_category_distribution(transactions_df), use_container_width=True)

    st.divider()
    st.plotly_chart(plot_50_30_20_breakdown(transactions_df), use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: Patrimonio Neto & Saldos de Cuentas
# -----------------------------------------------------------------------------
with tab2:
    st.header("🏦 Cuentas Financieras & Solvencia")
    c1, c2 = st.columns([6, 6])
    
    with c1:
        st.plotly_chart(plot_account_balances(accounts_df), use_container_width=True)
    with c2:
        st.subheader("📋 Detalle de Cuentas")
        if not accounts_df.empty:
            st.dataframe(
                accounts_df[['name', 'type', 'currency', 'balance', 'updated_at']],
                column_config={
                    'name': 'Cuenta',
                    'type': 'Tipo',
                    'currency': 'Moneda',
                    'balance': st.column_config.NumberColumn('Saldo Conciliado', format="$%.0f"),
                    'updated_at': 'Última Actualización'
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Sin cuentas registradas en `accounts`.")

    st.divider()
    render_savings_goals_table(savings_df)

# -----------------------------------------------------------------------------
# TAB 3: Presupuestos & Radar de Pendientes
# -----------------------------------------------------------------------------
with tab3:
    st.header("🚨 Presupuestos & Radar de Vencimientos")
    
    st.plotly_chart(plot_budget_vs_actual(budgets_df), use_container_width=True)
    st.divider()
    render_pending_payments_table(pending_df)

# -----------------------------------------------------------------------------
# TAB 4: Productividad de Proyectos & Tareas
# -----------------------------------------------------------------------------
with tab4:
    st.header("🎯 Métricas de Productividad & Proyectos")
    
    total_tasks = len(tasks_df) if not tasks_df.empty else 0
    completed_tasks = len(tasks_df[tasks_df['status'] == 'Completado']) if not tasks_df.empty else 0
    in_progress_tasks = len(tasks_df[tasks_df['status'] == 'En Progreso']) if not tasks_df.empty else 0
    pending_tasks = total_tasks - completed_tasks - in_progress_tasks
    
    render_task_kpis(total_tasks, completed_tasks, in_progress_tasks, pending_tasks)
    st.divider()

    c1, c2 = st.columns([6, 6])
    with c1:
        st.plotly_chart(plot_tasks_status(tasks_df), use_container_width=True)
    with c2:
        st.subheader("🚀 Proyectos Activos")
        if not projects_df.empty:
            st.dataframe(
                projects_df[['id', 'name', 'priority', 'status']],
                column_config={
                    'id': 'ID',
                    'name': 'Proyecto',
                    'priority': 'Prioridad',
                    'status': 'Estado'
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No hay proyectos activos registrados.")

    st.divider()
    st.subheader("📋 Lista de Tareas Recientes")
    if not tasks_df.empty:
        st.dataframe(
            tasks_df[['title', 'project_name', 'priority', 'status', 'estimated_time', 'actual_time']],
            column_config={
                'title': 'Título Tarea',
                'project_name': 'Proyecto',
                'priority': 'Prioridad',
                'status': 'Estado',
                'estimated_time': 'Tiempo Est.',
                'actual_time': 'Tiempo Real'
            },
            use_container_width=True,
            hide_index=True
        )

# -----------------------------------------------------------------------------
# TAB 5: Exportar a Excel
# -----------------------------------------------------------------------------
with tab5:
    st.header("📥 Exportación de Reporte Financiero a Excel")
    st.write("Genera y descarga un libro de Excel (`.xlsx`) completo con múltiples pestañas conteniendo el saldo de cuentas, historial de transacciones, cobros/pagos pendientes y ejecución presupuestaria.")
    
    if st.button("📊 Generar Reporte Excel"):
        with st.spinner("Generando archivo Excel con openpyxl..."):
            excel_bytes = generate_excel_report()
            filename = f"Reporte_Financiero_Coach_{datetime.date.today().strftime('%Y-%m-%d')}.xlsx"
            st.download_button(
                label="💾 Descargar Archivo Excel (.xlsx)",
                data=excel_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("✅ ¡Reporte generado con éxito! Haz clic en el botón superior para descargar.")
