"""
Creates a geojson file from CSV that may be imported into JOSM for final amendments
and uploading to OSM
"""
import haversine as hs
from haversine import Unit
import overpy
import pandas as pd


def is_in_proximity(point1, point2, threshold=8):
    """Check if two points are close to each other based on a threshold"""
    distance_in_metres = hs.haversine(point1, point2, unit=Unit.METERS)
    if distance_in_metres > threshold:
        return False
    return True


def get_existing_bottlebanks(location):
    """Run an overpass turbo query for recycling facilities in a location"""
    api = overpy.Overpass()
    query = f"""
            area["name"="{location}"]->.boundaryarea;
            (
            nwr(area.boundaryarea)[amenity=recycling];
            );

            out body;
    """
    result = api.query(query)
    return result


def is_existing_node_nearby(point_from_csv, existing_bottlebanks):
    """Iterate through existing OSM map nodes to see if our imported node has already been mapped"""
    for node in existing_bottlebanks.nodes:
        existing_point = (node.lat, node.lon)
        if is_in_proximity(point_from_csv, existing_point, 20):
            return True
    return False


def main():
    """Import the CSV file and check if each node already exists on OSM"""
    existing_bottlebanks = get_existing_bottlebanks("Northern Ireland")
    print("Found %s results:" % len(existing_bottlebanks.nodes))

    data = pd.read_csv("bottlebanks.csv")
    already_mapped_count = 0
    need_mapped_count = 0
    geojson_output = """{
        "type": "FeatureCollection",
        "name": "5c72a936-df5e-40bd-8792-fb833c1d23952020329-1-ealxgy.utmh6",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, 
        "features": [

    """
    for index, row in data.iterrows():
        name = row["NAME"]
        address = row["ADDRESS"]
        postcode = row["POSTCODE"]
        lon = row["LONGITUDE"]
        lat = row["LATITUDE"]
        point_from_csv = (lat, lon)

        node_nearby_result = is_existing_node_nearby(
            point_from_csv, existing_bottlebanks
        )

        if node_nearby_result:
            already_mapped_count += 1
            print(f"OK - Node already mapped {name} {address} {lat},{lon}")
        else:
            need_mapped_count += 1
            print(f"TODO - Node needs mapped {name} {address} {lat},{lon}")
            geojson_output += """
                { "type": "Feature", "properties": 
                  {"Location": "%s", "Address": "%s", "Postcode": "%s"},
                  "geometry": { "type": "Point", "coordinates": [ %s, %s] 
                 } 
                }, 
            """ % (
                name,
                address,
                postcode,
                lon,
                lat,
            )
    geojson_output = geojson_output.rstrip().rstrip(",")
    geojson_output += """
        ]}
    """
    text_file = open("bottlebanks.geojson", "w")
    text_file.write(geojson_output)
    text_file.close()
    print(
        f"SUMMARY: {already_mapped_count} already mapped; {need_mapped_count} need mapped"
    )


if __name__ == "__main__":
    main()
