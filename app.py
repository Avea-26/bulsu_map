import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import numpy as np


# --- 0. UTILITY FUNCTIONS ---

# Function to calculate Haversine distance between two coordinates in meters
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


# Function to find the index of the point on the path closest to a given coordinate
def find_closest_point_index(target_lat, target_lon, path_coords):
    min_dist = float('inf')
    closest_index = -1

    for i, (lat, lon) in enumerate(path_coords):
        # We use a simple Euclidean distance approximation for path finding speed,
        # as Haversine is overkill for small distances like this.
        dist = sqrt((target_lat - lat) ** 2 + (target_lon - lon) ** 2)
        if dist < min_dist:
            min_dist = dist
            closest_index = i
    return closest_index


# Function to calculate the total length of a polyline in meters
def calculate_polyline_distance(coords):
    total_dist = 0
    for i in range(len(coords) - 1):
        lat1, lon1 = coords[i]
        lat2, lon2 = coords[i + 1]
        total_dist += haversine(lat1, lon1, lat2, lon2)
    return total_dist


# --- 1. CONFIGURATION AND DATA (30 TOTAL DESTINATIONS) ---

st.set_page_config(page_title="BulSU Campus Map for New Students", layout="wide")
st.title("🗺️ Bulacan State University – Malolos Campus Map: New Student Edition")

st.error(
    "🚨 **LIVE LOCATION (SIMULATED):** This Streamlit app runs server-side. **For dynamic routing, use the 'Start Location' selector.** The map still features the **🌐** icon for client-side geolocation."
)

# Campus center coordinates (Corrected for Malolos Campus)
campus_lat, campus_lon = 14.85806, 120.814

