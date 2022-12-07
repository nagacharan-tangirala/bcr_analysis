import pickle

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
output_folder = work_folder + 'output/'

with open(output_folder + 'bcr_agglomerative.pckl', 'rb') as i:
    [bcr_df, _] = pickle.load(i)

fig = plt.figure(figsize=(10, 7), facecolor='white')
ax = fig.add_subplot(1, 1, 1)
ax.set_facecolor('white')
matplotlib.rcParams['lines.linewidth'] = 2

linkage_matrix = linkage(bcr_df, metric='euclidean', method='ward', optimal_ordering=True)
dn = dendrogram(linkage_matrix, labels=np.array(bcr_df.index), color_threshold=2.2, orientation='right', p=12, truncate_mode='lastp')

matplotlib.rcParams['lines.linewidth'] = 3.5
plt.vlines(x=2.4, ymin=0, ymax=150, ls='--', color='black')
plt.hlines(y=[30, 60, 80, 100], xmin=0, xmax=2.4, linestyle="dashed", color='black')

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('Number of Cities', fontsize=15)
plt.title('Hierarchical Clustering Output', fontsize=18)
plt.tight_layout()
plt.savefig(output_folder + 'agglomerative_dendrogram.pdf', dpi=600)
plt.close()
