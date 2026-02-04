from src.diagnosis import SymptomAnalyzer
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'symptoms.json')

analyzer = SymptomAnalyzer(DATA_PATH)

test_cases = [
    (["red skin", "painful from sun"], "Sunburn"),
    (["vomiting", "stomach cramps", "ate bad food"], "Food Poisoning"),
    (["computer screen", "eye pain"], "Digital Eye Strain"),
    (["bee sting", "swelling"], "Bee Sting")
]

print("Running Diagnostics Test with New Data...")
for symptoms, expected in test_cases:
    print(f"\nInput: {symptoms}")
    results = analyzer.diagnose(symptoms)
    if results:
        top_result = results[0]
        print(f"Predicted: {top_result['name']} (Source: {top_result.get('source', 'Unknown')})")
        if top_result['name'] == expected:
            print("✅ MATCH")
        else:
            print(f"❌ MISMATCH (Expected {expected})")
    else:
        print("❌ NO RESULT")
