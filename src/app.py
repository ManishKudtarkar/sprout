from flask import Flask, render_template, request, jsonify
import os
from diagnosis import SymptomAnalyzer
from emergency import EmergencyDetector
from remedies import RemedyRecommender
from notifications import NotificationManager

app = Flask(__name__)

# Initialize modules
print("Initializing modules...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'symptoms.json')

emergency_detector = EmergencyDetector(DATA_PATH)
analyzer = SymptomAnalyzer(DATA_PATH)
remedy_recommender = RemedyRecommender()
notifier = NotificationManager()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_input = data.get('symptoms', '')
    user_profile = data.get('profile', {})  # Get user profile
    
    if not user_input:
        return jsonify({'error': 'No symptoms provided'}), 400

    symptoms = [s.strip() for s in user_input.split(',')]
    
    # 1. Check for Emergency
    emergencies = emergency_detector.check_emergency(symptoms)
    if emergencies:
        # Log and Notify
        msg = f"Emergency detected: {', '.join(emergencies)}"
        notifier.send_notification(msg, level="critical")
        
        return jsonify({
            'status': 'emergency',
            'emergencies': emergencies,
            'message': 'CRITICAL WARNING: High-risk symptoms detected. Seek immediate medical attention. Chat has been disabled for safety.',
            'lockdown': True
        })

    # 2. Diagnosis
    # Pass full profile to diagnosis for reranking
    predictions = analyzer.diagnose(symptoms, user_profile)
    
    if not predictions:
        return jsonify({
            'status': 'unknown',
            'message': 'Could not identify a specific condition. Please consult a doctor.'
        })

    top_prediction = predictions[0]
    # Pass profile to remedies
    remedies = remedy_recommender.get_remedies_for_condition(top_prediction, user_profile)
    remedy_details = []
    
    for remedy in remedies:
        # Clean remedy name for explanation lookup (remove warnings/details in brackets)
        # e.g. "Rest (Consult Doctor)" -> "Rest"
        clean_name = remedy.split(" (")[0]
        explanation = remedy_recommender.explain_remedy(clean_name)
        remedy_details.append({'name': remedy, 'explanation': explanation})

    return jsonify({
        'status': 'success',
        'condition': top_prediction['name'],
        'severity': top_prediction['severity'],
        'remedies': remedy_details
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
