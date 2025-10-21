import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import LocateControl  # NEW IMPORT
from fastkml import kml
from shapely.geometry import LineString, Point, Polygon
import pandas as pd
import numpy as np
import io

# ============ Streamlit Page Setup ============
st.set_page_config(page_title="BulSU Campus Interactive Map", layout="wide")
st.title("📍 BulSU Interactive Map (Road-Following Logic Applied)")

st.markdown("""
This map now includes a **live location feature**. Click the **Target icon** ($\odot$) on the map to find your current position!
***
### 🛣️ Interactive Routing:
* **Red Line (Road-Following):** Automatically draws the path from your KML file when the route between **Main Gate 1** and **BulSU Activity Center** is selected.
* **Orange Line (Straight-Line):** Draws the straight-line path for all other routes.
""")

# ============ KML Road Path Coordinates (Pre-loaded from your KML file) ============
# This path is for "Directions from VR47+XCR... to Activity Center".
# Coordinates from KML are (Lon, Lat, Alt), flipped to (Lat, Lon) for Folium.
kml_road_coords_lonlat = [
    (120.81229, 14.85719, 0), (120.81276, 14.8576, 0), (120.81301, 14.85782, 0), (120.8128, 14.85801, 0),
    (120.81301, 14.85782, 0), (120.81276, 14.8576, 0), (120.81308, 14.85727, 0), (120.81276, 14.8576, 0),
    (120.81301, 14.85782, 0), (120.81304, 14.85784, 0), (120.81351, 14.85825, 0), (120.81362, 14.85814, 0),
    (120.81385, 14.85787, 0), (120.81418, 14.85814, 0), (120.81422, 14.85816, 0), (120.81423, 14.85816, 0),
    (120.81424, 14.85815, 0), (120.81426, 14.85814, 0), (120.81427, 14.85813, 0), (120.81458, 14.85781, 0),
    (120.81507, 14.85825, 0), (120.81544, 14.85856, 0), (120.81557, 14.85843, 0), (120.81598, 14.85795, 0),
    (120.81515, 14.85724, 0), (120.81504, 14.85735, 0), (120.81496, 14.85745, 0), (120.8149, 14.85749, 0),
    (120.81486, 14.85751, 0), (120.81482, 14.85752, 0), (120.81479, 14.85752, 0), (120.81475, 14.85751, 0),
    (120.81472, 14.85749, 0), (120.81464, 14.85744, 0), (120.81439, 14.85727, 0), (120.81436, 14.8573, 0),
    (120.81408, 14.85761, 0), (120.81422, 14.85746, 0), (120.81436, 14.8573, 0), (120.81439, 14.85727, 0),
    (120.81464, 14.85744, 0), (120.81472, 14.85749, 0), (120.81475, 14.85751, 0), (120.81479, 14.85752, 0),
    (120.81482, 14.85752, 0), (120.81486, 14.85751, 0), (120.8149, 14.85749, 0), (120.81496, 14.85745, 0),
    (120.81504, 14.85735, 0), (120.81515, 14.85724, 0), (120.81598, 14.85795, 0), (120.81638, 14.85827, 0),
    (120.81598, 14.85795, 0), (120.81515, 14.85724, 0), (120.81504, 14.85735, 0), (120.81496, 14.85745, 0),
    (120.8149, 14.85749, 0), (120.81486, 14.85751, 0), (120.81482, 14.85752, 0), (120.81479, 14.85752, 0),
    (120.81475, 14.85751, 0), (120.81472, 14.85749, 0), (120.81464, 14.85744, 0), (120.81439, 14.85727, 0),
    (120.81436, 14.8573, 0), (120.81385, 14.85787, 0), (120.81362, 14.85814, 0), (120.81351, 14.85825, 0),
    (120.81339, 14.8584, 0), (120.81336, 14.85844, 0), (120.81334, 14.85848, 0), (120.81334, 14.8585, 0),
    (120.81334, 14.85852, 0), (120.81335, 14.85855, 0), (120.81336, 14.85856, 0), (120.81341, 14.85861, 0),
    (120.81352, 14.85872, 0), (120.81341, 14.85861, 0), (120.81336, 14.85856, 0), (120.81335, 14.85855, 0),
    (120.81334, 14.85852, 0), (120.81334, 14.8585, 0), (120.81334, 14.85848, 0), (120.81336, 14.85844, 0),
    (120.81339, 14.8584, 0), (120.81351, 14.85825, 0), (120.81304, 14.85784, 0), (120.81301, 14.85782, 0),
    (120.8128, 14.85801, 0), (120.81301, 14.85782, 0), (120.81304, 14.85784, 0), (120.81309, 14.8578, 0),
    (120.81316, 14.85774, 0), (120.81309, 14.8578, 0), (120.81304, 14.85784, 0), (120.81301, 14.85782, 0),
    (120.81276, 14.8576, 0), (120.81305, 14.85731, 0)
]
# Final list of coordinates for Folium in (Lat, Lon) format
kml_road_coords = [(lat, lon) for lon, lat, alt in kml_road_coords_lonlat]

