#!/usr/bin/env bash
# Script de gestión del Dashboard Streamlit para Coach

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_STREAMLIT="$PROJECT_DIR/.venv/bin/streamlit"
APP_PATH="$PROJECT_DIR/dashboard/app.py"
PID_FILE="$PROJECT_DIR/.dashboard.pid"

if [ ! -f "$VENV_STREAMLIT" ]; then
    echo "❌ Error: No se encontró el entorno virtual en $PROJECT_DIR/.venv"
    echo "Por favor, crea el entorno e instala las dependencias primero."
    exit 1
fi

case "$1" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "⚠️ El dashboard ya está en ejecución (PID: $(cat "$PID_FILE"))."
            echo "🌐 URL: http://localhost:8501"
            exit 0
        fi
        echo "🚀 Iniciando Dashboard en segundo plano..."
        "$VENV_STREAMLIT" run "$APP_PATH" > /dev/null 2>&1 &
        PID=$!
        echo $PID > "$PID_FILE"
        echo "✅ Dashboard iniciado (PID: $PID)"
        echo "🌐 Disponible en: http://localhost:8501"
        ;;

    stop)
        STOPPED=0
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                kill "$PID"
                echo "🛑 Dashboard detenido (PID: $PID)."
                STOPPED=1
            fi
            rm -f "$PID_FILE"
        fi
        
        PIDS=$(pgrep -f "streamlit run.*dashboard/app.py")
        if [ -n "$PIDS" ]; then
            kill $PIDS 2>/dev/null
            echo "🛑 Procesos de Streamlit detenidos ($PIDS)."
            STOPPED=1
        fi

        if [ $STOPPED -eq 0 ]; then
            echo "ℹ️ El dashboard no estaba en ejecución."
        fi
        ;;

    status)
        if pgrep -f "streamlit run.*dashboard/app.py" > /dev/null; then
            echo "🟢 El dashboard está en ejecución."
            echo "🌐 URL: http://localhost:8501"
        else
            echo "🔴 El dashboard está detenido."
        fi
        ;;

    *)
        echo "🚀 Iniciando Dashboard en primer plano (Presiona Ctrl+C para detener)..."
        exec "$VENV_STREAMLIT" run "$APP_PATH"
        ;;
esac
