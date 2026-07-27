import streamlit as st
import pandas as pd

def render_pending_payments_table(pending_df):
    """Render formatted pending payments radar table."""
    if pending_df.empty:
        st.info("ℹ️ No hay cobros ni pagos pendientes registrados.")
        return

    display_df = pending_df.copy()
    
    # Format status badges
    def format_status(status):
        if status == 'Pendiente':
            return '🟡 Pendiente'
        elif status == 'Pagado':
            return '✅ Pagado'
        elif status == 'Vencido':
            return '🔴 Vencido'
        return status

    display_df['status_badge'] = display_df['status'].apply(format_status)

    # Separate into Por Cobrar and Por Pagar
    receivables = display_df[display_df['type'] == 'Por Cobrar']
    payables = display_df[display_df['type'] == 'Por Pagar']

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Cuentas Por Cobrar (Ingresos Futuros)")
        if not receivables.empty:
            st.dataframe(
                receivables[['due_date', 'title', 'amount', 'currency', 'counterparty', 'status_badge']],
                column_config={
                    'due_date': st.column_config.DateColumn("Vencimiento"),
                    'title': "Concepto",
                    'amount': st.column_config.NumberColumn("Monto", format="$%.0f"),
                    'currency': "Moneda",
                    'counterparty': "Cliente/Entidad",
                    'status_badge': "Estado"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.caption("Sin cobros pendientes.")

    with col2:
        st.subheader("📤 Cuentas Por Pagar (Compromisos Egresos)")
        if not payables.empty:
            st.dataframe(
                payables[['due_date', 'title', 'amount', 'currency', 'counterparty', 'status_badge']],
                column_config={
                    'due_date': st.column_config.DateColumn("Vencimiento"),
                    'title': "Concepto",
                    'amount': st.column_config.NumberColumn("Monto", format="$%.0f"),
                    'currency': "Moneda",
                    'counterparty': "Proveedor/Entidad",
                    'status_badge': "Estado"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.caption("Sin pagos pendientes.")

def render_savings_goals_table(savings_df):
    """Render savings goals with progress bars."""
    if savings_df.empty:
        st.info("ℹ️ No hay bolsillos ni metas de ahorro registradas.")
        return

    st.subheader("🎯 Bolsillos & Metas de Ahorro")
    for _, row in savings_df.iterrows():
        pct = (row['current_amount'] / row['target_amount'] * 100) if row['target_amount'] > 0 else 0
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write(f"**{row['name']}** — Meta: ${row['target_amount']:,.0f} {row['currency']} (Actual: ${row['current_amount']:,.0f})")
            st.progress(min(pct / 100.0, 1.0))
        with c2:
            st.metric(label="Progreso", value=f"{pct:.1f}%")