# Define the names for the smart-routing feature
KML_START_NAME = "Main Gate 1 (VR47+XCR)"
KML_END_NAME = "BulSU Activity Center"

# ============ MARKERS WITH YOUR PROVIDED COORDINATES ============
building_data_list = [
    # (Name, Lat, Lon, Color, Icon)
    # ACADEMIC & RESEARCH HALLS (Blue)
    ("College of Social Sciences and Philosophy (CSSP)", 14.859139, 120.814932, "blue", "comment-dots"),
    ("BuLSU College of Arts and Letters (CAL)", 14.858742, 120.815004, "blue", "book-open"),
    ("College of Science (CS)", 14.858558, 120.814810, "blue", "flask"),
    ("CPERS (Physical Education, Recreation and Sport)", 14.858314, 120.814929, "blue", "futbol"),
    ("BuLSU College of Architecture and Fine Arts (CAFA)", 14.858110, 120.814670, "blue", "pencil-ruler"),
    ("BuLSU College of Education (CoEd) - Roxas Hall", 14.857366, 120.814234, "blue", "school"),
    ("BuLSU College of Engineering (CoE) - Natividad Hall", 14.857540, 120.814296, "blue", "cogs"),
    ("College of Business Administration (CBA)", 14.858245, 120.813953, "blue", "briefcase"),
    ("Bulsu College of Industrial Technology (CIT)", 14.857635, 120.812532, "blue", "tools"),
    ("BuLSU Science Research and Learning Center", 14.858191, 120.813788, "blue", "microscope"),
    ("BuLSU e-Library (Main Library)", 14.858503, 120.813680, "blue", "book"),
    ("BuLSU Laboratory High School (LHS Quadrangle)", 14.857892, 120.813756, "blue", "graduation-cap"),

    # ADMINISTRATION & FACILITIES (Green)
    (KML_START_NAME, 14.857194, 120.812285, "darkgreen", "archway"),  # Main Gate 1
    (KML_END_NAME, 14.857309, 120.813046, "darkgreen", "star"),  # Activity Center
    ("BuLSU Office of the Student Government", 14.858442, 120.815159, "darkgreen", "users"),
    ("CSSP Local Student Council, BuLSU SG", 14.858847, 120.815316, "darkgreen", "user-tie"),
    ("BuLSU Valencia Hall (Gymnasium)", 14.858245, 120.815233, "darkgreen", "dumbbell"),
    ("BuLSU Flores Hall", 14.857911, 120.815090, "darkgreen", "building"),
    ("BuLSU Admissions Office", 14.857870, 120.813270, "darkgreen", "clipboard"),
    ("BuLSU Hostel", 14.858643, 120.813355, "darkgreen", "bed"),
    ("University Canteen", 14.858313, 120.815551, "darkred", "cutlery"),
    ("BuLSU NSTP Building", 14.856889, 120.813646, "darkgreen", "shield-alt"),
    ("Pimentel Hall", 14.856951, 120.813400, "darkgreen", "door-open"),
    ("CURSOR Publication", 14.857175, 120.813651, "darkgreen", "newspaper"),
    ("Bulacan State University Main Parking Space", 14.857525, 120.813437, "darkgreen", "parking"),
    ("BSU Mini Rizal Park", 14.857458, 120.813203, "darkgreen", "tree"),
    ("BuLSU Tennis Court", 14.858208, 120.813048, "darkgreen", "tennis-ball"),

    # NEARBY LANDMARKS (Red)
    ("Bulacan Provincial Blood Center (Nearby)", 14.859200, 120.815100, "red", "heart"),
    ("The Engineers Publication (Natividad Hall)", 14.857540, 120.814296, "red", "pen-nib"),
]

# Convert to DataFrame for easy lookups
df_buildings = pd.DataFrame(building_data_list, columns=['name', 'lat', 'lon', 'color', 'icon'])
building_names = sorted(df_buildings['name'].unique().tolist())

# ============ MAP SETUP ============
campus_lat = 14.8580
campus_lon = 120.8160
# Initialize the map
m = folium.Map(location=[campus_lat, campus_lon], zoom_start=18, control_scale=True)

# Add Satellite and Street View layers
folium.TileLayer(tiles='https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', attr='Google Satellite',
                 name='Google Satellite View', subdomains=['mt0', 'mt1', 'mt2', 'mt3']).add_to(m)
folium.TileLayer(tiles='https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', attr='Google Maps',
                 name='Google Street View', subdomains=['mt0', 'mt1', 'mt2', 'mt3']).add_to(m)

# === NEW: ADD LIVE LOCATION CONTROL ===
# This adds the target icon (LocateControl) to the map
LocateControl(
    auto_start=False,
    position='topleft',
    strings={"title": "Show my location"},
    locateOptions={'enableHighAccuracy': True}
).add_to(m)

