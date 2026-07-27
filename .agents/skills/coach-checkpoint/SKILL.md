---
name: coach-checkpoint
description: 'Weekly summaries, checkpoints, and retrospectives. Generates a weekly kickoff (planning), a midweek checkpoint (course correction), and a wrap-up retrospective (learnings and replanning). Activates when the user asks for a weekly summary, weekly planning, retrospective, checkpoint, or the coach detects it is Monday/Wednesday/Friday.'
---

## Purpose

To give the user a panoramic and actionable view of their week at 3 key moments, with recommendations focused on maximizing results and adjusting course quickly.

---

## Data Sources

Before generating any report, the agent must query SQLite database `coach.db`:

1. **`tasks` & `task_tags`** — Active tasks (`WHERE status != 'Completado' AND status != 'Archivado'`), statuses, estimated times, and actual times spent.
2. **`projects`** — Active projects (`WHERE status = 'Activo'`) and priorities.
3. **`financial_goals`** — Monthly financial goal (`WHERE period = strftime('%Y-%m', 'now')`).
4. **`financial_projections`** — Income projections and actual billed for the current month.
5. **`growth_focus_areas`** — Active focus areas (`WHERE status = 'Activo'`).
6. **`user_profile`** — User context.
7. **`coaching_rules`** *(if exists)* — Rules, daily blocks, tone, and contingencies.

---

## The 3 Key Moments of the Week

### 🟢 1. Weekly Kickoff — "Startup" (Monday or first session of the week)

**Goal:** Total clarity on what to attack this week.

**Report Structure:**

```
📅 WEEKLY STARTUP — [start date] to [end date]

🎯 WEEKLY FOCUS
   Top 3 priorities ordered by financial goal impact.

💰 FINANCIAL OVERVIEW
   - Monthly Goal: $X
   - Billed this month: $Y
   - Gap: $Z
   - Days remaining in the month: N

📋 CRITICAL TASKS (max 5)
   The tasks that move the needle this week, with total estimated time.

⚠️ ALERTS
   - Projects at risk or with upcoming deliverables.
   - Clients requiring follow-up.

💡 COACH RECOMMENDATION
   A concrete strategic recommendation based on the current situation.
```

**Rules:**
- If the financial gap is > 50% of the goal and there are < 15 days left in the month → activate urgency mode: reorder priorities putting commercial prospecting first.
- If there are completed tasks from the previous week, acknowledge them briefly ("Last week you closed X — good momentum").
- Close with: **"Should we adjust anything or do we kick off with this?"**

---

### 🟡 2. Midweek — "Checkpoint" (Wednesday or third session)

**Goal:** Course correction before it is too late.

**Report Structure:**

```
🔄 MIDWEEK CHECKPOINT — [date]

✅ PROGRESS
   Completed tasks since startup (with ✅).
   Tasks in progress (with 🔄).

❌ BLOCKED OR NO PROGRESS
   Tasks without movement and possible cause.

📊 VELOCITY
   - Planned tasks: N
   - Completed: M
   - Pace: [on track / delayed / ahead of schedule]

🔀 SUGGESTED ADJUSTMENTS
   If delayed:
   - What to eliminate or postpone.
   - What to reassign or simplify.
   If ahead:
   - What high-impact task to add.

💡 COACH RECOMMENDATION
   Tactical intervention for the rest of the week.
```

**Rules:**
- If completed < 30% of planned tasks → suggest reducing scope and protecting the 2 tasks with the highest financial impact.
- If completed > 70% → congratulate the user and suggest advancing tasks from the next week or investing in prospecting.
- Close with: **"What do you need to adjust to finish the week strong?"**

---

### 🔴 3. Weekend — "Retrospective" (Friday or last session)

**Goal:** Learn, celebrate, and replan.

**Report Structure:**

```
📊 WEEKLY RETROSPECTIVE — [start date] to [end date]

🏆 ACHIEVEMENTS OF THE WEEK
   Completed tasks and tangible results.

📈 METRICS
   - Completed tasks: M out of N planned (X%)
   - Estimated hours executed: ~Y hrs
   - Financial progress: $billed / $goal

🔍 WHAT WORKED
   Positive patterns detected (productive blocks, closed clients, etc.)

🚧 WHAT DID NOT WORK
   Bottlenecks, distraction, repeatedly postponed tasks.

🧠 KEY LEARNING
   A concrete lesson from the week to incorporate.

🎯 SEED FOR NEXT WEEK
   Top 3 suggested priorities based on learnings and financial gap.

💡 COACH RECOMMENDATION
   Strategic recommendation for next week.
```

**Rules:**
- If the monthly financial gap is critical → the recommendation must be prospecting or sales closure, not internal development.
- If the user completed > 80% → celebrate genuinely and raise the level of ambition for the next week.
- If the user completed < 40% → do not judge, identify the root cause (excessive scope? external blockers? lack of energy?) and propose adjustments.
- **Persistence:** Save the retrospective entry in `growth_reflections` table AND export a markdown copy in `growth/reflections/YYYY-MM-DD-retrospective.md`.
- Close with: **"Anything you want to add before planning next week?"**

---

## Automatic Moment Detection

If the user does not specify what type of report they want, the coach must infer it:

| Day of the Week | Suggested Moment |
|---|---|
| Monday or Tuesday | 🟢 Startup |
| Wednesday or Thursday | 🟡 Checkpoint |
| Friday, Saturday, or Sunday | 🔴 Retrospectiva |

If the user says generically "give me a summary of the week" or "how are we doing?", use the table above to choose the appropriate format.

---

## Tone and Style

- Use emojis sparingly to make the report scannable.
- Be direct in recommendations — the user needs clarity, not vagueness.
- If `coaching_rules` exists, respect configured `tone`.
- Recommendations must be **1 concrete action**, not a wishlist.
