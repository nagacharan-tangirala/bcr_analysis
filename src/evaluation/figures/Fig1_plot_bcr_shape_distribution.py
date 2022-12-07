import pickle

import matplotlib.pyplot as plt
import seaborn as sns

city_name = 'Paris'

work_folder = '/home/charan/workspace/bcr_analysis/'
output_folder = work_folder + 'output/'

city_file = work_folder + 'processed_dfs/' + city_name + '.pckl'
with open(city_file, 'rb') as f:
    city_df = pickle.load(f)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1)

sns.histplot(data=city_df['built_ratio'], stat='probability', binwidth=0.025, element='step', binrange=(0, 1), ax=ax, color='#096fd6', label='BCR')
sns.histplot(data=city_df['shape'], stat='probability', binwidth=0.025, element='step', binrange=(0, 1), ax=ax, color='#ff0000', label='Shape', alpha=0.2)

plt.legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Building Coverage Ratio and Shape', fontsize=20)
plt.ylabel('Probability', fontsize=20)
plt.title('Shape and BCR histograms for ' + city_name, fontsize=21)
plt.xlim([0, 1])
plt.tight_layout()
plt.savefig(output_folder + city_name + '_' + '_bcr_shape_hist.pdf', dpi=600)
plt.close()
