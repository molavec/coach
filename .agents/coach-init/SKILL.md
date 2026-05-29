---
name: coach-init
description: 'Onboarding inicial del coach. Se activa cuando el perfil del usuario (profile/user.yaml) no existe o está vacío. Guía una configuración mínima viable haciendo solo 3 preguntas esenciales y deja el resto para descubrimiento progresivo en conversaciones futuras.'
---

## Propósito

Este skill maneja el **primer contacto** con un usuario nuevo. El objetivo es crear una configuración mínima viable que permita al coach operar de inmediato, sin abrumar al usuario con demasiadas preguntas.

---

## Cuándo Activar

Activar este flujo **SOLO** cuando se detecte que `profile/user.yaml` no existe o está vacío (sin datos reales).

---

## Flujo de Onboarding Inicial (Máximo 3 preguntas)

### Pregunta 1: Identidad y Contexto
> "¡Hola! Soy tu coach de productividad y finanzas. Para conocerte mejor, cuéntame:
> **¿Cómo te llamas y a qué te dedicas profesionalmente?**
> (Ej: 'Soy Ana, desarrolladora frontend y diseñadora UX')"

Con la respuesta, crear `profile/user.yaml` con:
- `nombre`
- `habilidades_core` (inferidas de lo que describe)

### Pregunta 2: Meta Financiera
> "Perfecto, [nombre]. Ahora lo más importante:
> **¿Cuál es tu meta de ingresos mensuales y en qué moneda trabajas?**
> (Ej: '$2.000.000 CLP', '3.000 USD', '2.500 EUR')"

Con la respuesta, crear `finances/goals.yaml` con:
- `meta_mensual.monto`
- `meta_mensual.moneda`

### Pregunta 3: Situación Actual
> "Última pregunta para arrancar:
> **¿Tienes clientes o proyectos activos ahora, o estás partiendo de cero?**
> Si tienes, nombra los principales."

Con la respuesta:
- Si tiene proyectos → crear `projects/projects.yaml` con los mencionados
- Si parte de cero → crear `projects/projects.yaml` vacío y marcar en `finances/goals.yaml` → `notas: "Usuario sin clientes activos — priorizar prospección"`

---

## Después del Onboarding: Mensaje de Cierre

Tras las 3 preguntas, el coach debe:

1. Mostrar un resumen de lo configurado
2. Ofrecer comenzar a trabajar de inmediato
3. Mensaje modelo:

> "Listo, [nombre]. Ya tengo lo básico para funcionar. A medida que conversemos iré conociendo más sobre ti — tu rutina, tus servicios, tu estilo de trabajo — y ajustaré mi coaching.
>
> **¿En qué quieres que nos enfoquemos hoy?**"

---

## Archivos que Crea

| Archivo | Contenido Inicial |
|---|---|
| `profile/user.yaml` | Nombre y habilidades básicas |
| `finances/goals.yaml` | Meta mensual de ingresos |
| `projects/projects.yaml` | Proyectos activos (o vacío) |
| `projects/tasks.yaml` | Vacío (estructura base) |

---

## Archivos que NO Crea (Descubrimiento Progresivo)

Estos se crean más adelante, cuando surjan orgánicamente en la conversación:

| Archivo | Cuándo Crear |
|---|---|
| `profile/design-system.yaml` | Cuando el usuario mencione maquetar, diseñar o crear landings |
| `profile/coaching-rules.yaml` | Después de 2-3 sesiones, cuando el coach ya conozca los patrones del usuario |
| `finances/pricing.yaml` | Cuando el usuario mencione cotizar, cobrar o vender servicios |
| `finances/projections.yaml` | Cuando se hable de planificación financiera mensual |
| `growth/focus-areas.yaml` | Cuando se identifiquen patrones de enfoque en las conversaciones |
| `growth/checklists/*` | Cuando el usuario necesite documentar procedimientos de un proyecto |
| `growth/reflections/*` | Cuando surjan reflexiones vocacionales o de desarrollo personal |
