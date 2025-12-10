# 🏗️ System Architecture - Earthquake Alert System

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EARTHQUAKE ALERT SYSTEM                       │
│                      (Localhost Version)                         │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   DATA SOURCE    │
                    │                  │
                    │  earthquake_     │
                    │  data.csv        │
                    │  (30 records)    │
                    └────────┬─────────┘
                             │
                             │ Read CSV
                             ▼
        ┌────────────────────────────────────────────┐
        │         PYSPARK BATCH PROCESSOR            │
        │                                            │
        │  ┌──────────────────────────────────┐     │
        │  │  Data Loading & Validation       │     │
        │  └──────────┬───────────────────────┘     │
        │             │                              │
        │             ▼                              │
        │  ┌──────────────────────────────────┐     │
        │  │  Data Cleaning & Transformation  │     │
        │  │  - Remove nulls                  │     │
        │  │  - Extract timestamp features    │     │
        │  │  - Add severity levels           │     │
        │  │  - Add hazard classifications    │     │
        │  └──────────┬───────────────────────┘     │
        │             │                              │
        │             ▼                              │
        │  ┌──────────────────────────────────┐     │
        │  │  Feature Engineering             │     │
        │  │  - StringIndexer (region)        │     │
        │  │  - VectorAssembler (features)    │     │
        │  └──────────┬───────────────────────┘     │
        │             │                              │
        │             ▼                              │
        │  ┌──────────────────────────────────┐     │
        │  │  ML Model Training               │     │
        │  │  - RandomForestClassifier        │     │
        │  │  - 100 trees, maxDepth=10        │     │
        │  │  - 80/20 train/test split        │     │
        │  └──────────┬───────────────────────┘     │
        │             │                              │
        │             ▼                              │
        │  ┌──────────────────────────────────┐     │
        │  │  Predictions & Evaluation        │     │
        │  │  - Generate hazard predictions   │     │
        │  │  - Calculate probabilities       │     │
        │  └──────────┬───────────────────────┘     │
        │             │                              │
        │             ▼                              │
        │  ┌──────────────────────────────────┐     │
        │  │  Save Results                    │     │
        │  │  - CSV output                    │     │
        │  │  - Parquet output                │     │
        │  │  - Save trained model            │     │
        │  └──────────────────────────────────┘     │
        │                                            │
        │  Spark Web UI: http://localhost:4040      │
        └────────────────┬───────────────────────────┘
                         │
                         │ Output Files
                         ▼
        ┌────────────────────────────────────────────┐
        │         OUTPUT & MODEL STORAGE             │
        │                                            │
        │  📁 output/                                │
        │     ├── earthquake_alerts.csv/             │
        │     └── earthquake_alerts.parquet/         │
        │                                            │
        │  📁 models/                                │
        │     └── earthquake_model/                  │
        └────────────────┬───────────────────────────┘
                         │
                         │ Read Data
                         ▼
        ┌────────────────────────────────────────────┐
        │          FASTAPI BACKEND                   │
        │       http://localhost:8000                │
        │                                            │
        │  ┌──────────────────────────────────┐     │
        │  │  Data Loading Module             │     │
        │  │  - Load processed alerts         │     │
        │  │  - Cache in memory               │     │
        │  └──────────┬───────────────────────┘     │
        │             │                              │
        │             ▼                              │
        │  ┌──────────────────────────────────┐     │
        │  │  REST API Endpoints              │     │
        │  │                                  │     │
        │  │  GET /alerts                     │     │
        │  │  GET /stats                      │     │
        │  │  GET /predict                    │     │
        │  │  GET /regions                    │     │
        │  │  GET /health                     │     │
        │  └──────────┬───────────────────────┘     │
        │             │                              │
        │             ▼                              │
        │  ┌──────────────────────────────────┐     │
        │  │  Prediction Engine               │     │
        │  │  - Rule-based prediction         │     │
        │  │  - Hazard level calculation      │     │
        │  │  - Risk scoring                  │     │
        │  └──────────────────────────────────┘     │
        │                                            │
        │  Auto Docs: /docs (Swagger UI)             │
        │             /redoc (ReDoc)                 │
        └────────────────┬───────────────────────────┘
                         │
                         │ HTTP/JSON
                         ▼
        ┌────────────────────────────────────────────┐
        │        STREAMLIT FRONTEND                  │
        │       http://localhost:8501                │
        │                                            │
        │  ┌──────────────────────────────────┐     │
        │  │  📊 Dashboard Page               │     │
        │  │  - Key metrics                   │     │
        │  │  - Interactive filters           │     │
        │  │  - Plotly charts (4 types)       │     │
        │  │  - Alerts table                  │     │
        │  │  - CSV download                  │     │
        │  └──────────────────────────────────┘     │
        │                                            │
        │  ┌──────────────────────────────────┐     │
        │  │  🗺️ Risk Map Page                │     │
        │  │  - Folium interactive map        │     │
        │  │  - GPS markers (color-coded)     │     │
        │  │  - Heatmap overlay               │     │
        │  │  - Tooltips & popups             │     │
        │  │  - Regional statistics           │     │
        │  └──────────────────────────────────┘     │
        │                                            │
        │  ┌──────────────────────────────────┐     │
        │  │  🔮 Prediction Page              │     │
        │  │  - Input form                    │     │
        │  │  - API integration               │     │
        │  │  - Real-time prediction          │     │
        │  │  - Color-coded results           │     │
        │  └──────────────────────────────────┘     │
        │                                            │
        │  ┌──────────────────────────────────┐     │
        │  │  ⚡ Spark Web UI Page            │     │
        │  │  - Link to Spark UI              │     │
        │  │  - Usage documentation           │     │
        │  └──────────────────────────────────┘     │
        └────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐
