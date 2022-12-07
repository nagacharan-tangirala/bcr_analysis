import pickle

import matplotlib.pyplot as plt
import seaborn as sns

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
output_folder = work_folder + 'output/'

with open(input_folder + 'block_stats.pckl', 'rb') as i:
    block_stats_df = pickle.load(i)

plt.figure(figsize=(10, 10))

threshold = [0.5, 0.5]  # Threshold values for blocks built ratio and area retain ratio
class_1 = len(block_stats_df[(block_stats_df['blocks_built_ratio'] > threshold[0]) & (block_stats_df['area_retain_ratio'] > threshold[1])])
class_2 = len(block_stats_df[(block_stats_df['blocks_built_ratio'] > threshold[0]) & (block_stats_df['area_retain_ratio'] < threshold[1])])
class_3 = len(block_stats_df[(block_stats_df['blocks_built_ratio'] < threshold[0]) & (block_stats_df['area_retain_ratio'] > threshold[1])])
class_4 = len(block_stats_df[(block_stats_df['blocks_built_ratio'] < threshold[0]) & (block_stats_df['area_retain_ratio'] < threshold[1])])

box_color = 'white'
line_color = 'black'

g = sns.JointGrid(data=block_stats_df, x="blocks_built_ratio", y="area_retain_ratio", height=7, xlim=[0, 1], ylim=[0, 1])
g.plot_joint(sns.histplot, color='#ff0000', bins=20)
g.plot_marginals(sns.boxplot,
                 width=0.5,
                 boxprops=dict(color=line_color, facecolor='#096fd6'),
                 capprops=dict(color=line_color),
                 medianprops=dict(color=line_color),
                 whiskerprops=dict(color=line_color))

g.ax_joint.text(0.05, 0.55, 'A: ' + str(class_3), fontsize=12, bbox=dict(facecolor=box_color))
g.ax_joint.text(0.9, 0.55, 'B: ' + str(class_1), fontsize=12, bbox=dict(facecolor=box_color))
g.ax_joint.text(0.05, 0.05, 'C: ' + str(class_4), fontsize=12, bbox=dict(facecolor=box_color))
g.ax_joint.text(0.9, 0.05, 'D: ' + str(class_2), fontsize=12, bbox=dict(facecolor=box_color))

g.ax_joint.axvline(threshold[0], color=line_color, ls='--')
g.ax_joint.axhline(threshold[1], color=line_color, ls='--')

g.set_axis_labels('Change in Blocks', 'Change in Area', fontsize=17)
plt.tight_layout()
plt.savefig(output_folder + 'dist_plot.pdf', dpi=600)
plt.close()
