# ⚡ Quick Start Guide

Get the Earthquake Alert System running in 3 minutes!

---

## 🚀 Installation (One-Time Setup)

### Step 1: Open Command Prompt in project folder

```bash
cd earthquake_alert_system
```

### Step 2: Run Setup

**Double-click `setup.bat`** or run:

```bash
setup.bat
```

This installs all dependencies automatically.

---

## 🎯 Running the System

You need to run **3 components** in **3 separate terminal windows**:

### Terminal 1: Data Processing

**Option 1: PySpark Job (requires compatible Java version)**
```bash
run_spark.bat
```

✅ Processes data and trains ML model  
✅ Opens Spark Web UI at http://localhost:4040  
✅ Wait for completion, then press Enter after viewing Spark UI

**Option 2: Compatibility Processor (works with all Java versions)**
```bash
run_compatibility.bat
```

✅ Processes data and trains ML model  
✅ No Spark Web UI (uses pandas/scikit-learn instead)  
✅ Faster startup and no Java compatibility issues

---

### Terminal 2: API Backend

**Open NEW terminal**, then run:

```bash
run_api.bat
```

✅ Starts REST API at http://localhost:8000  
✅ API docs at http://localhost:8000/docs

---

### Terminal 3: Frontend

**Open ANOTHER NEW terminal**, then run:

```bash
run_frontend.bat
```

✅ Opens dashboard at http://localhost:8501  
✅ Your browser should open automatically

---

## 🌐 Access the System

| Component | URL |
|-----------|-----|
| **Main Dashboard** | http://localhost:8501 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Spark Web UI** | http://localhost:4040 |

---

## 🎨 What You Can Do

### 1. Dashboard (http://localhost:8501)
- View earthquake alerts
- Filter by region, magnitude, severity
- See interactive charts
- Download data

### 2. Risk Map
- Interactive map with GPS markers
- Color-coded by severity
- Heatmap visualization
- Click markers for details

### 3. Prediction
- Enter: magnitude, depth, region
- Get: hazard level and risk score
- Color-coded risk indicator

### 4. Spark Web UI (http://localhost:4040)
- View DAG visualization
- See job stages
- Monitor executors
- Check shuffle operations

---

## ❌ Troubleshooting

### Problem: "No data available"
**Solution:** Run the Spark job first (`run_spark.bat`)

### Problem: Port already in use
**Solution:** 
```bash
# Find and kill the process (Windows)
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Problem: Module not found
**Solution:** 
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📖 Full Documentation

See `README.md` for complete documentation.

---

**🎉 You're all set! Enjoy your Earthquake Alert System!**
