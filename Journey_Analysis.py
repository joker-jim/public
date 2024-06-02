import sys
import json
from googlesearch import search

def search_ticket_prices(origin, destination, date):
    query = f"flights from {origin} to {destination} on {date}"
    for i, url in enumerate(search(query)):
        if i == 0:  
            return url

def search_attractions(destination, total_people, children):
    query = f"{destination} attractions for {total_people} people or {children} children"
    for i, url in enumerate(search(query)):
        if i == 0: 
            return url

def search_hotel_prices(destination, date):
    query = f"hotels in {destination} on {date}"
    for i, url in enumerate(search(query)):
        if i == 0: 
            return url

def search_local_cuisine(destination):
    query = f"{destination} local cuisine"
    for i, url in enumerate(search(query)):
        if i == 0: 
            return url

def analyze_journey(json_input):
    input_data = json.loads(json_input)
    
    tickets_url = search_ticket_prices(input_data['origin'], input_data['destination'], input_data['date'])
    attractions_url = search_attractions(input_data['destination'], input_data['total_people'], input_data['children'])
    hotel_url = search_hotel_prices(input_data['destination'], input_data['date'])
    cuisine_url = search_local_cuisine(input_data['destination'])
    
    answer_data = {
        'ticket_info': tickets_url,
        'attraction_info': attractions_url,
        'hotel_info': hotel_url,
        'cuisine_info': cuisine_url
    }
    
    return json.dumps(answer_data, indent=4)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python Journey_Analysis.py <json_data>")
        sys.exit(1)

    json_input = sys.argv[1]
    response = analyze_journey(json_input)
    print(response)
