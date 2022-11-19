# Using Python to Prepare CSV data for OpenStreetMap 

## Overview
There are government data sources on OpenDataNI licensed under the UK Open Government Licence. Some of this data has a geospatial element that could be mapped on OpenStreetMap.

The example code here focuses on a very small dataset but the code can be amended for other geospatial data in future.

Automated bot imports of data are [frowned upon](https://wiki.openstreetmap.org/wiki/Automated_edits) in the OSM community so this code creates a geojson file that may be imported into JOSM for final amendments and uploading to the map. 

## Pre-requisites
Download the [Belfast City Council Bottle Bank CSV file](https://www.opendatani.gov.uk/dataset/bottle-banks) saving it as `bottlebank.csv`

Install the python libraries:
```
python3 -m venv env
source ./env/bin/activate.fish 
pip3 install -r requirements.txt
```

## Usage
Running the `main.py` file will read the CSV input file and generate a geojson file. It will also provide a summary about the nodes already mapped.
```
python3 main.py
```
The generated `bottlebanks.geojson` file can be opened in the JOSM editor for tagging.
![JOSM editor showing geojson import](JOSM.jpg "JOSM Editor")
## Example Script Output

```
TODO - Node needs mapped Ionad Uibh Eachach 34a Iveagh Crescent 54.59017011749692,-5.961594570944489
TODO - Node needs mapped Olympia Leisure Centre Boucher Road 54.58328265649366,-5.959791631964201
OK - Node already mapped Stranmillis car park Stranmillis Road roundabout 54.574239275800586,-5.932836605028399
TODO - Node needs mapped Malone Rugby Football Club Gibson Park Avenue, Cregagh Road, Belfast 54.58351957658916,-5.896705472706216
```



