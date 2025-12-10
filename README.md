# 🌍 Earthquake Alert System (Localhost Version)

A complete end-to-end earthquake monitoring, analysis, and prediction system running entirely on localhost using **PySpark**, **PySpark MLlib**, **FastAPI**, and **Streamlit**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Spark Web UI](#spark-web-ui)
- [Sample Dataset](#sample-dataset)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The **Earthquake Alert System** processes historical seismic data using PySpark in batch mode, generates alerts, visualizes earthquake patterns, maps risk zones, and predicts hazard levels using a Random Forest machine learning model.

### Problem Statement

Process historical seismic data to:
- Generate real-time earthquake alerts
- Visualize earthquake patterns and trends
- Map geographic risk zones
- Predict hazard levels using machine learning
- Provide disaster analysis and early warning research capabilities

### Use Case

Disaster analysis, seismic monitoring, and early warning research.

---

## ✨ Features

### 1️⃣ PySpark Batch Processing
- ✅ Reads CSV/JSON earthquake data
- ✅ Cleans and transforms data
- ✅ Adds severity levels and hazard classifications
- ✅ Feature engineering for ML
- ✅ Trains PySpark MLlib Random Forest model
- ✅ Generates hazard predictions
- ✅ Saves processed alerts (CSV/Parquet)
- ✅ **Spark Web UI at http://localhost:4040** with DAG visualization

### 2️⃣ Machine Learning Prediction
- ✅ PySpark MLlib RandomForestClassifier
- ✅ Inputs: magnitude, depth, region
- ✅ Outputs: hazard level (0-3) and probability
- ✅ API endpoint for real-time predictions

### 3️⃣ FastAPI Backend
- ✅ Runs at **http://localhost:8000**
- ✅ REST API endpoints for alerts, stats, predictions
- ✅ Auto-generated API documentation
- ✅ CORS enabled for frontend integration

### 4️⃣ Streamlit Frontend
- ✅ Runs at **http://localhost:8501**
- ✅ Interactive dashboard with filters
- ✅ Multiple visualization charts (Plotly)
- ✅ Risk-zone map with GPS markers (Folium)
- ✅ Heatmap visualization
- ✅ ML prediction interface
- ✅ Spark Web UI access button

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  EARTHQUAKE ALERT SYSTEM                     │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  CSV/JSON Data   │
│  (earthquake_    │
│   data.csv)      │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│     PySpark Batch Job                     │
│  ┌─────────────────────────────────┐     │
│  │ 1. Data Loading & Cleaning      │     │
│  │ 2. Feature Engineering          │     │
│  │ 3. MLlib Model Training         │     │
│  │ 4. Hazard Prediction            │     │
│  │ 5. Save Results (CSV/Parquet)   │     │
│  └─────────────────────────────────┘     │
│                                           │
│  Spark Web UI: http://localhost:4040     │
└────────┬──────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  Output Files                             │
│  - earthquake_alerts.csv                  │
│  - earthquake_alerts.parquet              │
│  - earthquake_model/ (trained model)      │
└────────┬──────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  FastAPI Backend                          │
│  http://localhost:8000                    │
│                                           │
│  Endpoints:                               │
│  - GET /alerts                            │
│  - GET /stats                             │
│  - GET /predict                           │
│  - GET /regions                           │
└────────┬──────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  Streamlit Frontend                       │
│  http://localhost:8501                    │
│                                           │
│  Pages:                                   │
│  - 📊 Dashboard (Charts & Filters)        │
│  - 🗺️ Risk Map (Folium + Markers)        │
│  - 🔮 Prediction (ML Interface)          │
│  - ⚡ Spark Web UI Link                  │
└───────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
earthquake_alert_system/
│
├── data/
│   └── earthquake_data.csv          # Sample earthquake dataset (30 records)
│
├── spark_job/
│   └── earthquake_processor.py      # PySpark batch processing job
│
├── backend/
│   └── api.py                       # FastAPI backend server
│
├── frontend/
│   └── app.py                       # Streamlit multi-page dashboard
│
├── models/
│   └── earthquake_model/            # Trained PySpark MLlib model (auto-generated)
│
├── output/
│   ├── earthquake_alerts.csv/       # Processed alerts in CSV format
│   └── earthquake_alerts.parquet/   # Processed alerts in Parquet format
│
├── requirements.txt                 # Python dependencies
├── setup.bat                        # Windows setup script
├── run_spark.bat                    # Run PySpark job (Windows)
├── run_api.bat                      # Run FastAPI backend (Windows)
├── run_frontend.bat                 # Run Streamlit frontend (Windows)
└── README.md                        # This file
```

---

## 🔧 Prerequisites

### Required Software

1. **Python 3.9 or higher**
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Java 8 or higher** (Required for PySpark)
   - Download from: https://www.oracle.com/java/technologies/downloads/
   - Or use OpenJDK: https://adoptium.net/

3. **Git** (Optional, for cloning)
   - Download from: https://git-scm.com/downloads

### Verify Installation

Open Command Prompt and verify:

```bash
python --version      # Should show Python 3.9+
java -version         # Should show Java 8+
```

---

## 🚀 Installation

### Step 1: Navigate to Project Directory

```bash
cd earthquake_alert_system
```

### Step 2: Install Dependencies

**Option A: Automatic Setup (Windows)**

Double-click `setup.bat` or run:

```bash
setup.bat
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up the project

**Option B: Manual Setup**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## 📖 Usage

### 🔴 STEP 1: Run PySpark Batch Job

This processes the earthquake data and trains the ML model.

**Option 1: Standard PySpark Processor (requires compatible Java version)**
```bash
run_spark.bat
```

**Manual Command:**
```bash
python spark_job/earthquake_processor.py
```

**Option 2: Compatibility Processor (works with all Java versions)**
```bash
run_compatibility.bat
```

**Manual Command:**
```bash
python spark_job/compatibility_processor.py
```

**What it does:**
- Loads earthquake data from `data/earthquake_data.csv`
- Cleans and transforms the data
- Adds severity levels and features
- Trains a Random Forest ML model
- Generates hazard predictions
- Saves results to `output/` directory
- Saves model to `models/earthquake_model/`
- **Spark Web UI at http://localhost:4040 (only available with Option 1)**

**Expected Output (Option 1 - PySpark):**
```
================================================================================
🌍 EARTHQUAKE ALERT SYSTEM - PySpark Batch Processor
================================================================================

✅ Starting Spark Session...
📊 Spark Web UI will be available at: http://localhost:4040

✅ Spark Session Created Successfully!
   Version: 3.5.0
   Web UI: http://localhost:4040

📂 Loading earthquake data from CSV...
✅ Successfully loaded 30 earthquake records

🧹 Cleaning and transforming data...
✅ Data transformation complete!

🔧 Feature Engineering...
✅ Feature columns: ['magnitude', 'depth', 'region_index', 'latitude', 'longitude']

🤖 Training Machine Learning Model...
   Model Type: Random Forest Classifier
   Training set: 24 records
   Test set: 6 records
✅ Model Training Complete!
   Test Accuracy: 0.8333

💾 Saving Results...
   ✅ CSV saved to: output/earthquake_alerts.csv
   ✅ Parquet saved to: output/earthquake_alerts.parquet

💾 Saving ML Model...
✅ Model saved successfully!

🎉 PROCESSING COMPLETE!

📊 Spark Web UI: http://localhost:4040
👉 Press Enter after viewing Spark Web UI to exit...
```

**Expected Output (Option 2 - Compatibility Processor):**
```
================================================================================
🌍 EARTHQUAKE ALERT SYSTEM - Compatibility Data Processor
================================================================================

📂 Loading earthquake data...
✅ Successfully loaded 30 earthquake records

Columns: ['sensor_id', 'timestamp', 'latitude', 'longitude', 'magnitude', 'depth', 'region']

First few records:
  sensor_id            timestamp  ...  depth         region
0       S01  2024-01-02 05:22:01  ...     12     California
1       S02  2024-01-03 08:15:23  ...     25          Japan
2       S03  2024-01-05 14:30:45  ...      8       New York
3       S04  2024-01-07 22:45:12  ...     15  San Francisco
4       S05  2024-01-10 03:20:55  ...     35          Japan

[5 rows x 7 columns]

🧹 Cleaning and transforming data...
✅ Data transformation complete!
   Total records: 30

🤖 Training Machine Learning Model...
   Model Type: Random Forest Classifier
   Training set: 24 records
   Test set: 6 records
   Training in progress...
✅ Model Training Complete!
   Test Accuracy: 0.6667

🔮 Generating Hazard Predictions...
✅ Predictions generated successfully!

💾 Saving Results...
   ✅ CSV saved to: c:\Users\Aruna varshini\Desktop\ssf1\earthquake_alert_system\output\earthquake_alerts.csv
   ✅ Parquet saved to: c:\Users\Aruna varshini\Desktop\ssf1\earthquake_alert_system\output\earthquake_alerts.parquet

📊 Statistics:

Severity Distribution:
severity
Medium    18
High      10
Low        2
Name: count, dtype: int64

Region Distribution:
region
Japan            13
California       11
New York          1
San Francisco     1
Los Angeles       1
Arizona           1
Illinois          1
Nevada            1
Name: count, dtype: int64

💾 Saving ML Model to: c:\Users\Aruna varshini\Desktop\ssf1\earthquake_alert_system\models\earthquake_model
✅ Model saved successfully!

================================================================================
🎉 Processing Complete!
================================================================================

📁 Output Location: c:\Users\Aruna varshini\Desktop\ssf1\earthquake_alert_system\output
🤖 Model Location: c:\Users\Aruna varshini\Desktop\ssf1\earthquake_alert_system\models\earthquake_model

⚡ Next Steps:
   1. Start the FastAPI backend: python backend\api.py
   2. Start the Streamlit frontend: streamlit run frontend\app.py
================================================================================
```

**⚡ Viewing Spark Web UI:**
1. While the Spark job is running or paused, open your browser
2. Navigate to: **http://localhost:4040**
3. Explore:
   - **Jobs**: See all Spark jobs
   - **Stages**: View DAG visualization and task metrics
   - **Storage**: Check cached data
   - **Environment**: View Spark configuration
   - **Executors**: Monitor executor performance

---

### 🔴 STEP 2: Start FastAPI Backend

Open a **NEW** terminal/command prompt window.

**Windows:**
```bash
run_api.bat
```

**Manual Command:**
```bash
python backend/api.py
```

**Expected Output:**
```
================================================================================
🌍 EARTHQUAKE ALERT SYSTEM - FastAPI Backend
================================================================================

🚀 Starting server on http://localhost:8000
📚 API Docs available at http://localhost:8000/docs

✅ Loaded 30 earthquake alerts
📡 API Server running at: http://localhost:8000
```

**Available at:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### 🔴 STEP 3: Start Streamlit Frontend

Open **ANOTHER NEW** terminal/command prompt window.

**Windows:**
```bash
run_frontend.bat
```

**Manual Command:**
```bash
streamlit run frontend/app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Open Browser:**
Navigate to **http://localhost:8501**

---

## 🌐 System URLs

Once all components are running, you can access:

| Component | URL | Description |
|-----------|-----|-------------|
| **Streamlit Dashboard** | http://localhost:8501 | Main web interface |
| **FastAPI Backend** | http://localhost:8000 | REST API |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs (Swagger) |
| **Spark Web UI** | http://localhost:4040 | Spark job monitoring |

---

## 🔌 API Endpoints

### Base URL: `http://localhost:8000`

### 1. Get All Alerts

```http
GET /alerts
```

**Query Parameters:**
- `region` (optional): Filter by region name
- `min_magnitude` (optional): Minimum magnitude
- `max_magnitude` (optional): Maximum magnitude
- `severity` (optional): Filter by severity (Low/Medium/High)
- `limit` (optional): Maximum results (default: 100)

**Example:**
```bash
http://localhost:8000/alerts?region=California&min_magnitude=5.0&limit=10
```

**Response:**
```json
[
  {
    "sensor_id": "S01",
    "timestamp": "2024-01-02 05:22:01",
    "latitude": 34.11,
    "longitude": -117.22,
    "magnitude": 5.4,
    "depth": 12.0,
    "region": "California",
    "severity": "Medium",
    "depth_category": "Intermediate",
    "hazard_level": 1,
    "prediction": 1.0,
    "hazard_probability": 0.85,
    "alert_message": "Medium Risk - Prepare"
  }
]
```

---

### 2. Get Statistics

```http
GET /stats
```

**Response:**
```json
{
  "total_earthquakes": 30,
  "avg_magnitude": 5.47,
  "max_magnitude": 7.3,
  "avg_depth": 21.3,
  "severity_distribution": {
    "Medium": 18,
    "High": 10,
    "Low": 2
  },
  "region_distribution": {
    "Japan": 12,
    "California": 15,
    "Nevada": 1,
    "Arizona": 1,
    "Illinois": 1
  }
}
```

---

### 3. Predict Hazard Level

```http
GET /predict
```

**Query Parameters (Required):**
- `magnitude`: Earthquake magnitude (0-10)
- `depth`: Depth in kilometers (0-700)
- `region`: Region name

**Example:**
```bash
http://localhost:8000/predict?magnitude=5.2&depth=10&region=Japan
```

**Response:**
```json
{
  "hazard_level": "Medium",
  "hazard_score": 0.333,
  "risk_indicator": "yellow",
  "message": "Medium Risk - Stay prepared",
  "input_data": {
    "magnitude": 5.2,
    "depth": 10.0,
    "region": "Japan"
  }
}
```

---

### 4. Get Regions

```http
GET /regions
```

**Response:**
```json
{
  "regions": [
    "Arizona",
    "California",
    "Illinois",
    "Japan",
    "Los Angeles",
    "Nevada",
    "New York",
    "San Francisco"
  ],
  "count": 8
}
```

---

## ⚡ Spark Web UI

### Accessing Spark Web UI

**URL:** http://localhost:4040

**When Available:**
- While the PySpark job (`earthquake_processor.py`) is running
- After the job completes (remains open until you press Enter)

### What You Can See

#### 1. **Jobs Tab**
- List of all Spark jobs (completed/running/failed)
- Job duration and number of stages
- Click on a job to see detailed DAG visualization

#### 2. **Stages Tab**
- Breakdown of each stage in the job
- Task metrics (duration, GC time, shuffle read/write)
- Task execution timeline
- Aggregated metrics per executor

#### 3. **Storage Tab**
- Cached RDDs and DataFrames
- Memory usage
- Number of partitions
- Storage level

#### 4. **Environment Tab**
- Spark configuration properties
- System properties
- Classpath entries
- Runtime information

#### 5. **Executors Tab**
- Executor statistics
- Memory usage per executor
- Task metrics
- Executor logs (stdout/stderr)

#### 6. **SQL Tab**
- SQL query execution plans
- Physical and logical plans
- Query duration
- DAG visualization for DataFrame operations

### Understanding the DAG

The **Directed Acyclic Graph (DAG)** shows:
- **Stages**: Groups of tasks that can run in parallel
- **Shuffle Operations**: Data redistribution between stages
- **Transformations**: Operations on DataFrames (map, filter, join, etc.)
- **Actions**: Operations that trigger computation (count, collect, save, etc.)

---

## 📊 Sample Dataset

The system includes a sample dataset with **30 earthquake records**.

### Input Format

**File:** `data/earthquake_data.csv`

**Columns:**
- `sensor_id`: Unique sensor identifier
- `timestamp`: Date and time of earthquake
- `latitude`: GPS latitude
- `longitude`: GPS longitude
- `magnitude`: Earthquake magnitude (Richter scale)
- `depth`: Depth of hypocenter in kilometers
- `region`: Geographic region

**Sample Records:**

```csv
sensor_id,timestamp,latitude,longitude,magnitude,depth,region
S01,2024-01-02 05:22:01,34.11,-117.22,5.4,12,California
S02,2024-01-03 08:15:23,35.68,139.65,6.2,25,Japan
S03,2024-01-05 14:30:45,40.73,-74.00,3.1,8,New York
S04,2024-01-07 22:45:12,37.77,-122.41,4.5,15,San Francisco
S05,2024-01-10 03:20:55,36.20,138.25,7.1,35,Japan
S16,2024-02-10 21:20:56,40.71,140.73,7.3,40,Japan
```

### Adding Your Own Data

1. Create a CSV file with the same format
2. Place it in the `data/` directory
3. Update the file path in `spark_job/earthquake_processor.py` (line ~345):
   ```python
   data_path = os.path.join(base_dir, "data", "your_data.csv")
   ```
4. Run the Spark job again

---

## 🎨 Frontend Features

### 📊 Dashboard Page

**Features:**
- **Filters**: Region, magnitude range, severity level
- **Key Metrics**: Total earthquakes, average magnitude, max magnitude, high-risk events
- **Visualizations**:
  - Magnitude distribution histogram
  - Severity pie chart
  - Region-wise bar chart
  - Depth vs Magnitude scatter plot
- **Alerts Table**: Sortable, filterable table with all earthquake alerts
- **Download**: Export filtered data as CSV

### 🗺️ Risk Map Page

**Features:**
- **Interactive Map**: Powered by Folium
- **GPS Markers**: Color-coded by severity
  - 🟢 Green: Low severity
  - 🟠 Orange: Medium severity
  - 🔴 Red: High severity
- **Tooltips**: Hover to see basic info
- **Popups**: Click markers for detailed information
- **Heatmap**: Toggle heatmap visualization
- **Filters**: Filter by severity level
- **Regional Statistics**: Aggregated stats by region

### 🔮 Prediction Page

**Features:**
- **Input Form**: Enter magnitude, depth, region
- **Real-time Prediction**: Get hazard level instantly
- **Visual Indicators**:
  - Hazard Level: Low/Medium/High/Critical
  - Hazard Score: Probability (0-1)
  - Risk Indicator: Color-coded (green/yellow/orange/red)
- **Alert Message**: Actionable recommendations
- **API Integration**: Connects to FastAPI backend

### ⚡ Spark Web UI Page

**Features:**
- **Direct Link**: One-click access to Spark Web UI
- **Documentation**: How to use Spark Web UI
- **Tab Explanations**: Detailed guide for each tab
- **Troubleshooting**: Tips if Spark UI is not available

---

## 🛠️ Troubleshooting

### ❌ Spark Web UI Not Opening

**Problem:** `http://localhost:4040` doesn't load

**Solutions:**
1. Make sure the Spark job is running:
   ```bash
   python spark_job/earthquake_processor.py
   ```
2. Check if port 4040 is already in use. Spark will try 4041, 4042, etc.
3. Check terminal output for the actual port number
4. Ensure Java is installed:
   ```bash
   java -version
   ```

---

### ❌ API Not Loading Data

**Problem:** API returns empty results or errors

**Solutions:**
1. Make sure you ran the Spark job first
2. Check if output files exist:
   ```
   output/earthquake_alerts.csv/
   ```
3. Restart the API server:
   ```bash
   python backend/api.py
   ```

---

### ❌ Frontend Shows No Data

**Problem:** Streamlit shows "No data available"

**Solutions:**
1. Run the Spark job to generate data
2. Make sure output files exist in `output/` directory
3. Restart Streamlit:
   ```bash
   streamlit run frontend/app.py
   ```

---

### ❌ Port Already in Use

**Problem:** `Address already in use` error

**Solutions:**

**For Port 8000 (FastAPI):**
```bash
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

**For Port 8501 (Streamlit):**
```bash
# Windows - Find and kill process
netstat -ano | findstr :8501
taskkill /PID <process_id> /F
```

**For Port 4040 (Spark):**
```bash
# Windows - Find and kill process
netstat -ano | findstr :4040
taskkill /PID <process_id> /F
```

---

### ❌ Module Not Found Error

**Problem:** `ModuleNotFoundError: No module named 'pyspark'`

**Solution:**
```bash
# Activate virtual environment first
venv\Scripts\activate

# Then install dependencies
pip install -r requirements.txt
```

---

### ❌ Java Not Found

**Problem:** `JAVA_HOME is not set`

**Solution:**
1. Install Java 8 or higher
2. Set JAVA_HOME environment variable (Windows):
   ```bash
   # Add to System Environment Variables
   JAVA_HOME=C:\Program Files\Java\jdk-11
   ```
3. Add to PATH:
   ```bash
   %JAVA_HOME%\bin
   ```

---

## 📝 Development Notes

### Technologies Used

- **PySpark 3.5.0**: Big data processing and ML
- **FastAPI**: Modern web framework for APIs
- **Streamlit**: Quick dashboard development
- **Plotly**: Interactive visualizations
- **Folium**: Interactive maps
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

### Performance Considerations

- **Spark Partitions**: Default is 4 (configured in `earthquake_processor.py`)
- **Spark Memory**: Default driver memory is 2GB
- **API Response Limit**: Default 100 records (configurable)

### Customization

**Change Spark Configuration:**

Edit `spark_job/earthquake_processor.py`:
```python
spark = SparkSession.builder \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()
```

**Change API Port:**

Edit `backend/api.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)
```

**Change Frontend Port:**

```bash
streamlit run frontend/app.py --server.port 8502
```

---

## 🎯 Next Steps

1. **Add More Data**: Expand the dataset with more earthquake records
2. **Improve Model**: Tune hyperparameters, try different algorithms
3. **Real-time Streaming**: Integrate Spark Streaming for real-time alerts
4. **Database Integration**: Store data in PostgreSQL/MongoDB
5. **Deployment**: Deploy to cloud (AWS, Azure, GCP)
6. **Mobile App**: Create mobile interface for alerts
7. **Email Notifications**: Send alerts via email
8. **Advanced Analytics**: Time-series forecasting, anomaly detection

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## 👨‍💻 Author

Earthquake Alert System - Built with ❤️ using PySpark, FastAPI, and Streamlit

---

## 🙏 Acknowledgments

- PySpark Documentation
- FastAPI Documentation
- Streamlit Documentation
- Folium Mapping Library
- Plotly Visualization Library

---

**🎉 Enjoy monitoring earthquakes with your complete localhost system!**
