import csv
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
output_folder = work_folder + 'output/'
dfs_folder = work_folder + 'processed_dfs/'

with open(output_folder + 'bcr_agglomerative.pckl', 'rb') as i:
    [_, clusters_df] = pickle.load(i)

file_names = {}
with open(input_folder + 'cities_ny.csv', 'r') as c:
    cities_reader = csv.reader(c, delimiter=';')
    next(cities_reader)
    for row in cities_reader:
        file_names[row[0]] = dfs_folder + row[0] + '.pckl'

built_df = pd.DataFrame()
for city in file_names:
    with open(file_names[city], 'rb') as f:
        city_df = pickle.load(f)

    city_class = clusters_df.loc[city]['5_clusters']

    counts_df = pd.DataFrame()
    counts_df = pd.concat([counts_df, city_df['built_ratio']], axis=0)
    counts_df['Borough'] = city + '(' + str(city_class + 1) + ')'

    counts_df.reset_index(inplace=True)

    built_df = pd.concat([built_df, counts_df], axis=0, ignore_index=True)
    dist = city_df['built_ratio']

params = {"legend.labelspacing": 1.2,
          "legend.handletextpad": 1.3,
          }
plt.rcParams.update(params)

colors = ['#ffffff', '#5e3c29', '#ff9a00']

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1)

p = sns.kdeplot(data=built_df, x=0, hue='Borough', palette=colors, fill=True, alpha=0.6, common_norm=False, legend='auto')

widths = [2, 3, 2]
hatches = ['//', '++', '..']

handles = p.legend_.legendHandles[::-1]
legend_patches = p.legend_.get_patches()

for line, h, w, handle, legend_patch in zip(p.collections, hatches, widths, handles, legend_patches):
    line.set_hatch(h)
    line.set_linewidth(w)
    line.set_edgecolor('black')
    handle.set_edgecolor('black')
    handle.set_hatch(h)
    legend_patch.set_height(17)
    legend_patch.set_width(26)

ax.get_legend().set_title('')
plt.setp(ax.get_legend().get_texts(), fontsize=17)

plt.xlabel('BCR', fontsize=20)
plt.xticks(fontsize=20)
plt.xlim([0, 1])

plt.ylabel('Percentage', fontsize=20)
plt.yticks(fontsize=20)

plt.title('BCR Distribution for New York Boroughs', fontsize=21)
plt.tight_layout()

plt.savefig(output_folder + 'bcr_hist_new_york.pdf', dpi=600)
plt.close()
