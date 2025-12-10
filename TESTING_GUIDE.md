# 🧪 Testing Guide - Earthquake Alert System

This guide will walk you through testing every feature of the system.

---

## 📋 Prerequisites Check

Before starting, verify you have:

```bash
# Check Python (should be 3.9+)
python --version

# Check Java (should be 8+)
java -version

# Check pip
pip --version
```

If any are missing, install them first!

---

## 🚀 Step-by-Step Testing

### ✅ STEP 1: Installation Test

**Action:**
```bash
cd earthquake_alert_system
setup.bat
```

**Expected Result:**
- Virtual environment created in `venv/` folder
- All packages installed successfully
- No error messages

**Verify:**
```bash
venv\Scripts\activate
pip list | findstr pyspark
pip list | findstr fastapi
pip list | findstr streamlit
```

Should show:
- pyspark 3.5.0
- fastapi 0.104.1
- streamlit 1.28.2

---

### ✅ STEP 2: PySpark Job Test

**Action:**
```bash
run_spark.bat
```

**Expected Console Output:**
```
================================================================================
🌍 EARTHQUAKE ALERT SYSTEM - PySpark Batch Processor
================================================================================

✅ Starting Spark Session...
📊 Spark Web UI will be available at: http://localhost:4040

✅ Spark Session Created Successfully!
   Version: 3.5.0
   Master: local[*]
   App Name: Earthquake Alert System
   Web UI: http://localhost:4040

📂 Loading earthquake data from CSV...
✅ Successfully loaded 30 earthquake records

🧹 Cleaning and transforming data...
✅ Data transformation complete!
   Total records after cleaning: 30

🔧 Feature Engineering...
✅ Feature columns: ['magnitude', 'depth', 'region_index', 'latitude', 'longitude']

🤖 Training Machine Learning Model...
   Model Type: Random Forest Classifier
   Training set: 24 records
   Test set: 6 records
   Training in progress...
✅ Model Training Complete!
   Test Accuracy: 0.XXXX

🔮 Generating Hazard Predictions for All Records...
✅ Predictions generated successfully!

💾 Saving Results...
   ✅ CSV saved to: output/earthquake_alerts.csv
   ✅ Parquet saved to: output/earthquake_alerts.parquet

📊 Generating Statistics...
   Severity Distribution:
   +--------+-----+
   |severity|count|
   +--------+-----+
   |  Medium|   18|
   |    High|   10|
   |     Low|    2|
   +--------+-----+

💾 Saving ML Model to: models/earthquake_model
✅ Model saved successfully!

🎉 EARTHQUAKE ALERT SYSTEM - Processing Complete!

📊 Spark Web UI is running at: http://localhost:4040
👉 Press Enter after viewing Spark Web UI to exit...
```

**What to Check:**

1. **No Errors**: Should complete without errors
2. **Data Loaded**: "Successfully loaded 30 earthquake records"
3. **Model Trained**: "Model Training Complete!" with accuracy score
4. **Files Created**: Check if these exist:
   - `output/earthquake_alerts.csv/`
   - `output/earthquake_alerts.parquet/`
   - `models/earthquake_model/`

**Spark Web UI Test:**

While the job is paused (waiting for Enter):

1. Open browser to: http://localhost:4040
2. You should see:
   - **Jobs tab**: List of completed jobs
   - **Stages tab**: Click to see DAG visualization
   - **Storage tab**: Cached data (if any)
   - **Executors tab**: Executor metrics

**Verify DAG:**
- Click on a completed job
- You should see a DAG (Directed Acyclic Graph) with:
  - Blue boxes (stages)
  - Arrows showing data flow
  - Details about transformations

**After Testing:**
- Press Enter in the terminal to stop Spark

---

### ✅ STEP 3: API Backend Test

**Action:**

Open a **NEW** terminal window:

```bash
cd earthquake_alert_system
run_api.bat
```

