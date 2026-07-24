-- Schema for Coach SQLite Database (coach.db)

-- User Profile
CREATE TABLE IF NOT EXISTS user_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    core_skills TEXT,
    stability_pillar TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Design System Preferences
CREATE TABLE IF NOT EXISTS design_system (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    style_preferences TEXT,
    typography TEXT,
    tech_stack TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Coaching Rules & Preferences
CREATE TABLE IF NOT EXISTS coaching_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tone TEXT,
    daily_blocks TEXT,
    contingencies TEXT,
    prohibitions TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Active & Archived Projects
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'Media',
    status TEXT DEFAULT 'Activo',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    archived_at DATETIME
);

-- Active & Archived Tasks
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    project_id TEXT,
    estimated_time TEXT,
    actual_time TEXT,
    assignee TEXT,
    priority TEXT DEFAULT 'Media',
    status TEXT DEFAULT 'Pendiente',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at DATETIME,
    completed_at DATETIME,
    archived_at DATETIME,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- Task Tags (N:M Relationship)
CREATE TABLE IF NOT EXISTS task_tags (
    task_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    PRIMARY KEY (task_id, tag),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Financial Goals
CREATE TABLE IF NOT EXISTS financial_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period TEXT,
    monthly_amount REAL,
    currency TEXT,
    billing_strategy TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Income Projections
CREATE TABLE IF NOT EXISTS financial_projections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period TEXT,
    project_id TEXT,
    client_name TEXT,
    projected_amount REAL,
    actual_billed REAL DEFAULT 0,
    status TEXT DEFAULT 'Proyectado',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- Service Rates & Pricing Catalog
CREATE TABLE IF NOT EXISTS financial_pricing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    description TEXT,
    price REAL,
    currency TEXT,
    billing_type TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Vocational & Growth Focus Areas
CREATE TABLE IF NOT EXISTS growth_focus_areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'Media',
    status TEXT DEFAULT 'Activo',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Work Checklists & SOPs
CREATE TABLE IF NOT EXISTS growth_checklists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    project_id TEXT,
    items TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- Weekly Reflections & Retrospectives Log
CREATE TABLE IF NOT EXISTS growth_reflections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT,
    content TEXT,
    achievements TEXT,
    learnings TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Institutional Memory (Coach Notes per Area)
CREATE TABLE IF NOT EXISTS coach_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area TEXT NOT NULL,
    date TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Personal Accounts & Finance Management
-- ============================================================================

-- 1. Financial Accounts (Cuentas Financieras: Bancos, Tarjetas, Efectivo, Inversiones)
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Identificador único de la cuenta
    name TEXT NOT NULL,                         -- Nombre descriptivo (ej: 'Banco Santander', 'Tarjeta VISA', 'Efectivo CLP')
    type TEXT NOT NULL,                         -- Tipo: 'Banco', 'Tarjeta Crédito', 'Efectivo', 'Inversión', 'Billetera Digital'
    currency TEXT DEFAULT 'CLP',                 -- Moneda principal de la cuenta ('CLP', 'USD', etc.)
    balance REAL DEFAULT 0.0,                   -- Saldo actual conciliado de la cuenta
    is_active INTEGER DEFAULT 1,                -- Estado: 1 para activa, 0 para archivada/desactivada
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de creación del registro
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- Fecha y hora de última actualización de saldo o datos
);

