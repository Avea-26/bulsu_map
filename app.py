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

# KML Content (Updated to use the data from Untitled map (2).kml)
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
    <Style id="line-1267FF-5000-nodesc-normal">
      <LineStyle>
        <color>ff67ff12</color>
        <width>5</width>
      </LineStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="line-1267FF-5000-nodesc-highlight">
      <LineStyle>
        <color>ff67ff12</color>
        <width>7</width>
      </LineStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="line-1267FF-5000-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#line-1267FF-5000-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#line-1267FF-5000-nodesc-highlight</styleUrl>
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
      <name>NSTP</name>
      <styleUrl>#icon-1899-DB4436-nodesc</styleUrl>
      <Point>
        <coordinates>
          120.8128336,14.8566904,0
        </coordinates>
      </Point>
    </Placemark>
    <Placemark>
      <name>Directions from Gate 1 to Admissions Office</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81232,14.85723,0
          120.81242,14.85727,0
          120.8126,14.85761,0
          120.8128,14.8579,0
          120.81306,14.85834,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from Admissions Office to Law Building</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81306,14.85834,0
          120.81333,14.85787,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from Law Building to CIT Building</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81333,14.85787,0
          120.81282,14.85798,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from Admissions Office to HRM Building</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81306,14.85834,0
          120.8131,14.85859,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from HRM Building to CBA Building</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.8131,14.85859,0
          120.81352,14.85872,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from CBA Building to Library</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81352,14.85872,0
          120.81395,14.85881,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from CBA Building to Gate 4</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81352,14.85872,0
          120.81423,14.85978,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from CBA Building to CS</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81352,14.85872,0
          120.81373,14.85852,0
          120.81395,14.85829,0
          120.81424,14.85804,0
          120.81453,14.85804,0
          120.81478,14.85843,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from Law Building to COED</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81333,14.85787,0
          120.81364,14.85732,0
          120.81412,14.85744,0
          120.81435,14.8575,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from COED to Gate 2</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81435,14.8575,0
          120.81435,14.85732,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from COED to NSTP</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81435,14.8575,0
          120.81415,14.85722,0
          120.81394,14.85719,0
          120.81358,14.85721,0
          120.81329,14.85721,0
          120.81316,14.85718,0
          120.81298,14.85703,0
          120.81283,14.85669,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from COED to SAO/REG</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81435,14.8575,0
          120.8144,14.85778,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from SAO/REG to Admin/Registrar</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.8144,14.85778,0
          120.81453,14.85804,0
          120.81492,14.85818,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from Admin/Registrar to Clinic</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81492,14.85818,0
          120.8152,14.85804,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from Clinic to ORES/CAL/CANTEEN</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.8152,14.85804,0
          120.81566,14.85809,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from ORES/CAL/CANTEEN to Federizo Hall</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81566,14.85809,0
          120.81607,14.85838,0
          120.81639,14.85827,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from ORES/CAL/CANTEEN to Gate 3</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81566,14.85809,0
          120.81596,14.85796,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from ORES/CAL/CANTEEN to CAFA</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81566,14.85809,0
          120.81516,14.85841,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from CAFA to CS</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81516,14.85841,0
          120.81478,14.85843,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from Gate 1 to AC</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81232,14.85723,0
          120.81263,14.85725,0
          120.81269,14.85764,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from AC to CIT</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81269,14.85764,0
          120.8127,14.85787,0
          120.8128,14.85801,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>Directions from Law Building to NURSING</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81333,14.85787,0
          120.81314,14.85732,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>NSTP to NURSING</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81283,14.85669,0
          120.8129,14.8568,0
          120.81302,14.85702,0
          120.81314,14.85732,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>NURSING to Eng'g</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81314,14.85732,0
          120.81388,14.85744,0
          120.81422,14.85746,0
        </coordinates>
      </LineString>
    </Placemark>
    <Placemark>
      <name>NSTP to AC</name>
      <styleUrl>#line-1267FF-5000-nodesc</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          120.81283,14.85669,0
          120.81277,14.85675,0
          120.81267,14.85695,0
          120.81269,14.85764,0
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
    if start_node not in distances:
        # Handle case where start node is not in the adjacency list (disconnected or missing)
        return [], float('infinity')

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
        current_node = previous_nodes.get(current_node)  # Use .get() in case end_node is unreachable

    # Return the path in correct order (start to end) and the total distance
    # Check if the path actually reaches the start node
    if path and path[-1] == start_node:
        return path[::-1], distances.get(end_node, float('infinity'))
    else:
        return [], float('infinity')


# --- KML Graph Parser ---
KML_NS = {'kml': 'http://www.opengis.net/kml/2.2'}
# INCREASED TOLERANCE from 15m to 20m for better connectivity
NODE_MATCH_TOLERANCE_M = 20  # Tolerance for snapping KML points to Buildings


