"""
Streamlit Frontend for Earthquake Alert System
Runs on: http://localhost:8501
Multi-page dashboard with visualizations, maps, and predictions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os
import glob
from datetime import datetime
import folium
from streamlit_folium import folium_static


# Page configuration
st.set_page_config(
    page_title="Earthquake Alert System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = "http://localhost:8000"


# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .alert-low { 
        background: linear-gradient(135deg, #a8ff78 0%, #78ffd6 100%);
        padding: 15px; 
        border-radius: 10px; 
        color: #2c3e50;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .alert-medium { 
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 15px; 
        border-radius: 10px; 
        color: #2c3e50;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .alert-high { 
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%);
        padding: 15px; 
        border-radius: 10px; 
        color: white;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .alert-critical { 
        background: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%);
        padding: 15px; 
        border-radius: 10px; 
        color: white;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    /* Add some modern styling for buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Styling for select boxes and inputs */
    .stSelectbox, .stSlider, .stTextInput {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        border-radius: 10px !important;
        padding: 5px !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Styling for dataframes */
    .stDataFrame {
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Styling for success messages */
    .stSuccess {
        background: linear-gradient(135deg, #a8ff78 0%, #78ffd6 100%) !important;
        color: #2c3e50 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    
    /* Styling for warning messages */
    .stWarning {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%) !important;
        color: #2c3e50 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    
    /* Styling for error messages */
    .stError {
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    
    /* Styling for info messages */
    .stInfo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
        font-weight: bold !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Add some spacing and modern look to sections */
    h1, h2, h3, h4 {
        color: #2c3e50 !important;
    }
    
    h2 {
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
    }
    
    /* Card-like containers */
    .element-container {
        background: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)


def load_data():
    """
    Load earthquake alerts data from output directory
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "output")
        
        # First try to load the simple CSV (single file)
        simple_csv = os.path.join(output_dir, "alerts_simple.csv")
        if os.path.exists(simple_csv):
            df = pd.read_csv(simple_csv)
            return df
        
        # Otherwise try to find CSV files in the earthquake_alerts.csv directory
        csv_dir = os.path.join(output_dir, "earthquake_alerts.csv")
        if os.path.exists(csv_dir):
            csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                return df
        
        return None
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def fetch_from_api(endpoint, params=None):
    """
    Fetch data from FastAPI backend
    """
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.warning(f"API not available. Using local data. ({str(e)})")
        return None


