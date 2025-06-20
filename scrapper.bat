@echo off
REM ─── Make sure we’re in the folder where this .bat lives ───
cd /d "%~dp0"

echo 🔧 Activating Python virtual environment…
call "venv\Scripts\activate.bat"

echo 🚀 Starting FastAPI backend (minimized)…
start "FastAPI Server" /min cmd /k ^
  "call \"%~dp0venv\Scripts\activate.bat\" && ^
   cd /d \"%~dp0app\" && ^
   python -m uvicorn app.fastapi_server:app --reload"

timeout /t 2 >nul

echo 🌐 Starting React frontend (minimized)…
start "React App" /min cmd /k ^
  "cd /d \"%~dp0metal-scraper-frontend\" && ^
   npm start"
