from flask import Flask, render_template, request, jsonify
import os
from diagnosis import SymptomAnalyzer
from emergency import EmergencyDetector
from remedies import RemedyRecommender

app = Flask(__name__)

# Initialize modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'symptoms.json')

emergency_detector = EmergencyDetector(DATA_PATH)
analyzer = SymptomAnalyzer(DATA_PATH)
remedy_recommender = RemedyRecommender()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_input = data.get('symptoms', '')
    
    if not user_input:
        return jsonify({'error': 'No symptoms provided'}), 400

    symptoms = [s.strip() for s in user_input.split(',')]
    
    # 1. Check for Emergency
    emergencies = emergency_detector.check_emergency(symptoms)
    if emergencies:
        return jsonify({
            'status': 'emergency',
            'emergencies': emergencies,
            'message': 'CRITICAL WARNING: High-risk symptoms detected. Seek immediate medical attention.'
        })

    # 2. Diagnosis
    predictions = analyzer.diagnose(symptoms)
    if not predictions:
        return jsonify({
            'status': 'unknown',
            'message': 'Could not identify a specific condition. Please consult a doctor.'
        })

    top_prediction = predictions[0]
    remedies = remedy_recommender.get_remedies_for_condition(top_prediction)
    remedy_details = []
    
    for remedy in remedies:
        explanation = remedy_recommender.explain_remedy(remedy)
        remedy_details.append({'name': remedy, 'explanation': explanation})

    return jsonify({
        'status': 'success',
        'condition': top_prediction['name'],
        'severity': top_prediction['severity'],
        'remedies': remedy_details
    })

if __name__ == '__main__':
    app.run(debug=True)
