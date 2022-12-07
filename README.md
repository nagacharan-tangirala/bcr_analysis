# BCR Analysis

This repository contains code to reproduce results in the paper titled 'City Classification using Buildings and Blocks'.

## Quick Steps

### Steps

To ensure smooth reviewing, the pre-processed dataframes with the distributions of BCR and Shapes for all cities are provided in the repository. All the necessary input files are also included.

- Install `osmnx 1.1.2` and its necessary dependencies using the steps mentioned here -  
https://osmnx.readthedocs.io/en/stable/#installation
- Select a location `<work_space>` where you want to clone the repository.
- Extract the `street_params.tar` and `input_files.tar` archives in the `<work_space>` folder.
- Run scripts starting with `4` and `5` to generate the clustering results and the plots.

This ensures one-to-one replication of the figures and tables in the paper.

### Paper Info 

The code was run on a system with the following configuration -
- OS - Ubuntu 20.04
- RAM - 64 GB
- CPU - Ryzen 7 3900X

The network and building files were downloaded from OSM in the period between `23.11.2022` and `27.11.2022`.

The population statistics were downloaded from https://www.geonames.org/ on `12.08.2022`.

## Detailed Steps

If you want to generate the data from scratch, follow the steps below.

### Setup

Install `osmnx 1.1.2` and its necessary dependencies using the steps mentioned here -
[osmnx_docs](https://osmnx.readthedocs.io/en/stable/#installation) <br>

Install `Qgis 3.26.1`. Download it from here - https://download.qgis.org/downloads/ <br>
Installation instructions are within the downloaded archive.

### Data
The list of cities and their population statistics must be downloaded from https://www.geonames.org/. <br>
It could be any source, the goal is to provide a list of cities with their population statistics. <br>
We have provided the CSV files that were used to generate the results in the paper. These can be used to understand the CSV format.

- Select a location `<work_space>` where there is sufficient hard disk drive to store network and buildings data.
- Clone the repository in the `<work_space>` folder, you can clone to other locations too. 
- Create a folder called `input_files` in the `<work_space>` folder.
- Place the population statistics CSV file in the `input_files` folder.
- Set `work_folder` variable in the python scripts to `<work_space>` wherever necessary (almost all scripts).
- Run scripts according to the numbers from `1` and `5`.
- The results are stored in the `output` folder.

##### NOTE:
- Downloading street networks and buildings requires high system memory. With `32GB` systems, the big cities like New York, London, Berlin cannot be downloaded. For these cities, `>32GB` RAM is required.
 - Downloading network files could take about 2-4 days for all the cities. It is highly recommended to have a local instance of OSM. For more details please refer - [OSM_Local_Setup](https://wiki.openstreetmap.org/wiki/Setting_up_a_local_copy_of_the_OpenStreetMap_database,_kept_up_to_date_with_minutely_diffs)
- The population statistics CSV files are hardcoded in the scripts. If you want to use a different CSV file, you must change the file name. 
- Any other errors due to newly provided filenames, directories must be fixed manually.
- If there are any changes in the format of the CSV, the code must be modified accordingly. <br>


