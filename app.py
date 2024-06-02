from flask import Flask, render_template, jsonify, request, Response
import subprocess
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify({'message': 'POST request processed'})
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    text = request.form['text']
    print(f"Received text: {text}")  

    if '##' in text:
        text_part, json_part = text.split('##', 1)  
        print(f"Text part: {text_part}")  
        print(f"JSON part: {json_part}")  
    else:
        text_part = text
        json_part = None 
        print("No JSON part to separate.")  

    args = ['python3', 'Main.py', text_part]
    if json_part:
        args.append(json_part)

    result = subprocess.run(args, capture_output=True, text=True)
    if result.stderr:
        print("Error from subprocess:", result.stderr)
        return jsonify({'success': False, 'error': result.stderr})

    text_result, json_result = result.stdout.split("##")
    json_data = json.loads(json_result)
    print("Returning to front end:", json_data) 

    

    return jsonify({'success': True, 'text': text_result, 'data': json_data})

@app.route('/submit-cached-data', methods=['POST'])
def submit_cached_data():
    try:
        data = request.json
     
        result = subprocess.run(['python3', 'Analysis.py', json.dumps(data)], capture_output=True, text=True)
        if result.stderr:
            print("Error from subprocess:", result.stderr)
            return jsonify({'success': False, 'error': result.stderr})
        
        print("Analysis result:", result.stdout)  
        return jsonify({'success': True, 'message': 'Data analyzed successfully', 'analysis': result.stdout})

    except Exception as e:
        print("Error handling submit-cached-data:", str(e))
        return Response("Error processing request", status=400)
    

if __name__ == '__main__':
    app.run(debug=True)