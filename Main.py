import json
import sys
import subprocess

def call_basic_information(text):
    result = subprocess.run(['python3', 'Basic_information.py', text], capture_output=True, text=True)
    if result.stderr:
        print("Error:", result.stderr)
        sys.exit(1)
    return json.loads(result.stdout)

def call_result(old_data, new_data):
    combined_data = json.dumps({"old_data": old_data, "new_data": new_data})
    result = subprocess.run(['python3', 'Result.py', combined_data], capture_output=True, text=True)
    if result.stderr:
        print("Error:", result.stderr)
        sys.exit(1)
    return result.stdout

def main():
    text_part = sys.argv[1]
    json_part = sys.argv[2] if len(sys.argv) > 2 else "{}"
    old_data = json.loads(json_part)
    
    new_data = call_basic_information(text_part)
    final_result = call_result(old_data, new_data)

    print(final_result)

if __name__ == "__main__":
    main()
