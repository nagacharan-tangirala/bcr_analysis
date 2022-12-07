import pickle

import pandas as pd

import matplotlib.colors as colors
import matplotlib.pyplot as plt

work_folder = '/home/charan/workspace/bcr_analysis/'
processed_dfs_folder = work_folder + 'processed_dfs/'
output_folder = work_folder + 'output/'

with open(output_folder + 'bcr_agglomerative.pckl', 'rb') as i:
    [_, clusters_df] = pickle.load(i)

fig, axarr = plt.subplots(2, 3, figsize=(14, 9), gridspec_kw={'width_ratios': [1, 1.15, 1]})
axes = [axarr[0][0], axarr[0][1], axarr[1][0], axarr[1][1], axarr[1][2]]

fig.subplots_adjust(wspace=-0.3, hspace=0)

legend_axis = axarr[0][2]

cities_of_interest = ['Barcelona', 'Ipswich', 'Miami', 'Budapest', 'Dublin']
bin_ranges = [0.0, 0.2, 0.4, 1.0]
bin_labels = ['Sparse', 'Moderate', 'Dense']

cols = ['#FAEBCD', '#EF6C35', '#000000']

i = 0
for city in cities_of_interest:
    with open(processed_dfs_folder + city + '.pckl', 'rb') as f:
        city_df = pickle.load(f)

    city_df = city_df[city_df['built_ratio'] >= 0.01]
    city_df = city_df[city_df['built_ratio'] <= 1.0]

    city_df = city_df.to_crs('epsg:4326')
    city_df['built_ratio_binned'] = pd.cut(city_df['built_ratio'], bins=bin_ranges, labels=bin_labels)

    city_df.plot(column='built_ratio_binned', ax=axes[i], edgecolor='none', cmap=colors.ListedColormap(cols))

    axes[i].set_title(city + ' (Class ' + str(i + 1) + ')', fontsize=15)
    axes[i].axis('off')

    i = i + 1

legend_axis.axis('off')
legend_axis.plot([], [], marker='o', color=cols[0], ms=12, ls='', label='Sparse')
legend_axis.plot([], [], marker='o', color=cols[1], ms=12, ls='', label='Moderate')
legend_axis.plot([], [], marker='o', color=cols[2], ms=12, ls='', label='Dense')
legend_axis.legend(fontsize=18, loc='upper center')

fig.suptitle("Cities with blocks colored according to BCR categories", fontweight=20, fontsize=18)
plt.tight_layout()
plt.savefig(output_folder + 'city_maps.pdf', dpi=600)
plt.close()
