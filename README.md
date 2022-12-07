# BCR Analysis

This repository contains code to reproduce results in the paper titled 'City Classification using Buildings and Blocks'.

## Process

### Setup
Install `osmnx 1.1.2` and its necessary dependencies using the steps mentioned here -  
https://osmnx.readthedocs.io/en/stable/#installation

Install `Qgis 3.26.1`. Download it from here - https://download.qgis.org/downloads/ <br>
Installation instructions are within the zip file.

### Data
The list of cities and their population statistics must be downloaded from https://www.geonames.org/. <br>
Separate the statistics into two CSV files namely `US_cities.csv` and `EU_cities.csv`.
For one of the figures, `cities_ny.csv` is used. This file is also available in the directory.
We have provided the CSV files that were used to generate the results in the paper.

### Steps
- Select a location `<work_space>` where there is sufficient hard disk drive to store network and buildings data.
- Create a folder called `input_files` in `<work_space>`. 
- Place `US_cities.csv`, `EU_cities.csv` and `polygon_extract.qgz` in the `input_files` folder.
- Set `work_folder` variable in the python scripts to `<work_space>` wherever necessary.
- Run scripts according to the numbers from `1` and `5`.
- The results are stored in the `output` folder.

### NOTE
Downloading street networks and buildings requires high system memory. With 32 GB systems, the big cities like New York, London, Berlin cannot be downloaded. For these cities, 64 GB is required. This is a one-time process and could take about couple of days for all the cities. To facilitate faster reviewing process, the downloaded files are provided at - xxx

If you want to skip the download process -  

- Download network files from - 
- Move the folders to `<work_space>` and do NOT change the folder names.
- Run the scripts in the same order, they will use the downloaded files.

We have provided the blocks files to remove the necessity to install QGIS. The blocks files are available at - xxx