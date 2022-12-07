import csv
import pickle
from os import makedirs
from os.path import exists

import colorama
import osmnx

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
gpkg_folder = work_folder + 'network_dfs/'
pckl_folder = work_folder + 'nx_graphs/'
buildings_folder = work_folder + 'buildings/'

makedirs(gpkg_folder, exist_ok=True)
makedirs(pckl_folder, exist_ok=True)
makedirs(buildings_folder, exist_ok=True)

city_download_tags = {}
with open(input_folder + 'cities.csv', 'r') as c:
    cities_reader = csv.reader(c, delimiter=';')
    next(cities_reader)
    for row in cities_reader:
        city_download_tags[row[0]] = row[1]

count = 1
for city, download_tag in city_download_tags.items():
    city_gpkg_file = gpkg_folder + city + '.gpkg'
    city_pckl_file = pckl_folder + city + '.pckl'
    count = count + 1

    # Skip if this city's files are already downloaded.
    if exists(city_gpkg_file) and exists(city_pckl_file):
        print(colorama.Fore.YELLOW + 'Already downloaded files for ' + city + '. ' + colorama.Style.RESET_ALL)
        continue

    print(colorama.Fore.CYAN + 'Downloading road network of ' + city + '. ' + str(count) + ' of ' + str(len(city_download_tags)) + colorama.Style.RESET_ALL)

    try:
        city_graph = osmnx.graph_from_place(download_tag, network_type='drive')
    except ValueError:
        print(colorama.Fore.RED + 'Failed to download, skipping ' + city + colorama.Style.RESET_ALL)
        continue

    # Save the graph as a geopackage for easier access later.
    if not exists(city_gpkg_file):
        osmnx.save_graph_geopackage(city_graph, filepath=city_gpkg_file)

    # Also save the graph as a pickle file.
    if not exists(city_pckl_file):
        with open(city_pckl_file, 'wb') as o:
            pickle.dump(city_graph, o)

count = 1
for city, download_tag in city_download_tags.items():
    buildings_file = buildings_folder + city + '.pckl'
    count = count + 1

    if exists(buildings_file):
        print(colorama.Fore.YELLOW + 'Already downloaded files for ' + city + '. ' + colorama.Style.RESET_ALL)
        continue

    print(colorama.Fore.MAGENTA + 'Downloading buildings of ' + city + '. ' + str(count) + ' of ' + str(len(city_download_tags)) + colorama.Style.RESET_ALL)

    try:
        buildings = osmnx.geometries_from_place(download_tag, tags={'building': True})
    except ValueError:
        print(colorama.Fore.RED + 'Failed to download, skipping ' + city + colorama.Style.RESET_ALL)
        continue
    except TimeoutError:
        print(colorama.Fore.RED + 'Failed to download, skipping ' + city + colorama.Style.RESET_ALL)
        continue

    with open(buildings_file, 'wb') as b:
        pickle.dump(buildings, b)
