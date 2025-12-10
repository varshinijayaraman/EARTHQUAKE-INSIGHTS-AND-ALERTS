# 📤 File Upload Feature Guide

## Overview

The Earthquake Alert System now supports **uploading your own earthquake data files**! You can analyze custom earthquake datasets without running the data processor.

---

## 🎯 How to Upload Files

### Step 1: Access the Dashboard

1. Open your browser to: **http://localhost:8502**
2. Navigate to the **📊 Dashboard** page

### Step 2: Select Upload Mode

In the **left sidebar**, you'll see:

```
📁 Data Source
○ Use Processed Data
○ Upload New File
```

Select **"Upload New File"**

### Step 3: Upload Your CSV File

1. Click the **"Browse files"** button
2. Select your earthquake CSV file
3. The system will:
   - ✅ Validate the file format
   - ✅ Process the data automatically
   - ✅ Calculate severity levels
   - ✅ Generate hazard predictions
   - ✅ Display charts and visualizations

---

## 📋 Required CSV Format

Your CSV file **must** contain these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `sensor_id` | String | Unique sensor identifier | S01, S02, etc. |
| `timestamp` | DateTime | Date and time of earthquake | 2024-01-02 05:22:01 |
| `latitude` | Float | GPS latitude | 34.11 |
| `longitude` | Float | GPS longitude | -117.22 |
| `magnitude` | Float | Earthquake magnitude | 5.4 |
| `depth` | Integer | Depth in kilometers | 12 |
| `region` | String | Geographic region | California |

---

## 📄 Sample CSV Template

```csv
sensor_id,timestamp,latitude,longitude,magnitude,depth,region
S01,2024-01-02 05:22:01,34.11,-117.22,5.4,12,California
S02,2024-01-03 08:15:23,35.68,139.65,6.2,25,Japan
S03,2024-01-05 14:30:45,40.73,-74.00,3.1,8,New York
S04,2024-01-07 22:45:12,37.77,-122.41,4.5,15,San Francisco
S05,2024-01-10 03:20:55,36.20,138.25,7.1,35,Japan
```

### Download Sample Template

In the upload section, click **"📥 Download Sample CSV Template"** to get a ready-to-use template.

---

## 🔄 Automatic Data Processing

When you upload a file, the system **automatically**:

### 1. Validates Columns
- Checks for all required columns
- Shows error if any are missing

### 2. Processes Data
- Converts timestamp to datetime format
- Validates data types

### 3. Calculates Derived Fields

If your CSV doesn't include these, they're calculated automatically:

| Field | Calculation |
|-------|-------------|
| `severity` | Based on magnitude: Low (<4.0), Medium (4.0-6.0), High (>6.0) |
| `hazard_level` | 0=Low, 1=Medium, 2=High, 3=Critical |
| `depth_category` | Shallow (<10km), Intermediate (10-30km), Deep (>30km) |
| `alert_message` | "Low Risk - Monitor", "Medium Risk - Prepare", etc. |
| `hazard_probability` | Normalized risk score (0-1) |
| `prediction` | Same as hazard_level |

---

## ✨ Features Available with Uploaded Data

Once uploaded, you can use **all system features**:

### ✅ Dashboard Page
- View interactive charts
- Apply filters (region, magnitude, severity)
- See key metrics
- Download filtered data

### ✅ Risk Map Page
- Interactive map with markers
- Heatmap visualization
- Color-coded by severity
- Detailed popups on click

### ✅ All Visualizations
- Magnitude distribution
- Severity pie chart
- Region-wise bar chart
- Depth vs Magnitude scatter plot

---

## 🔁 Switching Between Data Sources

You can easily switch between:

### Use Processed Data
- Shows the pre-loaded dataset (30 records)
- Data from `output/alerts_simple.csv`

### Upload New File
- Upload your custom earthquake data
- Data persists across pages until you switch back

**Note:** Uploaded data is stored in memory (session state) and available on all pages (Dashboard, Risk Map) during your session.

---

## 📊 Data Size Recommendations

| File Size | Records | Performance |
|-----------|---------|-------------|
| < 1 MB | < 10,000 | ⚡ Excellent |
| 1-5 MB | 10,000-50,000 | ✅ Good |
| 5-10 MB | 50,000-100,000 | ⚠️ May be slow |
| > 10 MB | > 100,000 | ❌ Not recommended |

For large datasets (>100K records), consider:
- Pre-processing with the data processor script
- Filtering data before upload
- Using the batch processor instead

---

## ❌ Common Errors & Solutions

### Error: "Missing required columns"

**Cause:** Your CSV is missing one or more required columns

**Solution:** 
- Check that your CSV has: sensor_id, timestamp, latitude, longitude, magnitude, depth, region
- Download the sample template and match the format

### Error: "Error reading file"

**Cause:** File format issue (wrong encoding, invalid CSV)

**Solution:**
- Save as UTF-8 encoded CSV
- Remove special characters
- Check for extra commas or quotes

### Error: "Invalid value for magnitude/depth"

**Cause:** Non-numeric values in magnitude or depth columns

**Solution:**
- Ensure magnitude is a number (e.g., 5.4)
- Ensure depth is a number (e.g., 12)
- Remove any text or special characters

### Error: "Cannot parse timestamp"

**Cause:** Timestamp format doesn't match expected format

**Solution:**
- Use format: YYYY-MM-DD HH:MM:SS
- Example: 2024-01-02 05:22:01
- Ensure consistent format throughout

---

## 💡 Tips for Best Results

### 1. Data Quality
- ✅ Remove duplicate records
- ✅ Ensure complete data (no missing values)
- ✅ Validate coordinates (lat: -90 to 90, lng: -180 to 180)
- ✅ Validate magnitude (typically 0-10)

### 2. File Preparation
- Use Excel or Google Sheets to prepare data
- Save as CSV (Comma delimited)
- Keep column names exactly as specified
- Don't include extra header rows

### 3. Testing
- Start with a small sample (5-10 records)
- Verify it loads correctly
- Then upload your full dataset

---

## 📚 Example Use Cases

### 1. Regional Analysis
Upload data for a specific region (e.g., California only) to analyze local earthquake patterns.

### 2. Time Period Analysis
Upload data for a specific time period (e.g., last 6 months) to study recent trends.

### 3. Custom Datasets
Integrate data from external sources or sensors for specialized analysis.

### 4. Historical Comparison
Upload historical data to compare with current patterns.

---

## 🔒 Data Privacy

- ✅ All uploaded files are processed **locally** in your browser
- ✅ No data is sent to external servers
- ✅ Data is stored in session memory (cleared on page refresh)
- ✅ Your data remains completely private

---

## 🆘 Need Help?

### Sample Files
- `data/sample_upload_template.csv` - Basic template
- `data/earthquake_data.csv` - Full example dataset

### Documentation
- See `README.md` for general system documentation
- See `TESTING_GUIDE.md` for testing procedures

---

## 🎯 Quick Start Example

1. **Download the sample template**
   - Click "📥 Download Sample CSV Template" in the upload section

2. **Edit the file**
   - Open in Excel or any text editor
   - Add your earthquake data

3. **Upload**
   - Select "Upload New File"
   - Choose your CSV file
   - View instant results!

---

**🎉 Happy Data Analysis!**

The upload feature makes it easy to analyze any earthquake dataset without technical setup or data processing!
