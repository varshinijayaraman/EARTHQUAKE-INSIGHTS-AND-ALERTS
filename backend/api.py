"""
FastAPI Backend for Earthquake Alert System
Runs on: http://localhost:8000
Provides REST API endpoints for earthquake data and predictions
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os
import glob
from datetime import datetime
import joblib
import numpy as np


# Initialize FastAPI app
app = FastAPI(
    title="Earthquake Alert System API",
    description="REST API for earthquake monitoring and prediction",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data models
class Alert(BaseModel):
    sensor_id: str
    timestamp: str
    latitude: float
    longitude: float
    magnitude: float
    depth: float
    region: str
    severity: str
    depth_category: str
    hazard_level: int
    prediction: float
    hazard_probability: float
    alert_message: str


class PredictionRequest(BaseModel):
    magnitude: float
    depth: float
    region: str


class PredictionResponse(BaseModel):
    hazard_level: str
    hazard_score: float
    risk_indicator: str
    message: str
    input_data: dict


class Stats(BaseModel):
    total_earthquakes: int
    avg_magnitude: float
    max_magnitude: float
    avg_depth: float
    severity_distribution: dict
    region_distribution: dict


# Global variable to store data
alerts_data = None


def load_alerts_data():
    """
    Load processed earthquake alerts from output directory
    """
    global alerts_data
    
    try:
        # Get the output directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "output")
        
        # First try to load the simple CSV (single file)
        simple_csv = os.path.join(output_dir, "alerts_simple.csv")
        if os.path.exists(simple_csv):
            df = pd.read_csv(simple_csv)
            print(f"✅ Loaded {len(df)} earthquake alerts from {simple_csv}")
            return df
        
        # Otherwise try to find CSV files in the earthquake_alerts.csv directory
        csv_dir = os.path.join(output_dir, "earthquake_alerts.csv")
        if os.path.exists(csv_dir):
            csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
            
            if csv_files:
                # Read the first CSV file found
                df = pd.read_csv(csv_files[0])
                print(f"✅ Loaded {len(df)} earthquake alerts from {csv_files[0]}")
                return df
        
        print(f"⚠️ No CSV files found in {output_dir}")
        return None
    
    except Exception as e:
        print(f"❌ Error loading alerts data: {str(e)}")
        return None


def get_hazard_prediction(magnitude: float, depth: float, region: str):
    """
    Simple rule-based prediction (since PySpark model requires Spark context)
    In production, you would load the actual model or use a REST API to Spark
    """
    # Rule-based prediction logic
    if magnitude < 4.0:
        hazard_level = 0
        level_name = "Low"
        message = "Low Risk - Continue monitoring"
    elif 4.0 <= magnitude < 5.5:
        hazard_level = 1
        level_name = "Medium"
        message = "Medium Risk - Stay prepared"
    elif 5.5 <= magnitude < 7.0:
        hazard_level = 2
        level_name = "High"
        message = "High Risk - Alert issued"
    else:
        hazard_level = 3
        level_name = "Critical"
        message = "Critical Risk - Immediate action required"
    
    # Adjust based on depth
    if depth > 30:
        hazard_score = hazard_level * 0.8  # Deep earthquakes are less dangerous
    elif depth < 10:
        hazard_score = min(hazard_level * 1.2, 3)  # Shallow earthquakes are more dangerous
    else:
        hazard_score = hazard_level
    
    # Normalize to probability (0-1)
    hazard_probability = min(hazard_score / 3.0, 1.0)
    
    # Risk indicator color
    if hazard_probability < 0.25:
        risk_indicator = "green"
    elif hazard_probability < 0.5:
        risk_indicator = "yellow"
    elif hazard_probability < 0.75:
        risk_indicator = "orange"
    else:
        risk_indicator = "red"
    
    return {
        "hazard_level": level_name,
        "hazard_score": round(hazard_probability, 3),
        "risk_indicator": risk_indicator,
        "message": message,
        "input_data": {
            "magnitude": magnitude,
            "depth": depth,
            "region": region
        }
    }


@app.on_event("startup")
async def startup_event():
    """
    Load data on startup
    """
    global alerts_data
    
    print("\n" + "=" * 80)
    print("🚀 Starting Earthquake Alert System API")
    print("=" * 80)
    
    alerts_data = load_alerts_data()
    
    if alerts_data is None:
        print("⚠️ Warning: No alerts data loaded. Some endpoints may not work.")
    
    print(f"\n📡 API Server running at: http://localhost:8000")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"📖 ReDoc Documentation: http://localhost:8000/redoc")
    print("=" * 80 + "\n")


@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "Earthquake Alert System API",
        "version": "1.0.0",
        "endpoints": {
            "/alerts": "Get all earthquake alerts",
            "/stats": "Get summary statistics",
            "/predict": "Predict hazard level",
            "/regions": "Get list of regions",
            "/docs": "API documentation"
        },
        "status": "running",
        "spark_ui": "http://localhost:4040",
        "frontend": "http://localhost:8501"
    }


@app.get("/alerts", response_model=List[Alert])
async def get_alerts(
    region: Optional[str] = Query(None, description="Filter by region"),
    min_magnitude: Optional[float] = Query(None, description="Minimum magnitude"),
    max_magnitude: Optional[float] = Query(None, description="Maximum magnitude"),
    severity: Optional[str] = Query(None, description="Filter by severity (Low/Medium/High)"),
    limit: int = Query(100, description="Maximum number of results")
):
    """
    Get earthquake alerts with optional filters
    """
    if alerts_data is None:
        raise HTTPException(status_code=503, detail="Alerts data not available")
    
    df = alerts_data.copy()
    
    # Apply filters
    if region:
        df = df[df['region'].str.contains(region, case=False, na=False)]
    
    if min_magnitude is not None:
        df = df[df['magnitude'] >= min_magnitude]
    
    if max_magnitude is not None:
        df = df[df['magnitude'] <= max_magnitude]
    
    if severity:
        df = df[df['severity'].str.lower() == severity.lower()]
    
    # Limit results
    df = df.head(limit)
    
    # Convert to list of dictionaries
    alerts = df.to_dict('records')
    
    return alerts


@app.get("/stats", response_model=Stats)
async def get_stats():
    """
    Get summary statistics
    """
    if alerts_data is None:
        raise HTTPException(status_code=503, detail="Alerts data not available")
    
    df = alerts_data
    
    # Calculate statistics
    stats = {
        "total_earthquakes": int(len(df)),
        "avg_magnitude": float(df['magnitude'].mean()),
        "max_magnitude": float(df['magnitude'].max()),
        "avg_depth": float(df['depth'].mean()),
        "severity_distribution": df['severity'].value_counts().to_dict(),
        "region_distribution": df['region'].value_counts().to_dict()
    }
    
    return stats


@app.get("/predict", response_model=PredictionResponse)
async def predict(
    magnitude: float = Query(..., description="Earthquake magnitude (e.g., 5.2)", ge=0, le=10),
    depth: float = Query(..., description="Earthquake depth in km (e.g., 10)", ge=0, le=700),
    region: str = Query(..., description="Region name (e.g., Japan, California)")
):
    """
    Predict hazard level based on earthquake parameters
    
    Example: /predict?magnitude=5.2&depth=10&region=Japan
    """
    try:
        prediction = get_hazard_prediction(magnitude, depth, region)
        return prediction
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/regions")
async def get_regions():
    """
    Get list of unique regions
    """
    if alerts_data is None:
        raise HTTPException(status_code=503, detail="Alerts data not available")
    
    regions = sorted(alerts_data['region'].unique().tolist())
    
    return {
        "regions": regions,
        "count": len(regions)
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_loaded": alerts_data is not None,
        "records": len(alerts_data) if alerts_data is not None else 0
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 80)
    print("🌍 EARTHQUAKE ALERT SYSTEM - FastAPI Backend")
    print("=" * 80)
    print("\n🚀 Starting server on http://localhost:8000")
    print("📚 API Docs available at http://localhost:8000/docs\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
