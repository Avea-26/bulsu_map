# app.py - Campus routing with KML data integration
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins
import math
import heapq
from xml.etree import ElementTree as ET


# -----------------------------
# Helpers
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def dijkstra(adj, start, end):
    if start not in adj or end not in adj:
        return [], float('inf')
    dist = {n: float('inf') for n in adj}
    prev = {n: None for n in adj}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == end:
            break
        for v, w in adj[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if dist[end] == float('inf'):
        return [], float('inf')
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1], dist[end]


# -----------------------------
# Parse KML Data (embedded)
# -----------------------------
KML_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>BulSU Campus Map</name>
    <Folder>
      <name>Buildings</name>
      <Placemark><name>gate 1</name><Point><coordinates>120.8123468,14.857199,0</coordinates></Point></Placemark>
      <Placemark><name>Bulsu College Of Industrial Technology</name><Point><coordinates>120.8124739,14.8575988,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Activity Center</name><Point><coordinates>120.8129463,14.8571973,0</coordinates></Point></Placemark>
      <Placemark><name>BSU Mini Rizal Park</name><Point><coordinates>120.8131742,14.8574316,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College of Law</name><Point><coordinates>120.8134628,14.8577083,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Pacesetter Office</name><Point><coordinates>120.8133915,14.8577582,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Admissions Office</name><Point><coordinates>120.8132402,14.8578601,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College of Nursing</name><Point><coordinates>120.8134642,14.8569883,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU NSTP Building</name><Point><coordinates>120.8136227,14.8568562,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College of Education</name><Point><coordinates>120.8142103,14.8573439,0</coordinates></Point></Placemark>
      <Placemark><name>Bulacan State University Heroes Park</name><Point><coordinates>120.8142017,14.8579017,0</coordinates></Point></Placemark>
      <Placemark><name>College of Business Administration</name><Point><coordinates>120.8139152,14.8582262,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Science Research and Learning Center</name><Point><coordinates>120.8137774,14.8581727,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College of Home Economics</name><Point><coordinates>120.8132252,14.8582897,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Hostel</name><Point><coordinates>120.8133047,14.8586429,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Office of the Registrars</name><Point><coordinates>120.8149438,14.8577661,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College Of Engineering</name><Point><coordinates>120.8143985,14.8576204,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Flores Hall</name><Point><coordinates>120.8150765,14.857891,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Natividad Hall</name><Point><coordinates>120.8150816,14.8578739,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College of Architecture and Fine Arts</name><Point><coordinates>120.8146495,14.8580875,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Graduate School</name><Point><coordinates>120.8146236,14.8580227,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Valencia Hall</name><Point><coordinates>120.8152496,14.8582025,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College of Physical Education, Recreation and Sport</name><Point><coordinates>120.8149004,14.8582616,0</coordinates></Point></Placemark>
      <Placemark><name>University Canteen</name><Point><coordinates>120.8155031,14.8582773,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU Office of the Student Government</name><Point><coordinates>120.8151019,14.8584384,0</coordinates></Point></Placemark>
      <Placemark><name>College of Science</name><Point><coordinates>120.8147537,14.8585331,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College of Arts and Letters Library</name><Point><coordinates>120.8151457,14.8587149,0</coordinates></Point></Placemark>
      <Placemark><name>BulSU College of Arts and Letters</name><Point><coordinates>120.8149633,14.8587356,0</coordinates></Point></Placemark>
      <Placemark><name>College of Social Sciences and Philosophy</name><Point><coordinates>120.8149123,14.8591141,0</coordinates></Point></Placemark>
      <Placemark><name>gate 4</name><Point><coordinates>120.8145156,14.8596125,0</coordinates></Point></Placemark>
      <Placemark><name>gate 2</name><Point><coordinates>120.8143784,14.8572791,0</coordinates></Point></Placemark>
      <Placemark><name>gate 3</name><Point><coordinates>120.8159642,14.8579783,0</coordinates></Point></Placemark>
    </Folder>
    <Folder>
      <name>Routes</name>
      <Placemark>
        <name>gate 1 to Registrars</name>
        <LineString><tessellate>1</tessellate><coordinates>120.81232,14.85723,0 120.8126,14.85746,0 120.81276,14.8576,0 120.81301,14.85782,0 120.81304,14.85784,0 120.81351,14.85825,0 120.81362,14.85814,0 120.81385,14.85787,0 120.81418,14.85814,0 120.81422,14.85816,0 120.81427,14.85813,0 120.81458,14.85781,0 120.81472,14.85768,0</coordinates></LineString>
      </Placemark>
      <Placemark>
        <name>gate 1 to Arts and Letters</name>
        <LineString><tessellate>1</tessellate><coordinates>120.81232,14.85723,0 120.81276,14.8576,0 120.81301,14.85782,0 120.81304,14.85784,0 120.81351,14.85825,0 120.81362,14.85814,0 120.81385,14.85787,0 120.81418,14.85814,0 120.81422,14.85816,0 120.81427,14.85813,0 120.81458,14.85781,0 120.81489,14.85808,0 120.81507,14.85825,0 120.81544,14.85856,0 120.81514,14.85889,0</coordinates></LineString>
      </Placemark>
      <Placemark>
        <name>gate 1 to Hostel</name>
        <LineString><tessellate>1</tessellate><coordinates>120.81232,14.85723,0 120.81276,14.8576,0 120.81301,14.85782,0 120.81304,14.85784,0 120.81351,14.85825,0 120.81339,14.8584,0 120.81338,14.85858,0</coordinates></LineString>
      </Placemark>
      <Placemark>
        <name>gate 1 to Admissions</name>
        <LineString><tessellate>1</tessellate><coordinates>120.81232,14.85723,0 120.81276,14.8576,0 120.81301,14.85782,0 120.81304,14.85784,0 120.81316,14.85795,0</coordinates></LineString>
      </Placemark>
      <Placemark>
        <name>gate 1 to Pacesetter</name>
        <LineString><tessellate>1</tessellate><coordinates>120.81232,14.85723,0 120.81276,14.8576,0 120.81301,14.85782,0 120.81304,14.85784,0 120.81309,14.8578,0 120.81326,14.85763,0</coordinates></LineString>
      </Placemark>
      <Placemark>
        <name>gate 1 to Law</name>
        <LineString><tessellate>1</tessellate><coordinates>120.81232,14.85723,0 120.81276,14.8576,0 120.81301,14.85782,0 120.81304,14.85784,0 120.81309,14.8578,0 120.81332,14.85757,0</coordinates></LineString>
      </Placemark>
      <Placemark>
        <name>gate 1 to Nursing</name>
        <LineString><tessellate>1</tessellate><coordinates>120.81232,14.85723,0 120.81276,14.8576,0 120.81331,14.85704,0 120.81337,14.85709,0</coordinates></LineString>
      </Placemark>
      <Placemark>
        <name>gate 1 to NSTP</name>
        <LineString><tessellate>1</tessellate><coordinates>120.81232,14.85723,0 120.81276,14.8576,0 120.81331,14.85704,0 120.81314,14.8569,0 120.81327,14.85667,0 120.81356,14.85691,0</coordinates></LineString>
      </Placemark>
    </Folder>
  </Document>
