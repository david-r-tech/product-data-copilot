@echo off
cd /d "%~dp0"

echo Starting Product Data Copilot...
echo.
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m streamlit run app.py
) else (
    python -m streamlit run app.py
)

pause
