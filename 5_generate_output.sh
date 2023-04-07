#!/bin/bash
echo "......Plotting Figures......"
sleep 2
python3 ./src/evaluation/figures/Fig1_plot_bcr_shape_distribution.py
python3 ./src/evaluation/figures/Fig2_plot_bivariate_distribution.py
python3 ./src/evaluation/figures/Fig3_plot_clustering_dendrogram.py
python3 ./src/evaluation/figures/Fig4_plot_cluster_city_examples.py
python3 ./src/evaluation/figures/Fig5_bcr_regional_distribution.py
python3 ./src/evaluation/figures/Fig6_bcr_shape_regional_distribution.py
python3 ./src/evaluation/figures/Fig7_newyork_bcr_comparison.py
echo "......Generating text files with stats displayed in the tables......"
sleep 2
python3 ./src/evaluation/tables/Tab2_bcr_clustering.py
python3 ./src/evaluation/tables/Tab3_bcr_shape_clustering.py
echo "......Done!!!......"
sleep 2
