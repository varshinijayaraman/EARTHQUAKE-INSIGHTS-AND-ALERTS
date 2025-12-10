@echo off
echo ================================================================================
echo Starting Earthquake Alert System - FastAPI Backend
echo ================================================================================
echo.
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

cd "%~dp0"
python backend\api.py

pause
