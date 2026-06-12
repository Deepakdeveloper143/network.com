@echo off
echo ======================================
echo  QuantumShieldAI - Installation
echo ======================================
echo.
echo Installing Backend Dependencies...
cd /d "%~dp0"
cd backend
python -m pip install -r requirements.txt
echo.
echo Backend dependencies installed!
echo.
echo Installing Frontend Dependencies...
cd /d "%~dp0"
cd frontend
python -m pip install -r requirements.txt
echo.
echo Frontend dependencies installed!
echo.
echo ======================================
echo  Installation Complete!
echo ======================================
echo.
echo To run the application:
echo 1. Double-click: start_backend.bat
echo 2. In another terminal: start_frontend.bat
echo.
pause