</kml>"""


def parse_kml():
    """Parse KML data and extract buildings and routes"""
    root = ET.fromstring(KML_DATA)
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    buildings = {}
    routes = {}
    
    for placemark in root.findall('.//kml:Placemark', ns):
        name_elem = placemark.find('kml:name', ns)
        if name_elem is None:
            continue
        name = name_elem.text
        
        point = placemark.find('.//kml:Point/kml:coordinates', ns)
        if point is not None:
            coords = point.text.strip().split(',')
            lon, lat = float(coords[0]), float(coords[1])
            buildings[name] = [lat, lon]
        
        linestring = placemark.find('.//kml:LineString/kml:coordinates', ns)
        if linestring is not None:
            coords_text = linestring.text.strip()
            coords_list = []
            for coord in coords_text.split():
                parts = coord.split(',')
                if len(parts) >= 2:
                    lon, lat = float(parts[0]), float(parts[1])
                    coords_list.append([lat, lon])
            if coords_list:
                routes[name] = coords_list
    
    return buildings, routes


BUILDINGS, KML_ROUTES = parse_kml()

BUILDING_MAPPING = {
    "gate 1": ("G1", "Gate 1 (Main Gate)"),
    "Bulsu College Of Industrial Technology": ("CIT", "College of Industrial Technology"),
    "BulSU Activity Center": ("AC", "Activity Center"),
    "BSU Mini Rizal Park": ("PARK", "Mini Rizal Park"),
    "BulSU College of Law": ("LAW", "College of Law"),
    "BulSU Pacesetter Office": ("PACE", "Pacesetter Office"),
    "BulSU Admissions Office": ("AO", "Admissions Office"),
    "BulSU College of Nursing": ("NURS", "College of Nursing"),
    "BulSU NSTP Building": ("NSTP", "NSTP Building"),
    "BulSU College of Education": ("COED", "College of Education"),
    "Bulacan State University Heroes Park": ("HP", "Heroes Park"),
    "College of Business Administration": ("CBA", "College of Business Administration"),
    "BulSU Science Research and Learning Center": ("SCI", "Science Research Center"),
    "BulSU College of Home Economics": ("CHK", "College of Home Economics"),
    "BulSU Hostel": ("HOST", "University Hostel"),
    "BulSU Office of the Registrars": ("REG", "Office of the Registrars"),
    "BulSU College Of Engineering": ("ENG", "College of Engineering"),
    "BulSU Flores Hall": ("FH", "Flores Hall"),
    "BulSU Natividad Hall": ("NH", "Natividad Hall"),
    "BulSU College of Architecture and Fine Arts": ("CAFA", "College of Architecture and Fine Arts"),
    "BulSU Graduate School": ("GRAD", "Graduate School"),
    "BulSU Valencia Hall": ("VH", "Valencia Hall"),
    "BulSU College of Physical Education, Recreation and Sport": ("CPERS", "College of Physical Education"),
    "University Canteen": ("CANT", "University Canteen"),
    "BulSU Office of the Student Government": ("OSG", "Office of Student Government"),
    "College of Science": ("CS", "College of Science"),
    "BulSU College of Arts and Letters Library": ("CALL", "Arts and Letters Library"),
    "BulSU College of Arts and Letters": ("CAL", "College of Arts and Letters"),
    "College of Social Sciences and Philosophy": ("CSSP", "College of Social Sciences"),
    "gate 2": ("G2", "Gate 2"),
    "gate 3": ("G3", "Gate 3"),
    "gate 4": ("G4", "Gate 4"),
}

BUILDING_CODES = {}
BUILDING_NAMES = {}
BUILDING_COORDS = {}

for full_name, (code, friendly_name) in BUILDING_MAPPING.items():
    if full_name in BUILDINGS:
        BUILDING_CODES[full_name] = code
        BUILDING_NAMES[code] = friendly_name
        BUILDING_COORDS[code] = BUILDINGS[full_name]

ROUTES = {"G1": [BUILDING_COORDS["G1"]]}

for route_name, route_coords in KML_ROUTES.items():
    if "Registrars" in route_name:
        ROUTES["REG"] = route_coords
    elif "Arts and Letters" in route_name:
        ROUTES["CAL"] = route_coords
    elif "Hostel" in route_name:
        ROUTES["HOST"] = route_coords
    elif "Admissions" in route_name:
        ROUTES["AO"] = route_coords
    elif "Pacesetter" in route_name:
        ROUTES["PACE"] = route_coords
    elif "Law" in route_name:
        ROUTES["LAW"] = route_coords
    elif "Nursing" in route_name:
        ROUTES["NURS"] = route_coords
    elif "NSTP" in route_name:
        ROUTES["NSTP"] = route_coords

# For buildings without detailed routes, create paths that connect to the road network
# by finding intermediate points from existing detailed routes
for code, coords in BUILDING_COORDS.items():
    if code not in ROUTES and code != "G1":
        # Strategy: Find a path that goes through the detailed route network
        # by connecting to intermediate points from existing routes

        # Get all unique points from detailed routes (excluding Gate 1)
        all_route_points = set()
        for route_name, route_coords in ROUTES.items():
            if route_name != "G1":
                for point in route_coords[1:]:  # Skip Gate 1 point
                    all_route_points.add(tuple(point))

        # Find the closest route point to the destination
        closest_point = None
        min_distance = float('inf')

        for point in all_route_points:
            dist = haversine(coords[0], coords[1], point[0], point[1])
            if dist < min_distance:
                min_distance = dist
                closest_point = point

        if closest_point and min_distance < 200:  # Only if reasonably close (200m)
            # Create path: Gate 1 -> closest route point -> destination
            ROUTES[code] = [BUILDING_COORDS["G1"], list(closest_point), coords]
        else:
            # For distant buildings, try to find a path through multiple intermediate points
            # This creates a more realistic walking path
            intermediate_points = []

            # Sample a few points from different routes to create connections
            route_sample_points = []
            for route_coords in ROUTES.values():
                if len(route_coords) > 2:  # Only detailed routes
                    # Take middle points from routes
                    mid_idx = len(route_coords) // 2
                    route_sample_points.append(route_coords[mid_idx])

            # Find 1-2 intermediate points that create a reasonable path
            for sample_point in route_sample_points[:3]:  # Limit to 3 samples
                dist_to_dest = haversine(sample_point[0], sample_point[1], coords[0], coords[1])
                if dist_to_dest < 500:  # If sample point is reasonably close to destination
                    intermediate_points.append(sample_point)
                    break

            if intermediate_points:
                path = [BUILDING_COORDS["G1"]] + intermediate_points + [coords]
                ROUTES[code] = path
            else:
                # Final fallback: straight line
                ROUTES[code] = [BUILDING_COORDS["G1"], coords]

# Build graph
MERGE_TOLERANCE_M = 4.0
nodes = {}
building_node = {}

def find_or_create_node(lat, lon):
    is_g1_coord = ROUTES.get("G1") and [lat, lon] == ROUTES["G1"][0]
    for nid, (nlat, nlon) in nodes.items():
        if haversine(lat, lon, nlat, nlon) <= MERGE_TOLERANCE_M:
            if is_g1_coord and nid != building_node.get("G1"):
                continue
            return nid
    nid = f"N{len(nodes):05d}"
    nodes[nid] = (lat, lon)
    return nid

if "G1" in ROUTES:
    g1_lat, g1_lon = ROUTES["G1"][0]
    G1_FIXED_NODE_ID = "N00000_G1"
    nodes[G1_FIXED_NODE_ID] = (g1_lat, g1_lon)
    building_node["G1"] = G1_FIXED_NODE_ID

edges = {}

def add_edge(u, v, w):
    edges.setdefault(u, {})[v] = min(edges.get(u, {}).get(v, float('inf')), w)
    edges.setdefault(v, {})[u] = min(edges.get(v, {}).get(u, float('inf')), w)

for bkey, poly in ROUTES.items():
    if bkey == "G1":
        continue
    prev_node = None
    for (lat, lon) in poly:
        nid = find_or_create_node(lat, lon)
        if prev_node is None and bkey != "G1" and "G1" in building_node:
            g1_node = building_node["G1"]
            g1_lat, g1_lon = nodes[g1_node]
            if haversine(lat, lon, g1_lat, g1_lon) <= MERGE_TOLERANCE_M:
                nid = g1_node
        if prev_node is not None and prev_node != nid:
            (plat, plon) = nodes[prev_node]
            (clat, clon) = nodes[nid]
            dist = haversine(plat, plon, clat, clon)
            add_edge(prev_node, nid, dist)
        prev_node = nid
    if prev_node is not None:
        building_node[bkey] = prev_node

for bkey, coords in BUILDING_COORDS.items():
    if bkey == "G1":
        continue
    if bkey not in building_node:
        lat, lon = coords
        best = None
        bd = float('inf')
        for nid, (nlat, nlon) in nodes.items():
            d = haversine(lat, lon, nlat, nlon)
            if d < bd:
                bd = d
                best = nid
        if best is None:
            best = find_or_create_node(lat, lon)
        building_node[bkey] = best

adj = {nid: {} for nid in nodes.keys()}
for u, nbrs in edges.items():
    for v, w in nbrs.items():
        adj[u][v] = w

for bkey, nid in building_node.items():
    if len(adj.get(nid, {})) == 0:
        best = None
        bd = float('inf')
        for other, (olat, olon) in nodes.items():
            if other == nid:
                continue
            d = haversine(nodes[nid][0], nodes[nid][1], olat, olon)
            if d < bd:
                bd = d
                best = other
        if best:
            adj[nid][best] = bd
            adj[best][nid] = bd

ICON_MAP = {
    "CALL": "book", "CANT": "cutlery", "ENG": "cog", "CIT": "wrench",
    "COED": "graduation-cap", "REG": "file-text-o", "AO": "info-circle",
    "HP": "flag", "AC": "home", "G1": "map-marker", "CBA": "briefcase",
    "LAW": "legal", "NURS": "heartbeat", "HOST": "bed", "CAL": "book",
    "CS": "flask", "CAFA": "paint-brush", "GRAD": "mortar-board",
}

def get_icon_for(bkey):
    return ICON_MAP.get(bkey, "university")

# Streamlit UI
st.set_page_config(page_title="BulSU Campus Navigation", layout="wide")
st.title("🗺️ BulSU Campus Navigation System")

st.sidebar.header("🧭 Navigation")
st.sidebar.info("📍 Click the locate button (➤) on the map to enable GPS")

dest_options = ["Select Destination"] + sorted([k for k in BUILDING_NAMES.keys() if k != "G1"])
selected_dest = st.sidebar.selectbox(
    "Where do you want to go?",
    options=dest_options,
    format_func=lambda x: BUILDING_NAMES.get(x, x) if x != "Select Destination" else x
)

st.sidebar.markdown("---")
st.sidebar.caption(f"📊 Graph: {len(nodes)} nodes | {sum(len(n) for n in adj.values()) // 2} edges")

campus_center = [14.85806, 120.814]
m = folium.Map(location=campus_center, zoom_start=17, tiles=None, control_scale=True)
folium.TileLayer('OpenStreetMap', name='Map').add_to(m)
folium.TileLayer('Esri.WorldImagery', name='Satellite').add_to(m)

locate_js = """
L.Control.EnhancedLocate = L.Control.extend({
    onAdd: function(map){
        var btn = L.DomUtil.create('button', 'locate-btn');
        btn.innerHTML = '➤';
        btn.title = 'Find My Location';
        btn.style.cssText = 'width:50px;height:50px;background:#4CAF50;color:white;font-size:24px;border:2px solid white;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,0.3);cursor:pointer;';
        btn.onmouseover = function(){ this.style.background='#45a049'; };
        btn.onmouseout = function(){ this.style.background='#4CAF50'; };
        L.DomEvent.on(btn, 'click', function(e){
            L.DomEvent.stopPropagation(e);
            map.locate({setView:true, maxZoom:18, enableHighAccuracy:true});
        });
        return btn;
    },
    onRemove: function(map){}
});
L.control.enhancedLocate = function(opts){ return new L.Control.EnhancedLocate(opts); };
L.control.enhancedLocate({ position: 'topleft' }).addTo(""" + m.get_name() + """);
"""
m.get_root().script.add_child(folium.Element(locate_js))

for bkey, node_id in building_node.items():
    lat, lon = nodes[node_id]
    folium.Marker(
        location=[lat, lon],
        popup=BUILDING_NAMES.get(bkey, bkey),
        tooltip=BUILDING_NAMES.get(bkey, bkey),
        icon=folium.Icon(icon=get_icon_for(bkey), prefix='fa', color='blue' if bkey == 'G1' else 'red')
    ).add_to(m)
    label_html = f"""<div style="background:rgba(0,0,0,0.7);color:white;padding:4px 8px;border-radius:4px;font-weight:bold;font-size:11px;white-space:nowrap;">{bkey}</div>"""
    folium.map.Marker([lat, lon], icon=folium.DivIcon(html=label_html)).add_to(m)

for poly in ROUTES.values():
    if len(poly) > 1:
        folium.PolyLine(locations=poly, color="#999999", weight=2, opacity=0.3).add_to(m)

DEST_PULSE_RADIUS = 8.0
if selected_dest and selected_dest != "Select Destination":
    dest_node = building_node[selected_dest]
    dlat, dlon = nodes[dest_node]
    m.get_root().html.add_child(folium.Element("""
        <style>
        .pulse-marker {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #FF0000;
            border: 4px solid white;
            box-shadow: 0 0 0 0 rgba(255, 0, 0, 1);
            animation: pulse-animation 1.5s infinite;
        }
        @keyframes pulse-animation {
            0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); transform: scale(1); }
            50% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); transform: scale(1.1); }
            100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); transform: scale(1); }
        }
        </style>
    """))
    folium.map.Marker([dlat, dlon], icon=folium.DivIcon(html='<div class="pulse-marker"></div>'),
                      tooltip=f"🎯 {BUILDING_NAMES.get(selected_dest, selected_dest)}").add_to(m)

map_data = st_folium(m, width=1100, height=700, key="main_map")

if "trail" not in st.session_state:
    st.session_state["trail"] = []

user_lat = user_lon = None
for k in ['last_clicked', 'last_object_clicked', 'geolocation', 'location', 'last_location', 
          'last_known_location', 'user_location', 'center']:
    if k in map_data and map_data[k]:
        val = map_data[k]
        if isinstance(val, dict) and 'lat' in val and 'lng' in val:
            user_lat, user_lon = val['lat'], val['lng']
            break
        if isinstance(val, (list, tuple)) and len(val) >= 2:
            user_lat, user_lon = val[0], val[1]
            break

if user_lat and user_lon:
    new_pt = [user_lat, user_lon]
    append_point = True
    if st.session_state["trail"]:
        last = st.session_state["trail"][-1]
        if haversine(last[0], last[1], new_pt[0], new_pt[1]) < 0.5:
            append_point = False
    if append_point:
        st.session_state["trail"].append(new_pt)

route_coords = None
route_dist_m = None

if selected_dest and selected_dest != "Select Destination" and user_lat and user_lon:
    best = None
    bd = float('inf')
    for nid, (nlat, nlon) in nodes.items():
        d = haversine(user_lat, user_lon, nlat, nlon)
        if d < bd:
            bd = d
            best = nid
    
    if best:
        end_node = building_node[selected_dest]
        path, dist = dijkstra(adj, best, end_node)
        if path:
            route_coords = [[nodes[n][0], nodes[n][1]] for n in path]
            route_dist_m = dist
            d_to_node = haversine(user_lat, user_lon, route_coords[0][0], route_coords[0][1])
            route_coords.insert(0, [user_lat, user_lon])
            route_dist_m += d_to_node

if st.session_state.get("trail") and len(st.session_state["trail"]) >= 1:
    folium.PolyLine(locations=st.session_state["trail"], color='#1E88E5', weight=5, opacity=0.8).add_to(m)
    cur = st.session_state["trail"][-1]
    folium.Marker(location=cur, icon=folium.Icon(color='blue', icon='circle', prefix='fa'),
                  tooltip="📍 You are here").add_to(m)

if route_coords:
    folium.PolyLine(locations=route_coords, color='#9C27B0', weight=8, opacity=0.9).add_to(m)
    folium.Marker(location=route_coords[0], icon=folium.Icon(color='green', icon='play', prefix='fa'),
                  tooltip='🚀 Start').add_to(m)
    folium.Marker(location=route_coords[-1], icon=folium.Icon(color='red', icon='flag-checkered', prefix='fa'),
                  tooltip='🏁 Destination').add_to(m)
    st_folium(m, width=1100, height=700, key="route_map")
    st.success(f"📏 Route distance: **{route_dist_m:.0f} meters** ({route_dist_m / 1000:.2f} km)")
    eta_seconds = route_dist_m / 1.4
    eta_minutes = int(eta_seconds / 60)
    st.info(f"⏱️ Estimated walking time: **{eta_minutes} minutes**")

# Arrival detection
if user_lat and user_lon and selected_dest and selected_dest != "Select Destination":
    dest_n = building_node[selected_dest]
    d_to_dest = haversine(user_lat, user_lon, nodes[dest_n][0], nodes[dest_n][1])
    if d_to_dest <= DEST_PULSE_RADIUS:
        st.balloons()
        st.success(f"🎉 Arrived at {BUILDING_NAMES.get(selected_dest, selected_dest)} (within {DEST_PULSE_RADIUS} m)!")
    else:
        if route_dist_m is None:
            st.info(f"{BUILDING_NAMES.get(selected_dest, selected_dest)} is {d_to_dest:.0f} meters away (Straight-line).")

# Diagnostics (optional)
with st.expander("📊 Graph diagnostics"):
    st.write(f"**Nodes:** {len(nodes)}")
    edge_count = sum(len(n) for n in adj.values()) // 2
    st.write(f"**Edges:** {edge_count}")
    st.write("**Building → Node mapping (sample):**")
    for k in sorted(list(building_node.keys())[:10]):  # Show first 10
        nid = building_node[k]
        lat, lon = nodes[nid]
        st.write(f"{k}: {nid} @ {lat:.6f},{lon:.6f}")