# Define the full set of 30 building and landmark data.
BUILDING_DATA = [
    # Original Core Locations (14)
    {"name": "Gate 1 (Main Gate)", "initials": "G1", "lat": 14.85723594755244, "lon": 120.8122796215916,
     "area": "Entrance", "color": "green", "icon": "info-sign", "essential": True},
    {"name": "Gate 2", "initials": "G2", "lat": 14.857314970938278, "lon": 120.81431249226469, "area": "Entrance",
     "color": "green", "icon": "info-sign", "essential": False},
    {"name": "Admissions Office", "initials": "AO", "lat": 14.85787281781839, "lon": 120.81324939963862,
     "area": "Admin", "color": "darkred", "icon": "clipboard", "essential": True},
    {"name": "BulSU e-Library (Main)", "initials": "LIB", "lat": 14.85850320691184, "lon": 120.8137132784873,
     "area": "Library", "color": "darkblue", "icon": "book", "essential": True},
    {"name": "Office of the Registrars", "initials": "REG", "lat": 14.857715559437853, "lon": 120.81491671412424,
     "area": "Admin", "color": "darkred", "icon": "users", "essential": True},
    {"name": "University Clinic/Infirmary", "initials": "CLINIC", "lat": 14.85830000000000, "lon": 120.815400000000,
     "area": "Safety", "color": "red", "icon": "plus", "essential": True},
    {"name": "Security & Vigilance Office", "initials": "SEC", "lat": 14.85710000000000, "lon": 120.812500000000,
     "area": "Safety", "color": "darkred", "icon": "exclamation-triangle", "essential": True},
    {"name": "CIT Building (College of Industrial Technology)", "initials": "CIT", "lat": 14.857678444483582,
     "lon": 120.812557298334, "area": "Technology", "color": "blue", "icon": "cogs", "essential": False},
    {"name": "CBA Building (College of Business Administration)", "initials": "CBA", "lat": 14.858265418626708,
     "lon": 120.81390368960794, "area": "Business", "color": "blue", "icon": "briefcase", "essential": False},
    {"name": "College of Engineering", "initials": "ENG", "lat": 14.857546982943054, "lon": 120.8143091116688,
     "area": "Engineering", "color": "blue", "icon": "wrench", "essential": False},
    {"name": "College of Nursing", "initials": "NUR", "lat": 14.856961206741117, "lon": 120.81345271593389,
     "area": "Health", "color": "blue", "icon": "medkit", "essential": False},
    {"name": "College of Law", "initials": "LAW", "lat": 14.857716890878411, "lon": 120.81346297233067, "area": "Law",
     "color": "blue", "icon": "legal", "essential": False},
    {"name": "College of Architecture and Fine Arts (CAFA)", "initials": "CAFA", "lat": 14.85812252860069,
     "lon": 120.81471377704729, "area": "Arts", "color": "blue", "icon": "camera-retro", "essential": False},
    {"name": "College of Arts and Letters (CAL)", "initials": "CAL", "lat": 14.858749479597106,
     "lon": 120.81496792254381, "area": "Arts", "color": "blue", "icon": "theater-masks", "essential": False},

    # 16 New Locations Added (Estimated Coordinates)
    {"name": "Gate 3 (Back Gate)", "initials": "G3", "lat": 14.859550, "lon": 120.815500, "area": "Entrance",
     "color": "green", "icon": "info-sign", "essential": False},
    {"name": "Activity Center (Gym Annex)", "initials": "AC", "lat": 14.858500, "lon": 120.815500, "area": "Sports",
     "color": "orange", "icon": "trophy", "essential": True},
    {"name": "University Gymnasium (Main)", "initials": "GYM", "lat": 14.857400, "lon": 120.815600, "area": "Sports",
     "color": "orange", "icon": "basketball-ball", "essential": True},
    {"name": "College of Education (CoEd)", "initials": "COED", "lat": 14.858900, "lon": 120.815200,
     "area": "Education", "color": "blue", "icon": "graduation-cap", "essential": False},
    {"name": "College of Science (CS)", "initials": "CS", "lat": 14.858800, "lon": 120.814000, "area": "Science",
     "color": "blue", "icon": "flask", "essential": False},
    {"name": "HRM Building (College of Hospitality)", "initials": "HRM", "lat": 14.859300, "lon": 120.813000,
     "area": "Hospitality", "color": "blue", "icon": "utensils", "essential": False},
    {"name": "University Administration Building", "initials": "ADMIN", "lat": 14.858300, "lon": 120.813000,
     "area": "Admin", "color": "darkred", "icon": "building", "essential": True},
    {"name": "Cultural Center (Auditorium)", "initials": "CC", "lat": 14.859000, "lon": 120.812500, "area": "Arts",
     "color": "cadetblue", "icon": "mask", "essential": False},
    {"name": "Student Affairs Office (SAO)", "initials": "SAO", "lat": 14.857200, "lon": 120.814000, "area": "Admin",
     "color": "darkred", "icon": "handshake", "essential": False},
    {"name": "Office of Research and Extension (ORES)", "initials": "ORES", "lat": 14.857900, "lon": 120.815500,
     "area": "Admin", "color": "darkred", "icon": "search", "essential": False},
    {"name": "Academic Services Office (ASO)", "initials": "AS", "lat": 14.858100, "lon": 120.814000, "area": "Admin",
     "color": "darkred", "icon": "lightbulb", "essential": True},
    {"name": "Food Stalls/Canteen Annex", "initials": "CANTEEN", "lat": 14.857900, "lon": 120.812800, "area": "Food",
     "color": "beige", "icon": "coffee", "essential": True},
    {"name": "University Museum", "initials": "MUSE", "lat": 14.858600, "lon": 120.813000, "area": "Culture",
     "color": "cadetblue", "icon": "eye", "essential": False},
    {"name": "University Chapel", "initials": "CHAP", "lat": 14.857100, "lon": 120.813000, "area": "Landmark",
     "color": "gray", "icon": "cross", "essential": False},
    {"name": "University Clock Tower", "initials": "TOWER", "lat": 14.857500, "lon": 120.813800, "area": "Landmark",
     "color": "gray", "icon": "clock", "essential": True},
    {"name": "Disaster Risk Mgt Office (DRMO)", "initials": "DRMO", "lat": 14.856900, "lon": 120.812800,
     "area": "Safety", "color": "red", "icon": "shield-alt", "essential": False},
]

# Create dictionaries for easy lookup of coordinates and names
LOCATION_COORDS = {item['initials']: (item['lat'], item['lon']) for item in BUILDING_DATA}
LOCATION_NAMES = {item['initials']: item['name'] for item in BUILDING_DATA}

df_buildings = pd.DataFrame(BUILDING_DATA)

# --- MASTER PATH DATA (Detailed KML Path representing the main loop) ---
# NOTE: This path is assumed to represent the main circular road/walkway.
# It is dense enough to ensure all 30 points can snap to the path accurately.

