import requests
import json

url = 'http://127.0.0.1:5000/analyze'
data = {
    "symptoms": "fever",
    "profile": {
        "age": 25,
        "body_type": "neutral"
    }
}

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Status: Success")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Status: Failed {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
