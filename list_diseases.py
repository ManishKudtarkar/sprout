import json
try:
    with open('data/symptoms.json', 'r') as f:
        data = json.load(f)
        keys = list(data.get('disease_symptoms', {}).keys())
        print(keys)
except Exception as e:
    print(e)
