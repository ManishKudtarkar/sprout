import json

class EmergencyDetector:
    def __init__(self, data_path):
        self.emergency_symptoms = []
        self._load_data(data_path)

    def _load_data(self, data_path):
        try:
            with open(data_path, 'r') as f:
                data = json.load(f)
                self.emergency_symptoms = [s.lower() for s in data.get("emergency_symptoms", [])]
                
                # Fallback if empty (new json structure might miss this)
                if not self.emergency_symptoms:
                    self.emergency_symptoms = [
                        "chest pain", "difficulty breathing", "heart attack", 
                        "severe fever", "unconsciousness", "severe bleeding", 
                        "sudden severe headache"
                    ]
        except FileNotFoundError:
            print(f"Error: Data file not found at {data_path}")
            self.emergency_symptoms = []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {data_path}")
            self.emergency_symptoms = []

    def check_emergency(self, user_symptoms):
        """
        Checks if any user-provided symptoms are emergency indicators.
        Returns a list of detected emergency symptoms.
        """
        detected_emergencies = []
        for symptom in user_symptoms:
            symptom_lower = symptom.lower().strip()
            
            # check if any emergency symptom is a substring of the user symptom
            # or if the user symptom is a substring of an emergency symptom (e.g. "pain" in "chest pain" - careful!)
            # Better: Check if the emergency phrase is present in the input
            
            for emergency in self.emergency_symptoms:
                if emergency in symptom_lower:
                     detected_emergencies.append(emergency)
        
        return list(set(detected_emergencies))
