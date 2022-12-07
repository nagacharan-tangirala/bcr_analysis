#!/bin/bash
echo "......Preparing CSV files with city names......"
sleep 2
python3 ./src/download/simplify_geonames_csv.py
sleep 2
echo "......Downloading network and building files from OSM......"
sleep 2
python3 ./src/download/download_streets_buildings.py
sleep 2
echo "......Done!!!......"
sleep 2