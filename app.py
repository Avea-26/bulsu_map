import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins
import json

# Page config
st.set_page_config(page_title="BulSU Campus Map", layout="wide")

# Title
st.title("Bulacan State University Malolos Campus Map")

# Load buildings and paths data (replace 'data.json' with your actual file or endpoint)
def load_data():
    return {
        "buildings": [
            {"name": "Gate 1 (Main Gate)", "initials": "G1", "lat": 14.85723594755244, "lon": 120.8122796215916},
            {"name": "Gate 2", "initials": "G2", "lat": 14.857314970938278, "lon": 120.81431249226469},
            {"name": "Gate 3", "initials": "G3", "lat": 14.857962089418534, "lon": 120.81590374653345},
            {"name": "Bulacan State University Heroes Park", "initials": "HP", "lat": 14.857859827168662, "lon": 120.81425777581251},
            {"name": "Roxas Hall", "initials": "RH", "lat": 14.857390463137973, "lon": 120.8141302146359},
            {"name": "Federizo Hall", "initials": "FH", "lat": 14.858092409454652, "lon": 120.81453338128564},
            {"name": "CBA Building", "initials": "CBA", "lat": 14.858265418626708, "lon": 120.81390368960794},
            {"name": "CIT Building", "initials": "CIT", "lat": 14.857678444483582, "lon": 120.812557298334},
            {"name": "Admissions Office", "initials": "AO", "lat": 14.85787281781839, "lon": 120.81324939963862},
            {"name": "Activity Center", "initials": "AC", "lat": 14.857236983842892, "lon": 120.81296440885298},
            {"name": "McDonald's", "initials": "MD", "lat": 14.857496410205641, "lon": 120.812098312232},
            {"name": "BSU Mini Rizal Park", "initials": "MRP", "lat": 14.857415748264787, "lon": 120.81321702036867},
            {"name": "College of Nursing", "initials": "NUR", "lat": 14.856961206741117, "lon": 120.81345271593389},
            {"name": "NSTP Building", "initials": "NSTP", "lat": 14.85690997538126, "lon": 120.81365345186897},
            {"name": "College of Law", "initials": "LAW", "lat": 14.857716890878411, "lon": 120.81346297233067},
            {"name": "College of Engineering", "initials": "ENG", "lat": 14.857546982943054, "lon": 120.8143091116688},
            {"name": "College of Arts and Trades", "initials": "CAT", "lat": 14.857490424275298, "lon": 120.81406733541326},
            {"name": "Science Research and Learning Center", "initials": "SRLC", "lat": 14.858234981834437, "lon": 120.81386159963195},
            {"name": "College of Home Economics", "initials": "CHE", "lat": 14.858393758789967, "lon": 120.81324120258154},
            {"name": "BulSU e-Library", "initials": "LIB", "lat": 14.85850320691184, "lon": 120.8137132784873},
            {"name": "Office of the Registrars", "initials": "REG", "lat": 14.857715559437853, "lon": 120.81491671412424},
            {"name": "Flores Hall", "initials": "FH", "lat": 14.857915377726254, "lon": 120.8151101681602},
            {"name": "College of Architecture and Fine Arts", "initials": "CAFA", "lat": 14.85812252860069, "lon": 120.81471377704729},
            {"name": "College of Physical Education, Recreation and Sport", "initials": "CPERS", "lat": 14.858254518437814, "lon": 120.8148427464029},
            {"name": "Valencia Hall", "initials": "VH", "lat": 14.858223354178708, "lon": 120.81523155108302},
            {"name": "College of Arts and Letters", "initials": "CAL", "lat": 14.858749479597106, "lon": 120.81496792254381},
            {"name": "College of Social Sciences and Philosophy", "initials": "CSSP", "lat": 14.859150947267924, "lon": 120.81494516324304},
            {"name": "CSSP Local Student Council, BulSU SG", "initials": "LSC", "lat": 14.858852138074056, "lon": 120.81524482733796}
        ],
        "paths": {
            "CIT": [[14.85725513788879, 120.81227566193445], [14.857612907614383, 120.81272627302701], [14.857681609704008, 120.81268469878931]],
            "CBA": [[14.85723594755244, 120.8122796215916], [14.85787281781839, 120.81324939963862], [14.858265418626708, 120.81390368960794]],
            "ENG": [[14.85723594755244, 120.8122796215916], [14.85787281781839, 120.81324939963862], [14.857546982943054, 120.8143091116688]],
            "NUR": [[14.85726550803233, 120.81227163862754], [14.857575315892026, 120.81275175402043], [14.85702051321428, 120.81333111113943]],
            "LAW": [[14.85723594755244, 120.8122796215916], [14.85787281781839, 120.81324939963862], [14.857716890878411, 120.81346297233067]],
            "CAFA": [[14.85723594755244, 120.8122796215916], [14.85787281781839, 120.81324939963862], [14.85812252860069, 120.81471377704729]],
            "CPERS": [[14.85723594755244, 120.8122796215916], [14.85787281781839, 120.81324939963862], [14.858254518437814, 120.8148427464029]],
            "CAL": [[14.85723594755244, 120.8122796215916], [14.85787281781839, 120.81324939963862], [14.858749479597106, 120.81496792254381]],
            "CSSP": [[14.85723594755244, 120.8122796215916], [14.85787281781839, 120.81324939963862], [14.859150947267924, 120.81494516324304]],
            "AC": [[14.85726550803233, 120.81227163862754], [14.857575315892026, 120.81275175402043], [14.857299210999242, 120.8129824239845]],
            "LIB": [[14.857270483830009, 120.81224450339876], [14.858294533203825, 120.81357219679651]],
            "CHE": [[14.857257521148588, 120.81225791444321], [14.85826601543889, 120.81343272193452]]
        }
    }

