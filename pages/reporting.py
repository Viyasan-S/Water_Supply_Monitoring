import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# Sample sensor data
sensor_data = {
    "Timestamp": [],
    "WaterFlow": [],
    "Pressure": [],
    "WaterQuality": [],
    "Leakage": [],
    "Breakage": [],
}

# Email configuration
email_sender = "innovatioki123@gmail.com"
email_receiver = "2k21ece062@kiot.ac.in"
email_password = "gdhdvfvpzawdgmim"
email_subject = "Pipeline Alert!"

# Simulate sensor data
def simulate_sensor_data():
    now = datetime.now()
    for i in range(50):
        timestamp = now - timedelta(seconds=i)
        sensor_data["Timestamp"].insert(0, timestamp)
        sensor_data["WaterFlow"].insert(0, random.uniform(0, 1))
        sensor_data["Pressure"].insert(0, random.uniform(5, 15))
        sensor_data["WaterQuality"].insert(0, random.uniform(0, 1))
        sensor_data["Leakage"].insert(0, random.choice([0, 1]))
        sensor_data["Breakage"].insert(0, random.choice([0, 1]))

# Send email notification
def send_email_alert(message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_sender, email_password)

            msg = MIMEText(message)
            msg["Subject"] = email_subject
            msg["From"] = email_sender
            msg["To"] = email_receiver

            server.sendmail(email_sender, [email_receiver], msg.as_string())
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")

# Real-time monitoring page
def real_time_monitoring():
    st.title("Automated Alerts - Pipeline Monitoring")

    # Simulate sensor data
    simulate_sensor_data()

    # Display real-time sensor data
    st.subheader("Real-time Sensor Data")
    st.dataframe(pd.DataFrame(sensor_data))

    # Plot real-time water flow
    fig_water_flow = px.line(
        pd.DataFrame(sensor_data),
        x="Timestamp",
        y="WaterFlow",
        title="Real-time Water Flow Monitoring",
        labels={"WaterFlow": "Water Flow"},
    )
    st.plotly_chart(fig_water_flow)

    # Plot real-time pressure
    fig_pressure = px.line(
        pd.DataFrame(sensor_data),
        x="Timestamp",
        y="Pressure",
        title="Real-time Pressure Monitoring",
        labels={"Pressure": "Pressure"},
    )
    st.plotly_chart(fig_pressure)

    # Plot real-time water quality
    fig_water_quality = px.line(
        pd.DataFrame(sensor_data),
        x="Timestamp",
        y="WaterQuality",
        title="Real-time Water Quality Monitoring",
        labels={"WaterQuality": "Water Quality"},
    )
    st.plotly_chart(fig_water_quality)

    # Automated Alerts
    st.subheader("Automated Alerts")

    # Check for issues and generate alerts
    if any(sensor_data["Leakage"]) or any(sensor_data["Breakage"]):
        alert_message = "Alert: Leakage or Breakage detected! Please investigate."
        st.error(alert_message)
        send_email_alert(alert_message)

    # Button to manually trigger an email alert
    if st.button("Send Alert Email"):
        manual_alert_message = "Manual Alert: This is a test email alert."
        st.success("Alert Email Sent!")
        send_email_alert(manual_alert_message)

# Main function
def main():
    real_time_monitoring()

if __name__ == "__main__":
    main()
