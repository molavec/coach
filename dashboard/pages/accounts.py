import streamlit as st
from utils.db import load_accounts, load_savings_goals
from components.charts import plot_account_balances
from components.tables import render_savings_goals_table

accounts_df = load_accounts()
savings_df = load_savings_goals()

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
