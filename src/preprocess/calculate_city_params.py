import csv
import pickle
import colorama
import osmnx

from os.path import exists
from os import makedirs

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
pckl_folder = work_folder + 'nx_graphs/'
params_folder = work_folder + 'street_params/'

makedirs(params_folder, exist_ok=True)

cities_nx_files = {}
with open(input_folder + 'cities_filtered.csv', 'r') as c:
    cities_reader = csv.reader(c, delimiter=';')
    next(cities_reader)
    for row in cities_reader:
        cities_nx_files[row[0]] = pckl_folder + row[0] + '.pckl'

count = 0
for city in cities_nx_files:
    params_file = params_folder + city + '.pckl'
    count = count + 1

    if exists(params_file):
        print(colorama.Fore.YELLOW + 'Already calculated. Skipping ' + city + colorama.Style.RESET_ALL)
        continue

    print(colorama.Fore.GREEN + 'Calculating street parameters for ' + city + '. ' + str(count) + ' of ' + str(len(cities_nx_files)) + colorama.Style.RESET_ALL)

    # Read the edges and nodes from the gpkg file
    with open(cities_nx_files[city], 'rb') as i:
        city_graph = pickle.load(i)

    # Calculate the params and write them to a file
    city_params = osmnx.basic_stats(city_graph)

    # Add edge bearing and get orientation entropy
    city_graph = osmnx.add_edge_bearings(city_graph)
    city_params['entropy'] = osmnx.orientation_entropy(osmnx.get_undirected(city_graph))

    with open(params_file, 'wb') as o:
        pickle.dump(city_params, o)
