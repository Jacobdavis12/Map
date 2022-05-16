import pickle
size = 1

with open('graph.pkl', 'rb') as f:
    distances = pickle.load(f)
    
paths = [[0, 'CV4 7ES', 0, ['CV4 7ES']]]#distance, current, stops, path
first = True
p = 0
while True:
    #print(paths[0][0], paths, len(paths))
    if paths[0][0] > p:
        input(paths[0][0])
        p = int(paths[0][0]) + 1
    path = paths[0]
    newPaths = []
    if path[1] == 'CV4 7ES' and not first:
        if path[2] >= size:
            print(size, path)
            size += 1
    else:
        first = False
        for i in distances[path[1]]:
            if path[3].count(i) < 2:
                #print(i)
                if len(i) > 3:
                    newPaths.append([path[0] + distances[path[1]][i], i, path[2] + 1, path[3] + [i]])
                else:
                    newPaths.append([path[0] + distances[path[1]][i], i, path[2], path[3] + [i]])
    del paths[0]
    inputI = 0
    
    for i in newPaths:
        while len(paths) > inputI and i[0] > paths[inputI][0]:
            inputI += 1
            
        paths.insert(inputI, i)
        
