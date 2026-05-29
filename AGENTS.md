# Financial, Vocational Coach & Productivity Strategist

This project implements a productivity, financial, and vocational development coach designed for senior technical and creative profiles. The coach helps maintain radical focus, optimize time management, avoid structured procrastination, and prioritize income-generating activities without neglecting physical and mental well-being.

## Project Structure

```
coach/
├── profile/               # Personal user configuration
│   ├── user.yaml           # Profile (name, skills, stability pillar)
│   ├── design-system.yaml  # Preferred design system
│   └── coaching-rules.yaml # Coaching rules (tone, blocks, contingencies)
│
├── projects/              # Project and task management
│   ├── projects.yaml       # Active projects
│   ├── tasks.yaml          # Active tasks
│   └── archived/           # Project and task history
│
├── finances/              # Financial planning
│   ├── goals.yaml          # Financial goals and billing strategy
│   ├── projections.yaml    # Income projections
│   └── pricing.yaml        # Service pricing catalog
│
└── growth/                # Vocational and personal growth
    ├── focus-areas.yaml    # Current focus areas
    ├── checklists/         # Work checklists
    └── reflections/        # Vocational reflections and journaling
```

## Project Management Rules

* **Active Projects:** Manage the list in `./projects/projects.yaml`.
* **Active Tasks:** Manage the list in `./projects/tasks.yaml`.
* **Archived Projects:** Archive in `./projects/archived/projects.yaml`.
* **Archived Tasks:** Archive by date in `./projects/archived/yyyy/mm/dd-tasks.yaml`.
* **Financial Goals:** Manage in `./finances/goals.yaml`.
* **Projections:** Update in `./finances/projections.yaml`.
* **Pricing:** Maintain the catalog in `./finances/pricing.yaml`.
* **Focus Areas:** Update in `./growth/focus-areas.yaml`.
* **Checklists:** Create and manage in `./growth/checklists/`.