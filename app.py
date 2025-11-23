# app.py - Campus routing from embedded polylines (no KML)
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins
import math
import heapq

# -----------------------------
# Helpers
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def dijkstra(adj, start, end):
    if start not in adj or end not in adj:
        return [], float('inf')
    dist = {n: float('inf') for n in adj}
    prev = {n: None for n in adj}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d,u = heapq.heappop(pq)
        if d>dist[u]:
            continue
        if u==end:
            break
        for v,w in adj[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq,(nd,v))
    # reconstruct
    if dist[end] == float('inf'):
        return [], float('inf')
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1], dist[end]

# -----------------------------
# User-supplied polylines (Gate 1 -> building paths)
# keys use short initials (consistent with earlier app)
# -----------------------------
ROUTES = {
    "G1": [  # Gate 1 main coordinate (start ref)
        [14.857227383607164, 120.81231458047134]
    ],
    "AO": [  # Admissions Office (polyline from your data)
        [14.857223717206535, 120.81231552877544],
        [14.857244799009289, 120.81234208129061],
        [14.857263131010008, 120.81236578889342],
        [14.857276880009541, 120.81238665158389],
        [14.857298878406947, 120.81241130749082],
        [14.857307127805404, 120.81242932526898],
        [14.857334625797986, 120.81244734304711],
        [14.857351124591831, 120.81246725743348],
        [14.857357540789103, 120.8124833786034],
        [14.85737495618073, 120.81250518959799],
        [14.857392371570958, 120.81252415568024],
        [14.857415286555966, 120.81255070819539],
        [14.857438201538544, 120.81256777766941],
        [14.857450117328524, 120.81258010562287],
        [14.8574730323074, 120.81260476152981],
        [14.85748586469451, 120.81262372761208],
        [14.857502363476803, 120.81264743521487],
        [14.857524361851258, 120.8126626080807],
        [14.857537194235327, 120.81268916059584],
        [14.857558276007472, 120.81271191989453],
        [14.857572941586888, 120.81273562749735],
        [14.857593106756976, 120.81274985205904],
        [14.857618771516158, 120.8127707147495],
        [14.857628854099273, 120.81278778422353],
        [14.857645352870664, 120.81281338843459],
        [14.857664601435681, 120.8128361477333],
        [14.857677141674149, 120.81286418726205],
        [14.85769872309557, 120.8128785409386],
        [14.85771413839527, 120.81290166630639],
        [14.857749593580392, 120.81293515821835],
        [14.857764238111672, 120.81296944755678],
        [14.857790444112537, 120.81297263726269],
        [14.857805088641056, 120.81299735748343],
        [14.857834377695106, 120.81301649571883],
        [14.857838231288541, 120.81303483631322],
        [14.857823586779652, 120.81305716422804],
        [14.857805088451215, 120.8130810869939],
        [14.85779121470385, 120.81310341490872],
        [14.85777271637264, 120.81312255312142],
        [14.857743427344987, 120.81315205786598],
        [14.857722616717663, 120.81317199350421],
    ],
    "ADMIN": [
        [14.857227383607164, 120.81231458047134],
        [14.858253523986543, 120.81350449542867],
        [14.858264505945309, 120.81349649102147],
        [14.858283949876494, 120.81348576218518],
        [14.85829237557947, 120.81348039776702],
        [14.858297560627278, 120.81346497506483],
        [14.858313763900917, 120.81346028119896],
        [14.858328022780693, 120.81344687015358],
        [14.858336448481952, 120.81343748242182],
    ],
    "REG": [
        [14.857231951696395, 120.81230999474423],
        [14.85824387586885, 120.81351054775081],
        [14.857875404028864, 120.81385383383957],
        [14.858133884344007, 120.81418005044027],
        [14.858143050306836, 120.81421608599655],
        [14.8581412171143, 120.81427108763508],
        [14.857712249633623, 120.81468454822817],
    ],
    "SAO": [
        [14.85722737753228, 120.8123075991754],
        [14.85760501646353, 120.81275709532477],
        [14.857053223433768, 120.81331090492655],
        [14.857249375934748, 120.8135460843465],
        [14.857291539533183, 120.81355556738761],
        [14.857377699904417, 120.81382678236385],
        [14.857207212328058, 120.8139747178054],
    ],
    "RH": [  # Roxas Hall - same as SAO path in your data
        [14.85722737753228, 120.8123075991754],
        [14.85760501646353, 120.81275709532477],
        [14.857053223433768, 120.81331090492655],
        [14.857249375934748, 120.8135460843465],
        [14.857291539533183, 120.81355556738761],
        [14.857377699904417, 120.81382678236385],
        [14.857207212328058, 120.8139747178054],
    ],
    "FH": [  # Federizo Hall
        [14.857222232375102, 120.81230441212736],
        [14.858248874509577, 120.81351140619314],
        [14.8578807357222, 120.81384936453658],
        [14.858129618353198, 120.81417927624206],
        [14.858145173507996, 120.81421146275096],
        [14.858129618353198, 120.81425437809614],
        [14.858007769601818, 120.81436971308635],
    ],
    "CIT": [
        [14.857231342857316, 120.81231006196273],
        [14.857585150218535, 120.812741540334],
        [14.857657561498218, 120.81269128021603],
    ],
    "CBA": [
        [14.857231737951556, 120.81231007737065],
        [14.858266157606362, 120.81351170703611],
        [14.858133938828905, 120.81362435981724],
        [14.858244926024813, 120.81375484455948],
    ],
    "COED": [
        [14.85723756264293, 120.81230881959102],
        [14.858258054075955, 120.81350176818223],
        [14.857857257411418, 120.81386858392554],
        [14.85813164905436, 120.81416203652014],
        [14.858122399903529, 120.81426091728572],
        [14.857801762429997, 120.81457031839095],
        [14.857820260758727, 120.81457669779518],
        [14.858560192608307, 120.8154602452812],
        [14.858849998558496, 120.81515403387809],
    ],
    "CHK": [
        [14.85723756264293, 120.81229606078254],
        [14.858254971027538, 120.81348900937378],
        [14.858412206441201, 120.81338055950185],
    ],
    "ENG": [
        [14.857221573677649, 120.8123046187677],
        [14.858255990827312, 120.8135008810616],
        [14.857488604143063, 120.81419557149684],
    ],
    "CAL": [
        [14.857239487230459, 120.81229892389935],
        [14.858250729509088, 120.81351101070327],
        [14.857856098939296, 120.81385868823384],
        [14.85813357363394, 120.81418084814753],
        [14.858155154984129, 120.81425740099832],
        [14.858121241432857, 120.81424783189196],
        [14.857809853122198, 120.81457637120987],
        [14.858546701963194, 120.8154471598874],
        [14.858824175770527, 120.81518241461181],
    ],
    "AC": [
        [14.85723286054277, 120.81230926933186],
        [14.857601000434475, 120.8127598804564],
        [14.857313229164221, 120.81303883020017],
    ],
    "LIB": [
        [14.85723522104112, 120.8123009072618],
        [14.858251122031646, 120.81349855399958],
    ],
    "HP": [
        [14.857235220206237, 120.81230090641704],
        [14.85826856368972, 120.81350306659485],
        [14.85773445216894, 120.813965435894],
        [14.857902315932083, 120.81418872643358],
    ],
    "CANTEEN": [
        [14.857239968415367, 120.81230782991943],
        [14.857600686477925, 120.81274960366244],
        [14.857044193830047, 120.81331099123477],
        [14.857258466792201, 120.81355500344662],
        [14.857266174448752, 120.81364750480797],
        [14.857238426883884, 120.8137368164672],
    ],
    "CLINIC": [
        [14.857232934975002, 120.81230328608719],
        [14.85825319820291, 120.813494168965],
        [14.857876050178037, 120.81384376526438],
        [14.858126755584948, 120.81417757332686],
        [14.858155096177963, 120.81423621528677],
        [14.857808468669555, 120.81457904520612],
        [14.858100595034262, 120.81491285328552],
    ],
}

