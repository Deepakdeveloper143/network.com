@echo off
echo ======================================
echo  QuantumShieldAI - Simple Install & Run
echo ======================================
echo.
echo This script will install and run the app with minimal dependencies!
echo.
pause

echo.
echo ======================================
echo  Installing Backend Dependencies...
echo ======================================
cd /d "%~dp0backend"
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn python-multipart python-dotenv groq requests pillow cryptography
if %ERRORLEVEL% NEQ 0 (
    echo Error installing backend dependencies!
    pause
    exit /b 1
)

echo.
echo ======================================
echo  Installing Frontend Dependencies...
echo ======================================
cd /d "%~dp0frontend"
python -m pip install --upgrade pip
python -m pip install streamlit requests plotly pillow
if %ERRORLEVEL% NEQ 0 (
    echo Error installing frontend dependencies!
    pause
    exit /b 1
)

echo.
echo ======================================
echo  Starting Backend Server...
echo ======================================
echo The backend will run in this window.
echo.
echo Open a NEW terminal and run: SIMPLE_START_FRONTEND.bat
echo.
cd /d "%~dp0backend"
python -m app.main
pause
