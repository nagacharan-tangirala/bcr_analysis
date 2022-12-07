import pickle

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
output_folder = work_folder + 'output/'

with open(input_folder + 'continent.pckl', 'rb') as i:
    continent_df = pickle.load(i)

col = '8_clusters'

# Read the pickle file of results
with open(output_folder + 'bcr_agglomerative.pckl', 'rb') as i:
    [_, clusters_df] = pickle.load(i)

merged_df = clusters_df.merge(continent_df, how='left', left_index=True, right_index=True)

count_df = pd.DataFrame(index=set(merged_df[col]))
count_df['eu_1'] = merged_df[merged_df['continent'] == 'Europe'].groupby(col).size()
count_df['us_1'] = merged_df[merged_df['continent'] == 'North America'].groupby(col).size()
count_df['eu_1'] = count_df['eu_1'].fillna(0)
count_df['us_1'] = count_df['us_1'].fillna(0)
count_df['all_1'] = count_df['eu_1'] + count_df['us_1']

# Read the pickle file of results
with open(output_folder + 'shape_agglomerative.pckl', 'rb') as i:
    [_, clusters_df] = pickle.load(i)

merged_df = clusters_df.merge(continent_df, how='left', left_index=True, right_index=True)
count_df['eu_2'] = merged_df[merged_df['continent'] == 'Europe'].groupby(col).size()
count_df['us_2'] = merged_df[merged_df['continent'] == 'North America'].groupby(col).size()
count_df['eu_2'] = count_df['eu_2'].fillna(0)
count_df['us_2'] = count_df['us_2'].fillna(0)
count_df['all_2'] = count_df['eu_2'] + count_df['us_2']

# Read the pickle file of results
with open(output_folder + 'bcr_shape_agglomerative.pckl', 'rb') as i:
    [_, _, clusters_df] = pickle.load(i)

merged_df = clusters_df.merge(continent_df, how='left', left_index=True, right_index=True)
count_df['eu_3'] = merged_df[merged_df['continent'] == 'Europe'].groupby(col).size()
count_df['us_3'] = merged_df[merged_df['continent'] == 'North America'].groupby(col).size()
count_df['eu_3'] = count_df['eu_3'].fillna(0)
count_df['us_3'] = count_df['us_3'].fillna(0)
count_df['all_3'] = count_df['eu_3'] + count_df['us_3']

plot_df = pd.DataFrame(index=count_df.index)

for i in range(1, 4):
    plot_df['Europe ' + str(i)] = count_df['eu_' + str(i)] / count_df['eu_' + str(i)].sum() * 50.0
    plot_df['North America ' + str(i)] = count_df['us_' + str(i)] / count_df['us_' + str(i)].sum() * 50.0

plot_df.index = [x for x in range(1, 9)]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1)

line_color = 'black'

pos = [1.5, 0.4, -0.5]
alphas = [0.7, 0.7, 1.0]
patterns = ['//', '++', None]
colors = ['darkorange', 'teal']
widths = [0.2, 0.2, 0.26]

for i in range(0, 3):
    hatches = [patterns[i] for x in range(len(plot_df))]
    plot_df[['Europe ' + str(i + 1), 'North America ' + str(i + 1)]].plot(kind='bar',
                                                                          stacked=True,
                                                                          position=pos[i],
                                                                          width=widths[i],
                                                                          rot=0,
                                                                          alpha=alphas[i],
                                                                          hatch=hatches,
                                                                          edgecolor=line_color,
                                                                          linewidth=1.7,
                                                                          ax=ax,
                                                                          color=colors)

patch_1 = mpatches.Patch(facecolor=colors[0], linewidth=2, label='Europe')
patch_2 = mpatches.Patch(facecolor=colors[1], linewidth=2, label='North America')
legend_1 = plt.legend(handles=[patch_1, patch_2], fontsize=20, loc='upper right', bbox_to_anchor=(1.0, 1.0))

labels = ['BCR', 'Shape', 'BCR + Shape']
patches = []
for i in range(0, 3):
    patch = mpatches.Patch(hatch=patterns[i], linewidth=2, edgecolor=line_color, label=labels[i], facecolor='white')
    patches.append(patch)

legend_2 = plt.legend(handles=patches, fontsize=20, bbox_to_anchor=(0.0, 1.0), loc='upper left')
fig.add_artist(legend_1)

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Region-wise distribution for different clustering inputs', fontsize=21)
plt.xlabel('Class IDs', fontsize=20)
plt.ylabel('Percentage of Cities', fontsize=20)

plt.ylim([0, 36.0])
plt.xlim([-0.5, 7.5])
plt.tight_layout()
plt.savefig(output_folder + 'region_counts_compare.pdf', dpi=600)
