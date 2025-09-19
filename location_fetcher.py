import folium
from folium.plugins import MarkerCluster
import requests
from streamlit_folium import st_folium

def get_coordinates_from_city(city_name):
    try:
        url = f"https://nominatim.openstreetmap.org/search?city={city_name}&country=India&format=json"
        headers = {"User-Agent": "HopeLine/1.0 (contact@example.com)"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        return None, None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

def fetch_osm_data(lat, lon, radius=3000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="police"](around:{radius},{lat},{lon});
      node["office"="lawyer"](around:{radius},{lat},{lon});
      node["amenity"="courthouse"](around:{radius},{lat},{lon});
    );
    out body;
    """
    response = requests.post(overpass_url, data=query)
    data = response.json()
    return data.get("elements", [])

def create_map(lat, lon, elements):
    m = folium.Map(location=[lat, lon], zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)
    
    for el in elements:
        lat = el.get("lat")
        lon = el.get("lon")
        tags = el.get("tags", {})
        name = tags.get("name", "Unknown")
        type_ = tags.get("amenity") or tags.get("office") or "N/A"
        popup_text = f"<b>{name}</b><br>Type: {type_}"
        folium.Marker([lat, lon], popup=popup_text, icon=folium.Icon(color="blue")).add_to(marker_cluster)
    
    return m

def show_osm_map(city_name):
    lat, lon = get_coordinates_from_city(city_name)
    if lat is not None and lon is not None:
        elements = fetch_osm_data(lat, lon)
        if elements:
            map_ = create_map(lat, lon, elements)
            st_folium(map_, width=700, height=500)
        else:
            st.warning("😔 No legal aid locations found nearby.")
    else:
        st.error("❌ Could not find the location. Please enter a valid city name.")
