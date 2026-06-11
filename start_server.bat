@echo off
cd /d "%~dp0backend"
set PYTHONIOENCODING=utf-8
echo [info] Starting Private Kitchen Assistant backend...
echo [info] Open frontend/index.html in browser after server starts
D:\leidian\python\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause
