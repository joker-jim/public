import sys
import json
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import math

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  
    distance = r * c

    return distance

def main():
    if len(sys.argv) != 2:
        print("Usage: python National_analysis.py <json_data>")
        sys.exit(1)

    data = pd.read_excel('file/Data/10.xlsx')
    data.fillna(0, inplace=True)
    features = ['money', 'total_people', 'adults', 'children']
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[features])

    json_input = sys.argv[1]
    input_data = json.loads(json_input)

    origin = input_data['origin']
    origin_row = data[data['destination'] == origin]
    origin_coordinates = origin_row[['Latitude', 'Longitude']].values

    knn_features = ['Latitude', 'Longitude', 'children', 'adults', 'total_people', 'money']
    knn_data = data[knn_features]

    knn = NearestNeighbors(n_neighbors=6)  
    knn.fit(data_scaled)

    input_vector = pd.DataFrame([[
        input_data['money'],
        input_data['total_people'],
        input_data['adults'],
        input_data['children']
    ]], columns=features)
    input_vector_scaled = scaler.transform(input_vector) 

    closest_indices = knn.kneighbors(input_vector_scaled, return_distance=False)

    threshold_distance = 400 
    nearby_cities = []
    distant_cities = []

    for idx in closest_indices[0][1:]: 
        city_coords = data.loc[idx, ['Latitude', 'Longitude']]
        distance = haversine(origin_coordinates[0][1], origin_coordinates[0][0], city_coords['Longitude'], city_coords['Latitude'])
        if distance <= threshold_distance:
            nearby_cities.append(data.loc[idx, 'destination'])
        else:
            distant_cities.append(data.loc[idx, 'destination'])

 
    num_nearby_cities = len(nearby_cities)
    num_distant_cities_needed = 5 - num_nearby_cities
    additional_distant_cities = distant_cities[:num_distant_cities_needed]
    recommended_cities = nearby_cities + additional_distant_cities

    print("Cities for you to visit:")
    print("Within {} km of the origin:".format(threshold_distance))
    print(", ".join(nearby_cities))
    print("Other cities:")
    print(", ".join(additional_distant_cities))

if __name__ == '__main__':
    main()
