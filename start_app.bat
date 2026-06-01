@echo off
cd /d "%~dp0"

echo Starting Commerce Readiness AI...
echo.
python -m streamlit run app.py

pause