# -----------------------------
# Map building initials to friendly names (keep consistent with app UI)
# -----------------------------
BUILDING_NAMES = {
    "G1": "Gate 1 (Main Gate)",
    "AO": "Admissions Office",
    "ADMIN": "University Administration",
    "REG": "Office of the Registrars",
    "SAO": "Student Affairs Office (SAO)",
    "RH": "Roxas Hall",
    "FH": "Federizo Hall",
    "CIT": "CIT Building",
    "CBA": "CBA Building",
    "COED": "College of Education (COED)",
    "CHK": "Home Economics / Kinesthetics (CHK)",
    "ENG": "College of Engineering (ENG)",
    "CAL": "College of Arts and Letters (CAL)",
    "AC": "Activity Center (AC)",
    "LIB": "BSU Main Library (LIB)",
    "HP": "Heroes Park / Rizal Monument (HP)",
    "CANTEEN": "Food Court / Canteen",
    "CLINIC": "University Infirmary / Clinic",
}

# -----------------------------
# Build graph: create unique nodes by merging nearby points
# -----------------------------
MERGE_TOLERANCE_M = 4.0  # merge points within 4 meters

# node_id -> (lat, lon)
nodes = {}
# map coordinate (lat, lon) candidate to node id by merging rule
def find_or_create_node(lat, lon):
    # try to find an existing node within tolerance
    for nid, (nlat, nlon) in nodes.items():
        if haversine(lat, lon, nlat, nlon) <= MERGE_TOLERANCE_M:
            return nid
    # else create new
    nid = f"N{len(nodes):05d}"
    nodes[nid] = (lat, lon)
    return nid

