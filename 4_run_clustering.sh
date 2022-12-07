#!/bin/bash
echo "......Clustering cities based on BCR......"
sleep 2
python3 ./src/clustering/bcr_agglomerative_clustering.py
sleep 2
echo "......Clustering cities based on Shape......"
sleep 2
python3 ./src/clustering/shape_agglomerative_clustering.py
sleep 2
echo "......Clustering cities based on BCR and Shape combined......"
sleep 2
python3 ./src/clustering/bcr_shape_agglomerative_clustering.py
sleep 2
echo "......Done!!!......"
sleep 2