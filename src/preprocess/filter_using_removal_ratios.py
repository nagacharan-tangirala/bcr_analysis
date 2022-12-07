import csv
import pickle

import pandas as pd

from os.path import exists

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
removal_ratios_folder = work_folder + 'removal_ratios/'

removal_ratio_files = {}
city_rows = {}
with open(input_folder + 'cities.csv', 'r') as c:
    cities_reader = csv.reader(c, delimiter=';')
    next(cities_reader)
    header_row = next(cities_reader)
    for row in cities_reader:
        city_rows[row[0]] = row
        removal_ratio_files[row[0]] = removal_ratios_folder + row[0] + '.pckl'

area_ratios = []
block_ratios = []
missing_cities = []
built_city_areas = {}
for city in removal_ratio_files:
    if not exists(removal_ratio_files[city]):
        print('Skipping ' + city)
        missing_cities.append(city)
        continue

    with open(removal_ratio_files[city], 'rb') as i:
        [area_retain_ratio, block_retain_ratio, built_city_area] = pickle.load(i)

    area_ratios.append(area_retain_ratio)
    block_ratios.append(block_retain_ratio)
    built_city_areas[city] = built_city_area

city_rows = {k: v for k, v in city_rows.items() if k not in missing_cities}

# Create a dataframe to store the ratios.
block_stats_df = pd.DataFrame(index=city_rows.keys())
block_stats_df['area_retain_ratio'] = area_ratios
block_stats_df['blocks_built_ratio'] = block_ratios

# Threshold values for blocks built ratio and area retain ratio
threshold = [0.5, 0.5]

# Filter the dataframe based on the threshold values.
temp_df_1 = block_stats_df[(block_stats_df['area_retain_ratio'] < threshold[0]) & (block_stats_df['blocks_built_ratio'] < threshold[1])]
temp_df_2 = block_stats_df[(block_stats_df['blocks_built_ratio'] < threshold[0]) & (block_stats_df['area_retain_ratio'] > threshold[1])]

filtered_cities_df = pd.concat([temp_df_1, temp_df_2], axis=0)

# Write a new CSV with cities that satisfy the filtering criteria.
with open(input_folder + 'cities_filtered.csv', 'w') as o:
    csv_writer = csv.writer(o, delimiter=';')
    header_row.append('built_area')
    csv_writer.writerow(header_row)

    # Iterate through the cities and write the rows by appending city area to it.
    for city in filtered_cities_df.index:
        city_rows[city].append(built_city_areas[city])
        csv_writer.writerow(city_rows[city])

# Write the dataframe to reuse later as an input for plotting Fig5.
with open(input_folder + 'block_stats.pckl', 'wb') as o:
    pickle.dump(block_stats_df, o)
