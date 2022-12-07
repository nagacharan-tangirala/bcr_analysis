import pickle

import matplotlib.pyplot as plt
import pandas as pd

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
output_folder = work_folder + 'output/'

with open(output_folder + 'bcr_agglomerative.pckl', 'rb') as i:
    [_, clusters_df] = pickle.load(i)

with open(input_folder + 'continent.pckl', 'rb') as i:
    continent_df = pickle.load(i)

clusters_df = clusters_df.merge(continent_df, how='left', left_index=True, right_index=True)

column = '5_clusters'

count_df = pd.DataFrame(index=set(clusters_df[column]))
count_df['eu'] = clusters_df[clusters_df['continent'] == 'Europe'].groupby(column).size()
count_df['us'] = clusters_df[clusters_df['continent'] == 'North America'].groupby(column).size()
count_df['eu'] = count_df['eu'].fillna(0)
count_df['us'] = count_df['us'].fillna(0)
count_df['all'] = count_df['eu'] + count_df['us']

count_df = count_df.reindex([2, 1, 4, 3, 0])
count_df.index = [x for x in range(0, 5)]

plot_df = pd.DataFrame(index=count_df.index)

# Make sure that the total percentage indicated in the graph is equal to 100.
plot_df['Europe'] = count_df['eu'] / count_df['eu'].sum() * 50.0
plot_df['North America'] = count_df['us'] / count_df['us'].sum() * 50.0

plot_df.index = [x for x in range(1, 6)]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1)

plot_df.plot(kind='bar', stacked=True, width=0.45, rot=0, ax=ax, color=['darkorange', 'teal'])

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20)
plt.title('Region-wise distribution of cities', fontsize=21)
plt.xlabel('Classes based on BCR', fontsize=20)
plt.ylabel('Percentage of Cities', fontsize=20)

plt.ylim([0, 31.0])
plt.xlim([-0.5, 4.5])
plt.tight_layout()
plt.savefig(output_folder + 'region_counts_bcr.pdf', dpi=600)
