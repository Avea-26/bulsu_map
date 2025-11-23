# app.py (improved, robust pathway snapping + full-building connectivity)
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
import math
import heapq
import xml.etree.ElementTree as ET

# -----------------------------
#  Helper functions (haversine, dijkstra)
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def dijkstra(graph, start_node, end_node):
    distances = {node: float('inf') for node in graph['adj']}
    if start_node not in distances or end_node not in distances:
        return [], float('inf')
    distances[start_node] = 0
    previous = {node: None for node in graph['adj']}
    pq = [(0, start_node)]
    while pq:
        dist_u, u = heapq.heappop(pq)
        if dist_u > distances[u]:
            continue
        for v, w in graph['adj'][u].items():
            nd = dist_u + w
            if nd < distances[v]:
                distances[v] = nd
                previous[v] = u
                heapq.heappush(pq, (nd, v))
    # reconstruct
    path = []
    cur = end_node
    while cur is not None:
        path.append(cur)
        cur = previous.get(cur)
    if path and path[-1] == start_node:
        return path[::-1], distances[end_node]
    else:
        return [], float('inf')

# -----------------------------
#  Embedded KML (keeps UX simple)
#  -- (kept the content you had, ensure this is comprehensive for the main campus)
# -----------------------------
KML_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <!-- ... (your original long KML content here) ... -->
    <!-- For brevity in this snippet, use the same KML you had embedded. -->
  </Document>
