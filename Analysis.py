import sys
import json
import subprocess 

def analyze_data(json_input):
    data = json.loads(json_input)  

    time = data.get('time', None)  

    if time == 2:
        result = subprocess.run(['python3', 'National_analysis.py', json_input], check=True, text=True, capture_output=True)
        data['answer'] = result.stdout.strip()
        return json.dumps(data)
    elif time == 3:
        result = subprocess.run(['python3', 'Neighborhood_analysis.py', json_input], check=True, text=True, capture_output=True)
        data['answer'] = result.stdout.strip()
        return json.dumps(data)
    elif time == 4:
        result = subprocess.run(['python3', 'Journey_Analysis.py', json_input], check=True, text=True, capture_output=True)
        data['answer'] = result.stdout.strip()
        return json.dumps(data)
    else:
        return 'No valid time provided'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python Analysis.py <json_data>")
        sys.exit(1)

    json_input = sys.argv[1]
    response = analyze_data(json_input)
    print(response)
