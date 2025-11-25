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

# Detailed road pathways from Google Maps data
ROUTES = {
    "G1": [[14.857227383607164, 120.81231458047134]],
    
    "AO": [  # Admissions Office
        [14.857223717206535, 120.81231552877544], [14.857244799009289, 120.81234208129061],
        [14.857263131010008, 120.81236578889342], [14.857276880009541, 120.81238665158389],
        [14.857298878406947, 120.81241130749082], [14.857307127805404, 120.81242932526898],
        [14.857334625797986, 120.81244734304711], [14.857351124591831, 120.81246725743348],
        [14.857357540789103, 120.8124833786034], [14.85737495618073, 120.81250518959799],
        [14.857392371570958, 120.81252415568024], [14.857415286555966, 120.81255070819539],
        [14.857438201538544, 120.81256777766941], [14.857450117328524, 120.81258010562287],
        [14.8574730323074, 120.81260476152981], [14.85748586469451, 120.81262372761208],
        [14.857502363476803, 120.81264743521487], [14.857524361851258, 120.8126626080807],
        [14.857537194235327, 120.81268916059584], [14.857558276007472, 120.81271191989453],
        [14.857572941586888, 120.81273562749735], [14.857593106756976, 120.81274985205904],
        [14.857618771516158, 120.8127707147495], [14.857628854099273, 120.81278778422353],
        [14.857645352870664, 120.81281338843459], [14.857664601435681, 120.8128361477333],
        [14.857677141674149, 120.81286418726205], [14.85769872309557, 120.8128785409386],
        [14.85771413839527, 120.81290166630639], [14.857749593580392, 120.81293515821835],
        [14.857764238111672, 120.81296944755678], [14.857790444112537, 120.81297263726269],
        [14.857805088641056, 120.81299735748343], [14.857834377695106, 120.81301649571883],
        [14.857838231288541, 120.81303483631322], [14.857823586779652, 120.81305716422804],
        [14.857805088451215, 120.8130810869939], [14.85779121470385, 120.81310341490872],
        [14.85777271637264, 120.81312255312142], [14.857743427344987, 120.81315205786598],
        [14.857722616717663, 120.81317199350421]
    ],
    
    "ADMIN": [  # Administration Building
        [14.857227383607164, 120.81231458047134], [14.858253523986543, 120.81350449542867],
        [14.858264505945309, 120.81349649102147], [14.858283949876494, 120.81348576218518],
        [14.85829237557947, 120.81348039776702], [14.858297560627278, 120.81346497506483],
        [14.858313763900917, 120.81346028119896], [14.858328022780693, 120.81344687015358],
        [14.858336448481952, 120.81343748242182]
    ],
    
    "REG": [  # Registrar's Office
        [14.857231951696395, 120.81230999474423], [14.85824387586885, 120.81351054775081],
        [14.857875404028864, 120.81385383383957], [14.858133884344007, 120.81418005044027],
        [14.858143050306836, 120.81421608599655], [14.8581412171143, 120.81427108763508],
        [14.857712249633623, 120.81468454822817]
    ],
    
    "SAO": [  # Student Affairs Office
        [14.85722737753228, 120.8123075991754], [14.85760501646353, 120.81275709532477],
        [14.857053223433768, 120.81331090492655], [14.857249375934748, 120.8135460843465],
        [14.857291539533183, 120.81355556738761], [14.857377699904417, 120.81382678236385],
        [14.857207212328058, 120.8139747178054]
    ],
    
    "RH": [  # Roxas Hall
        [14.85722737753228, 120.8123075991754], [14.85760501646353, 120.81275709532477],
        [14.857053223433768, 120.81331090492655], [14.857249375934748, 120.8135460843465],
        [14.857291539533183, 120.81355556738761], [14.857377699904417, 120.81382678236385],
        [14.857207212328058, 120.8139747178054]
    ],
    
    "FH": [  # Federizo Hall
        [14.857222232375102, 120.81230441212736], [14.858248874509577, 120.81351140619314],
        [14.8578807357222, 120.81384936453658], [14.858129618353198, 120.81417927624206],
        [14.858145173507996, 120.81421146275096], [14.858129618353198, 120.81425437809614],
        [14.858007769601818, 120.81436971308635]
    ],
    
    "CIT": [  # CIT Building
        [14.857231342857316, 120.81231006196273], [14.857585150218535, 120.812741540334],
        [14.857657561498218, 120.81269128021603]
    ],
    
    "CBA": [  # CBA Building
        [14.857231737951556, 120.81231007737065], [14.858266157606362, 120.81351170703611],
        [14.858133938828905, 120.81362435981724], [14.858244926024813, 120.81375484455948]
    ],
    
    "COED": [  # College of Education
        [14.85723756264293, 120.81230881959102], [14.858258054075955, 120.81350176818223],
        [14.857857257411418, 120.81386858392554], [14.85813164905436, 120.81416203652014],
        [14.858122399903529, 120.81426091728572], [14.857801762429997, 120.81457031839095],
        [14.857820260758727, 120.81457669779518], [14.858560192608307, 120.8154602452812],
        [14.858849998558496, 120.81515403387809]
    ],
    
    "CHK": [  # College of Home Economics
        [14.85723756264293, 120.81229606078254], [14.858254971027538, 120.81348900937378],
        [14.858412206441201, 120.81338055950185]
    ],
    
    "ENG": [  # College of Engineering
        [14.857221573677649, 120.8123046187677], [14.858255990827312, 120.8135008810616],
        [14.857488604143063, 120.81419557149684]
    ],
    
    "CAL": [  # College of Arts and Letters
        [14.857239487230459, 120.81229892389935], [14.858250729509088, 120.81351101070327],
        [14.857856098939296, 120.81385868823384], [14.85813357363394, 120.81418084814753],
        [14.858155154984129, 120.81425740099832], [14.858121241432857, 120.81424783189196],
        [14.857809853122198, 120.81457637120987], [14.858546701963194, 120.8154471598874],
        [14.858824175770527, 120.81518241461181]
    ],
    
    "AC": [  # Activity Center
        [14.85723286054277, 120.81230926933186], [14.857601000434475, 120.8127598804564],
        [14.857313229164221, 120.81303883020017]
    ],
    
    "LIB": [  # BSU Main Library
        [14.85723522104112, 120.8123009072618], [14.858251122031646, 120.81349855399958]
    ],
    
    "HP": [  # Heroes Park
        [14.857235220206237, 120.81230090641704], [14.85826856368972, 120.81350306659485],
        [14.85773445216894, 120.813965435894], [14.857902315932083, 120.81418872643358]
    ],
    
    "CANT": [  # Food Court / Canteen
        [14.857239968415367, 120.81230782991943], [14.857600686477925, 120.81274960366244],
        [14.857044193830047, 120.81331099123477], [14.857258466792201, 120.81355500344662],
        [14.857266174448752, 120.81364750480797], [14.857238426883884, 120.8137368164672]
    ],
    
    "CLINIC": [  # University Infirmary / Clinic
        [14.857232934975002, 120.81230328608719], [14.85825319820291, 120.813494168965],
        [14.857876050178037, 120.81384376526438], [14.858126755584948, 120.81417757332686],
        [14.858155096177963, 120.81423621528677], [14.857808468669555, 120.81457904520612],
        [14.858100595034262, 120.81491285328552]
    ]
}

# For buildings without detailed routes, use simple paths through common waypoints
for code, coords in BUILDING_COORDS.items():
    if code not in ROUTES and code != "G1":
        # Use a simple 2-point path for buildings without detailed routes
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

# Add locate control for GPS tracking
plugins.LocateControl(
    auto_start=False,
    position='topleft',
    strings={'title': 'Find My Location'},
    locateOptions={'enableHighAccuracy': True, 'maxZoom': 18}
).add_to(m)

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

# Don't show all route lines - only show the selected route later

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
