# Financial, Vocational Coach & Productivity Strategist

This project implements an intelligent coaching assistant designed for senior technical and creative profiles. It helps maintain radical focus, optimize time management, and prioritize billing/revenue generation without neglecting personal well-being.

---

## Key Benefits

* **Radical Focus:** Prevents structured procrastination (such as coding personal tools instead of selling).
* **Active Financial Management:** Maintains clear goals and plans contingency and prospecting actions during urgent periods.
* **Continuous Learning:** Automatically analyzes time usage by categories to detect bottlenecks.
* **Privacy by Design:** Personal and financial data remains secure locally in an SQLite database (`coach.db`) and Markdown files.

---

## How It Works

The coach operates dynamically through three integrated stages:

1. **Organic and Minimal Onboarding:**  
   When starting for the first time, the coach asks three essential questions to set up your profile. To see how the initial onboarding works, check the [Onboarding Skill](file:///home/angel/git/agents/coach/.agents/skills/coach-init/SKILL.md).

2. **Daily and Contextual Support:**  
   Manages your projects, automates smart task tagging, and estimates ideal times based on your history. You can dive deeper into operational, contingency, and inference rules by reading the [Core Coach Skill](file:///home/angel/git/agents/coach/.agents/skills/coach/SKILL.md).

3. **Weekly Checkpoints and Retrospectives:**  
   Delivers startup reports (Mondays), speed checkpoints (Wednesdays), and week-ending reviews (Fridays), accumulating learnings continuously. Learn about templates and workflows in the [Checkpoint Skill](file:///home/angel/git/agents/coach/.agents/skills/coach-checkpoint/SKILL.md).

---

## Streamlit Dashboard

To visualize financial metrics, active projects, tasks, and generate Excel reports, run the dashboard management script:

```bash
# Start in background
./dashboard.sh start

# Check status
./dashboard.sh status

# Stop server
./dashboard.sh stop

# Start in foreground (Ctrl+C to stop)
./dashboard.sh
```

The dashboard will be available at `http://localhost:8501`.

---

## Workspace Structure

* **`dashboard.sh`** — Executable management script to start, stop, or check status of the Streamlit dashboard.
* **`dashboard/`** — Streamlit app files and components.
* **`coach.db`** — SQLite database holding user profile, projects, tasks, financial goals, projections, pricing catalog, focus areas, and institutional notes.
* **`db/schema.sql`** — DDL database schema defining all relational tables.
* **`growth/reflections/`** — Markdown copies of weekly retrospectives and vocational reflections.


