import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins

# Page config
st.set_page_config(page_title="BulSU Campus Map", layout="wide")

# Title
st.title("Bulacan State University Malolos Campus Map")

# Center map at BulSU Malolos Main Campus
campus_lat, campus_lon = 14.85806, 120.814

# Create map object
m = folium.Map(location=[campus_lat, campus_lon], zoom_start=18, tiles=None)

# Add tile layers
folium.TileLayer('OpenStreetMap', name='Map View').add_to(m)
folium.TileLayer('Esri.WorldImagery', name='Satellite View').add_to(m)

# Add campus boundary
folium.Circle(
    location=[campus_lat, campus_lon],
    radius=200,
    color="orange",
    fill=True,
    fill_opacity=0.2,
    popup="Campus Boundary"
).add_to(m)

# Enable user location control
plugins.LocateControl(auto_start=True).add_to(m)

# Building markers
buildings = {
    "G1": [14.857235, 120.812279],
    "CIT": [14.857678, 120.812557],
    "CBA": [14.858265, 120.813903],
    "ENG": [14.857547, 120.814309],
    "NUR": [14.856961, 120.813452],
    "LAW": [14.857717, 120.813463],
    "CAFA": [14.858123, 120.814713],
    "CPERS": [14.858255, 120.814843],
    "CAL": [14.858749, 120.814968],
    "CSSP": [14.859151, 120.814945]
}

# Place markers
for name, coords in buildings.items():
    folium.Marker(
        location=coords,
        popup=f"<b>{name}</b>",
        icon=folium.DivIcon(html=f"""
            <div style="font-size:12px; font-weight:bold; color:white;
            -webkit-text-stroke: 1px black; background:rgba(0,0,0,0.6);
            padding:4px 6px; border-radius:4px; text-align:center;">
            {name}</div>""")
    ).add_to(m)

# Department paths (internal campus paths)
paths = {
    "CIT": [[14.857235, 120.812279], [14.857300, 120.812600], [14.857500, 120.812550], [14.857678, 120.812557]],
    "CBA": [[14.857235, 120.812279], [14.857300, 120.812600], [14.857700, 120.813200], [14.858265, 120.813903]],
    "ENG": [[14.857235, 120.812279], [14.857300, 120.812600], [14.857400, 120.813600], [14.857547, 120.814309]],
    "NUR": [[14.857235, 120.812279], [14.857300, 120.812600], [14.857000, 120.813100], [14.856961, 120.813452]],
    "LAW": [[14.857235, 120.812279], [14.857300, 120.812600], [14.857600, 120.813200], [14.857717, 120.813463]],
    "CAFA": [[14.857235, 120.812279], [14.857300, 120.812600], [14.857800, 120.814000], [14.858123, 120.814713]],
    "CPERS": [[14.857235, 120.812279], [14.857300, 120.812600], [14.858000, 120.814200], [14.858255, 120.814843]],
    "CAL": [[14.857235, 120.812279], [14.857300, 120.812600], [14.858400, 120.814600], [14.858749, 120.814968]],
    "CSSP": [[14.857235, 120.812279], [14.857300, 120.812600], [14.858600, 120.814800], [14.859151, 120.814945]]
}

# UI Controls
col1, col2 = st.columns([3, 1])
with col1:
    selected = st.selectbox("Select a Department to Trace Path", ["None"] + list(paths.keys()))
with col2:
    reset = st.button("Reset View")

# Show path and simulate animation
if selected != "None":
    route = paths[selected]
    folium.PolyLine(route, color="red", weight=6, opacity=0.9, tooltip=f"Path to {selected}").add_to(m)
    for point in route:
        folium.CircleMarker(point, radius=5, color="red", fill=True, fill_opacity=0.7).add_to(m)
    m.fit_bounds(route)

# Reset zoom to full campus view
if reset:
    m.location = [campus_lat, campus_lon]
    m.zoom_start = 18

# Map controls
folium.LayerControl().add_to(m)

# Display map
st_folium(m, width=1000, height=700)