def dashboard_page():
    """
    Main Dashboard Page
    """
    st.markdown('<div class="main-header">Earthquake Alert Dashboard</div>', unsafe_allow_html=True)
    
    # File Upload Section - MOVED TO MAIN AREA for better visibility
    st.subheader("Data Source")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        data_source = st.radio(
            "Choose data source:",
            ["Use Processed Data", "Upload New File"],
            horizontal=True
        )
    
    with col2:
        if data_source == "Upload New File":
            st.info("👇 Upload your CSV file below")
    
    df = None
    
    if data_source == "Upload New File":
        st.markdown("---")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload CSV file",
                type=['csv'],
                help="Upload a CSV file with columns: sensor_id, timestamp, latitude, longitude, magnitude, depth, region"
            )
        
        with col2:
            st.markdown("**Expected CSV format:**")
            st.code("""sensor_id,timestamp,latitude,longitude,magnitude,depth,region
S01,2024-01-02 05:22:01,34.11,-117.22,5.4,12,California""")
            
            # Download sample template
            sample_csv = """sensor_id,timestamp,latitude,longitude,magnitude,depth,region
S01,2024-01-02 05:22:01,34.11,-117.22,5.4,12,California
S02,2024-01-03 08:15:23,35.68,139.65,6.2,25,Japan
S03,2024-01-05 14:30:45,40.73,-74.00,3.1,8,New York
S04,2024-01-07 22:45:12,37.77,-122.41,4.5,15,San Francisco
S05,2024-01-10 03:20:55,36.20,138.25,7.1,35,Japan"""
            
            st.download_button(
                label="Download Sample CSV",
                data=sample_csv,
                file_name="earthquake_sample.csv",
                mime="text/csv",
                help="Download this template"
            )
        
        if uploaded_file is not None:
            # Show upload progress
            st.info("Processing uploaded file through Spark...")
            
            # Create a progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Reading CSV file
                status_text.text("Reading CSV file...")
                progress_bar.progress(10)
                
                # Read uploaded file with pandas first (to validate)
                pandas_df = pd.read_csv(uploaded_file)
                status_text.text("File read successfully")
                progress_bar.progress(20)
                
                # Validate required columns
                status_text.text("Validating data structure...")
                progress_bar.progress(30)
                
                required_cols = ['sensor_id', 'timestamp', 'latitude', 'longitude', 'magnitude', 'depth', 'region']
                missing_cols = [col for col in required_cols if col not in pandas_df.columns]
                
                if missing_cols:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"Missing required columns: {', '.join(missing_cols)}")
                    st.info("Required columns: sensor_id, timestamp, latitude, longitude, magnitude, depth, region")
                    return
                
                # Step 2: Save temporary file for Spark processing
                status_text.text("Saving temporary file for Spark processing...")
                progress_bar.progress(40)
                
                import tempfile
                import os
                temp_dir = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir, "uploaded_data.csv")
                pandas_df.to_csv(temp_file_path, index=False)
                
                # Step 3: Process through Spark
                status_text.text("Processing through Spark (check Spark Web UI at http://localhost:4040)...")
                progress_bar.progress(50)
                
                # Run Spark processor on uploaded data
                import subprocess
                import sys
                import os
                
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                spark_processor = os.path.join(base_dir, "spark_job", "upload_processor.py")
                
                # Run the Spark processor
                cmd = [sys.executable, spark_processor, temp_file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_dir)
                
                # Clean up temporary file
                try:
                    os.remove(temp_file_path)
                    os.rmdir(temp_dir)
                except:
                    pass
                
                if result.returncode != 0:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"Spark processing failed: {result.stderr}")
                    return
                
                progress_bar.progress(80)
                status_text.text("Spark processing complete")
                
                # Step 4: Load processed results
                status_text.text("Loading processed results...")
                progress_bar.progress(90)
                
                # Load the processed data
                output_dir = os.path.join(base_dir, "output")
                processed_csv = os.path.join(output_dir, "uploaded_alerts_simple.csv")
                
                if os.path.exists(processed_csv):
                    df = pd.read_csv(processed_csv)
                else:
                    # Fallback to original data
                    df = pandas_df
                    # Add missing columns if needed
                    if 'severity' not in df.columns:
                        df['severity'] = pd.cut(
                            df['magnitude'],
                            bins=[-float('inf'), 4.0, 6.0, float('inf')],
                            labels=['Low', 'Medium', 'High']
                        )
                    
                    if 'hazard_level' not in df.columns:
                        df['hazard_level'] = pd.cut(
                            df['magnitude'],
                            bins=[-float('inf'), 4.0, 5.5, 7.0, float('inf')],
                            labels=[0, 1, 2, 3]
                        ).astype(int)
                    
                    if 'depth_category' not in df.columns:
                        df['depth_category'] = pd.cut(
                            df['depth'],
                            bins=[-float('inf'), 10, 30, float('inf')],
                            labels=['Shallow', 'Intermediate', 'Deep']
                        )
                    
                    if 'alert_message' not in df.columns:
                        alert_map = {
                            0: "Low Risk - Monitor",
                            1: "Medium Risk - Prepare",
                            2: "High Risk - Alert",
                            3: "Critical Risk - Evacuate"
                        }
                        df['alert_message'] = df['hazard_level'].map(alert_map)
                    
                    if 'hazard_probability' not in df.columns:
                        # Simple probability based on magnitude
                        df['hazard_probability'] = (df['magnitude'] - df['magnitude'].min()) / (df['magnitude'].max() - df['magnitude'].min())
                    
                    if 'prediction' not in df.columns:
                        df['prediction'] = df['hazard_level']
                
                # Convert timestamp to datetime
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Store in session state for other pages
                st.session_state.uploaded_data = df
                
                # Complete progress
                status_text.text("Processing complete!")
                progress_bar.progress(100)
                
                # Show success message
                st.success(f"Successfully processed {len(df)} records through Spark! View the Spark Web UI at http://localhost:4040")
                
                # Add a small delay to show the completed progress bar
                import time
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"Error processing file: {str(e)}")
                return
        else:
            st.warning("Please upload a CSV file to view earthquake data")
            return
    else:
        # Load processed data
        # Clear uploaded data from session state
        if 'uploaded_data' in st.session_state:
            st.session_state.uploaded_data = None
        
        df = load_data()
        
        if df is None:
            st.error("No processed data available. Please run the data processor first!")
            st.code("python spark_job/simple_processor.py")
            st.info("🔁 Or switch to 'Upload New File' above to upload your own data.")
            return
        else:
            st.success(f"Loaded {len(df)} records from processed data")
    
    st.markdown("---")
    
    # Filters in main area instead of sidebar
    st.header("Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        regions = ["All"] + sorted(df['region'].unique().tolist())
        selected_region = st.selectbox("Select Region", regions)
    
    with col2:
        min_mag, max_mag = st.slider(
            "Magnitude Range",
            float(df['magnitude'].min()),
            float(df['magnitude'].max()),
            (float(df['magnitude'].min()), float(df['magnitude'].max()))
        )
    
    with col3:
        severity_options = ["All"] + sorted(df['severity'].unique().tolist())
        selected_severity = st.selectbox("Severity Level", severity_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    filtered_df = filtered_df[
        (filtered_df['magnitude'] >= min_mag) &
        (filtered_df['magnitude'] <= max_mag)
    ]
    
    if selected_severity != "All":
        filtered_df = filtered_df[filtered_df['severity'] == selected_severity]
    
    # Key Metrics
    st.header("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Earthquakes",
            len(filtered_df),
            delta=f"{len(filtered_df) - len(df)} from total"
        )
    
    with col2:
        avg_mag = filtered_df['magnitude'].mean()
        st.metric(
            "Average Magnitude",
            f"{avg_mag:.2f}",
            delta=f"{avg_mag - df['magnitude'].mean():.2f}"
        )
    
    with col3:
        max_mag = filtered_df['magnitude'].max()
        st.metric(
            "Max Magnitude",
            f"{max_mag:.2f}",
            delta="Highest"
        )
    
    with col4:
        high_risk = len(filtered_df[filtered_df['severity'] == 'High'])
        st.metric(
            "High Risk Events",
            high_risk,
            delta=f"{(high_risk/len(filtered_df)*100):.1f}%"
        )
    
    # Charts
    st.header("📈 Data Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Magnitude Distribution
        st.subheader("Magnitude Distribution")
        fig_mag = px.histogram(
            filtered_df,
            x='magnitude',
            nbins=20,
            color='severity',
            title="Earthquake Magnitude Distribution",
            color_discrete_map={
                'Low': '#90EE90',
                'Medium': '#FFD700',
                'High': '#FF6347'
            }
        )
        st.plotly_chart(fig_mag, use_container_width=True)
    
    with col2:
        # Severity Count
        st.subheader("Severity Distribution")
        severity_counts = filtered_df['severity'].value_counts()
        fig_severity = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            title="Earthquakes by Severity Level",
            color=severity_counts.index,
            color_discrete_map={
                'Low': '#90EE90',
                'Medium': '#FFD700',
                'High': '#FF6347'
            }
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Region-wise Earthquakes
        st.subheader("Earthquakes by Region")
        region_counts = filtered_df['region'].value_counts().head(10)
        fig_region = px.bar(
            x=region_counts.values,
            y=region_counts.index,
            orientation='h',
            title="Top Regions by Earthquake Count",
            labels={'x': 'Count', 'y': 'Region'},
            color=region_counts.values,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col4:
        # Depth vs Magnitude
        st.subheader("Depth vs Magnitude")
        fig_scatter = px.scatter(
            filtered_df,
            x='depth',
            y='magnitude',
            color='severity',
            size='magnitude',
            hover_data=['region', 'sensor_id'],
            title="Earthquake Depth vs Magnitude",
            color_discrete_map={
                'Low': '#90EE90',
                'Medium': '#FFD700',
                'High': '#FF6347'
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Alerts Table
    st.header("🚨 Recent Earthquake Alerts")
    
    # Display table
    display_cols = [
        'sensor_id', 'timestamp', 'region', 'magnitude',
        'depth', 'severity', 'alert_message', 'hazard_probability'
    ]
    
    st.dataframe(
        filtered_df[display_cols].head(20),
        use_container_width=True,
        hide_index=True
    )
    
    # Download data
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=csv,
        file_name=f"earthquake_alerts_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


def risk_map_page():
    """
    Risk Zone Map Page
    """
    st.markdown('<div class="main-header">Earthquake Risk Zone Map</div>', unsafe_allow_html=True)
    
    # Check if we're using uploaded data from session state
    if 'uploaded_data' in st.session_state and st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        st.info("📄 Using uploaded data")
    else:
        df = load_data()
    
    if df is None:
        st.error("⚠️ No data available. Please run the data processor or upload a file from the Dashboard!")
        return
    
    st.header("Interactive Risk Map")
    
    # Map controls
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("Map Settings")
        
        show_markers = st.checkbox("Show Markers", value=True)
        show_heatmap = st.checkbox("Show Heatmap", value=False)
        
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=['Low', 'Medium', 'High'],
            default=['Low', 'Medium', 'High']
        )
    
    with col1:
        # Create base map
        m = folium.Map(
            location=[df['latitude'].mean(), df['longitude'].mean()],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Filter data
        map_df = df[df['severity'].isin(severity_filter)]
        
        # Add markers
        if show_markers:
            for idx, row in map_df.iterrows():
                # Color based on severity
                if row['severity'] == 'Low':
                    color = 'green'
                    icon = 'info-sign'
                elif row['severity'] == 'Medium':
                    color = 'orange'
                    icon = 'warning-sign'
                else:
                    color = 'red'
                    icon = 'exclamation-sign'
                
                # Create popup
                popup_html = f"""
                <div style="font-family: Arial; width: 200px;">
                    <h4 style="color: {color};">{row['region']}</h4>
                    <b>Sensor:</b> {row['sensor_id']}<br>
                    <b>Magnitude:</b> {row['magnitude']}<br>
                    <b>Depth:</b> {row['depth']} km<br>
                    <b>Severity:</b> {row['severity']}<br>
                    <b>Alert:</b> {row['alert_message']}<br>
                    <b>Time:</b> {row['timestamp']}
                </div>
                """
                
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{row['region']} - Mag: {row['magnitude']}",
                    icon=folium.Icon(color=color, icon=icon)
                ).add_to(m)
        
        # Add heatmap
        if show_heatmap:
            from folium.plugins import HeatMap
            
            heat_data = [
                [row['latitude'], row['longitude'], row['magnitude']]
                for idx, row in map_df.iterrows()
            ]
            
            HeatMap(
                heat_data,
                min_opacity=0.3,
                radius=15,
                blur=20,
                gradient={
                    0.0: 'blue',
                    0.5: 'yellow',
                    0.7: 'orange',
                    1.0: 'red'
                }
            ).add_to(m)
        
        # Display map
        folium_static(m, width=1000, height=600)
    
    # Statistics by region
    st.header("Regional Statistics")
    
    region_stats = df.groupby('region').agg({
        'magnitude': ['mean', 'max', 'count'],
        'depth': 'mean',
        'severity': lambda x: x.value_counts().to_dict()
    }).round(2)
    
    st.dataframe(region_stats, use_container_width=True)


def prediction_page():
    """
    ML Prediction Page
    """
    st.markdown('<div class="main-header">Earthquake Hazard Prediction</div>', unsafe_allow_html=True)
    
    st.header("Predict Earthquake Hazard Level")
    
    st.write("""
    Enter earthquake parameters below to predict the hazard level using our machine learning model.
    The model uses **Random Forest Classifier** trained on historical earthquake data.
    """)
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        magnitude = st.number_input(
            "Magnitude",
            min_value=0.0,
            max_value=10.0,
            value=5.2,
            step=0.1,
            help="Earthquake magnitude on Richter scale"
        )
        
        depth = st.number_input(
            "Depth (km)",
            min_value=0.0,
            max_value=700.0,
            value=10.0,
            step=1.0,
            help="Depth of earthquake hypocenter"
        )
    
    with col2:
        regions = [
            "California", "Japan", "San Francisco", "Los Angeles",
            "New York", "Arizona", "Illinois", "Nevada"
        ]
        
        region = st.selectbox(
            "Region",
            options=regions,
            help="Geographic region"
        )
        
        st.write("")
        st.write("")
        predict_button = st.button("Predict Hazard Level", type="primary", use_container_width=True)
    
    # Make prediction
    if predict_button:
        with st.spinner("Analyzing earthquake parameters..."):
            # Try API first
            result = fetch_from_api(
                "/predict",
                params={
                    "magnitude": magnitude,
                    "depth": depth,
                    "region": region
                }
            )
            
            if result:
                st.success("✅ Prediction Complete!")
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Hazard Level", result['hazard_level'])
                
                with col2:
                    st.metric("Hazard Score", f"{result['hazard_score']:.3f}")
                
                with col3:
                    # Color-coded risk indicator
                    color = result['risk_indicator']
                    st.markdown(f"""
                    <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center;">
                        <h3 style="color: white; margin: 0;">Risk: {color.upper()}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Alert message
                st.info(f"📢 **Alert:** {result['message']}")
                
                # Input summary
                st.subheader("Input Parameters")
                st.json(result['input_data'])
                
            else:
                st.error("❌ Unable to get prediction. Make sure the API is running.")
                st.code("python backend/api.py")


def spark_ui_page():
    """
    Spark Web UI Information Page
    """
    st.markdown('<div class="main-header">Spark Web UI</div>', unsafe_allow_html=True)
    
    st.header("Access Spark Web UI")
    
    st.write("""
    The Spark Web UI provides detailed information about your Spark jobs, including:
    - **Jobs**: All Spark jobs with their status
    - **Stages**: Breakdown of job stages
    - **Storage**: RDD and DataFrame caching information
    - **Environment**: Spark configuration
    - **Executors**: Executor metrics and logs
    - **SQL**: SQL query execution plans
    """)
    
    st.info("🌐 **Spark Web UI URL:** http://localhost:4040")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            '<a href="http://localhost:4040" target="_blank"><button style="background-color: #FF4B4B; color: white; padding: 12px 24px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">🚀 Open Spark Web UI</button></a>',
            unsafe_allow_html=True
        )
    
    st.write("---")
    
    st.warning("⚠️ **Note:** Spark Web UI is only available when a Spark job is running or has just completed.")
    
    st.code("""
# To run the Spark job and start the Web UI:
python spark_job/earthquake_processor.py

# The Spark Web UI will be available at http://localhost:4040
# Keep the terminal open to keep the Web UI running
    """)


def main():
    """
    Main application
    """
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Risk Map", "Prediction", "Spark Web UI"]
    )
    

    
    # Route to pages
    if page == "Dashboard":
        dashboard_page()
    elif page == "Risk Map":
        risk_map_page()
    elif page == "Prediction":
        prediction_page()
    elif page == "Spark Web UI":
        spark_ui_page()


if __name__ == "__main__":
    main()
