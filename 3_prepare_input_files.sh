#!/bin/bash
echo "......Calculating BCR for all the cities......"
sleep 2
python3 ./src/preprocess/calculate_bcr.py
sleep 2
echo "......Filtering cities based on removal ratios......"
sleep 2
python3 ./src/preprocess/filter_using_removal_ratios.py
sleep 2
echo "......Preparing Dataframes......"
sleep 2
python3 ./src/preprocess/prepare_input_dataframes.py
sleep 2
echo "......Calculating Street Network parameters......"
sleep 2
python3 ./src/preprocess/calculate_city_params.py
sleep 2
echo "......Done!!!......"
sleep 2