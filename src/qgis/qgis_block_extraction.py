######################################################################
#
#
# NOTE: This script only runs in QGIS Python environment.
#
#
######################################################################
import csv

from os.path import exists
from os import makedirs, rename

from qgis.utils import iface
import processing as P

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'
gpkg_folder = work_folder + 'network_dfs/'
blocks_folder = work_folder + 'blocks/'

makedirs(blocks_folder, exist_ok=True)

geopackage_filenames = {}
with open(input_folder + 'cities.csv', 'r') as c:
    cities_reader = csv.reader(c, delimiter=';')
    next(cities_reader)
    for row in cities_reader:
        geopackage_filenames[row[0]] = gpkg_folder + row[0] + '.gpkg'

count = 0
for city, city_file in geopackage_filenames.items():
    count = count + 1

    blocks_file = blocks_folder + city + '.gpkg'
    if exists(blocks_file):
        print('Already extracted blocks for ' + city + '. ')
        continue

    if not exists(city_file):
        print('Network file not found. Skipping ' + city)
        continue

    renamed_file = False
    if '\'' in city:
        old_blocks_file = blocks_file
        city = city.replace('\'', '')
        blocks_file = blocks_folder + city + '.gpkg'
        renamed_file = True
    
    if '.' in city:
        old_blocks_file = blocks_file
        city = city.replace('.', '')
        blocks_file = blocks_folder + city + '.gpkg'
        renamed_file = True

    print('Processing ' + city + '. ' + str(count) + ' of ' + str(len(geopackage_filenames)))

    road_layer = iface.addVectorLayer(city_file + '|layername=edges', city, "ogr")

    # print('Buffering')
    buffer = P.run("native:buffer",
                   {'INPUT': road_layer, 'DISTANCE': 0.00005, 'SEGMENTS': 15,
                    'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2,
                    'DISSOLVE': True, 'OUTPUT': 'memory:buffer'})["OUTPUT"]

    # print('Convering polygons to lines')
    buffered_lines = P.run("native:polygonstolines",
                           {'INPUT': buffer, 'OUTPUT': 'memory:buffered_lines'})["OUTPUT"]

    # print('Convering Multipart to single part lines')
    part_lines = P.run("native:multiparttosingleparts",
                       {'INPUT': buffered_lines, 'OUTPUT': 'memory:part_lines'})["OUTPUT"]

    # print('Polygonising blocks')
    buffered_polygons = P.run("native:polygonize",
                              {'INPUT': part_lines,
                               'KEEP_FIELDS': False,
                               'OUTPUT': 'memory:buffered_polygons'})["OUTPUT"]

    # print('Saving blocks')
    P.run("native:multiparttosingleparts",
          {'INPUT': buffered_polygons,
           # 'OUTPUT': 'ogr:dbname=\'/mnt/hdd/workspace/osm_blocks_analysis/buffered_blocks/' + road_layer.name() + '.gpkg\' table="blocks" (geom)'})
           'OUTPUT': 'ogr:dbname=\'' + blocks_file + '\' table="blocks" (geom)'})
           # 'OUTPUT': 'ogr:dbname=\' + blocks_file + '\table="blocks" (geom)'})

    if renamed_file:
        rename(blocks_file, old_blocks_file)