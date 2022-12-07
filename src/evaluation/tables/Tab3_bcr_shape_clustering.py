import pickle
import csv

import pandas as pd

from math import log


def calculate_relative_entropy(entropy):
    grid_entropy = 0 - log(1 / 4)
    max_entropy = 0 - log(1 / 36)
    rel_entropy = 1 - pow((entropy - grid_entropy) / (max_entropy - grid_entropy), 2)
    return rel_entropy


work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
street_params_folder = work_folder + 'street_params/'
output_folder = work_folder + 'output/'

# Load the city params here.
file_names = {}
areas = {}
with open(input_folder + 'cities_filtered.csv', 'r') as c:
    cities_reader = csv.reader(c, delimiter=';')
    next(cities_reader)
    for row in cities_reader:
        file_names[row[0]] = street_params_folder + row[0] + '.pckl'
        areas[row[0]] = float(row[4])

street_params_df = pd.DataFrame()
parameter_list = []
for city in file_names:
    with open(file_names[city], 'rb') as f:
        city_params = pickle.load(f)

    if len(street_params_df) == 0:
        parameter_list = list(city_params.keys())
        street_params_df.index = parameter_list

    params_df = pd.DataFrame(data=list(city_params.values()), index=parameter_list, columns=[city])
    street_params_df.index = params_df.index.copy()
    street_params_df = pd.concat([street_params_df, params_df], axis=1)

city_street_df = street_params_df.transpose(copy=True)

city_street_df['area'] = city_street_df.index.map(areas)
city_street_df['area'] = city_street_df['area'].apply(lambda x: x / 1000000)

city_street_df['edge_length_total'] = city_street_df['edge_length_total'].apply(lambda x: x / 1000)

city_street_df.drop(['streets_per_node_counts', 'streets_per_node_proportions'], axis=1, inplace=True)
parameter_list.remove('streets_per_node_counts')
parameter_list.remove('streets_per_node_proportions')

city_street_df['entropy'] = city_street_df['entropy'].apply(lambda x: calculate_relative_entropy(x))

# Load clustering results here.
with open(output_folder + 'bcr_shape_agglomerative.pckl', 'rb') as i:
    [_, _, clusters_df] = pickle.load(i)

# Combine street params with the clusters df.
# merged_df = bcr_df.merge(clusters_df, how='left', left_index=True, right_index=True)
merged_df = clusters_df.merge(city_street_df, how='left', left_index=True, right_index=True)

n = 8
col = str(n) + '_clusters'

interested_columns = ['Sparse', 'Moderate', 'Dense', 'Low', 'Medium', 'High', 'entropy', 'k_avg', 'edge_length_avg', 'edge_length_total', '8_clusters', 'area']
delete_columns = [x for x in merged_df.columns if x not in interested_columns]

output_table = merged_df.drop(delete_columns, axis=1, inplace=False)

# We can convert this table into latex table format by calling the helper function.
final_table = output_table.astype(float).groupby(col).median().round(2)

# Re-index to match with the Fig5 plotting arrangement.
final_table = final_table.reindex([2, 0, 4, 1, 7, 5, 6, 3])
final_table = final_table.applymap("{0:.2f}".format).astype(str)

# We can convert this table into latex table format by calling the helper function.
final_table_string = final_table.to_latex(index=False)

with open(output_folder + 'Tab3_bcr_shape_clustering.txt', 'w') as f:
    f.write(final_table_string)
