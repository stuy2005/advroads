## License and Copyright
## © 2024 Stuart Young. All rights reserved.
## Unauthorized copying or re-distibution of this file, via any medium, is strictly prohibited.

import streamlit as st
import overpy
import simplekml
from geopy.distance import geodesic

@st.cache
def fetch_states(api):
    """Fetch a list of U.S. states that have defined boundaries in OpenStreetMap."""
    try:
        result = api.query("""
            [out:json][timeout:60];
            rel["ISO3166-2"~"^US-"]["admin_level"="4"];
            out tags;
        """)
        return {rel.tags['name']: rel.tags['ISO3166-2'] for rel in result.relations if
                'name' in rel.tags and 'ISO3166-2' in rel.tags}
    except Exception as e:
        st.error(f"Error fetching states: {e}")
        return {}

@st.cache
def fetch_counties(api, state_iso):
    try:
        result = api.query(f"""
            [out:json][timeout:60];
            area["ISO3166-2"="{state_iso}"]->.state;
            rel(area.state)["admin_level"="6"];
            out tags;
        """)
        return {rel.tags['name']: rel.id for rel in result.relations if 'name' in rel.tags and hasattr(rel, 'id')}
    except Exception as e:
        st.error(f"Error fetching counties: {e}")
        return {}

@st.cache
def fetch_roads(api, area_id):
    """Fetch roads from a given area using area ID."""
    adjusted_area_id = 3600000000 + area_id  # Adjust area ID for OSM
    query = f"""
    [out:json][timeout:90];
    (
        area({adjusted_area_id})->.a;
        way(area.a)["highway"]["tracktype"~"grade[1-5]"];
    );
    out body;
    >;
    out skel qt;
    """
    try:
        result = api.query(query)
        return result
    except Exception as e:
        st.error(f"Error fetching roads: {e}")
        return None

def calculate_length(way_nodes):
    """Calculate the total length of a way in miles."""
    total_length = 0
    previous_node = None
    for node in way_nodes:
        if previous_node is not None:
            total_length += geodesic((previous_node.lat, previous_node.lon), (node.lat, node.lon)).meters
        previous_node = node
    return total_length * 0.000621371  # Convert meters to miles

def save_kml(ways, min_length_miles, filename="roads.kml"):
    """Save the fetched roads into a KML file."""
    kml = simplekml.Kml()
    for way in ways:
        length_in_miles = calculate_length(way.nodes)
        if length_in_miles >= min_length_miles:  # Only include roads longer than the user-defined minimum length
            line = kml.newlinestring(name=way.tags.get("name", "Unnamed Road"),
                                     coords=[(node.lon, node.lat) for node in way.nodes])
            line.description = f"Track Type: {way.tags.get('tracktype', 'No data')}, Length: {length_in_miles:.2f} miles"
    kml.save(filename)
    st.success(f"KML file has been saved as '{filename}'.")
    return filename

def main():
    st.title("Unpaved Track Finder")
    api = overpy.Overpass()

    # Disclaimer
    st.markdown("""
        **Disclaimer:** This application is intended for informational purposes only. Users are responsible for adhering to local laws and regulations regarding outdoor activities and land use. We do not condone illegal activities or trespassing. Always ensure that you have the proper permissions and are aware of local laws before engaging in any activities on the tracks identified by this tool.
    """)

    states = fetch_states(api)
    state_names = list(states.keys())
    state_select = st.selectbox("Select a State:", state_names)

    counties = fetch_counties(api, states[state_select])
    county_names = list(counties.keys())
    county_select = st.selectbox("Select a County:", county_names)

    # User input for minimum road length
    min_length_miles = st.number_input("Enter minimum road length in miles:", min_value=0.1, value=1.0, step=0.1)

    if st.button("Fetch Roads"):
        roads = fetch_roads(api, counties[county_select])
        if roads:
            kml_filename = save_kml(roads.ways, min_length_miles, f"{county_select.replace(' ', '_').lower()}_roads.kml")
            st.download_button(label="Download KML", data=open(kml_filename, 'rb'), file_name=kml_filename)

        # Copyright in footer
    st.markdown("---")  # Optional: add a horizontal line for better separation
    st.markdown("""
    <div style="text-align: center; color: grey; margin-top: 50px;">
        © 2024 Stuart Young. All rights reserved.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
