@echo off
echo 🔧 Activating Python virtual environment...
call metal-scraper\venv\Scripts\activate

echo 🚀 Starting FastAPI backend (minimized)...
start "FastAPI Server" /min cmd /k "cd /d %CD%\metal-scraper && uvicorn fastapi_server:app --reload"

timeout /t 2 >nul

echo 🌐 Starting React frontend (minimized)...
start "React App" /min cmd /k "cd /d %CD%\metal-scraper-frontend && npm start"
