import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins

st.set_page_config(page_title="BulSU Campus Map", layout="wide")

st.title("Bulacan State University Malolos Campus Map")

campus_lat, campus_lon = 14.85806, 120.814

m = folium.Map(location=[campus_lat, campus_lon], zoom_start=18, tiles=None)

map_view = folium.TileLayer('OpenStreetMap', name='Map View')
satellite_view = folium.TileLayer('Esri.WorldImagery', name='Satellite View')

map_view.add_to(m)
satellite_view.add_to(m)

folium.Circle(
    location=[campus_lat, campus_lon],
    radius=200,
    color="orange",
    fill=True,
    fill_opacity=0.2,
    popup="Campus Boundary"
).add_to(m)

plugins.LocateControl(auto_start=True).add_to(m)

buildings = [
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
    {"name": "CSSP Local Student Council, BulSU SG", "initials": "LSC", "lat": 14.858852138074056, "lon": 120.81524482733796},
]


for b in buildings:
    folium.Marker(
        location=[b["lat"], b["lon"]],
        popup=f"<b>{b['name']}</b>",
        icon=folium.DivIcon(
            html=f"""
            <div style="
                font-size:12px;
                font-weight:bold;
                color:white;
                -webkit-text-stroke: 1px black;
                background:rgba(0,0,0,0.6);
                padding:4px 6px;
                border-radius:4px;
                text-align:center;">
                {b["initials"]}
            </div>
            """
        )
    ).add_to(m)


folium.LayerControl().add_to(m)




department_paths = {
    "CIT": {
        "name": "CIT Building",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.857496410205641, 120.812098312232],
            [14.857678444483582, 120.812557298334]
        ]
    },
    "CBA": {
        "name": "CBA Building",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.85787281781839, 120.81324939963862],
            [14.858265418626708, 120.81390368960794]
        ]
    },
    "ENG": {
        "name": "College of Engineering",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.85787281781839, 120.81324939963862],
            [14.857546982943054, 120.8143091116688]
        ]
    },
    "NUR": {
        "name": "College of Nursing",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.85787281781839, 120.81324939963862],
            [14.856961206741117, 120.81345271593389]
        ]
    },
    "LAW": {
        "name": "College of Law",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.85787281781839, 120.81324939963862],
            [14.857716890878411, 120.81346297233067]
        ]
    },
    "CAFA": {
        "name": "College of Architecture and Fine Arts",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.85787281781839, 120.81324939963862],
            [14.85812252860069, 120.81471377704729]
        ]
    },
    "CPERS": {
        "name": "College of Physical Education, Recreation and Sport",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.85787281781839, 120.81324939963862],
            [14.858254518437814, 120.8148427464029]
        ]
    },
    "CAL": {
        "name": "College of Arts and Letters",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.85787281781839, 120.81324939963862],
            [14.858749479597106, 120.81496792254381]
        ]
    },
    "CSSP": {
        "name": "College of Social Sciences and Philosophy",
        "path": [
            [14.85723594755244, 120.8122796215916],
            [14.85787281781839, 120.81324939963862],
            [14.859150947267924, 120.81494516324304]
        ]
    }
}


selected_department = st.selectbox("Select Department to Highlight Path:", ["None"] + list(department_paths.keys()))


if selected_department and selected_department != "None":
    selected = department_paths[selected_department]
    folium.PolyLine(
        locations=selected["path"],
        color="red",
        weight=5,
        opacity=0.8,
        tooltip=f"Path to {selected['name']}"
    ).add_to(m)

st_data = st_folium(m, width=1000, height=700)
