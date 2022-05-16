import numpy as np
import json
import pickle

with open("spoons.txt", "r") as f:
    content = f.read().splitlines()
    
with open("spoonsc.txt", "r") as f:
    coords = [[float(j) for j in i.split()] for i in f.read().splitlines()]

with open("distance.txt", "r") as f:
    dist = {}
    for i in f.read().splitlines():
        j = i.split(',')
        if j[0] in dist:
            dist[j[0]][j[1]] = int(j[2])/10
        else:
            dist[j[0]] = {}
            dist[j[0]][j[1]] = int(j[2])/10

with open('stations.json') as json_file:
    trains = json.load(json_file)
    
from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
def getDistance(coord1, coord2):
    R = 6373.0
    
    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

# index = [['CV4 7ES', 52.37938629541749, -1.5586861859549261],
#          ['CNL', 52.399418, -1.547232],
#          ['COV', 52.400787, -1.513466],
#          ['LMS', 52.284893, -1.536723]]

# for i in trains:
#     if i['crsCode'] not in ['CNL', 'COV', 'LMS']:
#         index.append([i['crsCode'], i['lat'], i['long']])

coordinates = {}
for i in trains:
    coordinates[i['crsCode']] = [i['lat'], i['long']]

content.append('CV4 7ES')
coords.append([52.37938629541749, -1.5586861859549261])

for i in range(len(content)):
    currentDict = {}
    for d in dist:
        time = getDistance(coords[i], coordinates[d])*12
        if time < 30:
            dist[d][content[i]] = time
            currentDict[d] = time
    
    dist[content[i]] = currentDict
    coordinates[content[i]] = coords[i]
    
dist['CV4 7ES']['COV'] = 30
dist['COV']['CV4 7ES'] = 30

dist['CV4 7ES']['LMS'] = 30
dist['LMS']['CV4 7ES'] = 30

sortedGraph = {}

for i in dist:
    sortedGraph[i] = dict(sorted(dist[i].items(), key=lambda item: item[1]))
    
with open('graph.pkl', 'wb') as f:
    pickle.dump(sortedGraph, f)