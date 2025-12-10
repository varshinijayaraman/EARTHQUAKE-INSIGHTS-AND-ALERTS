"""
PySpark Batch Job for Earthquake Alert System
Processes earthquake data, trains ML model, generates predictions
Spark Web UI available at: http://localhost:4040
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, lit, unix_timestamp, year, month, dayofmonth, hour
)
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier, GBTClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import os
import sys


def create_spark_session():
    """
    Create SparkSession with Web UI enabled on port 4040
    """
    print("=" * 80)
    print("EARTHQUAKE ALERT SYSTEM - PySpark Batch Processor")
    print("=" * 80)
    print("\nStarting Spark Session...")
    print("Spark Web UI will be available at: http://localhost:4040\n")
    
    # Configure Spark for Java 21 compatibility with PySpark 4.0.1
    import os
    import sys
    os.environ['SPARK_LOCAL_IP'] = '127.0.0.1'
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    
    spark = SparkSession.builder \
        .appName("Earthquake Alert System") \
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


def load_data(spark, data_path):
    """
    Load earthquake data from CSV
    """
    print("Loading earthquake data from CSV...")
    
    try:
        df = spark.read.csv(
            data_path,
            header=True,
            inferSchema=True
        )
        
        record_count = df.count()
        print(f"Successfully loaded {record_count} earthquake records")
        print(f"   Schema:")
        df.printSchema()
        
        return df
    
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        sys.exit(1)


def clean_and_transform(df):
    """
    Clean data and add derived features
    """
    print("\nCleaning and transforming data...")
    
    # Remove null values
    df_clean = df.dropna()
    
    # Add timestamp features
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
    
    # Add depth category
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
    
    # Index categorical variable (region)
    region_indexer = StringIndexer(
        inputCol="region",
        outputCol="region_index",
        handleInvalid="keep"
    )
    
    # Assemble features into vector
    feature_cols = ["magnitude", "depth", "region_index", "latitude", "longitude"]
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features"
    )
    
    print(f"Feature columns: {feature_cols}")
    
    return region_indexer, assembler


def train_ml_model(df, region_indexer, assembler):
    """
    Train Random Forest Classifier for hazard prediction
    """
    print("\nTraining Machine Learning Model...")
    print("   Model Type: Random Forest Classifier")
    
    # Split data
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    
    print(f"   Training set: {train_df.count()} records")
    print(f"   Test set: {test_df.count()} records")
    
    # Create Random Forest Classifier
    rf = RandomForestClassifier(
        featuresCol="features",
        labelCol="hazard_level",
        numTrees=100,
        maxDepth=10,
        seed=42
    )
    
    # Create pipeline
    pipeline = Pipeline(stages=[region_indexer, assembler, rf])
    
    # Train model
    print("   Training in progress...")
    model = pipeline.fit(train_df)
    
    # Make predictions on test set
    predictions = model.transform(test_df)
    
    # Evaluate model
    evaluator = MulticlassClassificationEvaluator(
        labelCol="hazard_level",
        predictionCol="prediction",
        metricName="accuracy"
    )
    
    accuracy = evaluator.evaluate(predictions)
    
    print(f"Model Training Complete!")
    print(f"   Test Accuracy: {accuracy:.4f}")
    
    # Show sample predictions
    print("\n   Sample Predictions:")
    predictions.select(
        "sensor_id", "magnitude", "depth", "region",
        "hazard_level", "prediction", "probability"
    ).show(5, truncate=False)
    
    return model, accuracy


def generate_predictions(model, df):
    """
    Generate predictions for all earthquake records
    """
    print("\nGenerating Hazard Predictions for All Records...")
    
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
    
    print("✅ Predictions generated successfully!")
    
    return predictions


def save_results(predictions, output_dir):
    """
    Save processed alerts to CSV and Parquet
    """
    print("\nSaving Results...")
    
    # Select relevant columns
    output_df = predictions.select(
        "sensor_id", "timestamp", "latitude", "longitude",
        "magnitude", "depth", "region", "severity",
        "depth_category", "hazard_level", "prediction",
        "hazard_probability", "alert_message"
    )
    
    # Convert to Pandas for easier file handling
    pandas_df = output_df.toPandas()
    
    # Handle existing directory conflicts
    import shutil
    csv_path = os.path.join(output_dir, "earthquake_alerts.csv")
    
    # Remove existing directory if it exists
    if os.path.isdir(csv_path):
        try:
            shutil.rmtree(csv_path)
            print(f"   Removed existing directory: {csv_path}")
        except Exception as e:
            print(f"   Warning: Could not remove existing directory: {str(e)}")
    
    # Save as CSV using pandas (more reliable on Windows)
    try:
        pandas_df.to_csv(csv_path, index=False)
        print(f"   CSV saved to: {csv_path}")
    except Exception as e:
        print(f"   Warning: Could not save CSV: {str(e)}")
    
    # Save as Parquet if possible
    try:
        parquet_path = os.path.join(output_dir, "earthquake_alerts.parquet")
        output_df.write.mode("overwrite").parquet(parquet_path)
        print(f"   Parquet saved to: {parquet_path}")
    except Exception as e:
        print(f"   Warning: Could not save Parquet: {str(e)}")
    
    # Save a simple CSV for API access
    try:
        simple_csv_path = os.path.join(output_dir, "alerts_simple.csv")
        pandas_df.to_csv(simple_csv_path, index=False)
        print(f"   Simple CSV saved to: {simple_csv_path}")
    except Exception as e:
        print(f"   Warning: Could not save simple CSV: {str(e)}")
    
    # Show statistics using pandas (more reliable)
    print("\nGenerating Statistics...")
    
    try:
        print("\n   Severity Distribution:")
        severity_counts = pandas_df['severity'].value_counts()
        print(severity_counts.to_string())
        
        print("\n   Region Distribution:")
        region_counts = pandas_df['region'].value_counts()
        print(region_counts.to_string())
    except Exception as e:
        print(f"   Warning: Could not generate statistics: {str(e)}")
    
    return output_df


def save_model(model, model_path):
    """
    Save trained ML model
    """
    print(f"\nSaving ML Model to: {model_path}")
    
    try:
        model.write().overwrite().save(model_path)
        print("Model saved successfully!")
    except Exception as e:
        print(f"Warning: Could not save model: {str(e)}")


def main():
    """
    Main execution function
    """
    # Get base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "earthquake_data.csv")
    output_dir = os.path.join(base_dir, "output")
    model_dir = os.path.join(base_dir, "models", "earthquake_model")
    
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(model_dir), exist_ok=True)
    
    # Step 1: Create Spark Session
    spark = create_spark_session()
    
    try:
        # Step 2: Load Data
        df = load_data(spark, data_path)
        
        # Step 3: Clean and Transform
        df_transformed = clean_and_transform(df)
        
        # Step 4: Feature Engineering
        region_indexer, assembler = feature_engineering(df_transformed)
        
        # Step 5: Train ML Model
        model, accuracy = train_ml_model(df_transformed, region_indexer, assembler)
        
        # Step 6: Generate Predictions
        predictions = generate_predictions(model, df_transformed)
        
        # Step 7: Save Results
        output_df = save_results(predictions, output_dir)
        
        # Step 8: Save Model
        save_model(model, model_dir)
        
        print("\n" + "=" * 80)
        print("EARTHQUAKE ALERT SYSTEM - Processing Complete!")
        print("=" * 80)
        print(f"\nSpark Web UI is running at: http://localhost:4040")
        print(f"   View DAG, Stages, and Executors in the Web UI")
        print(f"\nOutput Location: {output_dir}")
        print(f"Model Location: {model_dir}")
        print(f"Model Accuracy: {accuracy:.4f}")
        print("\nNext Steps:")
        print("   1. Open http://localhost:4040 in your browser")
        print("   2. Start the FastAPI backend: python backend/api.py")
        print("   3. Start the Streamlit frontend: streamlit run frontend/app.py")
        print("=" * 80 + "\n")
        
        # Keep Spark UI running
        print("Press Ctrl+C to stop Spark and close Web UI...")
        spark.sparkContext.setJobDescription("Earthquake Alert System - Job Complete")
        
        # Wait for user to view Spark UI
        input("\nPress Enter after viewing Spark Web UI to exit...\n")
        
    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\nStopping Spark Session...")
        spark.stop()
        print("Spark Session stopped. Goodbye!\n")


if __name__ == "__main__":
    main()
