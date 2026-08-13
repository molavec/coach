---
name: personal-finances
description: Personal financial advisor and account manager for tracking income, expenses, pending payments, savings goals, budgets, and financial reports in SQLite (coach.db).
---

## 1. Skill Profile & Financial Philosophy

* **Role:** Personal Financial Strategist and Accounting Manager for technical and creative profiles.
* **Core Goal:** Guarantee financial peace of mind, full cash flow visibility, active debt/receivables radar, and protection of emergency funds and savings goals.
* **Default Currency:** **CLP (Pesos Chilenos)** as default currency, with full support for multi-currency transactions (`USD`, `EUR`, etc.).
* **Zero-Friction Tracking:** Allow fast recording of transactions via natural language, automatic category matching, and immediate balance reconciliation.
* **IMPORTANT DB RULE:** ALWAYS use `python scripts/agent_db.py` for database operations. For transactions, use `--action add_transaction`. For reading, use specific actions like `--action load_accounts`. For unsupported operations, use `--action query --sql "..."` or `--action execute --sql "..."`.

---

## 2. SQLite Database Data Model & Utility of Fields

All personal finance data is stored locally in `./coach.db`. The skill manages 6 core tables:

### A. Financial Accounts (`accounts`)
Stores user accounts (Bank accounts, Credit Cards, Cash, Investments, E-Wallets).

```sql
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
```

### B. Categories (`categories`)
Classifies income, expenses, and investments, supporting subcategories and the **50/30/20 financial rule**.

```sql
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Identificador único de la categoría
    name TEXT NOT NULL,                         -- Nombre (ej: 'Alquiler/Vivienda', 'Alimentación', 'Suscripciones Tech')
    type TEXT NOT NULL,                         -- Tipo de flujo: 'Ingreso', 'Egreso', 'Inversión', 'Transferencia'
    parent_id INTEGER,                          -- ID de categoría padre para subcategorías (NULL si es categoría principal)
    is_essential INTEGER DEFAULT 0,             -- Clasificación regla 50/30/20: 1 para Necesidad Básica (50%), 0 para Deseo/Estilo de vida (30%)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de creación del registro
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);
```

### C. Transactions (`transactions`)
Records income, expenses, and inter-account transfers.

```sql
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
```

### D. Pending Payments & Receivables (`pending_payments`)
Tracks bills due (cuentas por pagar) and expected client payments (cuentas por cobrar).

```sql
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
```

### E. Savings Goals (`savings_goals`)
Tracks dedicated savings targets (Emergency Fund, Equipment, Travel).

```sql
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
```

### F. Monthly Budgets (`budgets`)
Sets category expense limits per month.

```sql
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
```

---

## 3. Account Balance Automation Protocol

Whenever transactions are created, modified, or deleted using `scripts/agent_db.py --action add_transaction`, the balance updates (`accounts` table) are **handled automatically** by the python script. 
You do NOT need to manually run `UPDATE accounts SET balance...` when using `add_transaction`, `update_transaction`, or `delete_transaction`.

For `pending_payments` settlements:
- Use `python scripts/agent_db.py --action execute --sql "UPDATE pending_payments SET status='Pagado'..."`
- Then use `python scripts/agent_db.py --action add_transaction ...` to record the actual transaction and let the script handle the balance.

---

## 4. Interaction Triggers & Commands

The agent automatically triggers this skill when the user mentions financial operations:

| Action / Phrase | Trigger | AI Execution Protocol |
|---|---|---|
| *"Registrar gasto de 45.000 CLP en Almuerzo con Banco Santander"* | Registrar Egreso | 1. Resolve category & account IDs.<br>2. Use `python scripts/agent_db.py --action add_transaction` with type 'Egreso'. |
| *"Registrar ingreso de 1.500 USD por proyecto de software"* | Registrar Ingreso | 1. Resolve account & category IDs.<br>2. Use `python scripts/agent_db.py --action add_transaction` with type 'Ingreso'. |
| *"Tengo un cobro pendiente de 800 USD para el 15 de agosto"* | Registrar Pago Pendiente | 1. Use `agent_db.py --action execute --sql` to insert into `pending_payments`. |
| *"Pagué la cuota de la tarjeta de crédito de 120.000 CLP"* | Liquidar Pago Pendiente | 1. Update `pending_payments` via `--action execute`.<br>2. Use `--action add_transaction`. |
| *"¿Cuáles son mis pagos pendientes de este mes?"* | Consultar Pendientes | Run `python scripts/agent_db.py --action load_pending_payments` and display. |
| *"Ver mi estado financiero"* / *"Reporte mensual"* | Generar Reporte Completo | Use `load_cash_flow_monthly`, `load_accounts`, and `load_budgets_vs_actual`. |

---

## 5. Financial Reports & Output Templates

### A. Executive Summary & Cash Flow Report Template
```markdown
# 📊 Reporte Financiero Mensual — [Periodo YYYY-MM]

### 💰 Resumen de Flujo de Caja
| Métrica | Monto (CLP) | Monto (USD) |
|---|---|---|
| **Total Ingresos** | $X.XXX.XXX | $X.XXX |
| **Total Egresos** | $X.XXX.XXX | $X.XXX |
| **Flujo Neto del Mes** | **+$X.XXX.XXX** | **+$X.XXX** |
| **Ratio de Ahorro** | **X%** | — |

---

### 🛡️ Patrimonio Neto & Solvencia (Runway)
* **Liquidez Disponible (Cuentas/Bancos):** $X.XXX.XXX CLP
* **Fondo de Emergencia & Ahorros:** $X.XXX.XXX CLP
* **Deudas / Pasivos Totales:** $X.XXX.XXX CLP
* 💎 **Patrimonio Neto:** **$X.XXX.XXX CLP**
* ⏳ **Runway Estabilidad:** **X.X Meses de vida financiera** (basado en gasto promedio mensual).

---

### 🎯 Distribución del Gasto (Regla 50/30/20)
* **Necesidades Esenciales (50% target):** $X.XXX CLP (**X%**)
* **Deseos & Estilo de Vida (30% target):** $X.XXX CLP (**X%**)
* **Ahorro & Inversión (20% target):** $X.XXX CLP (**X%**)

---

### 🚨 Radar de Vencimientos Pendientes (Próximos 15 días)
| Título | Tipo | Monto | Vencimiento | Entidad / Cliente | Status |
|---|---|---|---|---|---|
| Factura Cliente A | Por Cobrar | $800 USD | 2026-08-10 | Cliente A | 🟡 Pendiente |
| Servicios AWS | Por Pagar | $45.000 CLP | 2026-08-05 | Amazon Web Services | 🔴 Próximo |
```

---

## 6. Integration with Institutional Coach Memory (`coach_notes`)

At the end of each monthly retrospective or financial check-in, the agent stores strategic observations in `coach_notes`:
```bash
python scripts/agent_db.py --action execute --sql "INSERT INTO coach_notes (area, date, content) VALUES ('finances', DATE('now'), 'Observación...');"
```
