@echo off
echo ======================================
echo  Starting QuantumShieldAI Frontend
echo ======================================
echo.
echo Installing frontend dependencies...
cd /d "%~dp0frontend"
python -m pip install -r requirements.txt
echo.
echo Starting Streamlit app...
cd app
streamlit run main.py
pause
