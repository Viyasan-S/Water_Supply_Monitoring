import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

# Simulate predictive maintenance data
def simulate_predictive_maintenance_data():
    data = {
        "Timestamp": [],
        "Equipment": [],
        "Temperature": [],
        "Vibration": [],
        "Pressure": [],
        "FailureProbability": [],
    }

    for _ in range(100):
        now = datetime.now()
        timestamp = now - timedelta(days=100 - _)
        data["Timestamp"].append(timestamp)
        equipment = random.choice(["Machine A", "Machine B", "Machine C","Machine D"])
        data["Equipment"].append(equipment)
        data["Temperature"].append(random.uniform(20, 40))
        data["Vibration"].append(random.uniform(0, 10))
        data["Pressure"].append(random.uniform(5, 20))

        # Simulate failure probability based on conditions
        failure_probability = 0.1  # Base failure probability
        if equipment == "Machine A":
            failure_probability += 0.2 * data["Temperature"][-1] / 40
            failure_probability += 0.1 * data["Vibration"][-1] / 10
            failure_probability += 0.15 * data["Pressure"][-1] / 20
        elif equipment == "Machine B":
            failure_probability += 0.15 * data["Temperature"][-1] / 40
            failure_probability += 0.2 * data["Vibration"][-1] / 10
            failure_probability += 0.1 * data["Pressure"][-1] / 20
        elif equipment == "Machine C":
            failure_probability += 0.1 * data["Temperature"][-1] / 40
            failure_probability += 0.15 * data["Vibration"][-1] / 10
            failure_probability += 0.2 * data["Pressure"][-1] / 20
        elif equipment == "Machine D":
            failure_probability += 0.1 * data["Temperature"][-1] / 40
            failure_probability += 0.15 * data["Vibration"][-1] / 10
            failure_probability += 0.2 * data["Pressure"][-1] / 20

        # Introduce randomness
        failure_probability += random.uniform(-0.05, 0.05)
        failure_probability = max(0, min(1, failure_probability))

        data["FailureProbability"].append(failure_probability)

    return pd.DataFrame(data)

# Predictive maintenance dashboard
def predictive_maintenance_dashboard():
    st.title("Predictive Maintenance Dashboard")

    # Simulate predictive maintenance data
    predictive_maintenance_data = simulate_predictive_maintenance_data()

    # Display the simulated data
    st.subheader("Simulated Predictive Maintenance Data")
    st.dataframe(predictive_maintenance_data)

    # Create line charts for temperature, vibration, pressure, and failure probability
    st.subheader("Equipment Metrics Over Time")
    fig_temperature = px.line(
        predictive_maintenance_data,
        x="Timestamp",
        y="Temperature",
        color="Equipment",
        labels={"Temperature": "Temperature (°C)"},
        title="Equipment Temperature Over Time",
    )
    st.plotly_chart(fig_temperature)

    fig_vibration = px.line(
        predictive_maintenance_data,
        x="Timestamp",
        y="Vibration",
        color="Equipment",
        labels={"Vibration": "Vibration Level"},
        title="Equipment Vibration Over Time",
    )
    st.plotly_chart(fig_vibration)

    fig_pressure = px.line(
        predictive_maintenance_data,
        x="Timestamp",
        y="Pressure",
        color="Equipment",
        labels={"Pressure": "Pressure (MPa)"},
        title="Equipment Pressure Over Time",
    )
    st.plotly_chart(fig_pressure)

    fig_failure_probability = px.line(
        predictive_maintenance_data,
        x="Timestamp",
        y="FailureProbability",
        color="Equipment",
        labels={"FailureProbability": "Failure Probability"},
        title="Equipment Failure Probability Over Time",
    )
    st.plotly_chart(fig_failure_probability)

    # Additional charts
    st.subheader("Additional Metrics")
    # Add more charts based on your specific needs

    # Failure prediction indicator
    st.subheader("Failure Prediction Indicator")
    failure_prediction_indicator = (
        predictive_maintenance_data.groupby("Equipment")
        .agg({"FailureProbability": "max"})
        .reset_index()
    )
    failure_prediction_indicator["Prediction"] = failure_prediction_indicator[
        "FailureProbability"
    ].apply(lambda x: "High" if x > 0.8 else "Low")
    st.table(failure_prediction_indicator[["Equipment", "Prediction"]])

# Main function
def main():
    predictive_maintenance_dashboard()

if __name__ == "__main__":
    main()
