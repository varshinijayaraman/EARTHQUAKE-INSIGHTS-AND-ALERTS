@echo off
echo ================================================================================
echo EARTHQUAKE ALERT SYSTEM - COMPLETE SETUP
echo ================================================================================
echo.
echo This will install all required dependencies for the Earthquake Alert System
echo.
pause

echo.
echo [1/3] Creating virtual environment...
python -m venv venv

echo.
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/3] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ================================================================================
echo INSTALLATION COMPLETE!
echo ================================================================================
echo.
echo Next steps:
echo 1. Run the Spark batch job: run_spark.bat
echo 2. Start the API backend: run_api.bat
echo 3. Start the frontend: run_frontend.bat
echo.
echo Or use: start_all.bat to run everything
echo.
pause