# ============ INTERACTIVE SIDEBAR FOR PATHWAYS ============
st.sidebar.header("🗺️ Find Your Route")

start_location = st.sidebar.selectbox("Starting Location", building_names, index=building_names.index(
    KML_START_NAME) if KML_START_NAME in building_names else 0)
end_location = st.sidebar.selectbox("Destination", [name for name in building_names if name != start_location],
                                    index=building_names.index(
                                        KML_END_NAME) - 1 if KML_END_NAME in building_names else 0)

# ============ PATH CALCULATION AND DISPLAY (Smart Routing) ============

if start_location and end_location:

    # Check if the selection matches the known KML road path (in either direction)
    route_pair = tuple(sorted((start_location, end_location)))
    kml_pair = tuple(sorted((KML_START_NAME, KML_END_NAME)))
    is_kml_route = (route_pair == kml_pair)

    if is_kml_route:
        # --- Draw the Road-Following KML Path (Red Line) ---
        route_coords = kml_road_coords
        route_weight = 6

        # Reverse coordinates if the user chose the opposite direction
        if start_location == KML_END_NAME:
            route_coords = route_coords[::-1]

        folium.PolyLine(
            route_coords,
            color="red",
            weight=route_weight,
            opacity=0.9,
            tooltip=f"ROAD ROUTE: {start_location} to {end_location} (From KML File)"
        ).add_to(m)
        st.sidebar.success(f"**Road-following route** found and drawn in **Red!**")

    else:
        # --- Draw the Straight-Line Path (Orange Line) ---
        start_data = df_buildings[df_buildings['name'] == start_location].iloc[0]
        end_data = df_buildings[df_buildings['name'] == end_location].iloc[0]
        start_coords = (start_data['lat'], start_data['lon'])
        end_coords = (end_data['lat'], end_data['lon'])
        path_coordinates = [start_coords, end_coords]

        # Simple Euclidean distance approximation
        distance_approx = np.sqrt((end_coords[0] - start_coords[0]) ** 2 + (end_coords[1] - start_coords[1]) ** 2)

        folium.PolyLine(
            path_coordinates,
            color="orange",
            weight=5,
            opacity=0.8,
            tooltip=f"STRAIGHT-LINE ROUTE: {start_location} to {end_location}"
        ).add_to(m)

        st.sidebar.info(f"**Straight line** (Orange) is drawn. **Distance:** ≈ {distance_approx:.4f} degrees.")

# ============ ADD ALL BUILDING MARKERS ============
for index, row in df_buildings.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"<b>{row['name']}</b><br>Lat: {row['lat']:.6f}, Lon: {row['lon']:.6f}",
        tooltip=row['name'],
        icon=folium.Icon(color=row['color'], icon=row['icon'], prefix="fa")
    ).add_to(m)

# ============ KML PATH UPLOAD (For other custom road-following paths) ============
st.sidebar.markdown("---")
st.sidebar.header("⬆️ Upload Other Road Paths (KML/GeoJSON)")
st.sidebar.caption("Upload a file to add a **Dark Red** custom road trace.")
uploaded_file = st.sidebar.file_uploader("Choose a .kml file or .geojson", type=["kml", "geojson"])

if uploaded_file is not None:
    file_color = "darkred"
    try:
        if uploaded_file.name.endswith('.kml'):
            kml_content = uploaded_file.read()
            k = kml.KML()
            k.from_string(kml_content)

            features = list(k.features())
            if features:
                document = features[0]
                line_count = 0
                for feature in document.features():
                    if isinstance(feature.geometry, LineString):
                        # KML coordinates are (Lon, Lat, Alt) -> flip to (Lat, Lon)
                        coords = [(coord[1], coord[0]) for coord in feature.geometry.coords]
                        folium.PolyLine(coords, color=file_color, weight=6, opacity=0.9,
                                        tooltip=f"Custom KML Path: {feature.name}").add_to(m)
                        line_count += 1

                if line_count > 0:
                    st.sidebar.info(f"{line_count} custom KML path(s) loaded successfully.")
                else:
                    st.sidebar.warning("KML file uploaded, but no LineString paths were found within it.")

        elif uploaded_file.name.endswith('.geojson'):
            geojson_data = uploaded_file.read().decode('utf-8')
            folium.GeoJson(
                geojson_data,
                name='Custom GeoJSON Path',
                style_function=lambda x: {'color': file_color, 'weight': 6}
            ).add_to(m)
            st.sidebar.info("GeoJSON path loaded successfully.")

    except Exception as e:
        st.sidebar.error(f"Error loading file. Check file format: {e}")

# ============ Add Layer Control and Display Map ============
folium.LayerControl(collapsed=False).add_to(m)
st_data = st_folium(m, width=1200, height=700)