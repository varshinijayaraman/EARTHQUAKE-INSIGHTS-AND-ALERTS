@echo off
echo ================================================================================
echo Starting Earthquake Alert System - Compatibility Data Processor
echo ================================================================================
echo Processing earthquake data using pandas and scikit-learn...
echo Spark Web UI will NOT be available with this processor, but all data will be processed.
echo ================================================================================

python spark_job\compatibility_processor.py

echo.
echo ================================================================================
echo Processing Complete!
echo ================================================================================
echo To start the web interface:
echo   1. Start the FastAPI backend: run_api.bat
echo   2. Start the Streamlit frontend: run_frontend.bat
echo ================================================================================
pause