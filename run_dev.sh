#!/bin/bash

# Ruta absoluta del proyecto
PROJECT_ROOT="/Users/sultan/CGR/2025/SIGEDAPP/APPRELOADED"

# Abrir terminal para el backend
osascript <<END
tell application "Terminal"
    do script "cd $PROJECT_ROOT/backend && source venv/bin/activate && uvicorn main:app --reload"
end tell
END

# Abrir terminal para el frontend
osascript <<END
tell application "Terminal"
    do script "cd $PROJECT_ROOT/frontend && npm run dev"
end tell
END