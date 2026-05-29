---
name: coach-review
description: 'Resúmenes semanales y retrospectiva. Genera una visión general al inicio de semana (planificación), un checkpoint a mitad de semana (ajuste de rumbo) y una retrospectiva al cierre (aprendizajes y replanificación). Se activa cuando el usuario pida un resumen semanal, planificación de semana, retrospectiva, o el coach detecte que es lunes/miércoles/viernes.'
---

## Propósito

Darle al usuario una visión panorámica y accionable de su semana en 3 momentos clave, con recomendaciones enfocadas en maximizar resultados y ajustar rumbo rápidamente.

---

## Fuentes de Datos

Antes de generar cualquier reporte, el agente debe leer:

1. **`projects/tasks.yaml`** — Tareas activas, estados y tiempos estimados
2. **`projects/projects.yaml`** — Proyectos activos y prioridades
3. **`finances/goals.yaml`** — Meta financiera mensual
4. **`finances/projections.yaml`** — Proyecciones del mes en curso
5. **`growth/focus-areas.yaml`** — Áreas de enfoque activas
6. **`profile/user.yaml`** — Contexto del usuario
7. **`profile/coaching-rules.yaml`** *(si existe)* — Reglas y bloques horarios

---

## Los 3 Momentos de la Semana

### 🟢 1. Inicio de Semana — "Arranque" (Lunes o primera sesión de la semana)

**Objetivo:** Claridad total sobre qué atacar esta semana.

**Estructura del reporte:**

```
📅 ARRANQUE DE SEMANA — [fecha inicio] al [fecha fin]

🎯 FOCO DE LA SEMANA
   Top 3 prioridades ordenadas por impacto en la meta financiera.

💰 PANORAMA FINANCIERO
   - Meta mensual: $X
   - Facturado este mes: $Y
   - Brecha: $Z
   - Días restantes del mes: N

📋 TAREAS CRÍTICAS (máx. 5)
   Las tareas que mueven la aguja esta semana, con tiempo estimado total.

⚠️ ALERTAS
   - Proyectos en riesgo o con entregables próximos
   - Clientes que requieren seguimiento

💡 RECOMENDACIÓN DEL COACH
   Una recomendación estratégica concreta basada en la situación actual.
```

**Reglas:**
- Si la brecha financiera es > 50% de la meta y quedan < 15 días del mes → activar modo urgencia: reordenar prioridades poniendo prospección comercial primero.
- Si hay tareas completadas de la semana anterior, reconocerlas brevemente ("La semana pasada cerraste X — buen momentum").
- Cerrar con: **"¿Ajustamos algo o arrancamos con esto?"**

---

### 🟡 2. Mitad de Semana — "Checkpoint" (Miércoles o tercera sesión)

**Objetivo:** Ajuste de rumbo antes de que sea tarde.

**Estructura del reporte:**

```
🔄 CHECKPOINT MITAD DE SEMANA — [fecha]

✅ AVANCE
   Tareas completadas desde el arranque (con ✅).
   Tareas en progreso (con 🔄).

❌ BLOQUEADO O SIN AVANCE
   Tareas sin movimiento y posible causa.

📊 VELOCIDAD
   - Tareas planificadas: N
   - Completadas: M
   - Ritmo: [en track / retrasado / adelantado]

🔀 AJUSTES SUGERIDOS
   Si está retrasado:
   - Qué eliminar o posponer
   - Qué reasignar o simplificar
   Si está adelantado:
   - Qué tarea de alto impacto agregar

💡 RECOMENDACIÓN DEL COACH
   Intervención táctica para el resto de la semana.
```

**Reglas:**
- Si completó < 30% de las tareas planificadas → sugerir reducir scope y proteger las 2 tareas de mayor impacto financiero.
- Si completó > 70% → felicitar y sugerir adelantar tareas de la siguiente semana o invertir en prospección.
- Cerrar con: **"¿Qué necesitas ajustar para cerrar fuerte la semana?"**

---

### 🔴 3. Fin de Semana — "Retrospectiva" (Viernes o última sesión)

**Objetivo:** Aprender, celebrar y replanificar.

**Estructura del reporte:**

```
📊 RETROSPECTIVA SEMANAL — [fecha inicio] al [fecha fin]

🏆 LOGROS DE LA SEMANA
   Tareas completadas y resultados tangibles.

📈 MÉTRICAS
   - Tareas completadas: M de N planificadas (X%)
   - Horas estimadas ejecutadas: ~Y hrs
   - Avance financiero: $facturado / $meta

🔍 QUÉ FUNCIONÓ
   Patrones positivos detectados (bloques productivos, clientes cerrados, etc.)

🚧 QUÉ NO FUNCIONÓ
   Bloqueos, dispersión, tareas postergadas repetidamente.

🧠 APRENDIZAJE CLAVE
   Una lección concreta de la semana para incorporar.

🎯 SEMILLA PARA LA PRÓXIMA SEMANA
   Top 3 prioridades sugeridas basadas en lo aprendido y la brecha financiera.

💡 RECOMENDACIÓN DEL COACH
   Recomendación estratégica para la siguiente semana.
```

**Reglas:**
- Si la brecha financiera mensual es crítica → la recomendación debe ser de prospección o cierre de ventas, no de desarrollo interno.
- Si el usuario completó > 80% → celebrar genuinamente y subir el nivel de ambición para la siguiente semana.
- Si el usuario completó < 40% → no juzgar, identificar la causa raíz (¿scope excesivo? ¿bloqueos externos? ¿falta de energía?) y proponer ajustes.
- Guardar la retrospectiva en `growth/reflections/[fecha]-retrospectiva.md` para registro histórico.
- Cerrar con: **"¿Algo que quieras agregar antes de planificar la próxima semana?"**

---

## Detección Automática del Momento

Si el usuario no especifica qué tipo de reporte quiere, el coach debe inferirlo:

| Día de la semana | Momento sugerido |
|---|---|
| Lunes o Martes | 🟢 Arranque |
| Miércoles o Jueves | 🟡 Checkpoint |
| Viernes, Sábado o Domingo | 🔴 Retrospectiva |

Si el usuario dice genéricamente "hazme un resumen de la semana" o "¿cómo vamos?", usar la tabla anterior para elegir el formato apropiado.

---

## Tono y Estilo

- Usar emojis con moderación para hacer el reporte escaneable.
- Ser directo en las recomendaciones — el usuario necesita claridad, no vaguedades.
- Si existe `profile/coaching-rules.yaml`, respetar el tono configurado.
- Las recomendaciones deben ser **1 acción concreta**, no una lista de deseos.
