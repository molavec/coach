---
name: coach-init
description: 'Initial onboarding for the coach. Activates when the user profile (profile/user.yaml) does not exist or is empty. Guides a minimum viable setup by asking only 3 essential questions and leaves the rest for progressive discovery in future conversations.'
---

## Purpose

This skill handles the **first contact** with a new user. The goal is to create a minimum viable setup that allows the coach to operate immediately, without overwhelming the user with too many questions.

---

## When to Activate

Activate this flow **ONLY** when `profile/user.yaml` does not exist or is empty (contains no real data).

---

## Initial Onboarding Flow (Maximum 3 questions)

### Question 1: Identity and Context
> "Hello! I am your productivity and financial coach. To get to know you better, tell me:
> **What is your name and what do you do professionally?**
> (E.g., 'I'm Ana, a frontend developer and UX designer')"

Based on the response, create `profile/user.yaml` with:
- `name`
- `core_skills` (inferred from description)

### Question 2: Financial Goal
> "Great, [name]. Now, the most important part:
> **What is your monthly income goal and what currency do you work with?**
> (E.g., '$2,000,000 CLP', '3,000 USD', '2,500 EUR')"

Based on the response, create `finances/goals.yaml` with:
- `monthly_goal.amount`
- `monthly_goal.currency`

### Question 3: Current Situation
> "One last question to get started:
> **Do you have active clients or projects right now, or are you starting from scratch?**
> If you do, please name the main ones."

Based on the response:
- If they have projects → create `projects/projects.yaml` with the mentioned ones.
- If they start from scratch → create an empty `projects/projects.yaml` and mark in `finances/goals.yaml` → `notes: "User without active clients — prioritize prospecting"`.

---

## After Onboarding: Wrap-up Message

After the 3 questions, the coach should:

1. Display a summary of the configuration.
2. Offer to start working immediately.
3. Template message:

> "Done, [name]. I have the basics to start working. As we talk, I'll learn more about you — your routine, your services, your working style — and adjust my coaching accordingly.
>
> **What would you like us to focus on today?**"

---

## Files Created

| File | Initial Content |
|---|---|
| `profile/user.yaml` | Name and core skills |
| `finances/goals.yaml` | Monthly income goal |
| `projects/projects.yaml` | Active projects (or empty) |
| `projects/tasks.yaml` | Empty (base structure) |

---

## Files NOT Created (Progressive Discovery)

These are created later, when they arise organically in conversation:

| File | When to Create |
|---|---|
| `profile/design-system.yaml` | When the user mentions layouts, design, or landing pages |
| `profile/coaching-rules.yaml` | After 2-3 sessions, once the coach identifies the user's patterns |
| `finances/pricing.yaml` | When the user mentions quoting, charging, or selling services |
| `finances/projections.yaml` | When discussing monthly financial planning |
| `growth/focus-areas.yaml` | When focus patterns are identified in conversations |
| `growth/checklists/*` | When the user needs to document SOPs for a project |
| `growth/reflections/*` | When vocational reflections or personal development moments occur |
