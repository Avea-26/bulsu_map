import streamlit as st
import folium
from streamlit_folium import st_folium

# Title
st.title("Bulacan State University Campus Map")

# Create Folium map centered on BSU Malolos
bsu_map = folium.Map(location=[14.8441, 120.8115], zoom_start=18)

# Add markers
folium.Marker(
    [14.8441, 120.8115],
    popup='Bulacan State University - Main Gate',
    icon=folium.Icon(color='red')
).add_to(bsu_map)

folium.Marker(
    [14.8445, 120.8117],
    popup='College of ICT (CICT)',
    icon=folium.Icon(color='blue')
).add_to(bsu_map)

folium.Marker(
    [14.8437, 120.8113],
    popup='University Library',
    icon=folium.Icon(color='green')
).add_to(bsu_map)

# Restrict map bounds to the campus
bounds = [[14.8432, 120.8105], [14.8450, 120.8125]]
bsu_map.fit_bounds(bounds)

# Display map inside Streamlit app
st_folium(bsu_map, width=700, height=500)