-- 2. Categories (Categorías y Subcategorías con clasificación 50/30/20)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Identificador único de la categoría
    name TEXT NOT NULL,                         -- Nombre (ej: 'Alquiler/Vivienda', 'Alimentación', 'Suscripciones Tech')
    type TEXT NOT NULL,                         -- Tipo de flujo: 'Ingreso', 'Egreso', 'Inversión', 'Transferencia'
    parent_id INTEGER,                          -- ID de categoría padre para subcategorías (NULL si es categoría principal)
    is_essential INTEGER DEFAULT 0,             -- Clasificación regla 50/30/20: 1 para Necesidad Básica (50%), 0 para Deseo/Estilo de vida (30%)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de creación del registro
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- 3. Transactions (Movimientos Financieros de Ingreso, Egreso o Transferencia)
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Identificador único de la transacción
    date TEXT NOT NULL,                         -- Fecha de la transacción en formato YYYY-MM-DD
    type TEXT NOT NULL,                         -- Tipo de movimiento: 'Ingreso', 'Egreso', 'Transferencia'
    amount REAL NOT NULL,                       -- Monto del movimiento (positivo)
    currency TEXT DEFAULT 'CLP',                 -- Moneda de la transacción ('CLP', 'USD')
    account_id INTEGER NOT NULL,                -- ID de la cuenta de origen/afectada (FK -> accounts.id)
    destination_account_id INTEGER,             -- ID de la cuenta de destino (requerido solo para 'Transferencia')
    category_id INTEGER,                        -- ID de la categoría asociada (FK -> categories.id)
    description TEXT,                           -- Detalle o nota explicativa del movimiento (ej: 'Supermercado Lider', 'Pago cliente X')
    status TEXT DEFAULT 'Completado',            -- Estado del movimiento: 'Completado', 'Pendiente', 'Cancelado'
    is_recurring INTEGER DEFAULT 0,             -- Flag de recurrencia: 1 si es suscripción o gasto fijo mensual, 0 si es puntual
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de registro en la base de datos
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (destination_account_id) REFERENCES accounts(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- 4. Pending Payments & Receivables (Pagos y Cobros Pendientes / Cuentas por Cobrar y por Pagar)
CREATE TABLE IF NOT EXISTS pending_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Identificador único de la cuenta pendiente
    title TEXT NOT NULL,                        -- Título descriptivo (ej: 'Factura Cliente ABC', 'Cuota 3 Tarjeta Crédito')
    type TEXT NOT NULL,                         -- Tipo: 'Por Cobrar' (ingreso futuro esperable), 'Por Pagar' (compromiso de gasto)
    amount REAL NOT NULL,                       -- Monto adeudado o a cobrar
    currency TEXT DEFAULT 'CLP',                 -- Moneda de la deuda ('CLP', 'USD')
    due_date TEXT NOT NULL,                     -- Fecha límite o de vencimiento en formato YYYY-MM-DD
    account_id INTEGER,                         -- ID de la cuenta en la que se espera liquidar o pagar (FK -> accounts.id)
    category_id INTEGER,                        -- ID de la categoría presupuestaria asignada (FK -> categories.id)
    status TEXT DEFAULT 'Pendiente',            -- Estado: 'Pendiente', 'Pagado', 'Vencido', 'Parcial'
    counterparty TEXT,                          -- Nombre de la tercera parte: cliente, proveedor, banco o persona
    paid_date TEXT,                             -- Fecha en la que se liquidó o pagó el compromiso (YYYY-MM-DD)
    notes TEXT,                                 -- Notas u observaciones adicionales sobre la gestión del pago
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación del compromiso
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- 5. Savings & Investment Goals (Objetivos de Ahorro y Bolsillos Financieros)
CREATE TABLE IF NOT EXISTS savings_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Identificador único del meta/bolsillo de ahorro
    name TEXT NOT NULL,                         -- Nombre de la meta (ej: 'Fondo de Emergencia 6 Meses', 'Viaje Conferencia', 'Renovación Laptop')
    target_amount REAL NOT NULL,                -- Monto objetivo total a alcanzar
    current_amount REAL DEFAULT 0.0,            -- Monto acumulado actualmente en esta meta
    currency TEXT DEFAULT 'CLP',                 -- Moneda del ahorro ('CLP', 'USD')
    target_date TEXT,                           -- Fecha estimada o meta para completar el fondo (YYYY-MM-DD)
    account_id INTEGER,                         -- Cuenta específica donde se custodia este dinero reservado (FK -> accounts.id)
    status TEXT DEFAULT 'En Progreso',            -- Estado de la meta: 'En Progreso', 'Completado', 'Pausado'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación de la meta
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE SET NULL
);

-- 6. Monthly Budgets per Category (Presupuestos Mensuales por Categoría)
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Identificador único de la regla presupuestaria
    period TEXT NOT NULL,                       -- Período del presupuesto en formato YYYY-MM (ej: '2026-08')
    category_id INTEGER NOT NULL,               -- ID de la categoría a la que se aplica el límite (FK -> categories.id)
    allocated_amount REAL NOT NULL,             -- Monto máximo presupuestado o tope asignado para el mes
    currency TEXT DEFAULT 'CLP',                 -- Moneda del presupuesto ('CLP', 'USD')
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha de configuración del presupuesto
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE(period, category_id)                 -- Evita presupuestos duplicados para una misma categoría en el mismo mes
);
