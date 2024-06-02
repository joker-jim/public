import sys
import json
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

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

   
    input_vector = pd.DataFrame([[
        input_data['money'],
        input_data['total_people'],
        input_data['adults'],
        input_data['children']
    ]], columns=features)

    input_vector = scaler.transform(input_vector)  

    knn = NearestNeighbors(n_neighbors=5)
    knn.fit(data_scaled)
    closest_indices = knn.kneighbors(input_vector, return_distance=False)

    recommended_cities = data.iloc[closest_indices[0]].sort_values(by='count', ascending=False)
    recommended_cities_list = recommended_cities['destination'].tolist()
    recommended_cities_formatted = "Cities for you to visit: " + ", ".join(recommended_cities_list)
    print(recommended_cities_formatted)

if __name__ == '__main__':
    main()