# We'll also track building -> node association to ensure each building has a node
building_node = {}

# iterate routes and create nodes + edges
edges = {}  # edges as adjacency temporary: (u)-> {v:distance}
def add_edge(u, v, w):
    edges.setdefault(u, {})[v] = min(edges.get(u, {}).get(v, float('inf')), w)
    edges.setdefault(v, {})[u] = min(edges.get(v, {}).get(u, float('inf')), w)

# Build graph from each route polyline
for bkey, poly in ROUTES.items():
    prev_node = None
    for (lat, lon) in poly:
        nid = find_or_create_node(lat, lon)
        # if this polyline represents a building endpoint (not G1 reference), associate last point
        prev_node = prev_node if prev_node is not None else None
        if prev_node is not None and prev_node != nid:
            # compute distance between nodes' coordinates (use stored coords)
            (plat, plon) = nodes[prev_node]
            (clat, clon) = nodes[nid]
            dist = haversine(plat, plon, clat, clon)
            add_edge(prev_node, nid, dist)
        prev_node = nid
    # after processing polyline, tag building key to the last node in that polyline
    if prev_node is not None:
        building_node[bkey] = prev_node

# Ensure all building keys are present in building_node (snap building coordinate to nearest node if necessary)
for bkey, poly in ROUTES.items():
    if bkey not in building_node:
        # try snapping building's first poly point to nearest node
        lat, lon = poly[-1]
        # find closest node
        best = None; bd = float('inf')
        for nid, (nlat, nlon) in nodes.items():
            d = haversine(lat, lon, nlat, nlon)
            if d < bd:
                bd = d; best = nid
        if best is None:
            # create node
            best = find_or_create_node(lat, lon)
        building_node[bkey] = best

# Also ensure "G1" exists and is included as start node
if "G1" in ROUTES:
    g1_lat, g1_lon = ROUTES["G1"][0]
    g1_node = find_or_create_node(g1_lat, g1_lon)
    building_node["G1"] = g1_node

# Build adjacency dict with all nodes present
adj = {nid: {} for nid in nodes.keys()}
for u, nbrs in edges.items():
    for v, w in nbrs.items():
        adj[u][v] = w