</kml>"""
# NOTE: In your real file, keep the full KML content (the large string from your earlier app.py).

# -----------------------------
#  BUILDING DATA (all buildings MUST be included)
# -----------------------------
BUILDING_DATA = [
    {"name": "Gate 1 (Main Gate)", "initials": "G1", "lat": 14.857238955221407, "lon": 120.81232477926912, "essential": True},
    {"name": "Gate 2", "initials": "G2", "lat": 14.857300700584918, "lon": 120.81435233511922, "essential": False},
    {"name": "Gate 3 (Back Gate)", "initials": "G3", "lat": 14.857964639512025, "lon": 120.8159557242234, "essential": False},
    {"name": "Gate 4", "initials": "G4", "lat": 14.859785542562445, "lon": 120.8143242171718, "essential": False},
    {"name": "Admissions Office", "initials": "AO", "lat": 14.857873189628554, "lon": 120.8132365530903, "essential": True},
    {"name": "Office of the Registrars", "initials": "REG", "lat": 14.857698785690705, "lon": 120.81485371788727, "essential": True},
    {"name": "Student Affairs Office (SAO)", "initials": "SAO", "lat": 14.857199922401415, "lon": 120.81399243466453, "essential": False},
    {"name": "University Administration Building", "initials": "ADMIN", "lat": 14.857944003200735, "lon": 120.81502639264933, "essential": True},
    {"name": "Academic Services Office (ASO)", "initials": "AS", "lat": 14.85811640625455, "lon": 120.81402190536379, "essential": True},
    {"name": "Office of Research and Extension (ORES)", "initials": "ORES", "lat": 14.857860301934194, "lon": 120.81558075766027, "essential": False},
    {"name": "BulSU e-Library (Main)", "initials": "LIB", "lat": 14.858511328844196, "lon": 120.81363203587286, "essential": True},
    {"name": "University Clinic/Infirmary", "initials": "CLINIC", "lat": 14.858069005870963, "lon": 120.8150577454633, "essential": True},
    {"name": "CIT Building (College of Industrial Technology)", "initials": "CIT", "lat": 14.857916898968318, "lon": 120.8124644476262, "essential": False},
    {"name": "CBA Building (College of Business Administration)", "initials": "CBA", "lat": 14.858113743130097, "lon": 120.81395446499842, "essential": False},
    {"name": "College of Engineering", "initials": "ENG", "lat": 14.857516165033935, "lon": 120.81425755461224, "essential": False},
    {"name": "College of Nursing", "initials": "NUR", "lat": 14.857001546558466, "lon": 120.81346496183792, "essential": False},
    {"name": "College of Law", "initials": "LAW", "lat": 14.85771684777094, "lon": 120.81346247026019, "essential": False},
    {"name": "College of Architecture and Fine Arts (CAFA)", "initials": "CAFA", "lat": 14.858106757593719, "lon": 120.81463715167531, "essential": False},
    {"name": "College of Arts and Letters (CAL)", "initials": "CAL", "lat": 14.858728209078443, "lon": 120.81515208080097, "essential": False},
    {"name": "College of Education (CoEd)", "initials": "COED", "lat": 14.857358838901337, "lon": 120.81420846891311, "essential": False},
    {"name": "College of Science (CS)", "initials": "CS", "lat": 14.858556881619181, "lon": 120.81474858877631, "essential": False},
    {"name": "HRM Building (College of Hospitality)", "initials": "HRM", "lat": 14.858318644487495, "lon": 120.81334666644518, "essential": False},
    {"name": "Activity Center (Gym Annex)", "initials": "AC", "lat": 14.857219535229188, "lon": 120.81294476398705, "essential": True},
    {"name": "Food Stalls/Canteen Annex", "initials": "CANTEEN", "lat": 14.858289546983633, "lon": 120.81549844558987, "essential": True},
    {"name": "NSTP Building", "initials": "NSTP", "lat": 14.8566904, "lon": 120.8128336, "essential": False},
    # Add any other buildings here to be sure nothing is left out
]

df_buildings = pd.DataFrame(BUILDING_DATA)
LOCATION_COORDS = {b['initials']:(b['lat'], b['lon']) for b in BUILDING_DATA}
LOCATION_NAMES = {b['initials']: b['name'] for b in BUILDING_DATA}

# -----------------------------
#  KML -> Graph parser (robust)
#    - snaps line points to buildings within SNAP_TO_BUILDING_M
#    - merges junctions within MERGE_JUNCTION_M
#    - ensures every building is present in nodes
#    - auto-connects isolated buildings to nearest junction/path if within CONNECT_ISOLATED_M
# -----------------------------
KML_NS = {'kml': 'http://www.opengis.net/kml/2.2'}

# Tuning params (adjust if you need stricter/looser snapping)
SNAP_TO_BUILDING_M = 30      # if a LineString point is within this to a building, snap to that building
MERGE_JUNCTION_M = 6         # merge two junctions if closer than this
CONNECT_ISOLATED_M = 50      # connect an otherwise isolated building to nearest path/junction within this distance
MIN_SEGMENT_M = 0.5          # ignore tiny segments under this length (meters)

def parse_kml_paths(kml_content, building_locations):
    # building_locations: dict initials -> (lat, lon)
    all_nodes = building_locations.copy()  # includes building nodes with initials
    edges = set()
    junction_counter = 0

    # Helper functions
    def find_building_snap(lat, lon):
        best = None
        best_d = float('inf')
        for b_id, (b_lat, b_lon) in building_locations.items():
            d = haversine(lat, lon, b_lat, b_lon)
            if d < best_d:
                best_d = d; best = b_id
        if best_d <= SNAP_TO_BUILDING_M:
            return best, best_d
        return None, best_d

    def find_closest_node(lat, lon, only_junctions=False):
        best = None
        best_d = float('inf')
        for nid, (nlat, nlon) in all_nodes.items():
            if only_junctions and not str(nid).startswith('J'):
                continue
            d = haversine(lat, lon, nlat, nlon)
            if d < best_d:
                best_d = d; best = nid
        return best, best_d

    # Parse KML
    try:
        ET.register_namespace('', KML_NS['kml'])
        root = ET.fromstring(kml_content)
    except ET.ParseError as e:
        st.error(f"KML parse error: {e}")
        return {"nodes": all_nodes, "adj": {nid:{} for nid in all_nodes}}

    for placemark in root.findall('.//kml:Placemark', KML_NS):
        line = placemark.find('kml:LineString', KML_NS)
        if line is None:
            continue
        coords_el = line.find('kml:coordinates', KML_NS)
        if coords_el is None or not coords_el.text:
            continue
        raw_points = []
        for triple in coords_el.text.strip().split():
            parts = triple.strip().split(',')
            if len(parts) < 2:
                continue
            lon, lat = float(parts[0]), float(parts[1])
            raw_points.append((lat, lon))
        if not raw_points:
            continue

        prev_node = None
        for (lat, lon) in raw_points:
            # 1) snap to building if close enough
            b_snap, d_build = find_building_snap(lat, lon)
            if b_snap:
                node_id = b_snap
            else:
                # 2) check if near existing junction (merge if within MERGE_JUNCTION_M)
                # find closest junction-only node
                closest_junc, d_junc = find_closest_node(lat, lon, only_junctions=True)
                if closest_junc and d_junc <= MERGE_JUNCTION_M:
                    node_id = closest_junc
                else:
                    # create new junction
                    node_id = f"J{junction_counter:05d}"
                    all_nodes[node_id] = (lat, lon)
                    junction_counter += 1
            # add edge from prev_node
            if prev_node and prev_node != node_id:
                u, v = sorted((prev_node, node_id))
                edges.add((u, v))
            prev_node = node_id

    # Build adjacency
    adj = {nid: {} for nid in all_nodes.keys()}
    for u, v in edges:
        u_lat, u_lon = all_nodes[u]; v_lat, v_lon = all_nodes[v]
        dist = haversine(u_lat, u_lon, v_lat, v_lon)
        if dist < MIN_SEGMENT_M:
            continue
        adj[u][v] = dist
        adj[v][u] = dist

    # Now ensure every building has at least one connection; if isolated, try to connect
    for b_id, (b_lat, b_lon) in building_locations.items():
        if len(adj.get(b_id, {})) == 0:
            # find nearest junction or node within CONNECT_ISOLATED_M
            best_node = None; best_d = float('inf')
            for nid, (nlat, nlon) in all_nodes.items():
                if nid == b_id:
                    continue
                d = haversine(b_lat, b_lon, nlat, nlon)
                if d < best_d:
                    best_d = d; best_node = nid
            if best_node and best_d <= CONNECT_ISOLATED_M:
                adj.setdefault(b_id, {})[best_node] = best_d
                adj.setdefault(best_node, {})[b_id] = best_d
            else:
                # fallback: connect to nearest building (even if farther)
                best_other = None; best_d2 = float('inf')
                for other_id, (olat, olon) in building_locations.items():
                    if other_id == b_id:
                        continue
                    d2 = haversine(b_lat, b_lon, olat, olon)
                    if d2 < best_d2:
                        best_d2 = d2; best_other = other_id
                if best_other:
                    adj.setdefault(b_id, {})[best_other] = best_d2
                    adj.setdefault(best_other, {})[b_id] = best_d2

    return {"nodes": all_nodes, "adj": adj}

# Build the graph once
GRAPH = parse_kml_paths(KML_CONTENT, LOCATION_COORDS)
GRAPH_NODES = GRAPH['nodes']
GRAPH_ADJ = GRAPH['adj']

# -----------------------------
#  Streamlit UI
# -----------------------------
st.set_page_config(page_title="BulSU Campus Map (Accurate Campus Pathways)", layout="wide")
st.title("BulSU Campus Map — Accurate Pathways (Gates → All Buildings)")

st.sidebar.header("Controls")
use_live_start = st.sidebar.checkbox("Use device location as Start (recommended)", value=True)
show_essentials = st.sidebar.checkbox("Show essentials only (quick view)", value=False)

initials_list = sorted(LOCATION_NAMES.keys())
dest_options = ["Select Destination"] + initials_list
selected_dest = st.sidebar.selectbox("Select Destination", options=dest_options, format_func=lambda x: LOCATION_NAMES.get(x, x))

if not use_live_start:
    start_options = ["Select Start"] + initials_list
    selected_start = st.sidebar.selectbox("Select Start", options=start_options, format_func=lambda x: LOCATION_NAMES.get(x, x))
else:
    selected_start = None

st.sidebar.markdown("---")
st.sidebar.caption("Routing uses Dijkstra on campus pathways parsed from embedded KML. All buildings forced into the graph to avoid missing nodes.")

# Map init
campus_lat, campus_lon = 14.85806, 120.814
m = folium.Map(location=[campus_lat, campus_lon], zoom_start=18, control_scale=True, tiles=None)
folium.TileLayer('OpenStreetMap', name='Map').add_to(m)
folium.TileLayer('Esri.WorldImagery', name='Satellite').add_to(m)

# Locate controls
plugins.LocateControl(auto_start=False, position='topleft', strings={"title":"Locate Me"}, locateOptions={'enableHighAccuracy':True}).add_to(m)

# Add left-side simple locate button (helps on mobile)
locate_js = """
L.Control.SimpleLocate = L.Control.extend({
    onAdd: function(map){
        var btn = L.DomUtil.create('button', '');
        btn.innerHTML = '&#10148;'; // arrow symbol
        btn.title = 'Locate (left)';
        btn.style.width='36px'; btn.style.height='36px'; btn.style.background='white';
        btn.style.border='1px solid #888'; btn.style.borderRadius='4px';
        L.DomEvent.on(btn, 'click', function(){ map.locate({setView:true, maxZoom:18, enableHighAccuracy:true}); });
        return btn;
    },
    onRemove: function(map){}
});
L.control.simpleLocate = function(opts){ return new L.Control.SimpleLocate(opts); }
L.control.simpleLocate({ position: 'topleft' }).addTo({{this._parent.get_name()}});
"""
m.get_root().script.add_child(folium.Element(locate_js))

# Add building markers
if show_essentials:
    df_display = df_buildings[df_buildings['essential']==True]
else:
    df_display = df_buildings

for idx, row in df_display.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"{row['name']} ({row['initials']})",
        tooltip=row['name'],
        icon=folium.DivIcon(html=f"""<div style="background:rgba(0,0,0,0.6);color:white;padding:4px 6px;border-radius:4px;font-weight:bold;">{row['initials']}</div>""")
    ).add_to(m)

# If destination selected, add pulsing marker
DEST_PULSE_RADIUS = 8  # meters: considered "arrived"
if selected_dest and selected_dest != "Select Destination":
    dlat, dlon = LOCATION_COORDS[selected_dest]
    # css for pulse
    css = """
    <style>
    .pulse {
      width:18px;height:18px;border-radius:9px;background:#d00;border:3px solid white;
      box-shadow:0 0 8px rgba(255,0,0,0.6);
      animation: pulse 1.2s infinite;
    }
    @keyframes pulse {
      0% { transform: scale(1); opacity: 1;}
      70% { transform: scale(1.8); opacity: 0;}
      100% { transform: scale(1); opacity: 0;}
    }
    </style>
    """
    m.get_root().html.add_child(folium.Element(css))
    folium.map.Marker([dlat, dlon], icon=folium.DivIcon(html='<div class="pulse"></div>'), tooltip=f"Destination: {LOCATION_NAMES[selected_dest]}").add_to(m)

# Render map and capture st_folium output
st_map = st_folium(m, width=1100, height=700)

# Extract user location from st_folium return (supports multiple versions)
user_lat = user_lon = None
candidates = ['last_clicked','last_object_clicked','geolocation','location','last_location','last_known_location','user_location']
for k in candidates:
    if k in st_map:
        val = st_map[k]
        if isinstance(val, dict) and 'lat' in val and 'lng' in val:
            user_lat, user_lon = val['lat'], val['lng']; break
        if isinstance(val, (list,tuple)) and len(val) >= 2:
            user_lat, user_lon = val[0], val[1]; break

if use_live_start and not (user_lat and user_lon):
    st.sidebar.info("Click the locate button on the map and allow browser geolocation to set your start position.")

# Route calculation
route_coords = None
route_distance_m = None

if use_live_start and (user_lat and user_lon) and selected_dest and selected_dest != "Select Destination":
    # snap user to nearest graph node
    nearest = None; nearest_d = float('inf')
    for nid, (nlat, nlon) in GRAPH_NODES.items():
        d = haversine(user_lat, user_lon, nlat, nlon)
        if d < nearest_d:
            nearest_d = d; nearest = nid
    start_node = nearest
    end_node = selected_dest
    path, dist = dijkstra({'adj':GRAPH_ADJ}, start_node, end_node)
    if path:
        route_coords = [[GRAPH_NODES[n][0], GRAPH_NODES[n][1]] for n in path]
        route_distance_m = dist

elif (not use_live_start) and selected_start and selected_start != "Select Start" and selected_dest and selected_dest != "Select Destination":
    path, dist = dijkstra({'adj':GRAPH_ADJ}, selected_start, selected_dest)
    if path:
        route_coords = [[GRAPH_NODES[n][0], GRAPH_NODES[n][1]] for n in path]
        route_distance_m = dist

# Draw route if available (re-render minimal overlay)
if route_coords:
    folium.PolyLine(route_coords, color='purple', weight=7, opacity=0.9, tooltip=f"Route: {route_distance_m/1000:.2f} km").add_to(m)
    # add start and end markers
    s = route_coords[0]; e = route_coords[-1]
    folium.Marker(location=s, icon=folium.Icon(color='purple', icon='street-view', prefix='fa'), tooltip='Start').add_to(m)
    folium.Marker(location=e, icon=folium.Icon(color='black', icon='flag-checkered', prefix='fa'), tooltip='Destination').add_to(m)
    # re-render map with route
    st_folium(m, width=1100, height=700)
    st.success(f"Route distance: {route_distance_m:.0f} meters ({route_distance_m/1000:.2f} km)")

# Arrival detection
if user_lat and user_lon and selected_dest and selected_dest != "Select Destination":
    d_to_dest = haversine(user_lat, user_lon, LOCATION_COORDS[selected_dest][0], LOCATION_COORDS[selected_dest][1])
    if d_to_dest <= DEST_PULSE_RADIUS:
        st.balloons()
        st.success(f"Arrived at {LOCATION_NAMES[selected_dest]} (within {DEST_PULSE_RADIUS} m).")
    else:
        st.info(f"{LOCATION_NAMES[selected_dest]} is {d_to_dest:.0f} meters away.")

# Debug / info (optional)
with st.expander("Graph diagnostics (show/hide)"):
    st.write(f"Total graph nodes: {len(GRAPH_NODES)}")
    # show any isolated nodes (degree 0)
    isolated = [nid for nid, nbrs in GRAPH_ADJ.items() if len(nbrs)==0]
    if isolated:
        st.warning(f"Isolated nodes (should be none): {isolated}")
    else:
        st.success("No isolated nodes detected.")

# End of app
