import streamlit as st
from datetime import datetime
from services.finance_cache import (
    load_pending_payments, load_budgets_vs_actual, load_categories, load_accounts,
    add_budget, add_pending_payment
)
from components.charts import plot_budget_vs_actual
from components.tables import render_pending_payments_table

pending_df = load_pending_payments()
budgets_df = load_budgets_vs_actual()
categories_df = load_categories()
accounts_df = load_accounts()

cat_options = {row['name']: row['id'] for _, row in categories_df.iterrows()} if not categories_df.empty else {}
acc_options = {row['name']: row['id'] for _, row in accounts_df.iterrows()} if not accounts_df.empty else {}

st.plotly_chart(plot_budget_vs_actual(budgets_df), use_container_width=True)

with st.expander("➕ Añadir Presupuesto", expanded=False):
    with st.form("add_budget_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            b_period = st.text_input("Período (YYYY-MM)", value=datetime.now().strftime("%Y-%m"))
        with c2:
            b_cat_name = st.selectbox("Categoría", options=list(cat_options.keys()))
        with c3:
            b_amount = st.number_input("Monto Asignado", value=0.0, format="%.2f")
            
        b_submitted = st.form_submit_button("Guardar Presupuesto", use_container_width=True)
        if b_submitted:
            if not b_cat_name:
                st.error("Debes seleccionar una categoría.")
            else:
                cat_id = cat_options[b_cat_name]
                success, msg = add_budget(b_period, cat_id, b_amount)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(f"Error: {msg}")

st.divider()

render_pending_payments_table(pending_df)

with st.expander("➕ Añadir Pago Pendiente", expanded=False):
    with st.form("add_pending_form", clear_on_submit=True):
        p_title = st.text_input("Título", placeholder="Ej: Factura Proveedor, Cuota 3")
        c1, c2 = st.columns(2)
        with c1:
            p_type = st.selectbox("Tipo", ["Por Cobrar", "Por Pagar"])
            p_due_date = st.date_input("Fecha de Vencimiento", value=datetime.now())
            p_cat_name = st.selectbox("Categoría (Opcional)", options=[""] + list(cat_options.keys()))
        with c2:
            p_amount = st.number_input("Monto", value=0.0, format="%.2f")
            p_acc_name = st.selectbox("Cuenta (Opcional)", options=[""] + list(acc_options.keys()))
            p_status = st.selectbox("Estado", ["Pendiente", "Pagado", "Vencido", "Parcial"])
            
        p_counterparty = st.text_input("Contraparte (Cliente/Proveedor)", placeholder="Opcional")
        p_notes = st.text_area("Notas", placeholder="Opcional")
            
        p_submitted = st.form_submit_button("Guardar Pago Pendiente", use_container_width=True)
        if p_submitted:
            if not p_title.strip():
                st.error("El título es requerido.")
            else:
                cat_id = cat_options[p_cat_name] if p_cat_name else None
                acc_id = acc_options[p_acc_name] if p_acc_name else None
                
                success, msg = add_pending_payment(
                    p_title.strip(), p_type, p_amount, 'CLP', p_due_date.strftime("%Y-%m-%d"), 
                    acc_id, cat_id, p_status, p_counterparty, p_notes
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(f"Error: {msg}")