# If any building node had zero-degree, connect it to nearest node
for bkey, nid in building_node.items():
    if len(adj.get(nid, {})) == 0:
        # connect to nearest other node
        best = None; bd = float('inf')
        for other, (olat, olon) in nodes.items():
            if other == nid: continue
            d = haversine(nodes[nid][0], nodes[nid][1], olat, olon)
            if d < bd:
                bd = d; best = other
        if best:
            adj[nid][best] = bd
            adj[best][nid] = bd

# -----------------------------
# Streamlit UI and Map
# -----------------------------
st.set_page_config(page_title="BulSU Campus Map (Graph Routes)", layout="wide")
st.title("BulSU Campus Map — Graph-based Routes (Gate1 → All Buildings)")

st.sidebar.header("Routing Controls")
use_live_start = st.sidebar.checkbox("Use device location as Start (recommended)", value=True)
dest_options = ["Select Destination"] + sorted([k for k in BUILDING_NAMES.keys() if k != "G1"])
selected_dest = st.sidebar.selectbox("Destination", options=dest_options, format_func=lambda x: BUILDING_NAMES.get(x, x))
if not use_live_start:
    start_options = ["Select Start"] + sorted([k for k in BUILDING_NAMES.keys()])
    selected_start = st.sidebar.selectbox("Start", options=start_options, format_func=lambda x: BUILDING_NAMES.get(x, x))
else:
    selected_start = None

