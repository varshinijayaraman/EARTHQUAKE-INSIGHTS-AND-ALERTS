"""
PySpark Processor for Uploaded Earthquake Datasets
Processes user-uploaded earthquake data through the same Spark pipeline as the preloaded dataset
Spark Web UI available at: http://localhost:4040
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, lit, unix_timestamp, year, month, dayofmonth, hour
)
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import os
import sys
import tempfile
import pandas as pd


def create_spark_session():
    """
    Create SparkSession with Web UI enabled on port 4040
    """
    print("=" * 80)
    print("EARTHQUAKE ALERT SYSTEM - Uploaded Dataset Processor")
    print("=" * 80)
    print("\nStarting Spark Session...")
    print("Spark Web UI will be available at: http://localhost:4040\n")
    
    # Configure Spark for Java 21 compatibility with PySpark 4.0.1
    os.environ['SPARK_LOCAL_IP'] = '127.0.0.1'
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    
    spark = SparkSession.builder \
        .appName("Earthquake Alert System - Upload Processor") \
        .master("local[2]") \
        .config("spark.ui.port", "4040") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    print("Spark Session Created Successfully!")
    print(f"   Version: {spark.version}")
    print(f"   Master: {spark.sparkContext.master}")
    print(f"   App Name: {spark.sparkContext.appName}")
    print(f"   Web UI: http://localhost:4040")
    print("=" * 80 + "\n")
    
    return spark


def load_uploaded_data(spark, pandas_df):
    """
    Load uploaded earthquake data from Pandas DataFrame
    """
    print("Loading uploaded earthquake data...")
    
    try:
        # Convert Pandas DataFrame to Spark DataFrame
        df = spark.createDataFrame(pandas_df)
        
        record_count = df.count()
        print(f"Successfully loaded {record_count} earthquake records from upload")
        print(f"   Schema:")
        df.printSchema()
        
        return df
    
    except Exception as e:
        print(f"Error loading uploaded data: {str(e)}")
        sys.exit(1)


def clean_and_transform(df):
    """
    Clean data and add derived features
    """
    print("\nCleaning and transforming data...")
    
    # Remove null values
    df_clean = df.dropna()
    
    # Add timestamp features if timestamp column exists
    if "timestamp" in df_clean.columns:
        df_clean = df_clean.withColumn(
            "timestamp_unix",
            unix_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
        )
        
        df_clean = df_clean.withColumn("year", year(col("timestamp")))
        df_clean = df_clean.withColumn("month", month(col("timestamp")))
        df_clean = df_clean.withColumn("day", dayofmonth(col("timestamp")))
        df_clean = df_clean.withColumn("hour", hour(col("timestamp")))
    
    # Add severity level based on magnitude
    df_clean = df_clean.withColumn(
        "severity",
        when(col("magnitude") < 4.0, "Low")
        .when((col("magnitude") >= 4.0) & (col("magnitude") < 6.0), "Medium")
        .when(col("magnitude") >= 6.0, "High")
        .otherwise("Unknown")
    )
    
    # Add hazard level (target variable for ML)
    # 0 = Low, 1 = Medium, 2 = High, 3 = Critical
    df_clean = df_clean.withColumn(
        "hazard_level",
        when(col("magnitude") < 4.0, 0)
        .when((col("magnitude") >= 4.0) & (col("magnitude") < 5.5), 1)
        .when((col("magnitude") >= 5.5) & (col("magnitude") < 7.0), 2)
        .when(col("magnitude") >= 7.0, 3)
        .otherwise(0)
    )
    
    # Add depth category if depth column exists
    if "depth" in df_clean.columns:
        df_clean = df_clean.withColumn(
            "depth_category",
            when(col("depth") < 10, "Shallow")
            .when((col("depth") >= 10) & (col("depth") < 30), "Intermediate")
            .when(col("depth") >= 30, "Deep")
            .otherwise("Unknown")
        )
    
    print("Data transformation complete!")
    print(f"   Total records after cleaning: {df_clean.count()}")
    
    return df_clean


def feature_engineering(df):
    """
    Prepare features for machine learning
    """
    print("\nFeature Engineering...")
    
    # Check which columns are available for feature engineering
    available_features = [col for col in ["magnitude", "depth", "region", "latitude", "longitude"] if col in df.columns]
    
    if "region" in available_features:
        # Index categorical variable (region)
        region_indexer = StringIndexer(
            inputCol="region",
            outputCol="region_index",
            handleInvalid="keep"
        )
        feature_cols = [col for col in ["magnitude", "depth", "region_index", "latitude", "longitude"] if col in df.columns or col == "region_index"]
    else:
        region_indexer = None
        feature_cols = [col for col in ["magnitude", "depth", "latitude", "longitude"] if col in df.columns]
    
    # Assemble features into vector
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features"
    )
    
    print(f"Feature columns: {feature_cols}")
    
    return region_indexer, assembler, available_features


def load_existing_model(spark, model_path):
    """
    Load existing trained model
    """
    print(f"\nChecking for existing ML model at: {model_path}")
    
    # Check if model directory exists
    import os
    if not os.path.exists(model_path):
        print(f"Model directory does not exist: {model_path}")
        print("Will proceed without ML predictions.")
        return None
    
    # Check if model files exist
    model_files = [f for f in os.listdir(model_path) if os.path.isfile(os.path.join(model_path, f))]
    if not model_files:
        print(f"No model files found in directory: {model_path}")
        print("Will proceed without ML predictions.")
        return None
    
    try:
        from pyspark.ml import PipelineModel
        model = PipelineModel.load(model_path)
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        print("Will proceed without ML predictions.")
        return None


def generate_predictions(model, df):
    """
    Generate predictions for all earthquake records
    """
    print("\nGenerating Hazard Predictions for All Records...")
    
    try:
        predictions = model.transform(df)
        
        # Extract probability for highest hazard level
        from pyspark.sql.functions import udf
        from pyspark.sql.types import DoubleType
        from pyspark.ml.linalg import Vector, Vectors
        
        def get_max_prob(probability):
            if probability is not None:
                return float(max(probability))
            return 0.0
        
        max_prob_udf = udf(get_max_prob, DoubleType())
        
        predictions = predictions.withColumn(
            "hazard_probability",
            max_prob_udf(col("probability"))
        )
        
        # Add alert message
        predictions = predictions.withColumn(
            "alert_message",
            when(col("prediction") == 0, "Low Risk - Monitor")
            .when(col("prediction") == 1, "Medium Risk - Prepare")
            .when(col("prediction") == 2, "High Risk - Alert")
            .when(col("prediction") == 3, "Critical Risk - Evacuate")
            .otherwise("Unknown")
        )
        
        print("Predictions generated successfully!")
        
        return predictions
        
    except Exception as e:
        print(f"Error generating predictions: {str(e)}")
        return df  # Return original dataframe if prediction fails


def save_results(predictions, output_dir, filename_prefix="uploaded"):
    """
    Save processed alerts to CSV and Parquet
    """
    print("\nSaving Results...")
    
    # Select available columns
    available_columns = [
        "sensor_id", "timestamp", "latitude", "longitude",
        "magnitude", "depth", "region", "severity",
        "depth_category", "hazard_level", "prediction",
        "hazard_probability", "alert_message"
    ]
    
    # Filter to only columns that exist in the DataFrame
    existing_columns = [col for col in available_columns if col in predictions.columns]
    output_df = predictions.select(*existing_columns)
    
    # Convert to Pandas for easier file handling
    pandas_df = output_df.toPandas()
    
    # Handle existing file conflicts
    import shutil
    csv_path = os.path.join(output_dir, f"{filename_prefix}_earthquake_alerts.csv")
    
    # Save as CSV using pandas (more reliable on Windows)
    try:
        pandas_df.to_csv(csv_path, index=False)
        print(f"   CSV saved to: {csv_path}")
    except Exception as e:
        print(f"   Warning: Could not save CSV: {str(e)}")
    
    # Save a simple CSV for API access
    try:
        simple_csv_path = os.path.join(output_dir, f"{filename_prefix}_alerts_simple.csv")
        pandas_df.to_csv(simple_csv_path, index=False)
        print(f"   Simple CSV saved to: {simple_csv_path}")
    except Exception as e:
        print(f"   Warning: Could not save simple CSV: {str(e)}")
    
    # Show statistics using pandas (more reliable)
    print("\nGenerating Statistics...")
    
    try:
        if 'severity' in pandas_df.columns:
            print("\n   Severity Distribution:")
            severity_counts = pandas_df['severity'].value_counts()
            print(severity_counts.to_string())
        
        if 'region' in pandas_df.columns:
            print("\n   Region Distribution:")
            region_counts = pandas_df['region'].value_counts()
            print(region_counts.to_string())
    except Exception as e:
        print(f"   Warning: Could not generate statistics: {str(e)}")
    
    return pandas_df


def process_uploaded_dataset(pandas_df, base_dir):
    """
    Main function to process uploaded dataset through Spark
    """
    # Paths
    output_dir = os.path.join(base_dir, "output")
    model_dir = os.path.join(base_dir, "models", "earthquake_model")
    
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Create Spark Session
    spark = create_spark_session()
    
    try:
        # Step 2: Load Uploaded Data
        df = load_uploaded_data(spark, pandas_df)
        
        # Step 3: Clean and Transform
        df_transformed = clean_and_transform(df)
        
        # Step 4: Feature Engineering
        region_indexer, assembler, available_features = feature_engineering(df_transformed)
        
        # Step 5: Load Existing Model
        model = load_existing_model(spark, model_dir)
        
        if model:
            # Step 6: Generate Predictions
            predictions = generate_predictions(model, df_transformed)
        else:
            print("Skipping ML predictions as no trained model is available.")
            predictions = df_transformed
            
            # Add default values for missing columns that are expected by the frontend
            required_columns = ["prediction", "hazard_probability", "alert_message"]
            for col_name in required_columns:
                if col_name not in predictions.columns:
                    predictions = predictions.withColumn(col_name, lit("N/A"))
        
        # Step 7: Save Results
        output_df = save_results(predictions, output_dir, "uploaded")
        
        print("\n" + "=" * 80)
        print("EARTHQUAKE ALERT SYSTEM - Upload Processing Complete!")
        print("=" * 80)
        print(f"\nSpark Web UI is running at: http://localhost:4040")
        print(f"   View DAG, Stages, and Executors in the Web UI")
        print(f"\nOutput Location: {output_dir}")
        print("=" * 80 + "\n")
        
        return output_df
        
    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        print("\nStopping Spark Session...")
        spark.stop()
        print("Spark Session stopped. Goodbye!\n")


if __name__ == "__main__":
    # This script can be run standalone for testing
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load CSV file
        pandas_df = pd.read_csv(csv_file)
        
        # Process the dataset
        result = process_uploaded_dataset(pandas_df, base_dir)
        
        if result is not None:
            print("Processing completed successfully!")
        else:
            print("Processing failed!")
    else:
        print("Usage: python upload_processor.py <csv_file>")