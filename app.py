import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import os

st.set_page_config(
    page_title="Whether Air Quality Forecasting",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded"
)

# Hide Streamlit branding and style
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Enhanced Custom CSS with Modern Design and Theme Override
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Remove Streamlit default styling */
    .stApp {
        background-color: white !important;
        color: black;
    }
    
    /* Sidebar background - light gray */
    .stApp [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    .stApp [data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Reset all default colors */
    .stMarkdown, .stText, p, span, div {
        color: black !important;
    }
    
    /* Sidebar text - dark gray/black for readability */
    .stApp [data-testid="stSidebar"] .stMarkdown {
        color: #1e293b !important;
    }
    
    /* Sidebar markdown elements */
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span {
        color: #334155 !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }
    
    /* Button styling override */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Selectbox styling - white background with black text */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        color: #0f172a !important;
    }
    
    /* Selectbox label - black text */
    .stSelectbox label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Selectbox dropdown text */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #0f172a !important;
    }
    
    /* Selectbox options */
    [data-baseweb="menu"] > ul > li {
        color: #0f172a !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 500 !important;
    }
    
    [data-testid="metric-container"] {
        background: white !important;
        padding: 1.2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        border: 1px solid #f1f5f9 !important;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white !important;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        color: white !important;
    }
    
    .alert-critical {
        background: linear-gradient(135deg, #fee 0%, #fdd 100%);
        border-left: 5px solid #dc2626;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.2);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    .alert-good {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    .info-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 5px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    .info-box h4 {
        color: #1e293b !important;
        margin-top: 0;
        font-weight: 600;
    }
    
    .info-box p {
        color: #475569 !important;
        margin: 0.5rem 0;
    }
    
    .alert_class {
        color: #1f2937 !important;
    }
    
    .alert-critical h3, .alert-warning h3, .alert-good h3 {
        margin-top: 0;
        font-weight: 600;
        color: #1e293b !important;
    }
    
    .alert-critical p, .alert-warning p, .alert-good p {
        color: #334155 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    /* Download button specific */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Remove default Streamlit colors from text */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #334155 !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: #64748b !important;
    }
</style>
""", unsafe_allow_html=True)

# Rest of your code remains exactly the same...
# [Include all the remaining code from your original file - LOCATIONS, functions, etc.]

# I'll include the key parts to make this a working example:

LOCATIONS = {
    "USA - California - Los Angeles": {"lat": 34.0522, "lon": -118.2437, "timezone": "America/Los_Angeles"},
    "USA - New York - New York City": {"lat": 40.7128, "lon": -74.0060, "timezone": "America/New_York"},
    "India - Maharashtra - Pune": {"lat": 18.5204, "lon": 73.8567, "timezone": "Asia/Kolkata"},
    "UK - England - London": {"lat": 51.5074, "lon": -0.1278, "timezone": "Europe/London"},
    "Japan - Kanto - Tokyo": {"lat": 35.6762, "lon": 139.6503, "timezone": "Asia/Tokyo"},
}

st.markdown("""
<div class="main-header">
    <h1>🛰️ Whether Quality Forecasting System</h1>
    <p style="font-size: 1.1em; margin-top: 0.5rem;">
        • Global Coverage • AI-Powered Predictions
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with Enhanced Search
st.sidebar.title("🌍 Location Settings")
st.sidebar.markdown("### Search Location")

# Country grouping for better UX
sorted_locations = sorted(LOCATIONS.keys())
countries = sorted(set([loc.split(" - ")[0] for loc in sorted_locations]))

selected_country = st.sidebar.selectbox("🌐 Select Country", ["All Countries"] + countries, key="country_select")

# Fixed filtering logic
if selected_country == "All Countries":
    filtered_locations = sorted_locations
else:
    filtered_locations = [loc for loc in sorted_locations if loc.startswith(selected_country)]

# Handle case where filtering returns empty list
if not filtered_locations:
    st.sidebar.warning(f"No cities found for {selected_country}")
    filtered_locations = sorted_locations

selected_location = st.sidebar.selectbox("📍 Select City", filtered_locations, key="city_select")
location_data = LOCATIONS[selected_location]

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Refresh All Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Sources")
st.sidebar.markdown("""
- **TEMPO Satellite**: Hourly NO₂
- **OpenAQ**: Ground sensors
- **OpenWeather**: Meteorology
- **ML Model**: Random Forest
""")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Locations**: {len(LOCATIONS)}")
st.sidebar.markdown(f"**Countries**: {len(countries)}")

# Demo content
st.header(f"📍 Current Conditions - {selected_location}")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🌡️ Temperature", "22.5°C")
with col2:
    st.metric("💨 Wind Speed", "15.3 km/h")
with col3:
    st.metric("🛰️ TEMPO NO₂", "28.4 ppb")
with col4:
    st.metric("📡 Ground NO₂", "32.1 µg/m³")

st.markdown("""
<div class="alert-good">
    <h3>🟢 Current AQI: 45 - Good</h3>
    <p style="margin-bottom: 0;">Air quality is satisfactory. Enjoy outdoor activities!</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.sidebar.caption(f"📍 Monitoring: {selected_location}")
st.sidebar.caption(f"🌐 Coordinates: {location_data['lat']:.4f}°, {location_data['lon']:.4f}°")