data = load_data()

# Center map at BulSU Malolos Main Campus
campus_lat, campus_lon = 14.85806, 120.814
m = folium.Map(location=[campus_lat, campus_lon], zoom_start=18, tiles=None)

# Add tile layers
folium.TileLayer('OpenStreetMap', name='Map View').add_to(m)
folium.TileLayer('Esri.WorldImagery', name='Satellite View').add_to(m)

# Add campus boundary
folium.Circle(
    location=[campus_lat, campus_lon],
    radius=200,
    color="orange",
    fill=True,
    fill_opacity=0.2,
    popup="Campus Boundary"
).add_to(m)

# Enable user location control
plugins.LocateControl(auto_start=True).add_to(m)

# Add building markers
def add_building_markers(map_object, buildings):
    for building in buildings:
        folium.Marker(
            location=[building["lat"], building["lon"]],
            popup=f"<b>{building['name']}</b>",
            icon=folium.DivIcon(
                html=f"""
                <div style="font-size:12px; font-weight:bold; color:white;
                -webkit-text-stroke: 1px black; background:rgba(0,0,0,0.6);
                padding:4px 6px; border-radius:4px; text-align:center;">
                {building['initials']}</div>"""
            )
        ).add_to(map_object)

add_building_markers(m, data["buildings"])

# UI Controls
col1, col2 = st.columns([3, 1])
with col1:
    selected = st.selectbox("Select a Department to Trace Path", ["None"] + list(data["paths"].keys()))
with col2:
    reset = st.button("Reset View")

# Highlight path if selected
def highlight_path(map_object, path_coordinates, label):
    folium.PolyLine(path_coordinates, color="red", weight=6, opacity=0.9, tooltip=f"Path to {label}").add_to(map_object)
    for point in path_coordinates:
        folium.CircleMarker(point, radius=5, color="red", fill=True, fill_opacity=0.7).add_to(map_object)

if selected != "None":
    highlight_path(m, data["paths"][selected], selected)
    m.fit_bounds(data["paths"][selected])

# Reset view
if reset:
    m.location = [campus_lat, campus_lon]
    m.zoom_start = 18

# Map controls
folium.LayerControl().add_to(m)

# Display map
st_folium(m, width=1000, height=700)