FULL_CAMPUS_PATH_RAW = [
    # Start near Gate 1/SEC
    [14.8571871, 120.8122971],
    [14.8572111, 120.8123284],
    [14.8573138, 120.8124503],
    [14.8574043, 120.8125576],

    # Path towards Admissions/Law/CIT/Canteen/DRMO/CHAP
    [14.8574637, 120.8127027],
    [14.8575001, 120.8127928],
    [14.8575711, 120.8129033],
    [14.8576403, 120.8130282],
    [14.8576918, 120.8131379],
    [14.857715, 120.8132049],  # Near Admissions/Law
    [14.8577382, 120.8132959],

    # Path towards CBA/Library/ADMIN/MUSE
    [14.8577696, 120.8134101],
    [14.8577907, 120.8135293],
    [14.8578119, 120.8136894],
    [14.8578275, 120.8138721],
    [14.8578335, 120.8140416],

    # Path towards Engineering/Registrars/Gate 2/SAO/TOWER
    [14.8578401, 120.8142273],
    [14.8578491, 120.8144061],
    [14.8578591, 120.814571],
    [14.8578667, 120.8147313],
    [14.8578761, 120.8148906],

    # Path towards Clinic/CAL/CSSP/ORES/AC/GYM
    [14.8578877, 120.8150393],
    [14.8579057, 120.8151909],
    [14.8579455, 120.8153403],
    [14.8579998, 120.8154564],
    [14.8580718, 120.8155495],
    [14.8581788, 120.8156108],
    [14.8582772, 120.8156641],
    [14.8583492, 120.8157077],
    [14.8584507, 120.8157508],
    [14.8585465, 120.8157797],
    [14.8586326, 120.8158052],
    [14.8587396, 120.8158223],
    [14.8588526, 120.8158406],
    [14.8589709, 120.815862],
    [14.8590684, 120.815891],
    [14.8591699, 120.8159336],
    [14.8592505, 120.8159846],
    [14.8593452, 120.8160411],  # Far end of campus (near G3)
]

# --- 2. STREAMLIT SIDEBAR AND USER INPUTS ---

st.sidebar.header("🔍 Map Tools")

# Standard filters/search
show_essentials = st.sidebar.checkbox("✅ Show New Student Essentials Only", value=True)

if show_essentials:
    filtered_df = df_buildings[df_buildings['essential'] == True].copy()
    st.sidebar.markdown(
        """
        <div style='background-color: #1E88E5; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>
            <p style='margin: 0; color: white; font-weight: bold;'>
                Quick Find Active: Essential locations only. (10 locations)
            </p>
        </div>
        """, unsafe_allow_html=True
    )
else:
    # Existing search and filter logic
    search_query = st.sidebar.text_input("Search Building Name (e.g., CBA or Engineering):", "")
    area_options = ["All Areas"] + sorted(df_buildings['area'].unique().tolist())
    selected_area = st.sidebar.selectbox("Filter by College/Area", area_options)

    if selected_area != "All Areas":
        area_filtered_df = df_buildings[df_buildings['area'] == selected_area].copy()
    else:
        area_filtered_df = df_buildings.copy()

    if search_query:
        filtered_df = area_filtered_df[area_filtered_df['name'].str.contains(search_query, case=False, na=False) |
                                       area_filtered_df['initials'].str.contains(search_query, case=False,
                                                                                 na=False)].copy()
    else:
        filtered_df = area_filtered_df.copy()

st.sidebar.markdown("---")
st.sidebar.header(f"🛣️ Dynamic Route Planner (30 Total Destinations)")
st.sidebar.caption("Route calculated by snapping start/end points to the main campus road network.")

# --- FEATURE 4: Dynamic Route Planner (Using the Full Path Data) ---

# Prepare location selectors
route_locs = ["Select Start Location"] + sorted(LOCATION_NAMES.keys())
route_destinations = ["Select Destination"] + sorted(LOCATION_NAMES.keys())

# Select Start
selected_start_initials = st.sidebar.selectbox(
    "1. Start Location (Simulated)",
    options=route_locs,
    format_func=lambda x: LOCATION_NAMES.get(x, x)
)

# Select Destination
selected_end_initials = st.sidebar.selectbox(
    "2. Destination",
    options=route_destinations,
    format_func=lambda x: LOCATION_NAMES.get(x, x)
)

# --- Dynamic Route Calculation Logic (Fixed for better path approximation) ---

route_to_display = None
calculated_distance = 0

