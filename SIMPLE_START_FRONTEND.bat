@echo off
echo ======================================
echo  Starting QuantumShieldAI Frontend
echo ======================================
echo.
cd /d "%~dp0frontend\app"
streamlit run main.py
pause