│  CSV    │────▶│ PySpark │────▶│ Output  │────▶│  FastAPI │
│  Data   │     │  Job    │     │  Files  │     │   API    │
└─────────┘     └────┬────┘     └─────────┘     └────┬─────┘
                     │                                │
                     │                                │
                     ▼                                ▼
              ┌──────────┐                    ┌──────────────┐
              │   ML     │                    │  Streamlit   │
              │  Model   │                    │  Dashboard   │
              └──────────┘                    └──────────────┘
                                                     │
                                                     │
                                                     ▼
                                              ┌──────────────┐
                                              │    User      │
                                              │   Browser    │
                                              └──────────────┘
```

---

## 🧩 Component Details

### 1️⃣ PySpark Batch Processor

**File:** `spark_job/earthquake_processor.py` (372 lines)

**Purpose:** Process raw earthquake data and train ML model

**Key Functions:**
- `create_spark_session()`: Initialize Spark with Web UI
- `load_data()`: Read CSV data
- `clean_and_transform()`: Data cleaning and feature creation
- `feature_engineering()`: Prepare features for ML
- `train_ml_model()`: Train RandomForestClassifier
- `generate_predictions()`: Predict hazard levels
- `save_results()`: Save processed data

**Technologies:**
- PySpark 3.5.0
- PySpark MLlib
- PySpark SQL

**Inputs:**
- `data/earthquake_data.csv`

**Outputs:**
- `output/earthquake_alerts.csv/`
- `output/earthquake_alerts.parquet/`
- `models/earthquake_model/`

**Port:** 4040 (Spark Web UI)

---

### 2️⃣ FastAPI Backend

**File:** `backend/api.py` (334 lines)

**Purpose:** Provide REST API for earthquake data and predictions

**Key Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/alerts` | GET | Get earthquake alerts (with filters) |
| `/stats` | GET | Summary statistics |
| `/predict` | GET | Hazard prediction |
| `/regions` | GET | List of regions |
| `/health` | GET | Health check |

**Technologies:**
- FastAPI 0.104.1
- Uvicorn (ASGI server)
- Pydantic (data validation)
- Pandas (data processing)

**Port:** 8000

**API Docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### 3️⃣ Streamlit Frontend

**File:** `frontend/app.py` (605 lines)

**Purpose:** Interactive web dashboard for visualization and predictions

**Pages:**

1. **Dashboard** (`dashboard_page()`)
   - Key metrics display
   - Interactive filters
   - 4 Plotly charts
   - Data table
   - CSV download