**Expected Console Output:**
```
================================================================================
🌍 EARTHQUAKE ALERT SYSTEM - FastAPI Backend
================================================================================

🚀 Starting server on http://localhost:8000
📚 API Docs available at http://localhost:8000/docs

✅ Loaded 30 earthquake alerts from ...
📡 API Server running at: http://localhost:8000

INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete.
```

**Test 1: Root Endpoint**

Open browser to: http://localhost:8000

Expected JSON response:
```json
{
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
```

**Test 2: API Documentation**

Open: http://localhost:8000/docs

You should see:
- Swagger UI interface
- List of all endpoints
- Try them out interactively

**Test 3: Get Alerts**

URL: http://localhost:8000/alerts?limit=5

Should return JSON array with 5 earthquake records

**Test 4: Get Statistics**

URL: http://localhost:8000/stats

Expected response:
```json
{
  "total_earthquakes": 30,
  "avg_magnitude": 5.47,
  "max_magnitude": 7.3,
  "avg_depth": 21.3,
  "severity_distribution": {...},
  "region_distribution": {...}
}
```

**Test 5: Prediction**

URL: http://localhost:8000/predict?magnitude=5.2&depth=10&region=Japan

Expected response:
```json
{
  "hazard_level": "Medium",
  "hazard_score": 0.333,
  "risk_indicator": "yellow",
  "message": "Medium Risk - Stay prepared",
  "input_data": {
    "magnitude": 5.2,
    "depth": 10,
    "region": "Japan"
  }
}
```

**Test 6: Get Regions**

URL: http://localhost:8000/regions

Should return list of all unique regions

**Keep API Running** for frontend tests!

---

### ✅ STEP 4: Frontend Dashboard Test

**Action:**

Open **ANOTHER NEW** terminal window:

```bash
cd earthquake_alert_system
run_frontend.bat
```

**Expected Console Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Browser should automatically open to http://localhost:8501

---

### ✅ STEP 5: Frontend Features Test

#### 📊 Dashboard Page Test

**Navigation:**
- Sidebar should show: "📊 Dashboard" (selected by default)

**What to Check:**

1. **Header**: "🌍 Earthquake Alert Dashboard"

2. **Filters (Sidebar)**:
   - Region dropdown (should have: All, Arizona, California, Illinois, Japan, etc.)
   - Magnitude range slider
   - Severity dropdown (All, Low, Medium, High)

3. **Key Metrics (4 cards)**:
   - Total Earthquakes: 30
   - Average Magnitude: ~5.47
   - Max Magnitude: 7.3
   - High Risk Events: 10+

4. **Visualizations (4 charts)**:
   - **Magnitude Distribution**: Histogram with color-coded severity
   - **Severity Distribution**: Pie chart (Low/Medium/High)
   - **Earthquakes by Region**: Horizontal bar chart
   - **Depth vs Magnitude**: Scatter plot with hover info

5. **Alerts Table**:
   - Should show up to 20 recent alerts
   - Columns: sensor_id, timestamp, region, magnitude, depth, severity, alert_message, hazard_probability

6. **Download Button**: 
   - Click "📥 Download Filtered Data (CSV)"
   - Should download a CSV file

**Test Filters:**
- Change region to "California" → Chart and table should update
- Adjust magnitude slider → Data should filter
- Change severity → Only selected severity shown

---

#### 🗺️ Risk Map Page Test

**Navigation:**
- Click "🗺️ Risk Map" in sidebar

**What to Check:**

1. **Header**: "🌍 Earthquake Risk Zone Map"

2. **Map Controls (Right sidebar)**:
   - "Show Markers" checkbox (default: ON)
   - "Show Heatmap" checkbox (default: OFF)
   - "Filter by Severity" multi-select

3. **Interactive Map**:
   - Should show world map centered on earthquake locations
   - GPS markers visible (if "Show Markers" is ON)
   - Markers color-coded:
     - 🟢 Green: Low severity
     - 🟠 Orange: Medium severity
     - 🔴 Red: High severity

