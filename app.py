import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Bulacan State University Campus Map")

# Centered at BulSU Malolos
bulsu_center = [14.8441, 120.8110]

# Create map instance
m = folium.Map(location=bulsu_center, zoom_start=17, control_scale=True)

# Set max bounds (campus-only)
m.fit_bounds([[14.8428, 120.8090], [14.8455, 120.8125]])

# Optional: Disable panning outside campus
m.options['maxBounds'] = [[14.8428, 120.8090], [14.8455, 120.8125]]

# Add building markers (sample — you can add all campus buildings)
folium.Marker(
    location=[14.84415, 120.81060],
    popup="Rafael Palma Hall (RP)",
    icon=folium.Icon(color='green', icon='university')
).add_to(m)

folium.Marker(
    location=[14.84478, 120.81088],
    popup="Lorenzo Hall",
    icon=folium.Icon(color='blue', icon='university')
).add_to(m)

folium.Marker(
    location=[14.84390, 120.81110],
    popup="College of Engineering (COE)",
    icon=folium.Icon(color='red', icon='university')
).add_to(m)

folium.Marker(
    location=[14.84425, 120.81175],
    popup="University Library",
    icon=folium.Icon(color='purple', icon='book')
).add_to(m)

# Render map on Streamlit
st_folium(m, width=800, height=600)
