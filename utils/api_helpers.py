# cleaner_skies_dashboard.py
import streamlit as st
import pandas as pd
import requests

# ------------------------
# Configuration
# ------------------------
CITY_COORDS = {
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "London": {"lat": 51.5074, "lon": -0.1278},
}

OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_KEY"
NASA_API_KEY = "YOUR_NASA_KEY"

st.set_page_config(layout="wide")
st.title("🛰️ Cleaner Skies: Air Quality Dashboard")

# ------------------------
# Helper functions
# ------------------------
def fetch_json(url):
    """Fetch JSON safely with error handling."""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning(f"API fetch error: {e}")
        return {}

def get_weather_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = fetch_json(url)
    if data and "main" in data:
        return {
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "windspeed": data['wind']['speed']*3.6,  # m/s → km/h
            "condition": data['weather'][0]['description']
        }
    return {}

def get_openaq_data(city, parameter="no2", limit=50):
    city_query = city.replace(" ", "%20")
    url = f"https://api.openaq.org/v2/latest?city={city_query}&parameter={parameter}&limit={limit}"
    data = fetch_json(url)
    
    if "results" not in data or len(data["results"]) == 0:
        return pd.DataFrame()
    
    df = pd.json_normalize(data["results"])
    
    # Explode measurements
    if 'measurements' in df.columns:
        df = df.explode('measurements')
        df['value'] = df['measurements'].apply(lambda x: x.get('value') if x else None)
        df['unit'] = df['measurements'].apply(lambda x: x.get('unit') if x else None)
        df['datetime'] = df['measurements'].apply(lambda x: pd.to_datetime(x.get('lastUpdated')) if x else pd.NaT)
    
    # Coordinates
    if 'coordinates' in df.columns:
        df['coordinates.latitude'] = df['coordinates'].apply(lambda x: x.get('latitude') if x else None)
        df['coordinates.longitude'] = df['coordinates'].apply(lambda x: x.get('longitude') if x else None)
    
    # Keep relevant columns
    return df[['location','value','unit','datetime','coordinates.latitude','coordinates.longitude']]

# ------------------------
# Sidebar: City selection
# ------------------------
st.sidebar.header("Select Location")
city_selection = st.sidebar.selectbox("Choose a City", list(CITY_COORDS.keys()))
coords = CITY_COORDS[city_selection]

# ------------------------
# Fetch data
# ------------------------
@st.cache_data
def load_data(city, coords):
    weather = get_weather_data(coords['lat'], coords['lon'])
    ground_df = get_openaq_data(city)
    return weather, ground_df

weather_data, openaq_df = load_data(city_selection, coords)

# ------------------------
# KPIs
# ------------------------
st.header(f"Air Quality in {city_selection}")
k1, k2, k3 = st.columns(3)
k1.metric("Temperature", f"{weather_data.get('temperature','N/A')} °C")
k2.metric("Humidity", f"{weather_data.get('humidity','N/A')} %")
latest_no2 = openaq_df['value'].iloc[0] if not openaq_df.empty else None
k3.metric("Latest Ground NO₂", f"{latest_no2 if latest_no2 is not None else 'N/A'} µg/m³")

# ------------------------
# Map
# ------------------------
st.subheader("Ground NO₂ Map")
if not openaq_df.empty and 'coordinates.latitude' in openaq_df.columns:
    map_df = openaq_df[['coordinates.latitude','coordinates.longitude','value']].rename(
        columns={'coordinates.latitude':'lat','coordinates.longitude':'lon'}
    )
    st.map(map_df)
else:
    st.info("No ground location data available for map.")

# ------------------------
# Line chart (time series)
# ------------------------
st.subheader("Ground NO₂ Time Series")
if not openaq_df.empty and 'datetime' in openaq_df.columns:
    ts = openaq_df.set_index('datetime')['value'].resample('1H').mean()
    st.line_chart(ts)
else:
    st.info("No time series data available.")

# ------------------------
# Bar chart (by location)
# ------------------------
st.subheader("Latest NO₂ by Location")
if not openaq_df.empty and 'location' in openaq_df.columns:
    st.bar_chart(openaq_df.groupby('location')['value'].mean())
else:
    st.info("No location-based data available.")

# ------------------------
# Raw data
# ------------------------
with st.expander("Show raw OpenAQ data"):
    if not openaq_df.empty:
        st.dataframe(openaq_df)
    else:
        st.write("No data available.")
