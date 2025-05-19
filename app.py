import streamlit as st
import folium
from streamlit_folium import st_folium

# Page config
st.set_page_config(page_title="Bulacan State University Malolos Campus Map", layout="wide")

# Title
st.title("Bulacan State University Malolos Campus Map")

# Campus coordinates
campus_lat = 14.8581   # 14°51'29" N
campus_lon = 120.8139  # 120°48'50" E

# Create map
m = folium.Map(location=[campus_lat, campus_lon], zoom_start=18, tiles='Esri.WorldImagery')

# Add a marker for BulSU campus center
folium.Marker(
    [campus_lat, campus_lon],
    popup="Bulacan State University - Malolos Campus",
    tooltip="BulSU Main Campus",
    icon=folium.Icon(color='red', icon='university', prefix='fa')
).add_to(m)

# Add circle boundary (approx 200m radius)
folium.Circle(
    radius=200,
    location=[campus_lat, campus_lon],
    color="blue",
    fill=True,
    fill_opacity=0.2,
    popup="Approx. campus area"
).add_to(m)

# Display map in Streamlit
st_folium(m, width=900, height=600)