st.sidebar.markdown("Graph nodes: **%d**, graph edges: **%d**" % (len(nodes), sum(len(n) for n in adj.values())//2))
st.sidebar.caption("Routing uses Dijkstra on the internal graph built from your polylines.")

# Initialize folium map
campus_center = [14.85806, 120.814]
m = folium.Map(location=campus_center, zoom_start=18, tiles=None, control_scale=True)
folium.TileLayer('OpenStreetMap', name='Map').add_to(m)
folium.TileLayer('Esri.WorldImagery', name='Satellite').add_to(m)
plugins.LocateControl(auto_start=False).add_to(m)

# Custom left locate button (helps on mobile)
locate_js = """
L.Control.SimpleLocate = L.Control.extend({
    onAdd: function(map){
        var btn = L.DomUtil.create('button', '');
        btn.innerHTML = '&#10148;';
        btn.title = 'Locate';
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

# Plot building markers (use initials)
for bkey, node_id in building_node.items():
    lat, lon = nodes[node_id]
    folium.Marker(
        location=[lat, lon],
        popup=f"{BUILDING_NAMES.get(bkey,bkey)} ({bkey})",
        tooltip=f"{BUILDING_NAMES.get(bkey,bkey)}",
        icon=folium.DivIcon(html=f"""<div style="background:rgba(0,0,0,0.6);color:white;padding:4px 6px;border-radius:4px;font-weight:bold;">{bkey}</div>""")
    ).add_to(m)

# Draw all raw polylines lightly for network visibility
for poly in ROUTES.values():
    folium.PolyLine(locations=poly, color="#999999", weight=3, opacity=0.45).add_to(m)

# Optional: draw nodes (for debugging)
# for nid, (lat, lon) in nodes.items():
#     folium.CircleMarker(location=[lat, lon], radius=2, color='black', fill=True, fillOpacity=0.8).add_to(m)

# Show destination pulse
DEST_PULSE_RADIUS = 8.0  # meters
if selected_dest and selected_dest != "Select Destination":
    dest_node = building_node[selected_dest]
    dlat, dlon = nodes[dest_node]
    m.get_root().html.add_child(folium.Element("""
        <style>
        .pulse { width:18px;height:18px;border-radius:9px;background:#d00;border:3px solid white;
                box-shadow:0 0 8px rgba(255,0,0,0.6); animation: pulse 1.2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); opacity: 1;} 70% { transform: scale(1.8); opacity: 0;} 100% { transform: scale(1); opacity: 0;} }
        </style>
    """))
    folium.map.Marker([dlat, dlon], icon=folium.DivIcon(html='<div class="pulse"></div>'),
                      tooltip=f"Destination: {BUILDING_NAMES.get(selected_dest, selected_dest)}").add_to(m)

# Render map and capture output
map_data = st_folium(m, width=1100, height=700)

# Extract user location (supporting a few st_folium versions' keys)
user_lat = user_lon = None
for k in ['last_clicked','last_object_clicked','geolocation','location','last_location','last_known_location','user_location','center']:
    if k in map_data:
        val = map_data[k]
        if isinstance(val, dict) and 'lat' in val and 'lng' in val:
            user_lat, user_lon = val['lat'], val['lng']; break
        if isinstance(val, (list,tuple)) and len(val)>=2:
            user_lat, user_lon = val[0], val[1]; break

if use_live_start and not (user_lat and user_lon):
    st.sidebar.info("Click the locate button (top-left) to allow browser geolocation and set your start location.")

# Compute route
route_coords = None
route_dist_m = None

if use_live_start and user_lat and user_lon and selected_dest and selected_dest != "Select Destination":
    # snap user to nearest node
    best = None; bd = float('inf')
    for nid, (nlat, nlon) in nodes.items():
        d = haversine(user_lat, user_lon, nlat, nlon)
        if d < bd:
            bd = d; best = nid
    if best is None:
        st.error("No graph node available to snap your location.")
    else:
        start_node = best
        end_node = building_node[selected_dest]
        path, dist = dijkstra(adj, start_node, end_node)
        if path:
            route_coords = [[nodes[n][0], nodes[n][1]] for n in path]
            route_dist_m = dist

elif (not use_live_start) and selected_start and selected_start != "Select Start" and selected_dest and selected_dest != "Select Destination":
    if selected_start not in building_node:
        st.error("Selected start not recognized.")
    else:
        path, dist = dijkstra(adj, building_node[selected_start], building_node[selected_dest])
        if path:
            route_coords = [[nodes[n][0], nodes[n][1]] for n in path]
            route_dist_m = dist

# Draw route if found
if route_coords:
    folium.PolyLine(locations=route_coords, color='purple', weight=7, opacity=0.9).add_to(m)
    # add start and end markers
    s = route_coords[0]; e = route_coords[-1]
    folium.Marker(location=s, icon=folium.Icon(color='purple', icon='street-view', prefix='fa'), tooltip='Start').add_to(m)
    folium.Marker(location=e, icon=folium.Icon(color='black', icon='flag-checkered', prefix='fa'), tooltip='Destination').add_to(m)
    # re-render map with route overlay
    st_folium(m, width=1100, height=700)
    st.success(f"Route distance: {route_dist_m:.0f} meters ({route_dist_m/1000:.3f} km)")

# Arrival detection message
if user_lat and user_lon and selected_dest and selected_dest != "Select Destination":
    dest_n = building_node[selected_dest]
    d_to_dest = haversine(user_lat, user_lon, nodes[dest_n][0], nodes[dest_n][1])
    if d_to_dest <= DEST_PULSE_RADIUS:
        st.balloons()
        st.success(f"Arrived at {BUILDING_NAMES.get(selected_dest, selected_dest)} (within {DEST_PULSE_RADIUS} m).")
    else:
        st.info(f"{BUILDING_NAMES.get(selected_dest, selected_dest)} is {d_to_dest:.0f} meters away.")

# Diagnostics (optional)
with st.expander("Graph diagnostics"):
    st.write("Nodes:", len(nodes))
    edge_count = sum(len(v) for v in adj.values())//2
    st.write("Edges:", edge_count)
    # list buildings mapped to nodes
    st.write("Building → Node mapping (sample):")
    for k in sorted(building_node.keys()):
        nid = building_node[k]
        lat,lon = nodes[nid]
        st.write(f"{k}: {nid} @ {lat:.6f},{lon:.6f}")

