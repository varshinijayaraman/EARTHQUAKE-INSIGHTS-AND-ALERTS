@echo off
echo ================================================================================
echo Starting Earthquake Alert System - Streamlit Frontend
echo ================================================================================
echo.
echo Dashboard will be available at: http://localhost:8501
echo.

cd "%~dp0"
streamlit run frontend\app.py

pause
