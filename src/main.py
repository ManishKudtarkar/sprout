import os
import sys

# Add src to path so imports work if run from project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from diagnosis import SymptomAnalyzer
from emergency import EmergencyDetector
from remedies import RemedyRecommender

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'symptoms.json')

def main():
    print("==================================================")
    print("   Sprout AI - Intelligent Health Assistance")
    print("==================================================")
    print("Please describe your symptoms (separated by commas).")
    print("Example: fever, cough, runny nose")
    
    user_input = input("\nEnter Symptoms: ")
    if not user_input.strip():
        print("No symptoms entered. Exiting.")
        return

    symptoms = [s.strip() for s in user_input.split(',')]
    
    # Initialize modules
    emergency_detector = EmergencyDetector(DATA_PATH)
    analyzer = SymptomAnalyzer(DATA_PATH)
    remedy_recommender = RemedyRecommender()
    
    # 1. Check for Emergency
    emergencies = emergency_detector.check_emergency(symptoms)
    
    if emergencies:
        print("\n⚠️  CRITICAL WARNING: EMERGENCY DETECTED ⚠️")
        print(f"Detected high-risk symptoms: {', '.join(emergencies)}")
        print("Advisory: Please seek IMMEDIATE medical attention or call emergency services.")
        print("Sprout AI flags this as a critical case.")
        print("-" * 50)
        
    # 2. Diagnosis
    print("\n[Analysis Result]")
    predictions = analyzer.diagnose(symptoms)
    
    if not predictions:
        print("Could not identify a specific condition based on the provided symptoms.")
        print("Recommendation: Please consult a doctor for a detailed checkup.")
    else:
        # Show top 3 predictions if available, or just the top 1
        top_prediction = predictions[0]
        print(f"Possible Condition: {top_prediction['name']}")
        print(f"Estimated Severity: {top_prediction['severity']}")
        
        # 3. Remedies
        print("\n[Natural Remedies & Guidance]")
        remedies = remedy_recommender.get_remedies_for_condition(top_prediction)
        for remedy in remedies:
            explanation = remedy_recommender.explain_remedy(remedy)
            print(f"• {remedy}: {explanation}")

    print("\n" + "="*50)
    print("DISCLAIMER: Sprout AI is a support tool and DOES NOT replace professional medical advice.")
    print("==================================================")

if __name__ == "__main__":
    main()