def parse_kml_paths(kml_content, building_locations):
    all_nodes = building_locations.copy()
    raw_edges = set()
    junction_counter = 0

    try:
        # Register namespace for safer parsing
        ET.register_namespace('', KML_NS['kml'])
        root = ET.fromstring(kml_content)
    except ET.ParseError as e:
        st.error(f"Error: Could not parse KML content. {e}")
        return {"nodes": building_locations, "adj": {bid: {} for bid in building_locations}}

    # Helper to find the closest official building node or junction
    def find_closest_node(lat, lon):
        min_distance = float('inf')
        closest_id = None

        # Check against existing buildings (high priority, larger tolerance)
        for b_id, (b_lat, b_lon) in building_locations.items():
            dist = haversine(lat, lon, b_lat, b_lon)
            if dist < min_distance:
                min_distance = dist
                closest_id = b_id

        if min_distance <= NODE_MATCH_TOLERANCE_M:
            return closest_id, min_distance

        # If not close to a building, check against existing junctions (lower priority, smaller tolerance for merging)
        # Reset min distance for junction check
        min_distance = float('inf')
        closest_id = None

        for node_id, (n_lat, n_lon) in all_nodes.items():
            if node_id.startswith('J'):
                dist = haversine(lat, lon, n_lat, n_lon)
                if dist < min_distance:
                    min_distance = dist
                    closest_id = node_id

        if closest_id and min_distance < 5:  # Merge junctions within 5m
            return closest_id, min_distance

        return None, float('inf')

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

                # Iterate through all points in the line segment
                for lat, lon in points:
                    current_node_id, dist_to_closest = find_closest_node(lat, lon)

                    if current_node_id is None or (
                            not current_node_id.startswith('J') and dist_to_closest > NODE_MATCH_TOLERANCE_M):
                        # Create a new Junction Node if not close to a building or an existing junction
                        current_node_id = f"J{junction_counter:04d}"
                        all_nodes[current_node_id] = (lat, lon)
                        junction_counter += 1

                    if previous_node_id is not None and previous_node_id != current_node_id:
                        # Only add edge if the current node is truly new or significantly different from the previous one.
                        raw_edges.add(tuple(sorted((previous_node_id, current_node_id))))

                    previous_node_id = current_node_id

    # Build adjacency list structure for Dijkstra's
    adj_list = {node_id: {} for node_id in all_nodes.keys()}

    for u, v in raw_edges:
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
# --- 1. CONFIGURATION AND DATA (Updated Destinations including NSTP) ---
# ==============================================================================

st.set_page_config(page_title="BulSU Campus Map for New Students", layout="wide")
st.title("🗺️ Bulacan State University – Malolos Campus Map: KML Accurate Routing")

st.error(
    "🚨 **LIVE LOCATION (SIMULATED):** Routing uses the **accurate pathways** from your KML data via Dijkstra's algorithm, which ensures the shortest route across the campus road network. Use the 'Start Location' selector."
)

# Campus center coordinates
campus_lat, campus_lon = 14.85806, 120.814

# Definitive Locations (NSTP added)
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
    {"name": "NSTP Building", "initials": "NSTP", "lat": 14.8566904, "lon": 120.8128336, "area": "Education",
     "color": "blue", "icon": "users", "essential": False},  # Added NSTP from KML data
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
        # Pass the graph structure to Dijkstra's
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
                f"Could not find a connected path between **{LOCATION_NAMES[selected_start_initials]}** and **{LOCATION_NAMES[selected_end_initials]}**. The path network might be disconnected in this area.")

    except Exception as e:
        st.error(f"An unexpected error occurred during routing: {e}")

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
# To help visualize the network the shortest path is calculated on, uncomment the block below.
# The network includes all permanent buildings (IDs like 'AO') and temporary junctions (IDs like 'J0001').
# folium.FeatureGroup(name='Underlying Path Network', show=False).add_to(m)
# for u, neighbors in GRAPH_ADJACENCY.items():
#     for v, weight in neighbors.items():
#         # Ensure we only draw each unique segment once (since it's bidirectional)
#         if u < v:
#             u_lat, u_lon = GRAPH_NODES[u]
#             v_lat, v_lon = GRAPH_NODES[v]
#             folium.PolyLine(
#                 locations=[[u_lat, u_lon], [v_lat, v_lon]],
#                 color="#CCCCCC",
#                 weight=1,
#                 opacity=0.4
#             ).add_to(m.get_children()[-1]) # Add to the FeatureGroup

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
        lats = [p[0] for p in route_to_display]
        lons = [p[1] for p in route_to_display]
        m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]])

# Add Layer Control to switch between Map and Satellite
folium.LayerControl(collapsed=False).add_to(m)

# --- 5. RENDER MAP ---
st_folium(m, width=1200, height=700)