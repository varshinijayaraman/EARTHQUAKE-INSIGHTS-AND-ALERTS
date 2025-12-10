from pyspark.sql import SparkSession
import os
import sys

# Set environment variables for Java 21 compatibility
os.environ['SPARK_LOCAL_IP'] = '127.0.0.1'
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

try:
    print("Creating Spark session...")
    import sys
    python_executable = sys.executable
    # On Windows, we need to ensure we're using the correct Python executable
    if 'python.exe' in python_executable:
        python_executable = python_executable.replace('python.exe', 'python.exe')
    else:
        python_executable = 'python'
    
    spark = SparkSession.builder \
        .appName("Test Spark Session") \
        .master("local[2]") \
        .config("spark.ui.port", "4040") \
        .getOrCreate()
    
    print("Spark session created successfully!")
    print(f"Spark version: {spark.version}")
    print(f"Web UI: http://localhost:4040")
    
    # Create a simple DataFrame to test
    data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    columns = ["Name", "Age"]
    df = spark.createDataFrame(data, columns)
    
    print("Sample DataFrame:")
    df.show()
    
    input("Press Enter to stop Spark session...")
    
    spark.stop()
    print("Spark session stopped.")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()