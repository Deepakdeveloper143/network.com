@echo off
echo ======================================
echo  Starting QuantumShieldAI Backend
echo ======================================
echo.
echo Installing backend dependencies...
cd /d "%~dp0backend"
python -m pip install -r requirements.txt
echo.
echo Starting FastAPI server...
python -m app.main
pause
