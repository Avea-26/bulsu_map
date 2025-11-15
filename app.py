import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
import math
import heapq
import xml.etree.ElementTree as ET

# ==============================================================================
# --- 0. UTILITY FUNCTIONS & KML GRAPH CONSTRUCTION ---
# ==============================================================================

# KML Content (Full content provided by the user in Untitled map (1).kml)
KML_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Untitled map</name>
    <description/>
    <Style id="icon-1899-0288D1-nodesc-normal">
      <IconStyle>
        <color>ffd18802</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="icon-1899-0288D1-nodesc-highlight">
      <IconStyle>
        <color>ffd18802</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="icon-1899-0288D1-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1899-0288D1-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1899-0288D1-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>
    <Style id="icon-1899-DB4436-nodesc-normal">
      <IconStyle>
        <color>ff3644db</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="icon-1899-DB4436-nodesc-highlight">
      <IconStyle>
        <color>ff3644db</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="32" xunits="pixels" y="64" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="icon-1899-DB4436-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1899-DB4436-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1899-DB4436-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>
    <Style id="line-000000-5-nodesc-normal">
      <LineStyle>
        <color>ff000000</color>
        <width>5</width>
      </LineStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="line-000000-5-nodesc-highlight">
      <LineStyle>
        <color>ff000000</color>
        <width>7</width>
      </LineStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="line-000000-5-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#line-000000-5-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#line-000000-5-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>
    <Placemark>
      <name>Eng'g</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8142186,14.8574643,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Federizo Hall</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8163769,14.8582716,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>CBA Building</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8135223,14.8587155,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>CIT Building</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8128033,14.8580142,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Admissions Office</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8130833,14.858348,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Law Building</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8133502,14.8578964,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>NURSING</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8131379,14.857321,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>SAO and REG</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8144026,14.857777,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Admin/Registrar</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8149202,14.858177,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Clinic</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.815201,14.8580436,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>ORES/CAL/CANTEEN</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8156641,14.8580857,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>LIB</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.813955,14.8588078,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>CS</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8147814,14.8584346,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>CAFA</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.815162,14.8584065,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>HRM</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.813098,14.858591,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>COED</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8145229,14.8574768,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>AC</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8126866,14.8576402,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Line</name>
      <styleUrl>#line-000000-5-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.812328,14.857242,0
          120.812629,14.857247,0
          120.812822,14.857621,0
          120.812702,14.857867,0
          120.813088,14.857896,0
          120.813353,14.858003,0
          120.813498,14.858348,0
          120.813955,14.858718,0
          120.81412,14.858709,0
          120.814238,14.859781,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Line 2</name>
      <styleUrl>#line-000000-5-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.813364,14.857321,0
          120.813636,14.857321,0
          120.813876,14.857436,0
          120.813955,14.857662,0
          120.813936,14.857777,0
          120.813936,14.858043,0
          120.813955,14.858296,0
          120.813735,14.858522,0
          120.813522,14.858716,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Line 3</name>
      <styleUrl>#line-000000-5-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.813936,14.857185,0
          120.81421,14.857218,0
          120.814349,14.857501,0
          120.814387,14.857777,0
          120.814526,14.85804,0
          120.81484,14.858348,0
          120.814781,14.858435,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Line 4</name>
      <styleUrl>#line-000000-5-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.814526,14.858043,0
          120.815044,14.858296,0
          120.815201,14.858223,0
          120.815664,14.858296,0
          120.816075,14.858384,0
          120.81639,14.858272,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Line 5</name>
      <styleUrl>#line-000000-5-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.815664,14.858086,0
          120.815857,14.858025,0
          120.815957,14.857962,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Line 6</name>
      <styleUrl>#line-000000-5-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.814349,14.857501,0
          120.814402,14.857777,0
          120.814526,14.858043,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Line 7</name>
      <styleUrl>#line-000000-5-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.815162,14.858407,0
          120.815456,14.858686,0
          120.81577,14.858639,0
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>"""


# Haversine distance in meters
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# --- Dijkstra's Algorithm for Shortest Path ---
def dijkstra(graph, start_node, end_node):
    # Initialize distances and path tracking
    distances = {node: float('infinity') for node in graph['adj']}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph['adj']}
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if we found a shorter path already
        if current_distance > distances[current_node]:
            continue

        # Check neighbors
        for neighbor, weight in graph['adj'][current_node].items():
            distance = current_distance + weight

            # If a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruct the path from end_node to start_node
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]

    # Return the path in correct order (start to end) and the total distance
    if path and path[-1] == start_node:
        return path[::-1], distances[end_node]
    else:
        return [], float('infinity')


# --- KML Graph Parser ---
KML_NS = {'kml': 'http://www.opengis.net/kml/2.2'}
NODE_MATCH_TOLERANCE_M = 15  # Tolerance for snapping KML points to Buildings


def parse_kml_paths(kml_content, building_locations):
    all_nodes = building_locations.copy()
    raw_edges = set()
    junction_counter = 0

    try:
        root = ET.fromstring(kml_content)
    except ET.ParseError:
        st.error("Error: Could not parse KML content.")
        return {"nodes": building_locations, "adj": {bid: {} for bid in building_locations}}

    # Helper to find the closest official building node
    def find_closest_building(lat, lon):
        min_distance = float('inf')
        closest_id = None
        for b_id, (b_lat, b_lon) in building_locations.items():
            dist = haversine(lat, lon, b_lat, b_lon)
            if dist < min_distance:
                min_distance = dist
                closest_id = b_id

        if min_distance <= NODE_MATCH_TOLERANCE_M:
            return closest_id
        return None

    # Parse all LineString placemarks
    for placemark in root.findall('.//kml:Placemark', KML_NS):
        line_string = placemark.find('kml:LineString', KML_NS)
        if line_string is not None:
            coords_element = line_string.find('kml:coordinates', KML_NS)
            if coords_element is not None and coords_element.text:
                points = []
                for coord_triple in coords_element.text.strip().split():
                    try:
                        # KML is Lon, Lat, Alt. We want Lat, Lon.
                        lon, lat, _ = map(float, coord_triple.split(','))
                        points.append((lat, lon))
                    except ValueError:
                        continue

                previous_node_id = None
                for lat, lon in points:
                    current_node_id = find_closest_building(lat, lon)

                    if current_node_id is None:
                        # Create a new Junction Node if not close to a building
                        found_existing = False
                        for node_id, (n_lat, n_lon) in all_nodes.items():
                            # Merge junctions within 5m to simplify the graph at intersections
                            if node_id.startswith('J') and haversine(lat, lon, n_lat, n_lon) < 5:
                                current_node_id = node_id
                                found_existing = True
                                break

                        if not found_existing:
                            current_node_id = f"J{junction_counter:04d}"
                            all_nodes[current_node_id] = (lat, lon)
                            junction_counter += 1

                    if previous_node_id is not None and previous_node_id != current_node_id:
                        p_lat, p_lon = all_nodes[previous_node_id]
                        c_lat, c_lon = all_nodes[current_node_id]
                        distance = haversine(p_lat, p_lon, c_lat, c_lon)

                        # Store the edge (undirected graph means storing both directions)
                        raw_edges.add(tuple(sorted((previous_node_id, current_node_id))))
                        raw_edges.add(tuple(sorted((current_node_id, previous_node_id))))

                    previous_node_id = current_node_id

    # Build adjacency list structure for Dijkstra's
    adj_list = {node_id: {} for node_id in all_nodes.keys()}

    for u, v in set(raw_edges):
        u_lat, u_lon = all_nodes[u]
        v_lat, v_lon = all_nodes[v]
        weight = haversine(u_lat, u_lon, v_lat, v_lon)

        # Bidirectional edge
        adj_list[u][v] = weight
        adj_list[v][u] = weight

    return {
        "nodes": all_nodes,
        "adj": adj_list
    }


# ==============================================================================
# --- 1. CONFIGURATION AND DATA (Accurate 24 Destinations) ---
# ==============================================================================

st.set_page_config(page_title="BulSU Campus Map for New Students", layout="wide")
st.title("🗺️ Bulacan State University – Malolos Campus Map: KML Accurate Routing")

st.error(
    "🚨 **LIVE LOCATION (SIMULATED):** Routing uses the **accurate pathways** from your KML data via Dijkstra's algorithm, which ensures the shortest route across the campus road network. Use the 'Start Location' selector."
)

# Campus center coordinates
campus_lat, campus_lon = 14.85806, 120.814

# Definitive 24 Locations (with display properties)
BUILDING_DATA = [
    {"name": "Gate 1 (Main Gate)", "initials": "G1", "lat": 14.857238955221407, "lon": 120.81232477926912,
     "area": "Entrance", "color": "green", "icon": "info-sign", "essential": True},
    {"name": "Gate 2", "initials": "G2", "lat": 14.857300700584918, "lon": 120.81435233511922, "area": "Entrance",
     "color": "green", "icon": "info-sign", "essential": False},
    {"name": "Gate 3 (Back Gate)", "initials": "G3", "lat": 14.857964639512025, "lon": 120.8159557242234,
     "area": "Entrance", "color": "green", "icon": "info-sign", "essential": False},
    {"name": "Gate 4", "initials": "G4", "lat": 14.859785542562445, "lon": 120.8143242171718, "area": "Entrance",
     "color": "green", "icon": "info-sign", "essential": False},
    {"name": "Admissions Office", "initials": "AO", "lat": 14.857873189628554, "lon": 120.8132365530903,
     "area": "Admin", "color": "darkred", "icon": "clipboard", "essential": True},
    {"name": "Office of the Registrars", "initials": "REG", "lat": 14.857698785690705, "lon": 120.81485371788727,
     "area": "Admin", "color": "darkred", "icon": "users", "essential": True},
    {"name": "Student Affairs Office (SAO)", "initials": "SAO", "lat": 14.857199922401415, "lon": 120.81399243466453,
     "area": "Admin", "color": "darkred", "icon": "handshake", "essential": False},
    {"name": "University Administration Building", "initials": "ADMIN", "lat": 14.857944003200735,
     "lon": 120.81502639264933, "area": "Admin", "color": "darkred", "icon": "building", "essential": True},
    {"name": "Academic Services Office (ASO)", "initials": "AS", "lat": 14.85811640625455, "lon": 120.81402190536379,
     "area": "Admin", "color": "darkred", "icon": "lightbulb", "essential": True},
    {"name": "Office of Research and Extension (ORES)", "initials": "ORES", "lat": 14.857860301934194,
     "lon": 120.81558075766027, "area": "Admin", "color": "darkred", "icon": "search", "essential": False},
    {"name": "BulSU e-Library (Main)", "initials": "LIB", "lat": 14.858511328844196, "lon": 120.81363203587286,
     "area": "Library", "color": "darkblue", "icon": "book", "essential": True},
    {"name": "University Clinic/Infirmary", "initials": "CLINIC", "lat": 14.858069005870963, "lon": 120.8150577454633,
     "area": "Safety", "color": "red", "icon": "plus", "essential": True},
    {"name": "CIT Building (College of Industrial Technology)", "initials": "CIT", "lat": 14.857916898968318,
     "lon": 120.8124644476262, "area": "Technology", "color": "blue", "icon": "cogs", "essential": False},
    {"name": "CBA Building (College of Business Administration)", "initials": "CBA", "lat": 14.858113743130097,
     "lon": 120.81395446499842, "area": "Business", "color": "blue", "icon": "briefcase", "essential": False},
    {"name": "College of Engineering", "initials": "ENG", "lat": 14.857516165033935, "lon": 120.81425755461224,
     "area": "Engineering", "color": "blue", "icon": "wrench", "essential": False},
    {"name": "College of Nursing", "initials": "NUR", "lat": 14.857001546558466, "lon": 120.81346496183792,
     "area": "Health", "color": "blue", "icon": "medkit", "essential": False},
    {"name": "College of Law", "initials": "LAW", "lat": 14.85771684777094, "lon": 120.81346247026019, "area": "Law",
     "color": "blue", "icon": "legal", "essential": False},
    {"name": "College of Architecture and Fine Arts (CAFA)", "initials": "CAFA", "lat": 14.858106757593719,
     "lon": 120.81463715167531, "area": "Arts", "color": "blue", "icon": "camera-retro", "essential": False},
    {"name": "College of Arts and Letters (CAL)", "initials": "CAL", "lat": 14.858728209078443,
     "lon": 120.81515208080097, "area": "Arts", "color": "blue", "icon": "theater-masks", "essential": False},
    {"name": "College of Education (CoEd)", "initials": "COED", "lat": 14.857358838901337, "lon": 120.81420846891311,
     "area": "Education", "color": "blue", "icon": "graduation-cap", "essential": False},
    {"name": "College of Science (CS)", "initials": "CS", "lat": 14.858556881619181, "lon": 120.81474858877631,
     "area": "Science", "color": "blue", "icon": "flask", "essential": False},
    {"name": "HRM Building (College of Hospitality)", "initials": "HRM", "lat": 14.858318644487495,
     "lon": 120.81334666644518, "area": "Hospitality", "color": "blue", "icon": "utensils", "essential": False},
    {"name": "Activity Center (Gym Annex)", "initials": "AC", "lat": 14.857219535229188, "lon": 120.81294476398705,
     "area": "Sports", "color": "orange", "icon": "trophy", "essential": True},
    {"name": "Food Stalls/Canteen Annex", "initials": "CANTEEN", "lat": 14.858289546983633, "lon": 120.81549844558987,
     "area": "Food", "color": "beige", "icon": "coffee", "essential": True},
]

# Create data structures
df_buildings = pd.DataFrame(BUILDING_DATA)
LOCATION_COORDS = {item['initials']: (item['lat'], item['lon']) for item in BUILDING_DATA}
LOCATION_NAMES = {item['initials']: item['name'] for item in BUILDING_DATA}

# --- Graph Generation (Run only once) ---
# This runs the KML parser and builds the graph of nodes and edges
CAMPUS_PATHWAY_GRAPH = parse_kml_paths(KML_CONTENT, LOCATION_COORDS)
GRAPH_NODES = CAMPUS_PATHWAY_GRAPH['nodes']
GRAPH_ADJACENCY = CAMPUS_PATHWAY_GRAPH['adj']

# ==============================================================================
# --- 2. STREAMLIT SIDEBAR AND USER INPUTS ---
# ==============================================================================

st.sidebar.header("🔍 Map Tools")

# Standard filters/search
show_essentials = st.sidebar.checkbox("✅ Show New Student Essentials Only", value=True)

if show_essentials:
    filtered_df = df_buildings[df_buildings['essential'] == True].copy()
    st.sidebar.markdown(
        """
        <div style='background-color: #1E88E5; padding: 10px; border-radius: 5px; margin-bottom: 15px;'>
            <p style='margin: 0; color: white; font-weight: bold;'>
                Quick Find Active: Essential locations only.
            </p>
        </div>
        """, unsafe_allow_html=True
    )
else:
    # Existing search and filter logic
    search_query = st.sidebar.text_input("Search Building Name (e.g., CBA or Engineering):", "")
    area_options = ["All Areas"] + sorted(df_buildings['area'].unique().tolist())
    selected_area = st.sidebar.selectbox("Filter by College/Area", area_options)

    area_filtered_df = df_buildings.copy()
    if selected_area != "All Areas":
        area_filtered_df = df_buildings[df_buildings['area'] == selected_area].copy()

    if search_query:
        filtered_df = area_filtered_df[area_filtered_df['name'].str.contains(search_query, case=False, na=False) |
                                       area_filtered_df['initials'].str.contains(search_query, case=False,
                                                                                 na=False)].copy()
    else:
        filtered_df = area_filtered_df.copy()

st.sidebar.markdown("---")
st.sidebar.header(f"🛣️ Dynamic Route Planner ({len(BUILDING_DATA)} Total Destinations)")
st.sidebar.caption("Route calculated using Dijkstra's on KML pathway data.")

# --- Dynamic Route Planner (Using Graph Data) ---

# Prepare location selectors (only use actual building initials)
initials_list = sorted(LOCATION_NAMES.keys())
route_locs = ["Select Start Location"] + initials_list
route_destinations = ["Select Destination"] + initials_list

# Select Start
selected_start_initials = st.sidebar.selectbox(
    "1. Start Location",
    options=route_locs,
    format_func=lambda x: LOCATION_NAMES.get(x, x)
)

# Select Destination
selected_end_initials = st.sidebar.selectbox(
    "2. Destination",
    options=route_destinations,
    format_func=lambda x: LOCATION_NAMES.get(x, x)
)

# --- Dynamic Route Calculation Logic ---

route_to_display = None
calculated_distance = 0

if selected_start_initials not in ["Select Start Location", "Select Destination"] and selected_end_initials not in [
    "Select Start Location", "Select Destination"]:
    try:
        # 1. Find the shortest path of node IDs
        path_nodes, calculated_distance = dijkstra(
            {"adj": GRAPH_ADJACENCY},
            selected_start_initials,
            selected_end_initials
        )

        if path_nodes:
            # 2. Convert path of node IDs (Building + Junction) to Lat/Lon coordinates
            route_to_display = [[GRAPH_NODES[node][0], GRAPH_NODES[node][1]] for node in path_nodes]

            # Display Route Information
            st.info(f"""
            Route highlighted in purple: **{LOCATION_NAMES[selected_start_initials]}** to **{LOCATION_NAMES[selected_end_initials]}**.
            \n\nShortest Walking Distance: **{calculated_distance / 1000:.2f} km** (or **{calculated_distance:.0f} meters**)
            """)
        else:
            st.warning(
                f"Could not find a connected path between {LOCATION_NAMES[selected_start_initials]} and {LOCATION_NAMES[selected_end_initials]}.")

    except Exception as e:
        st.error(f"An error occurred during routing: {e}")

# ==============================================================================
# --- 3. FOLIUM MAP INITIALIZATION & RENDERING ---
# ==============================================================================

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

# --- 4. Draw all KML Path Segments (Optional: for network visibility) ---
# To see the underlying network the shortest path is calculated on:
# for u, neighbors in GRAPH_ADJACENCY.items():
#     for v, weight in neighbors.items():
#         # Ensure we only draw each unique segment once
#         if u < v:
#             u_lat, u_lon = GRAPH_NODES[u]
#             v_lat, v_lon = GRAPH_NODES[v]
#             folium.PolyLine(
#                 locations=[[u_lat, u_lon], [v_lat, v_lon]],
#                 color="#CCCCCC",
#                 weight=1,
#                 opacity=0.4
#             ).add_to(m)


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
        location=route_to_display[0],
        icon=folium.Icon(color='purple', icon='street-view', prefix='fa'),
        tooltip=f"Start: {LOCATION_NAMES.get(selected_start_initials, 'Unknown')}"
    ).add_to(m)

    # Add end marker
    folium.Marker(
        location=route_to_display[-1],
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
    if len(route_to_display) > 1:
        # Create bounds list [min_lat, min_lon], [max_lat, max_lon]
        lats = [p[0] for p in route_to_display]
        lons = [p[1] for p in route_to_display]
        m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]])

# Add Layer Control to switch between Map and Satellite
folium.LayerControl(collapsed=False).add_to(m)

# --- 5. RENDER MAP ---
st_folium(m, width=1200, height=700)