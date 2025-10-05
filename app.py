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
    page_title="Weather Air Quality Forecasting",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded"
)

# Hide Streamlit branding
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# FIXED CSS - All sidebar and selectbox colors corrected
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background-color: white !important;
    }
    
    /* SIDEBAR - Light background with dark text */
    .stApp [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #cbd5e1 !important;
    }
    
    /* All sidebar text elements - BLACK */
    [data-testid="stSidebar"] * {
        color: #0f172a !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown h4 {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span,
    [data-testid="stSidebar"] .stMarkdown strong {
        color: #1e293b !important;
    }
    
    /* SELECTBOX - White box with black text */
    [data-testid="stSidebar"] .stSelectbox label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid #cbd5e1 !important;
        color: #0f172a !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox input {
        color: #0f172a !important;
    }
    
    /* Selectbox dropdown menu */
    [data-baseweb="popover"] {
        background-color: white !important;
    }
    
    [role="listbox"] li {
        color: #0f172a !important;
        background-color: white !important;
    }
    
    [role="listbox"] li:hover {
        background-color: #f1f5f9 !important;
    }
    
    /* Sidebar captions */
    [data-testid="stSidebar"] .stCaption {
        color: #64748b !important;
        font-size: 0.85rem !important;
    }
    
    /* Button styling */
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
    
    .alert-critical h3, .alert-warning h3, .alert-good h3 {
        margin-top: 0;
        font-weight: 600;
        color: #1e293b !important;
    }
    
    .alert-critical p, .alert-warning p, .alert-good p {
        color: #334155 !important;
    }
    
    h1, h2, h3, h4 {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #334155 !important;
    }
</style>
""", unsafe_allow_html=True)

# Location database (shortened for demo)
LOCATIONS = {
    "USA - California - Los Angeles": {"lat": 34.0522, "lon": -118.2437, "timezone": "America/Los_Angeles"},
    "USA - California - San Francisco": {"lat": 37.7749, "lon": -122.4194, "timezone": "America/Los_Angeles"},
    "USA - New York - New York City": {"lat": 40.7128, "lon": -74.0060, "timezone": "America/New_York"},
    "USA - Illinois - Chicago": {"lat": 41.8781, "lon": -87.6298, "timezone": "America/Chicago"},
    "Canada - Ontario - Toronto": {"lat": 43.6532, "lon": -79.3832, "timezone": "America/Toronto"},
    "Canada - British Columbia - Vancouver": {"lat": 49.2827, "lon": -123.1207, "timezone": "America/Vancouver"},
    "UK - England - London": {"lat": 51.5074, "lon": -0.1278, "timezone": "Europe/London"},
    "UK - England - Manchester": {"lat": 53.4808, "lon": -2.2426, "timezone": "Europe/London"},
    "India - Maharashtra - Mumbai": {"lat": 19.0760, "lon": 72.8777, "timezone": "Asia/Kolkata"},
    "India - Maharashtra - Pune": {"lat": 18.5204, "lon": 73.8567, "timezone": "Asia/Kolkata"},
    "India - Delhi - New Delhi": {"lat": 28.6139, "lon": 77.2090, "timezone": "Asia/Kolkata"},
    "Japan - Kanto - Tokyo": {"lat": 35.6762, "lon": 139.6503, "timezone": "Asia/Tokyo"},
    "Australia - New South Wales - Sydney": {"lat": -33.8688, "lon": 151.2093, "timezone": "Australia/Sydney"},
}

# Main header
st.markdown("""
<div class="main-header">
    <h1>🛰️ Weather Air Quality Forecasting System</h1>
    <p style="font-size: 1.1em; margin-top: 0.5rem;">
        NASA TEMPO Satellite Data • Global Coverage • AI-Powered Predictions
    </p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR - Fixed filtering logic
st.sidebar.title("🌍 Location Settings")
st.sidebar.markdown("### Search Location")

# Get sorted locations and countries
sorted_locations = sorted(LOCATIONS.keys())
countries = sorted(set([loc.split(" - ")[0] for loc in sorted_locations]))

# Country filter with fixed logic
selected_country = st.sidebar.selectbox(
    "🌐 Select Country", 
    ["All Countries"] + countries,
    key="country_selector"
)

# Filter locations based on country selection
if selected_country == "All Countries":
    filtered_locations = sorted_locations
else:
    filtered_locations = [loc for loc in sorted_locations if loc.startswith(selected_country)]
    # Safety check
    if not filtered_locations:
        st.sidebar.error(f"No cities found for {selected_country}")
        filtered_locations = sorted_locations

# City selector
selected_location = st.sidebar.selectbox(
    "📍 Select City", 
    filtered_locations,
    key="city_selector"
)

location_data = LOCATIONS[selected_location]

st.sidebar.markdown("---")

# Refresh button
if st.sidebar.button("🔄 Refresh All Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")

# Data sources info
st.sidebar.markdown("### 📊 Data Sources")
st.sidebar.markdown("""
- **TEMPO Satellite**: Hourly NO₂
- **OpenAQ**: Ground sensors  
- **OpenWeather**: Meteorology
- **ML Model**: Random Forest
""")

st.sidebar.markdown("---")

# Statistics
st.sidebar.markdown(f"**Total Locations**: {len(LOCATIONS)}")
st.sidebar.markdown(f"**Countries**: {len(countries)}")
st.sidebar.markdown(f"**Selected**: {selected_location.split(' - ')[-1]}")

# Main content
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

# AQI alert
st.markdown("""
<div class="alert-good">
    <h3>🟢 Current AQI: 45 - Good</h3>
    <p style="margin-bottom: 0;">Air quality is satisfactory. Enjoy outdoor activities!</p>
</div>
""", unsafe_allow_html=True)

# Demo chart
st.header("🔮 Air Quality Trends")
dates = pd.date_range(start=datetime.now() - timedelta(hours=24), end=datetime.now(), freq='H')
values = 25 + 10 * np.sin(np.linspace(0, 4*np.pi, len(dates))) + np.random.normal(0, 3, len(dates))

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates, 
    y=values,
    mode='lines+markers',
    name='NO₂ Levels',
    line=dict(color='#667eea', width=3),
    marker=dict(size=6, color='#667eea')
))
fig.update_layout(
    title="24-Hour NO₂ Concentration",
    xaxis_title="Time",
    yaxis_title="NO₂ (ppb)",
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter')
)
st.plotly_chart(fig, use_container_width=True)

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.sidebar.caption(f"📍 Monitoring: {selected_location}")
st.sidebar.caption(f"🌐 Lat: {location_data['lat']:.4f}°, Lon: {location_data['lon']:.4f}°")
