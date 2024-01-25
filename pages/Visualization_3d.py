import plotly.graph_objects as go
import streamlit as st

# Sample data
cities = {
    "Coimbatore": [11.0178, 76.9565, 0],
    "Peelamedu": [11.0205, 76.9665, 0],
    "Gandhipuram": [11.016, 76.978, 0],
}

pipes = [
    {"start": "Coimbatore", "end": "Peelamedu"},
    {"start": "Peelamedu", "end": "Gandhipuram"},
    {"start": "Gandhipuram", "end": "Coimbatore"},
]

tanks = {
    "Coimbatore": [11.0168, 76.9558, 5],
    "Peelamedu": [11.0205, 76.9665, 5],
    "Gandhipuram": [11.016, 76.978, 5],
}

# Function to create enhanced 3D water supply network visualization
def create_enhanced_3d_water_supply_network(cities, pipes, tanks):
    fig = go.Figure()

    # Plot cities
    for city, coordinates in cities.items():
        fig.add_trace(
            go.Scatter3d(
                x=[coordinates[0]],
                y=[coordinates[1]],
                z=[coordinates[2]],
                mode="markers+text",
                text=[city],
                textposition="bottom center",
                marker=dict(size=10, color="red"),
                name=f"City: {city}",
            )
        )

    # Plot pipes
    for pipe in pipes:
        start_coords = cities[pipe["start"]]
        end_coords = cities[pipe["end"]]
        fig.add_trace(
            go.Scatter3d(
                x=[start_coords[0], end_coords[0]],
                y=[start_coords[1], end_coords[1]],
                z=[start_coords[2], end_coords[2]],
                mode="lines",
                line=dict(color="blue", width=5),
                name=f"Pipe: {pipe['start']} to {pipe['end']}",
            )
        )

    # Plot tanks
    for tank, coordinates in tanks.items():
        fig.add_trace(
            go.Scatter3d(
                x=[coordinates[0]],
                y=[coordinates[1]],
                z=[coordinates[2]],
                mode="markers",
                marker=dict(size=10, color="green"),
                name=f"Tank: {tank}",
            )
        )

    # Layout settings
    fig.update_layout(
        scene=dict(aspectmode="data"),
        margin=dict(l=0, r=0, b=0, t=0),
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 300}}],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
            }
        ],
        sliders=[{"steps": [{"args": [[f"{i}"]], "label": f"{i}", "method": "animate"} for i in range(len(cities))], "active": 0, "y": 0, "x": 0.1, "yanchor": "top", "xanchor": "left"}],
    )

    return fig

# Streamlit app
def main():
    st.title("Enhanced 3D Water Supply Network Visualization")

    # Create enhanced 3D water supply network visualization
    water_supply_3d = create_enhanced_3d_water_supply_network(cities, pipes, tanks)

    # Display the enhanced 3D plot using Streamlit
    st.plotly_chart(water_supply_3d)

if __name__ == "__main__":
    main()
