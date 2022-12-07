import csv
import pickle
from os.path import exists

import pandas as pd

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
dfs_folder = work_folder + 'processed_dfs/'

print('Writing continent df')
file_names = {}
continent_names = {}
with open(input_folder + 'cities_filtered.csv', 'r') as c:
    cities_reader = csv.reader(c, delimiter=';')
    next(cities_reader)
    for row in cities_reader:
        city = row[0]
        file_names[city] = dfs_folder + city + '.pckl'
        continent_names[city] = row[2]

continent_df = pd.DataFrame(data=continent_names.values(), index=continent_names.keys(), columns=['continent'])
with open(input_folder + 'continent.pckl', 'wb') as o:
    pickle.dump(continent_df, o)

print('Writing 3 binned BCR')

bcr_dist_df = pd.DataFrame()
bin_ranges = [0.0, 0.2, 0.4, 1.0]
bin_labels = ['Sparse', 'Moderate', 'Dense']

for city in file_names:
    with open(file_names[city], 'rb') as f:
        city_df = pickle.load(f)

    city_df['built_ratio_binned'] = pd.cut(city_df['built_ratio'], bins=bin_ranges, labels=bin_labels)

    counts = city_df.groupby('built_ratio_binned').size()
    counts = counts.sort_index()
    counts = [s / sum(counts) for s in counts]

    counts_df = pd.DataFrame(data=counts, columns=[city], index=bin_labels)
    bcr_dist_df = pd.concat([bcr_dist_df, counts_df], axis=1)

bcr_df = bcr_dist_df.transpose(copy=True)

with open(input_folder + 'bcr_3.pckl', 'wb') as o:
    pickle.dump(bcr_df, o)

print('Writing 10 binned BCR')

bcr_dist_df = pd.DataFrame()
bin_ranges = [s / 10 for s in range(0, 11)]
bin_labels = bin_ranges[1:]

for city in file_names:
    with open(file_names[city], 'rb') as f:
        city_df = pickle.load(f)

    city_df['built_ratio_binned'] = pd.cut(city_df['built_ratio'], bins=bin_ranges, labels=bin_labels)

    counts = city_df.groupby('built_ratio_binned').size()
    counts = counts.sort_index()
    counts = [s / sum(counts) for s in counts]

    counts_df = pd.DataFrame(data=counts, columns=[city])
    bcr_dist_df = pd.concat([bcr_dist_df, counts_df], axis=1)

bcr_df = bcr_dist_df.transpose(copy=True)

with open(input_folder + 'bcr_10.pckl', 'wb') as o:
    pickle.dump(bcr_df, o)

print('Writing 10 binned shape')

shapes_df = pd.DataFrame()
shapes_df.index = bin_labels

for city in file_names:
    with open(file_names[city], 'rb') as f:
        city_df = pickle.load(f)

    city_df['shape_binned'] = pd.cut(city_df['shape'], bins=bin_ranges, labels=bin_labels)
    counts = city_df.groupby('shape_binned').size()
    counts = counts.sort_index()
    counts = [s / sum(counts) for s in counts]

    counts_df = pd.DataFrame(data=counts, columns=[city], index=bin_labels)
    shapes_df = pd.concat([shapes_df, counts_df], axis=1)

shapes_df = shapes_df.transpose(copy=True)

with open(input_folder + 'shape_10.pckl', 'wb') as o:
    pickle.dump(shapes_df, o)

print('Writing 3 binned shape')

shapes_df = pd.DataFrame()
bin_ranges = [0.0, 0.25, 0.5, 1.0]
bin_labels = ['Low', 'Medium', 'High']
shapes_df.index = bin_labels

for city in file_names:
    with open(file_names[city], 'rb') as f:
        city_df = pickle.load(f)

    city_df['shape_binned'] = pd.cut(city_df['shape'], bins=bin_ranges, labels=bin_labels)
    counts = city_df.groupby('shape_binned').size()
    counts = counts.sort_index()
    counts = [s / sum(counts) for s in counts]

    counts_df = pd.DataFrame(data=counts, columns=[city], index=bin_labels)
    shapes_df = pd.concat([shapes_df, counts_df], axis=1)

shapes_df = shapes_df.transpose(copy=True)

with open(input_folder + 'shape_3.pckl', 'wb') as o:
    pickle.dump(shapes_df, o)

print('Done!')
