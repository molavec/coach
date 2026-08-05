import streamlit as st
import datetime
from utils.excel_exporter import generate_excel_report

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
