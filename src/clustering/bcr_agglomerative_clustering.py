import pickle
from os import makedirs

import pandas as pd
from sklearn.cluster import AgglomerativeClustering

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
output_folder = work_folder + 'output/'
makedirs(output_folder, exist_ok=True)

with open(input_folder + 'bcr_3.pckl', 'rb') as i:
    all_cities_df = pickle.load(i)

clusters_df = pd.DataFrame()
clusters_df.index = all_cities_df.index

cl_model = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
cl_model.fit(all_cities_df)
clusters_df['5_clusters'] = cl_model.labels_

cl_model = AgglomerativeClustering(n_clusters=8, affinity='euclidean', linkage='ward')
cl_model.fit(all_cities_df)
clusters_df['8_clusters'] = cl_model.labels_

with open(output_folder + 'bcr_agglomerative.pckl', 'wb') as o:
    pickle.dump([all_cities_df, clusters_df], o)
