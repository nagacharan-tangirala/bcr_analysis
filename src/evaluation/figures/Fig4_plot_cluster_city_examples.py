import pickle

import pandas as pd

import matplotlib.colors as colors
import matplotlib.pyplot as plt

work_folder = '/home/charan/workspace/bcr_analysis/'
processed_dfs_folder = work_folder + 'processed_dfs/'
output_folder = work_folder + 'output/'

with open(output_folder + 'bcr_agglomerative.pckl', 'rb') as i:
    [_, clusters_df] = pickle.load(i)

f, axarr = plt.subplots(2, 3, figsize=(12, 8))
axes = [axarr[0][0], axarr[0][1], axarr[0][2], axarr[1][0], axarr[1][1]]
axarr[1][2].axis('off')

for a in axes:
    a.set_aspect('equal')
    a.axis('off')

f.subplots_adjust(wspace=0, hspace=0)

cities_of_interest = ['Barcelona', 'Ipswich', 'Miami', 'Budapest', 'Dublin']

bin_ranges = [0.0, 0.2, 0.4, 1.0]
bin_labels = ['Sparse', 'Moderate', 'Dense']

cols = ['#bbbbbb', '#ff9a00', '#471c17']

i = 0
for city in cities_of_interest:
    with open(processed_dfs_folder + city + '.pckl', 'rb') as f:
        city_df = pickle.load(f)

    city_df = city_df.to_crs('epsg:4326')
    city_df['built_ratio_binned'] = pd.cut(city_df['built_ratio'], bins=bin_ranges, labels=bin_labels)

    city_df.plot(column='built_ratio_binned', ax=axes[i], edgecolor='none', cmap=colors.ListedColormap(cols))

    axes[i].set_title(city)
    i = i + 1

plt.tight_layout()
plt.savefig(output_folder + 'city_maps.pdf', dpi=600)
plt.close()
