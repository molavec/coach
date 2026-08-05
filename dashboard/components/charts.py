import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLOR_INCOME = "#2ECC71"
COLOR_EXPENSE = "#E74C3C"
COLOR_NET = "#3498DB"
COLOR_ESSENTIAL = "#F39C12"
COLOR_DISCRETIONARY = "#9B59B6"
COLOR_SAVINGS = "#1ABC9C"

# Configuración estándar para colocar la leyenda en la parte inferior de los gráficos
LEGEND_BOTTOM_CONFIG = dict(
    orientation="h",
    yanchor="top",
    y=-0.2,
    xanchor="center",
    x=0.5
)

def plot_cash_flow_monthly(cash_flow_df):
    """Plot monthly income vs expenses bar chart."""
    if cash_flow_df.empty:
        fig = go.Figure()
        fig.update_layout(title="Sin datos de Flujo de Caja")
        return fig
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cash_flow_df['month'],
        y=cash_flow_df['total_income'],
        name='Ingresos',
        marker_color=COLOR_INCOME
    ))
    fig.add_trace(go.Bar(
        x=cash_flow_df['month'],
        y=cash_flow_df['total_expenses'],
        name='Egresos',
        marker_color=COLOR_EXPENSE
    ))
    fig.add_trace(go.Scatter(
        x=cash_flow_df['month'],
        y=cash_flow_df['net_flow'],
        name='Flujo Neto',
        mode='lines+markers',
        line=dict(color=COLOR_NET, width=3)
    ))
    
    fig.update_layout(
        title="<b>Evolución de Flujo de Caja Mensual</b>",
        barmode='group',
        xaxis_title="Mes",
        yaxis_title="Monto (CLP)",
        legend=LEGEND_BOTTOM_CONFIG,
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=60)
    )
    return fig

def plot_category_distribution(transactions_df):
    """Plot expense distribution by category (Donut chart)."""
    expenses_df = transactions_df[transactions_df['type'] == 'Egreso']
    if expenses_df.empty:
        fig = go.Figure()
        fig.update_layout(title="Sin egresos en el periodo")
        return fig
    
    cat_summary = expenses_df.groupby('category_name')['amount'].sum().reset_index()
    fig = px.pie(
        cat_summary, 
        values='amount', 
        names='category_name',
        title="<b>Gastos por Categoría</b>",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        template="plotly_white",
        legend=LEGEND_BOTTOM_CONFIG,
        margin=dict(l=20, r=20, t=50, b=60)
    )
    return fig

def plot_50_30_20_breakdown(transactions_df):
    """Plot 50/30/20 Rule compliance breakdown."""
    expenses_df = transactions_df[transactions_df['type'] == 'Egreso'].copy()
    if expenses_df.empty:
        fig = go.Figure()
        fig.update_layout(title="Sin datos para Regla 50/30/20")
        return fig
    
    expenses_df['essential_label'] = expenses_df['is_essential'].apply(
        lambda x: 'Necesidad Esencial (50%)' if x == 1 else 'Deseo / Estilo de Vida (30%)'
    )
    
    summary = expenses_df.groupby('essential_label')['amount'].sum().reset_index()
    fig = px.bar(
        summary,
        x='essential_label',
        y='amount',
        color='essential_label',
        title="<b>Clasificación Regla 50/30/20 (Necesidades vs Deseos)</b>",
        labels={'amount': 'Monto (CLP)', 'essential_label': 'Clasificación'},
        color_discrete_map={
            'Necesidad Esencial (50%)': COLOR_ESSENTIAL,
            'Deseo / Estilo de Vida (30%)': COLOR_DISCRETIONARY
        }
    )
    fig.update_layout(
        legend=LEGEND_BOTTOM_CONFIG,
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=60)
    )
    return fig

def plot_account_balances(accounts_df):
    """Plot account balances as horizontal bar chart."""
    if accounts_df.empty:
        fig = go.Figure()
        fig.update_layout(title="Sin cuentas registradas")
        return fig
    
    fig = px.bar(
        accounts_df,
        x='balance',
        y='name',
        orientation='h',
        title="<b>Saldos por Cuenta Financiera</b>",
        labels={'balance': 'Saldo (CLP)', 'name': 'Cuenta'},
        color='type',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        template="plotly_white",
        yaxis=dict(autorange="reversed"),
        legend=LEGEND_BOTTOM_CONFIG,
        margin=dict(l=20, r=20, t=50, b=60)
    )
    return fig

def plot_budget_vs_actual(budgets_df):
    """Plot allocated budget vs actual spending per category."""
    if budgets_df.empty:
        fig = go.Figure()
        fig.update_layout(title="Sin presupuestos definidos")
        return fig
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=budgets_df['category_name'],
        x=budgets_df['allocated_amount'],
        name='Presupuestado',
        orientation='h',
        marker_color='#BDC3C7'
    ))
    fig.add_trace(go.Bar(
        y=budgets_df['category_name'],
        x=budgets_df['actual_amount'],
        name='Ejecutado Real',
        orientation='h',
        marker_color='#E74C3C'
    ))
    
    fig.update_layout(
        title="<b>Presupuesto Asignado vs Gasto Real</b>",
        barmode='group',
        xaxis_title="Monto (CLP)",
        yaxis_title="Categoría",
        legend=LEGEND_BOTTOM_CONFIG,
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=60)
    )
    return fig

def plot_tasks_status(tasks_df):
    """Plot task status distribution chart."""
    if tasks_df.empty:
        fig = go.Figure()
        fig.update_layout(title="Sin tareas registradas")
        return fig
    
    status_counts = tasks_df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig = px.pie(
        status_counts, 
        values='Count', 
        names='Status',
        title="<b>Estado de Tareas</b>",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(
        template="plotly_white",
        legend=LEGEND_BOTTOM_CONFIG,
        margin=dict(l=20, r=20, t=50, b=60)
    )
    return fig
