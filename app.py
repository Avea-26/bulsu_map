import streamlit as st
from streamlit_folium import st_folium
import folium

# Page config
st.set_page_config(page_title="BulSU Campus Map", layout="wide")

# Title
st.title("📍 Bulacan State University Malolos Campus Map")

# Center map at BulSU Malolos Main Campus
campus_lat, campus_lon = 14.85806, 120.814   # 14°51'29" N, 120°48'50" E
m = folium.Map(location=[campus_lat, campus_lon], zoom_start=18, tiles="Esri.WorldImagery")

# Markers for campus buildings (approximate coordinates — replace with accurate values)
buildings = [
    {"name": "Gate 1 (Main Gate)", "lat": 14.85723594755244, "lon": 120.8122796215916},
    {"name": "Gate 2", "lat": 14.857314970938278, "lon": 120.81431249226469},
    {"name": "Gate 3", "lat": 14.857962089418534, "lon": 120.81590374653345},
    {"name": "Bulacan State University Heroes Park", "lat": 14.857859827168662, "lon": 120.81425777581251},
    {"name": "Roxas Hall", "lat": 14.857390463137973, "lon": 120.8141302146359},
    {"name": "Federizo Hall", "lat": 14.858092409454652, "lon": 120.81453338128564},
    {"name": "CBA Building", "lat": 14.858265418626708, "lon": 120.81390368960794},
    {"name": "CIT Building", "lat": 14.857678444483582, "lon": 120.812557298334},
    {"name": "Admissions Office", "lat": 14.85787281781839, "lon": 120.81324939963862},
    {"name": "Activity Center", "lat": 14.857236983842892, "lon": 120.81296440885298},
    {"name": "McDonald's", "lat": 14.857496410205641, "lon": 120.812098312232},
    {"name": "BSU Mini Rizal Park", "lat": 14.857415748264787, "lon": 120.81321702036867},
    {"name": "College of Nursing", "lat": 14.856961206741117, "lon": 120.81345271593389},
    {"name": "NSTP Building", "lat": 14.85690997538126, "lon": 120.81365345186897},
    {"name": "College of Law", "lat": 14.857716890878411, "lon": 120.81346297233067},
    {"name": "College of Engineering", "lat": 14.8575469829430541, "lon": 120.8143091116688},
    {"name": "College of Arts and Trades", "lat": 14.857490424275298, "lon": 120.81406733541326},
    {"name": "Science Research and Learning Center", "lat": 14.858234981834437, "lon": 120.81386159963195},
    {"name": "College of Home Economics", "lat": 14.858393758789967, "lon": 120.81324120258154},
    {"name": "BulSU e-Library", "lat": 14.85850320691184, "lon": 120.8137132784873},
    {"name": "Office of the Registrars", "lat": 14.857715559437853, "lon": 120.81491671412424},
    {"name": "Flores Hall", "lat": 14.857915377726254, "lon": 120.8151101681602},
    {"name": "College of Architecture and Fine Arts", "lat": 14.85812252860069, "lon": 120.81471377704729},
    {"name": "College of Physical Education, Recreation and Sport", "lat": 14.858254518437814, "lon": 120.8148427464029},
    {"name": "Valencia Hall", "lat": 14.858223354178708, "lon": 120.81523155108302},
    {"name": "College of Arts and Letters", "lat": 14.858749479597106, "lon": 120.81496792254381},
    {"name": "College of Social Sciences and Philosophy", "lat": 14.859150947267924, "lon": 120.81494516324304},
    {"name": "CSSP Local Student Council, BulSU SG", "lat": 14.858852138074056, "lon": 120.81524482733796},
]

for b in buildings:
    folium.Marker(
        location=[b["lat"], b["lon"]],
        popup=b["name"],
        icon=folium.Icon(color="orange", icon="info-sign")
    ).add_to(m)

# Add locate control button (to get user's live location — via browser prompt)
folium.plugins.LocateControl(auto_start=True).add_to(m)

# Show map in Streamlit
st_data = st_folium(m, width=1000, height=700)
