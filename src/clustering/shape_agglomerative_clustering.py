import pickle

import pandas as pd

from os.path import exists
from sklearn.cluster import AgglomerativeClustering

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
output_folder = work_folder + 'output/'

with open(input_folder + 'shape_3.pckl', 'rb') as i:
    shape_df = pickle.load(i)

clusters_df = pd.DataFrame()
clusters_df.index = shape_df.index

cl_model = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
cl_model.fit(shape_df)
clusters_df['5_clusters'] = cl_model.labels_

cl_model = AgglomerativeClustering(n_clusters=8, affinity='euclidean', linkage='ward')
cl_model.fit(shape_df)
clusters_df['8_clusters'] = cl_model.labels_

with open(output_folder + 'shape_agglomerative.pckl', 'wb') as o:
    pickle.dump([shape_df, clusters_df], o)
