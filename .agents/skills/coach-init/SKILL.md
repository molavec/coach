---
name: coach-init
description: 'Initial onboarding for the coach. Activates when the user profile (user_profile table in coach.db) does not exist or is empty. Guides a minimum viable setup by asking only 3 essential questions and leaves the rest for progressive discovery in future conversations.'
---

## Purpose

This skill handles the **first contact** with a new user. The goal is to create a minimum viable setup in SQLite database `coach.db` that allows the coach to operate immediately, without overwhelming the user with too many questions.

---

## When to Activate

Activate this flow **ONLY** when `python scripts/agent_db.py --action query --sql "SELECT COUNT(*) FROM user_profile;"` returns `0` (or database is not initialized).

---

## Initial Onboarding Flow (Maximum 3 questions)

### Question 1: Identity and Context
> "Hello! I am your productivity and financial coach. To get to know you better, tell me:
> **What is your name and what do you do professionally?**
> (E.g., 'I'm Ana, a frontend developer and UX designer')"

Based on the response, insert into `user_profile` table:
```bash
python scripts/agent_db.py --action execute --sql "INSERT INTO user_profile (name, core_skills) VALUES ('Name', 'Inferred core skills');"
```

### Question 2: Financial Goal
> "Great, [name]. Now, the most important part:
> **What is your monthly income goal and what currency do you work with?**
> (E.g., '$2,000,000 CLP', '3,000 USD', '2,500 EUR')"

Based on the response, insert into `financial_goals` table:
```bash
python scripts/agent_db.py --action execute --sql "INSERT INTO financial_goals (period, monthly_amount, currency) VALUES (strftime('%Y-%m', 'now'), 2000000, 'CLP');"
```

### Question 3: Current Situation
> "One last question to get started:
> **Do you have active clients or projects right now, or are you starting from scratch?**
> If you do, please name the main ones."

Based on the response:
- If they have projects → insert into `projects` table with the mentioned ones:
  ```bash
  python scripts/agent_db.py --action execute --sql "INSERT INTO projects (id, name, status) VALUES ('proj_slug', 'Project Name', 'Activo');"
  ```
- If they start from scratch → mark in `financial_goals` table:
  ```bash
  python scripts/agent_db.py --action execute --sql "UPDATE financial_goals SET notes = 'User without active clients — prioritize prospecting' WHERE period = strftime('%Y-%m', 'now');"
  ```

---

## After Onboarding: Wrap-up Message

After the 3 questions, the coach should:

1. Display a summary of the configuration saved in SQLite.
2. Offer to start working immediately.
3. Template message:

> "Done, [name]. I have stored the basics in SQLite to start working. As we talk, I'll learn more about you — your routine, your services, your working style — and adjust my coaching accordingly.
>
> **What would you like us to focus on today?**"

---

## Database Tables Initialized

| Table | Initial Content |
|---|---|
| `user_profile` | Name and core skills |
| `financial_goals` | Monthly income goal amount and currency |
| `projects` | Active projects (or empty) |
| `tasks` | Base schema ready (empty) |

---

## Configuration Deferred to Progressive Discovery

These tables are populated later, when requirements arise organically in conversation:

| Table | When to Populate |
|---|---|
| `design_system` | When the user mentions layouts, design, or landing pages |
| `coaching_rules` | After 2-3 sessions, once the coach identifies the user's patterns |
| `financial_pricing` | When the user mentions quoting, charging, or selling services |
| `financial_projections` | When discussing monthly financial planning |
| `growth_focus_areas` | When focus patterns are identified in conversations |
| `growth_checklists` | When the user needs to document SOPs for a project |
| `growth_reflections` | When vocational reflections or personal retrospectives occur. Save a condensed summary to DB via `agent_db.py` and export the full narrative markdown to `./growth/reflections/` |
