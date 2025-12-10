@echo off
echo ================================================================================
echo Starting Earthquake Alert System - PySpark Batch Job
echo ================================================================================
echo.
echo Spark Web UI will be available at: http://localhost:4040
echo.

cd "%~dp0"
python spark_job\earthquake_processor.py

pause
