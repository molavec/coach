import streamlit as st
from datetime import datetime
from utils.db import load_accounts, load_savings_goals, add_account, add_savings_goal
from components.charts import plot_account_balances
from components.tables import render_savings_goals_table

accounts_df = load_accounts()
savings_df = load_savings_goals()

acc_options = {row['name']: row['id'] for _, row in accounts_df.iterrows()} if not accounts_df.empty else {}

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
        st.info("👋 **Sin cuentas registradas.**")
        
    with st.expander("➕ Añadir Nueva Cuenta", expanded=False):
        # El tipo se selecciona fuera del form para permitir renderizado condicional de los detalles
        new_type = st.selectbox("Tipo de Cuenta", ["Banco", "Tarjeta Crédito", "Efectivo", "Inversión", "Billetera Digital"], key="new_acc_type")
        
        with st.form("add_account_form", clear_on_submit=True):
            new_name = st.text_input("Nombre de la Cuenta", placeholder="Ej: Banco Santander, Visa Falabella")
            new_curr = st.selectbox("Moneda Principal", ["CLP", "USD", "EUR"])
            new_balance = st.number_input("Saldo Inicial / Deuda Inicial", value=0.0, format="%.2f")
            
            details = {}
            if new_type == "Tarjeta Crédito":
                st.markdown("##### 💳 Detalles de Tarjeta de Crédito")
                c_tc1, c_tc2 = st.columns(2)
                with c_tc1:
                    details['limit_clp'] = st.number_input("Cupo Nacional (CLP)", min_value=0.0, format="%.0f")
                    details['payment_day'] = st.number_input("Día de Pago/Facturación", min_value=1, max_value=31, value=5)
                with c_tc2:
                    details['limit_usd'] = st.number_input("Cupo Internacional (USD)", min_value=0.0, format="%.2f")
                    details['commission_value'] = st.number_input("Costo Mantención Mensual", min_value=0.0, format="%.0f")
            elif new_type == "Banco":
                st.markdown("##### 🏦 Detalles de Cuenta Bancaria")
                c_b1, c_b2 = st.columns(2)
                with c_b1:
                    details['overdraft_limit'] = st.number_input("Línea de Sobregiro", min_value=0.0, format="%.0f")
                    details['payment_day'] = st.number_input("Día Cobro Mantención", min_value=1, max_value=31, value=1)
                with c_b2:
                    details['commission_value'] = st.number_input("Costo Mantención Mensual", min_value=0.0, format="%.0f")
            
            submitted = st.form_submit_button("Guardar Cuenta", use_container_width=True)
            if submitted:
                if not new_name.strip():
                    st.error("El nombre de la cuenta es requerido.")
                else:
                    success, msg = add_account(new_name.strip(), new_type, new_curr, new_balance, details)
                    if success:
                        st.success(f"Cuenta '{new_name}' añadida con éxito.")
                        st.rerun()
                    else:
                        st.error(f"Error al añadir cuenta: {msg}")

st.divider()
render_savings_goals_table(savings_df)

with st.expander("➕ Añadir Meta de Ahorro", expanded=False):
    with st.form("add_savings_goal_form", clear_on_submit=True):
        sg_name = st.text_input("Nombre de la Meta", placeholder="Ej: Fondo de Emergencia, Viaje")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            sg_target = st.number_input("Monto Objetivo", min_value=1.0, value=1000.0, format="%.2f")
        with c2:
            sg_current = st.number_input("Monto Actual", value=0.0, format="%.2f")
        with c3:
            sg_curr = st.selectbox("Moneda", ["CLP", "USD", "EUR"], key="sg_curr")
            
        c4, c5, c6 = st.columns(3)
        with c4:
            sg_date = st.date_input("Fecha Objetivo (Opcional)", value=None)
        with c5:
            sg_acc_name = st.selectbox("Cuenta Asociada (Opcional)", [""] + list(acc_options.keys()))
        with c6:
            sg_status = st.selectbox("Estado", ["En Progreso", "Completado", "Pausado"])
            
        sg_submitted = st.form_submit_button("Guardar Meta", use_container_width=True)
        if sg_submitted:
            if not sg_name.strip():
                st.error("El nombre de la meta es requerido.")
            else:
                acc_id = acc_options[sg_acc_name] if sg_acc_name else None
                target_date_str = sg_date.strftime("%Y-%m-%d") if sg_date else None
                success, msg = add_savings_goal(
                    sg_name.strip(), sg_target, sg_current, sg_curr, target_date_str, acc_id, sg_status
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(f"Error: {msg}")
