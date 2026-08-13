# Financial, Vocational Coach & Productivity Strategist

This project implements a productivity, financial, and vocational development coach designed for senior technical and creative profiles. The coach helps maintain radical focus, optimize time management, avoid structured procrastination, and prioritize income-generating activities without neglecting physical and mental well-being.

## Project Structure

```
coach/
├── coach.db               # SQLite database (main local persistence)
├── db/
│   └── schema.sql         # DDL schema definition
└── growth/
    └── reflections/       # Markdown copies of weekly retrospectives
```

## Project Management Rules

* **Database Persistence:** All application data is stored in `./coach.db`. **IMPORTANT:** The agent MUST ALWAYS use `python scripts/agent_db.py` (e.g. `--action add_transaction`, `--action query --sql="..."`) to interact with the database. Never use raw `sqlite3` from the terminal.
* **Active Projects:** Manage in `projects` table (`WHERE status = 'Activo'`).
* **Active Tasks:** Manage in `tasks` and `task_tags` tables (`WHERE status != 'Completado' AND status != 'Archivado'`).
* **Archived Records:** Mark records with `status = 'Archivado'` and set `archived_at = CURRENT_TIMESTAMP`.
* **Financial Goals & Projections:** Manage in `financial_goals`, `financial_projections`, and `financial_pricing` tables.
* **Personal Finances & Accounts:** Manage in `accounts`, `categories`, `transactions`, `pending_payments`, `savings_goals`, and `budgets` tables.
* **Focus Areas:** Update in `growth_focus_areas` table.
* **Checklists:** Create and manage in `growth_checklists` table.
* **Retrospectives & Journaling (Hybrid Model):** Store a highly condensed summary (insights, alerts) in the `growth_reflections` table via `agent_db.py` AND save the full narrative markdown copy in `./growth/reflections/YYYY-MM-DD-retrospective.md`.
* **Coach Institutional Notes:** Store in `coach_notes` table (with `area` as 'profile', 'projects', 'finances', or 'growth').