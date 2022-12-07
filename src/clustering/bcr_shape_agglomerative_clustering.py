import pickle
import os

import pandas as pd

from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
output_folder = work_folder + 'output/'

with open(input_folder + 'bcr_10.pckl', 'rb') as i:
    built_df = pickle.load(i)

with open(input_folder + 'shape_10.pckl', 'rb') as i:
    shapes_df = pickle.load(i)

with open(input_folder + 'bcr_3.pckl', 'rb') as i:
    built_df_3 = pickle.load(i)

with open(input_folder + 'shape_3.pckl', 'rb') as i:
    shapes_df_3 = pickle.load(i)

# Combine BCR and shape into a single feature input.
df_20d = pd.concat([built_df, shapes_df], axis=1)
combined_20d = df_20d.to_numpy()

clusters_df = pd.DataFrame()
clusters_df.index = df_20d.index
clusters_df = clusters_df.join(built_df_3)
clusters_df = clusters_df.join(shapes_df_3)

# Use tSNE to convert 20 dimensional vector to 2-dimensional.
tsne_model = TSNE(n_components=2, learning_rate='auto', init='pca', early_exaggeration=12, n_iter=5000, method='exact', perplexity=35)
combined_tsne = tsne_model.fit_transform(combined_20d)

clusters_df['c1'] = combined_tsne[:, 0]
clusters_df['c2'] = combined_tsne[:, 1]

label = '8_clusters'
cl_model = AgglomerativeClustering(n_clusters=8, affinity='euclidean', linkage='ward').fit(combined_tsne)
clusters_df[label] = cl_model.labels_

with open(output_folder + 'bcr_shape_agglomerative.pckl', 'wb') as o:
    pickle.dump([built_df_3, shapes_df_3, clusters_df], o)
