import streamlit as st
import folium
from folium.plugins import TimestampedGeoJson
from streamlit_folium import folium_static
import pandas as pd
from datetime import datetime, timedelta

# Sample historical data
historical_data = {
    "timestamp": [
        datetime(2022, 1, 1, 12, 0, 0),
        datetime(2022, 1, 1, 12, 30, 0),
        datetime(2022, 1, 1, 13, 0, 0),
        datetime(2022, 1, 1, 14, 0, 0),
    ],
    "latitude": [11.0178, 11.0205, 11.016,11.0123],
    "longitude": [76.9565, 76.9665, 76.978,76.9456],
    "value": [15, 25, 20,25],
}

df = pd.DataFrame(historical_data)

# Streamlit app
st.title("Interactive Map with Historical Data")

# Initial map center
map_center = [11.018, 76.962]

# Create an interactive map
m = folium.Map(location=map_center, zoom_start=14)

# Convert the historical data to GeoJSON format
features = []
for i, row in df.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["longitude"], row["latitude"]],
        },
        "properties": {
            "time": row["timestamp"].isoformat(),
            "style": {"color": "red", "icon": "marker"},
            "iconstyle": {
                "iconUrl": "https://getbootstrap.com/docs/3.3/assets/img/bootstrap-stack.png",
                "iconSize": [38, 38],
                "iconAnchor": [22, 94],
                "popupAnchor": [-3, -76],
                "className": "dot",
            },
            "value": row["value"],
        },
    }
    features.append(feature)

# Create a TimestampedGeoJson layer
tgj = TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="PT15M",  # Update every 15 minutes
    duration="PT15M",  # Display data for 15 minutes
    add_last_point=True,
    auto_play=True,
    loop=True,
    max_speed=1,
    loop_button=True,
    date_options="YYYY/MM/DD HH:mm:ss",
    time_slider_drag_update=True,
)

# Add the TimestampedGeoJson layer to the map
tgj.add_to(m)

# Display the map in the Streamlit app
folium_static(m)
