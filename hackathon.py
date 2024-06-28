import csv
import os
import math

class EarthGrid:
    def __init__(self, lat_min, lat_max, lon_min, lon_max, rain_average=0):

        # variable values for debugging
        self.lat_min = lat_min
        self.lat_max = lat_max
        self.lon_min = lon_min
        self.lon_max = lon_max

        #actual important variables for the program
        self.rain_average = rain_average
        self.locSet = set()

    def printMe (self):
        print (f"Lat interval: {self.lat_min}, {self.lat_max}. Lon interval: {self.lon_min}, {self.lon_max} . Rain average: {self.rain_average}. Locations in rect count: {len(self.locSet)}")



print (os.getcwd())

#Rough Saarland extreme points
#latitude: from 49.0 to 49.7
#longitude: from 6.3 to 7.3


present_time = 1719097200
#in unix epoch.


rectMatrix = []
granularity = 0.1
latitude_min = 49.0
longitude_min = 6.3
latitude_max = 49.7
longitude_max = 7.3

second_window = 100000000
threshold = 2.0

longitude = longitude_min
latitude = latitude_min

latitude_total = 0
longitude_total = 0

while latitude < latitude_max:
    latitude += granularity
    latitude_total += 1

while longitude < longitude_max:
    longitude += granularity
    longitude_total += 1
    
longitude = longitude_min
latitude = latitude_min

print("latitude and longitude totals")
print (latitude_total)
print(longitude_total)

while latitude < latitude_max:
    while longitude < longitude_max:
        cur_grid = EarthGrid(latitude, latitude+granularity, longitude, longitude+granularity)
        longitude += granularity
        rectMatrix.append(cur_grid)
        #print (f"latitude: {cur_grid.lat_min}, longitude: {cur_grid.lon_min}")
    latitude += granularity
    longitude = longitude_min
    print(latitude)

p_lat = 49.45
p_lon = 6.78

p_x = math.floor((p_lat - latitude_min)/granularity)
p_y = math.floor((p_lon - longitude_min)/granularity)

print(f"Found: {p_x}, {p_y}")
rectMatrix[longitude_total*p_x + p_y].printMe()


# Open the CSV file
with open('input.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        p_lat = row["lat"]
        p_lon = row["lon"]
        p_x = math.floor((float(p_lat) - latitude_min)/granularity)
        p_y = math.floor((float(p_lon) - longitude_min)/granularity)
        index = longitude_total*p_x + p_y
        #rectMatrix[index].printMe()
        #print (f"{row["dt"]}, {row["city_name"]}, {row["lat"]}, {row["lon"]}")
        if present_time - int(row["dt"]) <= second_window: #number of seconds on a day: 86400
            if row["rain_3h"]!= "":
                rectMatrix[index].locSet.add((row["lat"], row["lon"],row["weather_description"]))
                rectMatrix[index].rain_average += float(row["rain_3h"])
            elif row["rain_1h"]!= "":
                rectMatrix[index].locSet.add((row["lat"], row["lon"],row["weather_description"]))
                rectMatrix[index].rain_average += float(row["rain_1h"])

danger_zones = []

for i in range (0, latitude_total):
    offset = longitude_total*i
    for j in range (0, longitude_total):
        index = offset + j
        
        locCount = len(rectMatrix[index].locSet)
        if locCount != 0 and rectMatrix[index].rain_average / locCount > threshold:
            rectMatrix[index].printMe()
            print("This location is in danger.")
            for i in rectMatrix[index].locSet:
                danger_zones.append(i)

        #print(row)
        #print(row["rain_1h"])

#print(danger_zones)

#
#
#                   PART 3 & 4
#
#   


