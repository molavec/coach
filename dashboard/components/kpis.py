import streamlit as st

def render_financial_kpis(income, expense, net_flow, total_liquidity, runway_months):
    """Render financial KPI metric cards."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="💰 Total Ingresos",
            value=f"${income:,.0f} CLP".replace(',', '.')
        )
    with col2:
        st.metric(
            label="💸 Total Egresos",
            value=f"${expense:,.0f} CLP".replace(',', '.')
        )
    with col3:
        delta_color = "normal" if net_flow >= 0 else "inverse"
        st.metric(
            label="📈 Flujo Neto",
            value=f"${net_flow:,.0f} CLP".replace(',', '.'),
            delta=f"{'Superávit' if net_flow >= 0 else 'Deficit'}",
            delta_color=delta_color
        )
    with col4:
        st.metric(
            label="🏦 Liquidez Disponible",
            value=f"${total_liquidity:,.0f} CLP".replace(',', '.')
        )
    with col5:
        st.metric(
            label="⏳ Runway Estabilidad",
            value=f"{runway_months:.1f} Meses",
            help="Meses de vida financiera basados en el gasto mensual promedio."
        )

def render_task_kpis(total_tasks, completed_tasks, in_progress, pending_tasks):
    """Render productivity KPI metric cards."""
    c1, c2, c3, c4 = st.columns(4)
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    with c1:
        st.metric(label="📋 Total Tareas", value=total_tasks)
    with c2:
        st.metric(label="✅ Completadas", value=completed_tasks, delta=f"{completion_rate:.0f}% Éxito")
    with c3:
        st.metric(label="🔄 En Progreso", value=in_progress)
    with c4:
        st.metric(label="⏳ Pendientes", value=pending_tasks)
