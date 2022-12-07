import csv

work_folder = '/home/charan/workspace/bcr_analysis/'
input_folder = work_folder + 'input_files/'

# Set the minimum population that cities should have.
pop_limit = 100000

# Read the geonames dataset and retain only cities which have population more than 100000.
eu_country_name = {}
population_info = {}
with open(input_folder + 'EU_cities.csv', 'r') as in_file:
    csv_reader = csv.reader(in_file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        pop = int(row[13])  # 13th column has the population stat.
        if pop > pop_limit:
            eu_country_name[row[2]] = row[7]  # 7th column has the country name.
            population_info[row[2]] = pop

us_city_names = []
with open(input_folder + 'US_cities.csv', 'r') as in_file:
    csv_reader = csv.reader(in_file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        pop = int(row[13])  # 13th column has the population stat.
        if pop > pop_limit:
            us_city_names.append(row[2])
            population_info[row[2]] = pop

with open(input_folder + 'cities.csv', 'w') as out_file:
    csv_writer = csv.writer(out_file, delimiter=';')

    # Write the generic header row.
    header_row = ['city', 'osm_name', 'Continent', 'Population']
    csv_writer.writerow(header_row)

    # Write the EU cities.
    for city in eu_country_name.keys():
        country = eu_country_name[city]
        population = population_info[city]
        if '/' in city:
            city = city.replace('/', '-').replace(' ', '')
        row = [city, city + ', ' + country, 'Europe', population]
        csv_writer.writerow(row)

    # Write the US cities.
    for city in us_city_names:
        row = [city, city + ', United States', 'North America', population_info[city]]
        csv_writer.writerow(row)
