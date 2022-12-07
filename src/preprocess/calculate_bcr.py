import csv
import math
import pickle
from os import makedirs
from os.path import exists

import colorama
import geopandas as gpd
import pandas as pd

from smallest_enclosing_circle import make_circle

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
buildings_folder = work_folder + 'buildings/'
blocks_folder = work_folder + 'blocks/'
removal_ratios_folder = work_folder + 'removal_ratios/'

processed_dfs_folder = work_folder + 'processed_dfs/'
makedirs(processed_dfs_folder, exist_ok=True)
makedirs(removal_ratios_folder, exist_ok=True)

osm_names = {}
with open(input_folder + 'cities.csv', 'r') as c:
    cities_reader = csv.reader(c, delimiter=';')
    next(cities_reader)
    for row in cities_reader:
        osm_names[row[0]] = row[1]

shape_built_df = pd.DataFrame()
count = 0
for city, osm_name in osm_names.items():
    count = count + 1
    # Store the processed dataframes in this file.
    output_file = processed_dfs_folder + city + '.pckl'
    if exists(output_file):
        print(colorama.Fore.YELLOW + 'Already processed, skipping ' + city + colorama.Style.RESET_ALL)
        continue

    # Load the buildings if present, otherwise skip to next city
    buildings_file = buildings_folder + city + '.pckl'
    if not exists(buildings_file):
        print(colorama.Fore.RED + 'No buildings file, skipping ' + city + colorama.Style.RESET_ALL)
        continue

    with open(buildings_file, 'rb') as b:
        buildings = pickle.load(b)

    # Retain only the geometry of the buildings.
    buildings = buildings[['geometry']]

    # Skip this city if buildings data is not empty.
    if not len(buildings) > 0:
        print(colorama.Fore.RED + 'Empty buildings file, skipping ' + city + colorama.Style.RESET_ALL)
        continue

    # Read the block info for this city from the file if it exists
    city_blocks_file = blocks_folder + city + '.gpkg'
    if not exists(city_blocks_file):
        print(colorama.Fore.RED + 'No blocks file, skipping ' + city + colorama.Style.RESET_ALL)
        continue
    
    # Read the city block polygons file
    city_blocks = gpd.read_file(city_blocks_file)

    if not len(city_blocks) > 0:
        print(colorama.Fore.RED + 'Empty blocks file, skipping ' + city + colorama.Style.RESET_ALL)
        continue

    print(colorama.Fore.CYAN + 'Processing ' + city + '. ' + str(count) + ' of ' + str(len(osm_names)) + colorama.Style.RESET_ALL)

    # Calculate the area of the city.
    city_area = sum(city_blocks['geometry'].to_crs({'proj': 'cea'}).area)

    # The first polygon is the buffered roads' polygon, drop it.
    city_blocks = city_blocks.drop(0, axis=0)
    
    # Count total number of blocks in the city. 
    all_polygons_count = len(city_blocks)
    
    if not all_polygons_count > 0:
        print(colorama.Fore.RED + 'Skipping ' + city + '. No valid blocks available.' + colorama.Style.RESET_ALL)
        continue

    # Match the buildings to their respective blocks
    building_and_block_df = gpd.sjoin(buildings, city_blocks, how="inner", predicate="intersects")

    # Retain only building geometry and block ID.
    building_and_block_df = building_and_block_df[['index_right', 'geometry']]

    # Convert to CEA projection and calculate the area of all the buildings
    building_and_block_df['geometry'] = building_and_block_df['geometry'].to_crs({'proj': 'cea'})
    building_and_block_df['building_area'] = building_and_block_df['geometry'].area

    # Calculate the sum of buildings area in each block.
    all_buildings_area_per_block = building_and_block_df.groupby('index_right').building_area.apply(lambda x: x.sum(skipna=False))

    # Convert to CEA projection and calculate the area of each block.
    city_blocks['geometry'] = city_blocks['geometry'].to_crs({'proj': 'cea'})
    city_blocks['block_area'] = city_blocks.geometry.area

    # Retain only blocks that have buildings.
    city_blocks = city_blocks[city_blocks.index.isin(all_buildings_area_per_block.index)]

    # Calculate the percentage of blocks removed after matching with the buildings.
    valid_polygons_count = len(city_blocks)
    removed_blocks_ratio = 1 - (valid_polygons_count / all_polygons_count)

    # Combine the total buildings area and city blocks into one dataframe.
    city_df = pd.concat([city_blocks, all_buildings_area_per_block], axis=1)

    # Calculate the building coverage ratio.
    city_df['built_ratio'] = city_df['building_area'] / city_df['block_area']

    # Filter the built ratio extreme values.
    city_df = city_df[city_df['built_ratio'] >= 0.01]
    city_df = city_df[city_df['built_ratio'] < 1.0]

    # Calculate the centers of all the blocks.
    block_vertices = city_df.geometry.apply(lambda x: list(x.exterior.coords))

    # Calculate the circum circle areas and the shape.
    circum_circle_areas = []
    for vertices_set in block_vertices:
        circle = make_circle(vertices_set)
        area_of_circle = circle[2] * circle[2] * math.pi
        circum_circle_areas.append(area_of_circle)
    city_df['circum_circle_area'] = circum_circle_areas

    city_df['shape'] = city_df['block_area'] / city_df['circum_circle_area']

    # Bin the shapes
    bin_ranges = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    bin_labels = bin_ranges[:-1]
    city_df['shape_binned'] = pd.cut(city_df['shape'], bins=bin_ranges, labels=bin_labels)

    # Bin the built ratio
    city_df['built_ratio_binned'] = pd.cut(city_df['built_ratio'], bins=bin_ranges, labels=bin_labels)

    with open(output_file, 'wb') as output_file:
        pickle.dump(city_df, output_file)

    # Calculate the percentage of area change after matching with the buildings.
    built_city_area = city_df['block_area'].sum()
    removed_area_ratio = 1 - (built_city_area / city_area)

    with open(removal_ratios_folder + city + '.pckl', 'wb') as removal_file:
        pickle.dump([removed_area_ratio, removed_blocks_ratio, built_city_area], removal_file)
