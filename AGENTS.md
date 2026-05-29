# Coach Financiero, Vocacional & Estratega de Productividad

Este proyecto implementa un coach de productividad, finanzas y desarrollo vocacional diseñado para perfiles técnicos y creativos senior. El coach ayuda a mantener el foco radical, optimizar la gestión del tiempo, evitar la procrastinación estructurada y priorizar actividades generadoras de ingresos sin descuidar el bienestar físico y mental.

## Estructura del Proyecto

```
coach/
├── profile/               # Configuración personal del usuario
│   ├── user.yaml           # Perfil (nombre, habilidades, pilar de estabilidad)
│   ├── design-system.yaml  # Sistema de diseño preferido
│   └── coaching-rules.yaml # Reglas de coaching (tono, bloques, contingencias)
│
├── projects/              # Gestión de proyectos y tareas
│   ├── projects.yaml       # Proyectos activos
│   ├── tasks.yaml          # Tareas activas
│   └── archived/           # Histórico de proyectos y tareas
│
├── finances/              # Planificación financiera
│   ├── goals.yaml          # Metas financieras y estrategia de cobro
│   ├── projections.yaml    # Proyecciones de ingresos
│   └── pricing.yaml        # Catálogo de precios de servicios
│
└── growth/                # Crecimiento vocacional y personal
    ├── focus-areas.yaml    # Áreas de enfoque actual
    ├── checklists/         # Checklists de trabajo
    └── reflections/        # Reflexiones y journaling vocacional
```

## Reglas de Gestión del Proyecto

* **Proyectos Activos:** Gestiona el listado en `./projects/projects.yaml`.
* **Tareas Activas:** Gestiona el listado en `./projects/tasks.yaml`.
* **Proyectos Archivados:** Archiva en `./projects/archived/projects.yaml`.
* **Tareas Archivadas:** Archiva por fecha en `./projects/archived/yyyy/mm/dd-tasks.yaml`.
* **Metas Financieras:** Gestiona en `./finances/goals.yaml`.
* **Proyecciones:** Actualiza en `./finances/projections.yaml`.
* **Pricing:** Mantiene el catálogo en `./finances/pricing.yaml`.
* **Áreas de Enfoque:** Actualiza en `./growth/focus-areas.yaml`.
* **Checklists:** Crea y gestiona en `./growth/checklists/`.