import streamlit as st

# Configure Streamlit page layout and theme
st.set_page_config(
    page_title="Coach",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to collapse stSidebarHeader height and streamline sidebar layout
st.markdown("""
    <style>
    /* 1. Colapsar el contenedor del header del sidebar (stSidebarHeader / eelgd2m4) a alto 0 para que no sobresalga */
    header[data-testid="stSidebarHeader"],
    div[data-testid="stSidebarHeader"] {
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: visible !important;
        background: transparent !important;
    }

    /* Posicionar exclusivamente el botón de toggle dentro del bloque de título Coach a la derecha */
    header[data-testid="stSidebarHeader"] button,
    div[data-testid="stSidebarHeader"] button,
    button[data-testid="stSidebarCollapseButton"] {
        position: absolute !important;
        top: 0.5rem !important;
        right: 0.5rem !important;
        z-index: 9999 !important;
        margin: 0 !important;
    }

    /* 2. Optimización de relleno e interior del sidebar */
    div[data-testid="stSidebarContent"] {
        padding-top: 0.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 0.1rem !important;
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
    }

    /* Título 'Coach' compacto y bien alineado */
    div[data-testid="stSidebarUserContent"] h1 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-top: 0rem !important;
        margin-bottom: 0.75rem !important;
        padding-top: 0.2rem !important;
        line-height: 1.2 !important;
    }

    /* Margen para el botón de acción en el sidebar */
    div[data-testid="stSidebarUserContent"] div.stButton {
        margin-top: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Definir páginas multipágina
page_cash_flow = st.Page("pages/cash_flow.py", title="Flujo de Caja & Resumen", icon="📊", default=True)
page_transactions = st.Page("pages/transactions.py", title="Transacciones", icon="💸")
page_accounts = st.Page("pages/accounts.py", title="Patrimonio & Cuentas", icon="🛡️")
page_budgets = st.Page("pages/budgets.py", title="Presupuestos & Pendientes", icon="🚨")
page_productivity = st.Page("pages/productivity.py", title="Productividad (Coach)", icon="🎯")
page_export = st.Page("pages/export.py", title="Exportar a Excel", icon="📥")

# Inicializar Navegación oculta (para renderizarla manualmente con control de orden)
pg = st.navigation(
    [page_cash_flow, page_transactions, page_accounts, page_budgets, page_productivity, page_export]
)

# Renderizar Sidebar personalizado: Título PRIMERO, luego los links de navegación
# st.sidebar.title("Coach")
# st.sidebar.page_link(page_cash_flow)
# st.sidebar.page_link(page_accounts)
# st.sidebar.page_link(page_budgets)
# st.sidebar.page_link(page_productivity)
# st.sidebar.page_link(page_export)

# Inyectar dinámicamente el título de la página activa en el header principal
st.markdown(f"""
    <style>
    header[data-testid="stHeader"]::after {{
        content: "{pg.title}";
        font-size: 1.25rem;
        font-weight: 700;
        position: absolute;
        left: 3.5rem;
        top: 50%;
        transform: translateY(-50%);
        white-space: nowrap;
        pointer-events: none;
    }}
    </style>
""", unsafe_allow_html=True)

# Ejecutar la página activa
pg.run()