4. **Marker Interactions**:
   - **Hover**: Shows tooltip with region and magnitude
   - **Click**: Opens popup with detailed info:
     - Region
     - Sensor ID
     - Magnitude
     - Depth
     - Severity
     - Alert message
     - Timestamp

5. **Heatmap Test**:
   - Toggle "Show Heatmap" to ON
   - Should see color gradient overlay (blue → yellow → orange → red)
   - More intense colors where earthquakes are clustered

6. **Filter Test**:
   - Uncheck "Medium" in severity filter
   - Medium severity markers should disappear

7. **Regional Statistics Table**:
   - Below map, should show stats by region
   - Columns: region, mean magnitude, max magnitude, count, etc.

---

#### 🔮 Prediction Page Test

**Navigation:**
- Click "🔮 Prediction" in sidebar

**What to Check:**

1. **Header**: "🔮 Earthquake Hazard Prediction"

2. **Description**: Explanation of ML model

3. **Input Form (Left side)**:
   - **Magnitude** input (0.0 - 10.0, default: 5.2)
   - **Depth** input (0.0 - 700.0 km, default: 10.0)
   - **Region** dropdown (California, Japan, etc.)
   - **Predict Button**: "🔮 Predict Hazard Level"

4. **Test Prediction - Low Risk**:
   - Magnitude: 3.0
   - Depth: 20
   - Region: California
   - Click "Predict"
   
   **Expected Result**:
   - Hazard Level: Low
   - Hazard Score: < 0.25
   - Risk Indicator: GREEN box
   - Message: "Low Risk - Continue monitoring"

5. **Test Prediction - Medium Risk**:
   - Magnitude: 5.0
   - Depth: 15
   - Region: Japan
   - Click "Predict"
   
   **Expected Result**:
   - Hazard Level: Medium
   - Hazard Score: 0.25 - 0.5
   - Risk Indicator: YELLOW box
   - Message: "Medium Risk - Stay prepared"

6. **Test Prediction - High Risk**:
   - Magnitude: 6.5
   - Depth: 10
   - Region: California
   - Click "Predict"
   
   **Expected Result**:
   - Hazard Level: High
   - Hazard Score: 0.5 - 0.75
   - Risk Indicator: ORANGE box
   - Message: "High Risk - Alert issued"

7. **Test Prediction - Critical Risk**:
   - Magnitude: 7.5
   - Depth: 5
   - Region: Japan
   - Click "Predict"
   
   **Expected Result**:
   - Hazard Level: Critical
   - Hazard Score: > 0.75
   - Risk Indicator: RED box
   - Message: "Critical Risk - Immediate action required"

8. **Results Display**:
   - Three metric cards (Hazard Level, Score, Risk)
   - Info box with alert message
   - JSON display of input parameters

---

#### ⚡ Spark Web UI Page Test

**Navigation:**
- Click "⚡ Spark Web UI" in sidebar

**What to Check:**

1. **Header**: "⚡ Spark Web UI"

2. **Information Section**:
   - Description of Spark Web UI features
   - URL display: http://localhost:4040

3. **Button**:
   - "🚀 Open Spark Web UI" button
   - Click it (if Spark job is still running)
   - Should open new browser tab

4. **Documentation**:
   - "How to Use Spark Web UI" section
   - Explains all tabs (Jobs, Stages, Storage, etc.)

5. **Note/Warning**:
   - Message about Spark UI only available when job is running

6. **Code Example**:
   - Shows how to run Spark job

---

### ✅ STEP 6: System Integration Test

**Verify All Components Running Together:**

1. **Check All URLs**:
   - http://localhost:8000 → API root (JSON response)
   - http://localhost:8000/docs → Swagger UI
   - http://localhost:8501 → Streamlit dashboard
   - http://localhost:4040 → Spark UI (if job running)

