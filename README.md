# Coach Financiero, Vocacional & Estratega de Productividad

Este proyecto implementa un asistente inteligente de coaching diseñado para perfiles técnicos y creativos senior. Ayuda a mantener el foco radical, optimizar la gestión del tiempo y priorizar la facturación/generación de ingresos sin descuidar el bienestar personal.

---

## Beneficios Clave

* **Foco Radical:** Evita la procrastinación estructurada (como programar herramientas propias en lugar de vender).
* **Gestión Financiera Activa:** Mantiene metas claras y planifica acciones de contingencia y prospección en periodos de urgencia.
* **Aprendizaje Continuo:** Analiza de forma automática el uso del tiempo por categorías para detectar cuellos de botella.
* **Privacidad por Diseño:** La información personal y financiera permanece segura de manera local en archivos YAML y Markdown.

---

## Cómo Funciona

El coach opera de forma dinámica estructurada en tres etapas integradas:

1. **Onboarding Orgánico y Mínimo:**  
   Al arrancar por primera vez, el coach realiza tres preguntas esenciales para configurar tu perfil. Si quieres ver cómo funciona el onboarding inicial, consulta el [Skill de Inicialización](file:///home/angel/git/agents/coach/.agents/coach-init/SKILL.md).

2. **Acompañamiento Diario y Contextual:**  
   Gestiona tus proyectos, automatiza el etiquetado inteligente de tareas y estima tiempos ideales basándose en tu historial. Puedes profundizar en las reglas operativas, de contingencia e inferencia leyendo el [Skill del Coach Principal](file:///home/angel/git/agents/coach/.agents/coach/SKILL.md).

3. **Retrospectivas y Resúmenes Semanales:**  
   Entrega reportes de arranque (lunes), checkpoints de velocidad (miércoles) y cierres de semana (viernes), acumulando aprendizajes de forma continua. Conoce las plantillas y flujos en el [Skill de Resúmenes y Retrospectivas](file:///home/angel/git/agents/coach/.agents/coach-review/SKILL.md).

---

## Estructura del Workspace

* **`profile/`** — Perfil de usuario, reglas de coaching personalizadas y sistemas de diseño.
* **`projects/`** — Proyectos activos, base de tareas con estados/etiquetas e historial archivado.
* **`finances/`** — Metas mensuales, tarifas de servicios y proyecciones de facturación.
* **`growth/`** — Áreas de enfoque vocacional, checklists reutilizables y bitácora de retrospectivas.
* **`coach-notes.md`** — Archivos de memoria local que el coach actualiza de manera autónoma en cada carpeta temática para recordar patrones históricos de tu flujo de trabajo.
