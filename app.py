import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins

# Streamlit App Title
st.title("Bulacan State University Malolos Campus Map")

# Center of Bulacan State University Malolos Campus
campus_center = [14.8443, 120.8111]

# Create Folium map with Esri WorldImagery (satellite view)
m = folium.Map(location=campus_center, zoom_start=18, tiles="Esri.WorldImagery")

# Example markers for main buildings (you can add more if you like)
folium.Marker(
    location=[14.8445, 120.8113],
    popup="Admin Building",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

folium.Marker(
    location=[14.8448, 120.8110],
    popup="College of Engineering",
    icon=folium.Icon(color="blue", icon="graduation-cap", prefix='fa')
).add_to(m)

folium.Marker(
    location=[14.8446, 120.8107],
    popup="College of Business",
    icon=folium.Icon(color="green", icon="building", prefix='fa')
).add_to(m)

folium.Marker(
    location=[14.8441, 120.8115],
    popup="Library",
    icon=folium.Icon(color="orange", icon="book", prefix='fa')
).add_to(m)

# Optional: add a minimap
minimap = plugins.MiniMap(toggle_display=True)
m.add_child(minimap)

# Display map in Streamlit
st_data = st_folium(m, width=725)
