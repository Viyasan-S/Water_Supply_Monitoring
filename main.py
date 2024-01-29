import streamlit as st
import folium
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import pyrebase
import geopandas as gpd  # Import GeoPandas for handling GeoJSON data

# Load Coimbatore GeoJSON file
coimbatore_geojson_path = "coimbatore.geojson"
coimbatore_gdf = gpd.read_file(coimbatore_geojson_path)

# Streamlit Configuration
st.set_page_config(
    page_title="Water Supply Network Tool",
    page_icon=":speech_balloon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Firebase Configuration
firebase_config = {
    "apiKey": "AIzaSyCDIJzy-F8CcLlUW8pOMUIUugp0_sEghxw",
    "authDomain": "swathi-388ae.firebaseapp.com",
    "projectId": "swathi-388ae",
    "databaseURL": "https://console.firebase.google.com/project/swathi-388ae/database/swathi-388ae-default-rtdb/data/~2F",
    "storageBucket": "swathi-388ae.appspot.com",
    "messagingSenderId": "350881361332",
    "appId": "1:350881361332:web:8df873605d84c7ffee16e1",
    "measurementId": "G-WHDCT99T1P"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)

# Get Firebase Authentication
auth = firebase.auth()

# Streamlit UI
if "user" not in st.session_state:
    st.session_state.user = None

page = None

if st.session_state.user is None:
    page = st.sidebar.selectbox("Select Page", ["Login", "Sign Up"])
else:
    page = st.sidebar.selectbox("Select Page", ["Dashboard", "Logout"])

if page == "Login":
    st.title("Water Supply Network Tool - Login")
    email_login = st.text_input("Email:", key="login_email")  # Add a unique key here
    password_login = st.text_input("Password:", type="password", key="login_password")  # Add a unique key here

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email_login, password_login)
            st.session_state.user = user
            st.success("Login successful!")
            st.sidebar.success(f"Logged in as {user['email']}")
        except auth.AuthError as e:
            st.error(f"Authentication failed: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif page == "Sign Up":
    st.title("Water Supply Network Tool - Sign Up")
    email_signup = st.text_input("Email:", key="signup_email")  # Add a unique key here
    password_signup = st.text_input("Password:", type="password", key="signup_password")  # Add a unique key here

    if st.button("Sign Up"):
        try:
            user = auth.create_user_with_email_and_password(email_signup, password_signup)
            st.success("Sign up successful! Please log in.")
        except auth.AuthError as e:
            st.error(f"Sign up failed: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif page == "Logout":
    st.session_state.user = None
    st.sidebar.success("Logged out successfully!")

if st.session_state.user:

    # Sample data for water supply network
    cities = {
        "Coimbatore": [11.0178, 76.9565],
        "Peelamedu": [11.0205, 76.9665],
        "Gandhipuram": [11.016, 76.978],
        "Kaundampalyaam": [11.0123, 76.9456],
    }

    pipes = [
        {"start": "Coimbatore", "end": "Peelamedu"},
        {"start": "Peelamedu", "end": "Gandhipuram"},
        {"start": "Gandhipuram", "end": "Coimbatore"},
        {"start": "Coimbatore", "end": "Kaundampalyaam"},
        {"start": "Kaundampalyaam", "end": "Gandhipuram"},
    ]

    tanks = {
        "Coimbatore": [11.0168, 76.9558],
        "Peelamedu": [11.0205, 76.9665],
        "Gandhipuram": [11.016, 76.978],
        "Kaundampalyaam": [11.0123, 76.9456],
    }
    middle_pipe_coords=[
        (cities["Coimbatore"][0] + cities["Kaundampalyaam"][0]) / 2,
        (cities["Coimbatore"][1] + cities["Kaundampalyaam"][1]) /2,
    ]
    middle_pipe_coords1=[
        (cities["Gandhipuram"][0] + cities["Kaundampalyaam"][0]) / 2,
        (cities["Gandhipuram"][1] + cities["Kaundampalyaam"][1]) /2,
    ]

    sensors = {
        "FlowSensor": [11.018, 76.958],
        "MoistureSensor": [11.020, 76.968],
        "PressureSensor": [11.017, 76.974],
        "FlowSensorB": middle_pipe_coords,
        "MoistureSensorB": middle_pipe_coords1,
    }

    # Sample data for water flow simulation
    tanks_flow = {
        "Tank A": [11.0168, 76.9558],
        "Tank B": [11.0205, 76.9665],
        "Tank C": [11.016, 76.978],
        "Tank D": [11.014, 76.960],
    }

    houses_flow = {
        "House 1": [11.022, 76.960],
        "House 2": [11.018, 76.968],
        "House 3": [11.014, 76.974],
        "House 4": [11.010, 76.954],
    }

    # Simulate sensor data
    def simulate_sensor_data():
        data = {
            "City": [],
            "Timestamp": [],
            "Leakage": [],
            "Breakage": [],
            "Pressure": [],
            "WaterQuality": [],
            "FlowSensor": [],
            "MoistureSensor": [],
            "PressureSensor": [],
        }

        for city in cities:
            data["City"].extend([city] * 5)
            now = datetime.now()
            timestamps = [now - timedelta(minutes=i) for i in range(5)]
            data["Timestamp"].extend(timestamps)
            data["Leakage"].extend([random.choice([0, 1]) for _ in range(5)])
            data["Breakage"].extend([random.choice([0, 1]) for _ in range(5)])
            data["Pressure"].extend([random.choice([0, 1]) for _ in range(5)])
            data["WaterQuality"].extend([random.choice([0, 1]) for _ in range(5)])
            data["FlowSensor"].extend([random.choice([0, 1]) for _ in range(5)])
            data["MoistureSensor"].extend([random.choice([0, 1]) for _ in range(5)])
            data["PressureSensor"].extend([random.choice([0, 1]) for _ in range(5)])

        return pd.DataFrame(data)

    # Simulate water flow data
    def simulate_water_flow_data():
        data = {
            "Source": [],
            "Destination": [],
            "Flow": [],
        }

        for tank in tanks_flow:
            for house in houses_flow:
                data["Source"].append(tank)
                data["Destination"].append(house)
                data["Flow"].append(random.uniform(0, 10))

        return pd.DataFrame(data)

    # Create water supply network map
    def create_water_supply_map(cities, pipes, tanks, sensors, sensor_data, coimbatore_gdf):
        m = folium.Map(location=cities["Coimbatore"], zoom_start=12)

        # Plot Coimbatore GeoJSON
        folium.GeoJson(
            coimbatore_gdf,
            name="geojson"
        ).add_to(m)

        # Plot cities
        for city, coordinates in cities.items():
            color = "red" if any(sensor_data[(sensor_data["City"] == city) & (sensor_data["Leakage"] == 1)].index) else "blue"
            folium.Marker(location=coordinates, popup=city, icon=folium.Icon(color=color)).add_to(m)

        # Plot pipes with color based on sensor data
        for pipe in pipes:
            start_coords = cities[pipe["start"]]
            end_coords = cities[pipe["end"]]
            pipe_color = "green" if any(
                sensor_data[
                    (
                        (sensor_data["City"] == pipe["start"])
                        | (sensor_data["City"] == pipe["end"])
                    )
                    & (sensor_data["FlowSensor"] > 0.7)
                ].index
            ) else "blue"
            line = folium.PolyLine(
                [start_coords, end_coords], color=pipe_color, weight=2, opacity=0.7
            )
            m.add_child(line)

        # Plot tanks
        for tank, coordinates in tanks.items():
            folium.Marker(
                location=coordinates, popup=f"{tank} Tank", icon=folium.Icon(color="red")
            ).add_to(m)

        # Plot sensors
        for sensor, coordinates in sensors.items():
            icon = folium.Icon(color="orange", icon="cog")
            folium.Marker(
                location=coordinates,
                popup=f"{sensor}",
                icon=icon,
            ).add_to(m)

        return m

    # Main function
    def main():
        st.title("Water Supply Network and Flow Simulation")

        # Sidebar to toggle between map and water flow simulation
        app_mode = st.sidebar.selectbox("Choose the App Mode", ["Water Supply Map", "Water Flow Simulation"])

        if app_mode == "Water Supply Map":
            # Simulate sensor data
            sensor_data = simulate_sensor_data()

            # Display the simulated sensor data
            st.subheader("Real time monitoring")
            st.dataframe(sensor_data)

            # Create the water supply map using the sample data and sensor data
            water_supply_map = create_water_supply_map(cities, pipes, tanks, sensors, sensor_data, coimbatore_gdf)

            # Save the map to an HTML file
            tmp_file = "water_supply_map.html"
            water_supply_map.save(tmp_file)

            # Display the saved HTML map
            with open(tmp_file, "r", encoding="utf-8") as f:
                st.components.v1.html(f.read(), height=700, scrolling=True)

            # Additional Feature: Show/hide layers
            show_layers = st.checkbox("Show/Hide Layers", True)
            if show_layers:
                st.subheader("Map Layers")
                st.markdown("Toggle the checkboxes to show/hide specific map layers.")
                # Add checkboxes for layers (Cities, Pipes, Tanks, Sensors)
                show_geojson = st.checkbox("Coimbatore GeoJSON", True)
                show_cities = st.checkbox("Cities", True)
                show_pipes = st.checkbox("Pipes", True)
                show_tanks = st.checkbox("Tanks", True)
                show_sensors = st.checkbox("Sensors", True)
                # Redraw the map based on user selections
                m = folium.Map(location=cities["Coimbatore"], zoom_start=12)

                if show_geojson:
                   folium.GeoJson(
                       coimbatore_gdf,
                       name="geojson"
                   ).add_to(m)
                   
                if show_cities:
                    for city, coordinates in cities.items():
                        color = "red" if any(
                            sensor_data[
                                (sensor_data["City"] == city) & (sensor_data["Leakage"] == 1)
                            ].index
                        ) else "blue"
                        folium.Marker(
                            location=coordinates, popup=city, icon=folium.Icon(color=color)
                        ).add_to(m)

                if show_pipes:
                    for pipe in pipes:
                        start_coords = cities[pipe["start"]]
                        end_coords = cities[pipe["end"]]
                        pipe_color = "green" if any(
                            sensor_data[
                                (
                                    (sensor_data["City"] == pipe["start"])
                                    | (sensor_data["City"] == pipe["end"])
                                )
                                & (sensor_data["FlowSensor"] > 0.7)
                            ].index
                        ) else "blue"
                        line = folium.PolyLine(
                            [start_coords, end_coords],
                            color=pipe_color,
                            weight=2,
                            opacity=0.7,
                        )
                        m.add_child(line)

                if show_tanks:
                    for tank, coordinates in tanks.items():
                        folium.Marker(
                            location=coordinates,
                            popup=f"{tank} Tank",
                            icon=folium.Icon(color="red"),
                        ).add_to(m)

                if show_sensors:
                    for sensor, coordinates in sensors.items():
                        icon = folium.Icon(color="orange", icon="cog")
                        folium.Marker(
                            location=coordinates, popup=f"{sensor}", icon=icon
                        ).add_to(m)

                # Save the updated map to an HTML file
                tmp_file_updated = "water_supply_map_updated.html"
                m.save(tmp_file_updated)

                # Display the updated HTML map
                with open(tmp_file_updated, "r", encoding="utf-8") as f:
                    st.components.v1.html(f.read(), height=700, scrolling=True)

        elif app_mode == "Water Flow Simulation":
            # Simulate water flow data
            water_flow_data = simulate_water_flow_data()

            # Display the simulated water flow data
            st.subheader("Water Flow Simulation Data")
            st.dataframe(water_flow_data)

            # Create water flow visualization using Plotly Express
            fig = px.line(
                water_flow_data,
                x="Source",
                y="Flow",
                color="Destination",
                labels={"Flow": "Water Flow"},
                title="Water Flow Simulation",
            )

            # Display the Plotly Express chart
            st.plotly_chart(fig)

    # Run the main function
    if __name__ == "__main__":
        main()
