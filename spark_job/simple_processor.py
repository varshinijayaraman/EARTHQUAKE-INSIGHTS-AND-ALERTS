"""
Simplified Earthquake Data Processor
Processes earthquake data and trains ML model using pandas and scikit-learn
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime


def load_data(file_path):
    """Load earthquake data from CSV"""
    print("\n" + "=" * 80)
    print("EARTHQUAKE ALERT SYSTEM - Data Processor")
    print("=" * 80)
    print("\nLoading earthquake data...")
    
    df = pd.read_csv(file_path)
    print(f"Successfully loaded {len(df)} earthquake records")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst few records:")
    print(df.head())
    
    return df


def clean_and_transform(df):
    """Clean and transform data"""
    print("\nCleaning and transforming data...")
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extract timestamp features
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    
    # Add severity level based on magnitude
    df['severity'] = pd.cut(
        df['magnitude'],
        bins=[-np.inf, 4.0, 6.0, np.inf],
        labels=['Low', 'Medium', 'High']
    )
    
    # Add hazard level (target variable for ML)
    df['hazard_level'] = pd.cut(
        df['magnitude'],
        bins=[-np.inf, 4.0, 5.5, 7.0, np.inf],
        labels=[0, 1, 2, 3]
    ).astype(int)
    
    # Add depth category
    df['depth_category'] = pd.cut(
        df['depth'],
        bins=[-np.inf, 10, 30, np.inf],
        labels=['Shallow', 'Intermediate', 'Deep']
    )
    
    print(f"Data transformation complete!")
    print(f"   Total records: {len(df)}")
    
    return df


def train_ml_model(df):
    """Train Random Forest Classifier"""
    print("\nTraining Machine Learning Model...")
    print("   Model Type: Random Forest Classifier")
    
    # Prepare features
    le = LabelEncoder()
    df['region_encoded'] = le.fit_transform(df['region'])
    
    # Feature columns
    feature_cols = ['magnitude', 'depth', 'region_encoded', 'latitude', 'longitude']
    X = df[feature_cols]
    y = df['hazard_level']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"   Training set: {len(X_train)} records")
    print(f"   Test set: {len(X_test)} records")
    
    # Train model
    print("   Training in progress...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    
    print(f"Model Training Complete!")
    print(f"   Test Accuracy: {accuracy:.4f}")
    
    return model, le, feature_cols


def generate_predictions(df, model, le, feature_cols):
    """Generate predictions for all records"""
    print("\nGenerating Hazard Predictions...")
    
    # Prepare features
    df['region_encoded'] = le.transform(df['region'])
    X = df[feature_cols]
    
    # Make predictions
    df['prediction'] = model.predict(X)
    df['hazard_probability'] = model.predict_proba(X).max(axis=1)
    
    # Add alert messages
    alert_map = {
        0: "Low Risk - Monitor",
        1: "Medium Risk - Prepare",
        2: "High Risk - Alert",
        3: "Critical Risk - Evacuate"
    }
    df['alert_message'] = df['prediction'].map(alert_map)
    
    print("Predictions generated successfully!")
    
    return df


def save_results(df, output_dir):
    """Save processed data"""
    print("\nSaving Results...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Select output columns
    output_cols = [
        'sensor_id', 'timestamp', 'latitude', 'longitude',
        'magnitude', 'depth', 'region', 'severity',
        'depth_category', 'hazard_level', 'prediction',
        'hazard_probability', 'alert_message'
    ]
    
    output_df = df[output_cols].copy()
    
    # Save simple CSV
    simple_csv = os.path.join(output_dir, 'alerts_simple.csv')
    output_df.to_csv(simple_csv, index=False)
    print(f"   CSV saved to: {simple_csv}")
    
    # Save Parquet
    parquet_path = os.path.join(output_dir, 'earthquake_alerts.parquet')
    output_df.to_parquet(parquet_path, index=False)
    print(f"   Parquet saved to: {parquet_path}")
    
    # Print statistics
    print("\nStatistics:")
    print("\nSeverity Distribution:")
    print(df['severity'].value_counts())
    print("\nRegion Distribution:")
    print(df['region'].value_counts())
    
    return output_df


def save_model(model, le, model_dir):
    """Save trained model"""
    print(f"\nSaving ML Model to: {model_dir}")
    
    os.makedirs(model_dir, exist_ok=True)
    
    model_file = os.path.join(model_dir, 'random_forest_model.pkl')
    encoder_file = os.path.join(model_dir, 'label_encoder.pkl')
    
    joblib.dump(model, model_file)
    joblib.dump(le, encoder_file)
    
    print("Model saved successfully!")


def main():
    """Main execution function"""
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'earthquake_data.csv')
    output_dir = os.path.join(base_dir, 'output')
    model_dir = os.path.join(base_dir, 'models', 'sklearn_model')
    
    try:
        # Step 1: Load data
        df = load_data(data_path)
        
        # Step 2: Clean and transform
        df = clean_and_transform(df)
        
        # Step 3: Train ML model
        model, le, feature_cols = train_ml_model(df)
        
        # Step 4: Generate predictions
        df = generate_predictions(df, model, le, feature_cols)
        
        # Step 5: Save results
        output_df = save_results(df, output_dir)
        
        # Step 6: Save model
        save_model(model, le, model_dir)
        
        print("\n" + "=" * 80)
        print("🎉 Processing Complete!")
        print("=" * 80)
        print(f"\n📁 Output Location: {output_dir}")
        print(f"🤖 Model Location: {model_dir}")
        print(f"\n⚡ Next Steps:")
        print("   1. Start the FastAPI backend: python backend\\api.py")
        print("   2. Start the Streamlit frontend: streamlit run frontend\\app.py")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