2. **Risk Map** (`risk_map_page()`)
   - Folium interactive map
   - GPS markers
   - Heatmap overlay
   - Regional statistics

3. **Prediction** (`prediction_page()`)
   - Input form
   - API integration
   - Real-time predictions
   - Color-coded results

4. **Spark Web UI** (`spark_ui_page()`)
   - Link to Spark UI
   - Documentation
   - Usage guide

**Technologies:**
- Streamlit 1.28.2
- Plotly 5.18.0
- Folium 0.15.0
- Pandas
- Requests

**Port:** 8501

---

## 🗄️ Data Model

### Input Data Schema

```
earthquake_data.csv
├── sensor_id: String (e.g., "S01")
├── timestamp: String (e.g., "2024-01-02 05:22:01")
├── latitude: Float (e.g., 34.11)
├── longitude: Float (e.g., -117.22)
├── magnitude: Float (e.g., 5.4)
├── depth: Integer (e.g., 12)
└── region: String (e.g., "California")
```

### Processed Data Schema

```
earthquake_alerts.csv
├── sensor_id: String
├── timestamp: String
├── latitude: Float
├── longitude: Float
├── magnitude: Float
├── depth: Float
├── region: String
├── severity: String (Low/Medium/High)
├── depth_category: String (Shallow/Intermediate/Deep)
├── hazard_level: Integer (0-3)
├── prediction: Float (predicted hazard level)
├── hazard_probability: Float (0-1)
└── alert_message: String
```

### ML Model Schema

**Input Features:**
- magnitude: Float
- depth: Float
- region_index: Integer (encoded)
- latitude: Float
- longitude: Float

**Output:**
- prediction: Integer (0-3)
- probability: Vector[4] (probabilities for each class)

**Classes:**
- 0: Low Risk
- 1: Medium Risk
- 2: High Risk
- 3: Critical Risk

---

## 🔒 Security Considerations

### Current Implementation (Localhost)
- No authentication required
- CORS enabled for all origins
- Data stored locally
- No encryption

### Production Recommendations
- Add API authentication (JWT/OAuth)
- Implement rate limiting
- Add input validation
- Use HTTPS
- Restrict CORS origins
- Add database with proper access controls
- Implement logging and monitoring
- Add data encryption

---

## ⚡ Performance Characteristics

### PySpark Job
- **Parallelism:** local[*] (all cores)
- **Shuffle Partitions:** 4
- **Driver Memory:** 2GB
- **Expected Runtime:** 30-60 seconds for 30 records

### API Backend
- **Concurrency:** Async with Uvicorn
- **Response Time:** < 100ms for most endpoints
- **Memory Usage:** ~100-200MB
- **Max Records:** Limited to 100 per request (configurable)

### Frontend
- **Load Time:** 1-3 seconds initial load
- **Chart Rendering:** < 1 second
- **Map Rendering:** 2-5 seconds
- **Memory Usage:** Depends on browser

---

## 📈 Scalability Considerations

### Current Limitations (Localhost)
- Single machine processing
- In-memory data storage
- No distributed computing
- Limited to local file system

### Scaling Options

**Horizontal Scaling:**
- Deploy Spark on cluster (YARN, Kubernetes)
- Use distributed storage (HDFS, S3)
- Add load balancer for API
- Implement caching (Redis)

**Vertical Scaling:**
- Increase driver/executor memory
- Add more CPU cores
- Use faster storage (SSD)

**Data Scaling:**
- Partition data by region/date
- Implement incremental processing
- Add streaming with Spark Structured Streaming
- Use column-oriented storage (Parquet)

---

## 🔄 Workflow Sequence

### Setup Workflow
```
1. User runs: setup.bat
2. Python venv created
3. Dependencies installed
4. Environment ready
```

### Data Processing Workflow
```
1. User runs: run_spark.bat
2. Spark session created (Web UI at :4040)
3. CSV data loaded (30 records)
4. Data cleaned and transformed
5. Features engineered
6. ML model trained (RandomForest)
7. Predictions generated
8. Results saved (CSV + Parquet)
9. Model saved
10. User views Spark Web UI
11. User presses Enter to exit
```

