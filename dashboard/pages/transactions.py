import streamlit as st
import datetime
import pandas as pd
from services.finance_cache import (
    load_accounts, 
    load_categories, 
    load_transactions, 
    add_transaction, 
    update_transaction,
    delete_transaction
)
from core.services.finance_service import process_credit_card_expense

def get_date_range(filter_range: str, today: datetime.date, custom_start=None, custom_end=None):
    if filter_range == "Hoy":
        return today, today
    if filter_range == "Últimos 7 días":
        return today - datetime.timedelta(days=6), today
    if filter_range == "Últimos 30 días":
        return today - datetime.timedelta(days=29), today
    if filter_range == "Esta semana":
        start = today - datetime.timedelta(days=today.weekday())
        return start, start + datetime.timedelta(days=6)
    if filter_range == "Este mes":
        start = today.replace(day=1)
        next_month = (today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        return start, next_month - datetime.timedelta(days=1)
    if filter_range == "Mes anterior":
        first_of_this_month = today.replace(day=1)
        end = first_of_this_month - datetime.timedelta(days=1)
        return end.replace(day=1), end
    if filter_range == "Este año":
        return today.replace(month=1, day=1), today.replace(month=12, day=31)
    if filter_range == "Personalizado" and custom_start:
        return custom_start, custom_end or custom_start
    return None, None

def parse_date(raw_date):
    if isinstance(raw_date, (datetime.date, datetime.datetime)):
        return raw_date.strftime("%Y-%m-%d")
    return str(raw_date)

# Cargar datos desde SQLite
accounts_df = load_accounts()
categories_df = load_categories()
transactions_df = load_transactions(limit=1000)

if accounts_df.empty:
    st.warning("⚠️ No hay cuentas financieras registradas. Primero crea una cuenta en la sección de Patrimonio & Cuentas.")
    st.stop()

# Mapeos útiles para selects en data_editor
account_name_to_id = {row['name']: row['id'] for _, row in accounts_df.iterrows()}
account_options = {
    f"{row['name']} ({row['currency']} - Saldo: ${row['balance']:,.0f})": row['id'] 
    for _, row in accounts_df.iterrows()
}

category_name_to_id = {row['name']: row['id'] for _, row in categories_df.iterrows()} if not categories_df.empty else {}
category_options = {
    f"[{row['type']}] {row['name']}": row['id'] 
    for _, row in categories_df.iterrows()
} if not categories_df.empty else {}

today = datetime.date.today()

# Barra de Filtros
tb_col1, tb_col2, tb_col3, tb_col4 = st.columns([3, 3, 3, 3])

date_filter_options = [
    "Todas las fechas",
    "Hoy",
    "Últimos 7 días",
    "Últimos 30 días",
    "Esta semana",
    "Este mes",
    "Mes anterior",
    "Este año",
    "Personalizado"
]

with tb_col1:
    filter_date_range = st.selectbox("Periodo", date_filter_options, index=0)
with tb_col2:
    filter_type = st.selectbox("Tipo", ["Todos", "Egreso", "Ingreso", "Transferencia"], index=0)
with tb_col3:
    accounts_list = ["Todas las cuentas"] + sorted(list(set(transactions_df['account_name'].dropna()))) if not transactions_df.empty else ["Todas las cuentas"]
    filter_account = st.selectbox("Cuenta", accounts_list, index=0)
with tb_col4:
    search_query = st.text_input("Buscar", placeholder="Buscar por texto...")

custom_start_date = None
custom_end_date = None
if filter_date_range == "Personalizado":
    custom_dates = st.date_input(
        "Rango de Fechas Personalizado",
        value=(today - datetime.timedelta(days=30), today)
    )
    if isinstance(custom_dates, (list, tuple)):
        if len(custom_dates) == 2:
            custom_start_date, custom_end_date = custom_dates
        elif len(custom_dates) == 1:
            custom_start_date = custom_end_date = custom_dates[0]

# Pre-procesado y Filtrado de DataFrame
filtered_df = transactions_df.copy()

if transactions_df.empty:
    st.info("👋 **Sin transacciones.** Añade tu primera transacción interactuando con la tabla de abajo.")

if not filtered_df.empty:
    # 1. Conversión de tipos
    filtered_df['date'] = pd.to_datetime(filtered_df['date']).dt.date
    filtered_df['is_recurring'] = filtered_df['is_recurring'].astype(bool)
    filtered_df['amount'] = filtered_df['amount'].astype(float)
    filtered_df['id'] = filtered_df['id'].astype(int)

    # 2. Filtro de Fechas
    if filter_date_range != "Todas las fechas":
        start_date, end_date = get_date_range(filter_date_range, today, custom_start_date, custom_end_date)
        if start_date and end_date:
            filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    # 3. Filtro por Tipo
    if filter_type != "Todos":
        filtered_df = filtered_df[filtered_df['type'] == filter_type]

    # 4. Filtro por Cuenta
    if filter_account != "Todas las cuentas":
        filtered_df = filtered_df[filtered_df['account_name'] == filter_account]

    # 5. Búsqueda por texto
    if search_query:
        q = search_query.lower()
        filtered_df = filtered_df[
            filtered_df['description'].fillna('').str.lower().str.contains(q) |
            filtered_df['category_name'].fillna('').str.lower().str.contains(q) |
            filtered_df['account_name'].fillna('').str.lower().str.contains(q)
        ]

# KPIs dinámicos filtrados
if not filtered_df.empty:
    total_ingresado = filtered_df[filtered_df['type'] == 'Ingreso']['amount'].sum()
    total_gastado = filtered_df[filtered_df['type'] == 'Egreso']['amount'].sum()
    flujo_neto = total_ingresado - total_gastado
    total_tx = len(filtered_df)
else:
    total_ingresado = 0.0
    total_gastado = 0.0
    flujo_neto = 0.0
    total_tx = 0

mc1, mc2, mc3, mc4 = st.columns(4)
with mc1:
    st.metric("Total Ingresos", f"${total_ingresado:,.0f}")
with mc2:
    st.metric("Total Egresos", f"${total_gastado:,.0f}")
with mc3:
    st.metric("Resultado Neto", f"${flujo_neto:,.0f}", delta=f"{flujo_neto:,.0f}")
with mc4:
    st.metric("Transacciones", total_tx)

st.markdown("---")
st.caption("💡 **Edición Directa:** Haz doble clic sobre cualquier celda para modificar su valor directamente, o añade/elimina filas en la tabla.")

# Manejo de cambios en el editor de datos
editor_changes = st.session_state.get("tx_editor", {})
has_pending_edits = bool(
    editor_changes.get("edited_rows") or 
    editor_changes.get("deleted_rows") or 
    editor_changes.get("added_rows")
)

if has_pending_edits:
    st.warning("⚠️ Hay cambios editados directamente en la tabla. Presiona **Guardar Cambios** para actualizar la base de datos y tus saldos.")
    col_save, col_reset = st.columns([3, 3])
    with col_save:
        if st.button("💾 Guardar Cambios en Tabla", type="primary", use_container_width=True):
            edited_rows = editor_changes.get("edited_rows", {})
            deleted_rows = editor_changes.get("deleted_rows", [])
            added_rows = editor_changes.get("added_rows", [])
            
            errors = []
            
            # 1. Procesar Eliminaciones
            for row_idx in deleted_rows:
                if row_idx < len(filtered_df):
                    tx_id = int(filtered_df.iloc[row_idx]['id'])
                    ok, msg = delete_transaction(tx_id)
                    if not ok:
                        errors.append(f"Error al eliminar ID {tx_id}: {msg}")

            # 2. Procesar Ediciones directas por celda
            for row_idx_str, changes in edited_rows.items():
                row_idx = int(row_idx_str)
                if row_idx < len(filtered_df):
                    orig_row = filtered_df.iloc[row_idx]
                    tx_id = int(orig_row['id'])

                    raw_date = changes.get('date', orig_row['date'])
                    d_str = parse_date(raw_date)

                    t_str = changes.get('type', orig_row['type'])
                    amt = float(changes.get('amount', orig_row['amount']))
                    curr = changes.get('currency', orig_row['currency'])
                    
                    acc_name = changes.get('account_name', orig_row['account_name'])
                    acc_id = account_name_to_id.get(acc_name)

                    dest_name = changes.get('destination_account_name', orig_row['destination_account_name'])
                    dest_acc_id = account_name_to_id.get(dest_name)

                    cat_name = changes.get('category_name', orig_row['category_name'])
                    cat_id = category_name_to_id.get(cat_name)

                    desc = changes.get('description', orig_row['description'] or '')
                    status_val = changes.get('status', orig_row['status'])
                    rec_val = 1 if changes.get('is_recurring', orig_row['is_recurring']) else 0
                    inst_val = int(changes.get('installments', orig_row.get('installments', 1)))

                    ok, msg = update_transaction(
                        transaction_id=tx_id,
                        date_str=d_str,
                        type_str=t_str,
                        amount=amt,
                        currency=curr,
                        account_id=acc_id,
                        destination_account_id=dest_acc_id,
                        category_id=cat_id,
                        description=desc,
                        status=status_val,
                        is_recurring=rec_val,
                        installments=inst_val
                    )
                    if not ok:
                        errors.append(f"Error al actualizar ID {tx_id}: {msg}")

            # 3. Procesar Adiciones de nuevas filas
            for row_data in added_rows:
                a_amount = float(row_data.get('amount', 0.0))
                a_acc_name = row_data.get('account_name')
                a_acc_id = account_name_to_id.get(a_acc_name)
                
                if a_amount > 0 and a_acc_id:
                    a_raw_date = row_data.get('date', datetime.date.today())
                    a_d_str = parse_date(a_raw_date)

                    a_type = row_data.get('type', 'Egreso')
                    a_curr = row_data.get('currency', 'CLP')
                    a_dest_name = row_data.get('destination_account_name')
                    a_dest_acc_id = account_name_to_id.get(a_dest_name)
                    a_cat_name = row_data.get('category_name')
                    a_cat_id = category_name_to_id.get(a_cat_name)
                    a_desc = row_data.get('description', '')
                    a_status = row_data.get('status', 'Completado')
                    a_rec = 1 if row_data.get('is_recurring') else 0
                    a_installments = int(row_data.get('installments', 1))
                    
                    acc_type = None
                    if a_acc_id:
                        acc_match = accounts_df[accounts_df['id'] == a_acc_id]
                        if not acc_match.empty:
                            acc_type = acc_match['type'].values[0]

                    if acc_type == 'Tarjeta Crédito' and a_type == 'Egreso':
                        ok, msg = process_credit_card_expense(
                            account_id=a_acc_id,
                            date_str=a_d_str,
                            amount=a_amount,
                            currency=a_curr,
                            category_id=a_cat_id,
                            description=a_desc,
                            installments=a_installments,
                            status=a_status,
                            is_recurring=a_rec
                        )
                    else:
                        ok, msg = add_transaction(
                            date_str=a_d_str,
                            type_str=a_type,
                            amount=a_amount,
                            currency=a_curr,
                            account_id=a_acc_id,
                            destination_account_id=a_dest_acc_id,
                            category_id=a_cat_id,
                            description=a_desc,
                            status=a_status,
                            is_recurring=a_rec,
                            installments=a_installments
                        )
                    if not ok:
                        errors.append(f"Error al añadir fila: {msg}")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                st.success("✅ Cambios guardados con éxito en la base de datos.")
                st.rerun()

    with col_reset:
        if st.button("❌ Descartar Cambios", use_container_width=True):
            st.rerun()

# Tabla interactiva con edición directa por celda
st.data_editor(
    filtered_df[['id', 'date', 'type', 'amount', 'currency', 'account_name', 'destination_account_name', 'category_name', 'description', 'status', 'is_recurring', 'installments']],
    column_config={
        'id': st.column_config.NumberColumn('ID', disabled=True, format="%d"),
        'date': st.column_config.DateColumn('Fecha', format="YYYY-MM-DD"),
        'type': st.column_config.SelectboxColumn('Tipo', options=['Egreso', 'Ingreso', 'Transferencia'], required=True),
        'amount': st.column_config.NumberColumn('Monto', format="$%.0f", min_value=0.0, required=True),
        'currency': st.column_config.SelectboxColumn('Moneda', options=['CLP', 'USD', 'EUR'], required=True),
        'account_name': st.column_config.SelectboxColumn('Cuenta Origen', options=list(account_name_to_id.keys()), required=True),
        'destination_account_name': st.column_config.SelectboxColumn('Cuenta Destino', options=list(account_name_to_id.keys())),
        'category_name': st.column_config.SelectboxColumn('Categoría', options=list(category_name_to_id.keys())),
        'description': st.column_config.TextColumn('Descripción'),
        'status': st.column_config.SelectboxColumn('Estado', options=['Completado', 'Pendiente', 'Cancelado'], required=True),
        'is_recurring': st.column_config.CheckboxColumn('Recurrente'),
        'installments': st.column_config.NumberColumn('Cuotas', min_value=1, default=1, format="%d", step=1)
    },
    hide_index=True,
    num_rows="dynamic",
    key="tx_editor"
)