2. **Test Data Flow**:
   - Run Spark job → generates data
   - API reads data → serves endpoints
   - Frontend calls API → displays data

3. **Test End-to-End Prediction**:
   - Go to frontend prediction page
   - Enter values
   - Click predict
   - Frontend calls API → API returns prediction → Frontend displays result

---

## 🧪 Advanced Tests

### Test 1: Custom Data

**Add your own earthquake:**

1. Open `data/earthquake_data.csv`
2. Add a new row:
   ```
   S99,2024-12-03 10:30:00,40.00,-120.00,6.5,18,Nevada
   ```
3. Save file
4. Re-run Spark job
5. Verify new data appears in dashboard

### Test 2: API Filtering

Test various filter combinations:

```
http://localhost:8000/alerts?region=California
http://localhost:8000/alerts?min_magnitude=6.0
http://localhost:8000/alerts?severity=High&limit=10
http://localhost:8000/alerts?region=Japan&min_magnitude=6.0&max_magnitude=7.0
```

### Test 3: Data Download

1. Go to dashboard
2. Apply some filters
3. Click download button
4. Open downloaded CSV
5. Verify it contains filtered data only

---

## ❌ Troubleshooting Tests

### Test: Port Conflict

**Simulate:** Run API twice

**Expected:** Second instance should fail with "Address already in use"

**Fix:**
```bash
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Test: Missing Data

**Simulate:** Delete output folder

**Expected:** 
- API shows "No data available"
- Frontend shows "Please run Spark job first"

**Fix:** Re-run Spark job

### Test: API Connection Failure

**Simulate:** Stop API while frontend is running

**Expected:** Frontend shows warning: "API not available"

**Fix:** Restart API

---

## ✅ Success Criteria

### PySpark Job ✅
- Loads 30 records
- Processes without errors
- Generates output files
- Saves model
- Spark UI accessible

### API Backend ✅
- Starts on port 8000
- All endpoints respond
- Returns valid JSON
- Docs accessible
- Handles errors gracefully

### Frontend ✅
- Starts on port 8501
- All 4 pages load
- Charts render correctly
- Map shows markers
- Predictions work
- Filters update data
- Download works

### Integration ✅
- All components run simultaneously
- Data flows from Spark → API → Frontend
- Predictions work end-to-end
- No errors in any console

---

## 📊 Performance Benchmarks

**Expected Performance:**

| Operation | Expected Time |
|-----------|---------------|
| Spark job (30 records) | 30-60 seconds |
| API startup | 5-10 seconds |
| Frontend startup | 5-10 seconds |
| API response (/alerts) | < 100ms |
| API response (/predict) | < 50ms |
| Dashboard page load | 1-3 seconds |
| Map rendering | 2-5 seconds |
| Chart updates | < 1 second |

---

## 🎯 Final Checklist

Before considering testing complete, verify:

- [ ] All dependencies installed
- [ ] Spark job runs without errors
- [ ] Output files created
- [ ] Model saved
- [ ] Spark Web UI accessible
- [ ] API starts successfully
- [ ] All API endpoints work
- [ ] API docs accessible
- [ ] Frontend starts successfully
- [ ] All 4 pages load
- [ ] Dashboard charts render
- [ ] Map shows markers
- [ ] Predictions work
- [ ] Filters work
- [ ] Download works
- [ ] No console errors
- [ ] All URLs accessible

---

## 🎉 Congratulations!

If all tests pass, your Earthquake Alert System is fully functional!

**You now have:**
- ✅ Working PySpark batch processor
- ✅ Trained ML model
- ✅ REST API backend
- ✅ Interactive dashboard
- ✅ Risk zone map
- ✅ Prediction system
- ✅ Spark Web UI monitoring

**Next Steps:**
- Explore the data
- Try different predictions
- Add your own earthquake data
- Customize visualizations
- Enhance the ML model

---

**Happy Testing! 🚀**