### Runtime Workflow
```
1. User runs: run_api.bat (Terminal 1)
   - API loads processed data
   - Server starts at :8000
   
2. User runs: run_frontend.bat (Terminal 2)
   - Frontend starts at :8501
   - Browser opens automatically
   
3. User interacts with dashboard:
   a. View charts and metrics
   b. Filter data
   c. Download CSV
   
4. User views risk map:
   a. See GPS markers
   b. Click for details
   c. Toggle heatmap
   
5. User makes prediction:
   a. Enter magnitude, depth, region
   b. Click predict
   c. Frontend calls API
   d. API returns prediction
   e. Results displayed
```

---

## 🧪 Testing Architecture

### Unit Testing (Recommended)
- Test individual functions
- Mock Spark context
- Test API endpoints
- Test data transformations

### Integration Testing (Recommended)
- Test Spark → API integration
- Test API → Frontend integration
- Test end-to-end predictions

### Performance Testing (Recommended)
- Load test API endpoints
- Benchmark Spark job with larger datasets
- Test frontend with many markers

---

## 📦 Deployment Architecture

### Current: Localhost Development

```
┌──────────────────────────────┐
│     Developer Machine        │
│  ┌────────────────────────┐  │
│  │  PySpark :4040         │  │
│  ├────────────────────────┤  │
│  │  FastAPI :8000         │  │
│  ├────────────────────────┤  │
│  │  Streamlit :8501       │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

### Future: Production Deployment

```
┌─────────────────────────────────────────┐
│            Load Balancer                │
└───────────┬─────────────────────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
┌────────┐      ┌────────┐
│  API   │      │  API   │
│ Server │      │ Server │
│   1    │      │   2    │
└────┬───┘      └───┬────┘
     │              │
     └──────┬───────┘
            ▼
    ┌───────────────┐
    │   Database    │
    │ (PostgreSQL)  │
    └───────────────┘
    
    ┌───────────────┐
    │  Spark        │
    │  Cluster      │
    │  (YARN/K8s)   │
    └───────────────┘
    
    ┌───────────────┐
    │  Frontend     │
    │  (CDN)        │
    └───────────────┘
```

---

## 🔌 Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Processing** | PySpark | 3.5.0 | Batch processing |
| **ML** | PySpark MLlib | 3.5.0 | Machine learning |
| **API** | FastAPI | 0.104.1 | REST endpoints |
| **Server** | Uvicorn | 0.24.0 | ASGI server |
| **Frontend** | Streamlit | 1.28.2 | Dashboard |
| **Charts** | Plotly | 5.18.0 | Visualizations |
| **Maps** | Folium | 0.15.0 | Geographic viz |
| **Data** | Pandas | 2.1.3 | Data manipulation |
| **Compute** | NumPy | 1.26.2 | Numerical ops |
| **HTTP** | Requests | 2.31.0 | API calls |

---

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `setup.bat` | Installation script |
| `run_spark.bat` | Run PySpark job |
| `run_api.bat` | Run API server |
| `run_frontend.bat` | Run dashboard |
| `.gitignore` | Git exclusions |

---

## 🎯 Design Principles

1. **Modularity**: Each component is independent
2. **Separation of Concerns**: Clear separation of layers
3. **Scalability**: Can be extended to cloud
4. **Maintainability**: Well-commented, organized code
5. **User-Friendly**: Simple setup and run scripts
6. **Documentation**: Comprehensive guides
7. **Error Handling**: Graceful error management
8. **Performance**: Optimized for localhost

---

## 🚀 Future Enhancements

### Short Term
- Add more ML models (GBT, Neural Networks)
- Implement caching for faster API responses
- Add user authentication
- Add email/SMS alerts

### Medium Term
- Real-time streaming with Spark Structured Streaming
- Database integration (PostgreSQL/MongoDB)
- Advanced analytics (time-series forecasting)
- Mobile app

### Long Term
- Cloud deployment (AWS/Azure/GCP)
- Kubernetes orchestration
- Microservices architecture
- Global CDN for frontend
- Multi-region deployment

---

**📊 This architecture is designed to be simple yet scalable, perfect for both learning and production use!**
