import json
import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'symptoms.json')
MODEL_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'symptom_model.pkl')

def train_model():
    print("Loading data...")
    try:
        # Load main data
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
            
        # Load additional data
        remedies_path = os.path.join(os.path.dirname(BASE_DIR), 'data', 'remedies.json')
        additional = []
        try:
            with open(remedies_path, 'r') as rf:
                additional = json.load(rf).get("additional_conditions", [])
        except:
            pass
            
        # Handle new structure
        raw_conditions = data.get("disease_symptoms", {})
        conditions = []
        if raw_conditions:
                for name, symptoms in raw_conditions.items():
                    conditions.append({
                        "name": name, 
                        "symptoms": symptoms
                    })
        else:
                conditions = data.get("conditions", [])
        
        # Merge
        conditions.extend(additional)

    except FileNotFoundError:
        print(f"Error: {DATA_PATH} not found.")
        return

    # Prepare dataset
    # Since we have very few examples, we will "explode" the data a bit 
    # or just use the combined symptoms string as one sample per condition.
    # For better results with such small data, we might want to augment, 
    # but for this demo, we'll map "symptom string" -> "condition name".
    
    X = []
    y = []
    
    for condition in conditions:
        # Create a combined string of symptoms
        # Example: "runny nose sneezing sore throat" -> "Common Cold"
        symptoms_text = " ".join(condition["symptoms"])
        X.append(symptoms_text)
        y.append(condition["name"])
        
        # Data Augmentation (Simple): define single symptoms also pointing to the condition
        # This helps if user only types one symptom.
        for symptom in condition["symptoms"]:
            X.append(symptom)
            y.append(condition["name"])

    print(f"Training on {len(X)} samples...")

    # Create a wrapper pipeline
    # We use SGDClassifier (SVM) or MultinomialNB. SVM is often good for text text.
    text_clf = Pipeline([
        ('vect', CountVectorizer(stop_words='english')),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(loss='hinge', penalty='l2',
                              alpha=1e-3, random_state=42,
                              max_iter=5, tol=None)),
    ])

    text_clf.fit(X, y)

    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(text_clf, MODEL_PATH)
    print("Model training complete.")

if __name__ == "__main__":
    train_model()