if selected_start_initials != "Select Start Location" and selected_end_initials != "Select Destination":
    try:
        start_lat, start_lon = LOCATION_COORDS[selected_start_initials]
        end_lat, end_lon = LOCATION_COORDS[selected_end_initials]

        # 1. Find the index of the closest point on the master path for the START point
        start_index = find_closest_point_index(start_lat, start_lon, FULL_CAMPUS_PATH_RAW)

        # 2. Find the index of the closest point on the master path for the END point
        end_index = find_closest_point_index(end_lat, end_lon, FULL_CAMPUS_PATH_RAW)

        # 3. Determine the path segment
        # Check if the path needs to be reversed based on the index order
        if start_index <= end_index:
            path_segment = FULL_CAMPUS_PATH_RAW[start_index: end_index + 1]
        else:
            # Reverse the path segment if the end point index is numerically smaller
            path_segment = FULL_CAMPUS_PATH_RAW[end_index: start_index + 1]
            path_segment.reverse()

        # 4. Connect the actual start/end location coordinates to the path segment

        # Prepend the true start location coordinate
        if [start_lat, start_lon] != path_segment[0]:
            path_segment.insert(0, [start_lat, start_lon])

        # Append the true end location coordinate
        if [end_lat, end_lon] != path_segment[-1]:
            path_segment.append([end_lat, end_lon])

        route_to_display = path_segment
        calculated_distance = calculate_polyline_distance(route_to_display)

        # Display Route Information
        st.info(f"""
        Route highlighted in purple: **{LOCATION_NAMES[selected_start_initials]}** to **{LOCATION_NAMES[selected_end_initials]}**.
        \n\nApproximate Walking Distance: **{calculated_distance / 1000:.2f} km** (or **{calculated_distance:.0f} meters**)
        """)

    except KeyError:
        st.warning("Please select valid Start and Destination locations.")
    except Exception as e:
        st.error(f"An error occurred during routing: {e}")

# --- 3. FOLIUM MAP INITIALIZATION ---

m = folium.Map(
    location=[campus_lat, campus_lon],
    zoom_start=18,
    tiles=None,
    control_scale=True
)

# Add Tile Layers
folium.TileLayer('OpenStreetMap', name='Map View (Standard)', control=True).add_to(m)
folium.TileLayer('Esri.WorldImagery', name='Satellite View', control=True).add_to(m)

# Add Locate Control (Geolocation) - Live Location Feature
plugins.LocateControl(
    auto_start=False,
    position='topleft',
    strings={"title": "Locate Me (Your Live Position)"},
    locateOptions={'enableHighAccuracy': True, 'maxAge': 5000}
).add_to(m)

# --- 4. MARKER AND FEATURE RENDERING ---

# Add markers for filtered buildings
for index, b in filtered_df.iterrows():
    popup_html = f"""
        <div style="font-family: sans-serif;">
            <b>{b['name']} ({b['initials']})</b><br>
            Area: <i>{b['area']}</i><br>
            Lat: {b['lat']:.5f}, Lon: {b['lon']:.5f}
        </div>
    """
    folium.Marker(
        location=[b["lat"], b["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=f"{b['name']} ({b['initials']})",
        icon=folium.Icon(color=b['color'], icon=b['icon'], prefix='fa')
    ).add_to(m)

# Highlighted Dynamic Path Drawing
if route_to_display:
    # Add start marker
    folium.Marker(
        location=[route_to_display[0][0], route_to_display[0][1]],
        icon=folium.Icon(color='purple', icon='street-view', prefix='fa'),
        tooltip=f"Start: {LOCATION_NAMES.get(selected_start_initials, 'Unknown')}"
    ).add_to(m)

    # Add end marker
    folium.Marker(
        location=[route_to_display[-1][0], route_to_display[-1][1]],
        icon=folium.Icon(color='black', icon='flag-checkered', prefix='fa'),
        tooltip=f"Destination: {LOCATION_NAMES.get(selected_end_initials, 'Unknown')}"
    ).add_to(m)

    # Draw the path
    folium.PolyLine(
        locations=route_to_display,
        color="purple",
        weight=8,
        opacity=0.9,
        tooltip=f"Route: {LOCATION_NAMES.get(selected_start_initials, '')} to {LOCATION_NAMES.get(selected_end_initials, '')}"
    ).add_to(m)

    # Zoom to fit the route
    if len(route_to_display) > 2:
        m.fit_bounds(
            [[min(p[0] for p in route_to_display), min(p[1] for p in route_to_display)],
             [max(p[0] for p in route_to_display), max(p[1] for p in route_to_display)]]
        )
    elif len(route_to_display) == 1:
        m.location = route_to_display[0]
        m.zoom_start = 19

# Add Layer Control to switch between Map and Satellite
folium.LayerControl(collapsed=False).add_to(m)

# --- 5. RENDER MAP ---
st_folium(m, width=1200, height=700)