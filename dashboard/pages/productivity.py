import streamlit as st
from utils.db import load_projects_and_tasks
from components.kpis import render_task_kpis
from components.charts import plot_tasks_status

projects_df, tasks_df = load_projects_and_tasks()

total_tasks = len(tasks_df) if not tasks_df.empty else 0
completed_tasks = len(tasks_df[tasks_df['status'] == 'Completado']) if not tasks_df.empty else 0
in_progress_tasks = len(tasks_df[tasks_df['status'] == 'En Progreso']) if not tasks_df.empty else 0
pending_tasks = total_tasks - completed_tasks - in_progress_tasks

render_task_kpis(total_tasks, completed_tasks, in_progress_tasks, pending_tasks)
st.divider()

c1, c2 = st.columns([6, 6])
with c1:
    st.plotly_chart(plot_tasks_status(tasks_df), use_container_width=True)
with c2:
    st.subheader("🚀 Proyectos Activos")
    if not projects_df.empty:
        st.dataframe(
            projects_df[['id', 'name', 'priority', 'status']],
            column_config={
                'id': 'ID',
                'name': 'Proyecto',
                'priority': 'Prioridad',
                'status': 'Estado'
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay proyectos activos registrados.")

st.divider()
st.subheader("📋 Lista de Tareas Recientes")
if not tasks_df.empty:
    st.dataframe(
        tasks_df[['title', 'project_name', 'priority', 'status', 'estimated_time', 'actual_time']],
        column_config={
            'title': 'Título Tarea',
            'project_name': 'Proyecto',
            'priority': 'Prioridad',
            'status': 'Estado',
            'estimated_time': 'Tiempo Est.',
            'actual_time': 'Tiempo Real'
        },
        use_container_width=True,
        hide_index=True
    )
