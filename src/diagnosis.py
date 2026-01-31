import json
import os
import sys

# Try imports for advanced features, handle failure gracefully
try:
    import chromadb
    from chromadb.utils import embedding_functions
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False

try:
    import joblib
    ML_MODEL_AVAILABLE = True
except ImportError:
    ML_MODEL_AVAILABLE = False

class SymptomAnalyzer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.conditions = []
        self._load_data(data_path)
        
        # Paths
        base_dir = os.path.dirname(os.path.dirname(data_path)) # up from data/symptoms.json to root
        self.db_path = os.path.join(base_dir, "data", "chroma_db")
        self.model_path = os.path.join(base_dir, "data", "symptom_model.pkl")
        
        self.vector_client = None
        self.collection = None
        self.ml_model = None
        
        # Initialize Advanced Modules
        self._init_vector_db()
        self._init_ml_model()

    def _load_data(self, data_path):
        try:
            # 1. Load Main Data
            with open(data_path, "r") as f:
                data = json.load(f)
                
            # 2. Load Remedies & Additional Conditions
            remedies_path = os.path.join(os.path.dirname(os.path.dirname(data_path)), 'data', 'remedies.json')
            remedy_map = {}
            additional_conditions = []
            
            try:
                with open(remedies_path, 'r') as rf:
                    rdata = json.load(rf)
                    remedy_map = rdata.get("disease_remedies", {})
                    additional_conditions = rdata.get("additional_conditions", [])
            except:
                pass

            # Handle new structure
            raw_conditions = data.get("disease_symptoms", {})
            if raw_conditions:
                    self.conditions = []
                    for name, symptoms in raw_conditions.items():
                        self.conditions.append({
                            "name": name, 
                            "symptoms": symptoms,
                            "remedies": remedy_map.get(name.lower().strip(), ["Consult a doctor."]),
                            "severity": "Unknown"
                        })
            else:
                self.conditions = data.get("conditions", [])
            
            # 3. Append Additional Conditions (Nose Bleed, etc.)
            self.conditions.extend(additional_conditions)
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.conditions = []

    def _init_vector_db(self):
        if VECTOR_DB_AVAILABLE:
            try:
                # Check if DB exists
                if os.path.exists(self.db_path):
                    self.vector_client = chromadb.PersistentClient(path=self.db_path)
                    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
                    self.collection = self.vector_client.get_collection(name="health_conditions", embedding_function=ef)
                    print("Debug: Vector DB loaded successfully.")
            except Exception as e:
                # print(f"Debug: Vector DB init failed: {e}")
                pass

    def _init_ml_model(self):
        if ML_MODEL_AVAILABLE:
            try:
                if os.path.exists(self.model_path):
                    self.ml_model = joblib.load(self.model_path)
                    print("Debug: ML Model loaded successfully.")
            except Exception as e:
                # print(f"Debug: ML Model init failed: {e}")
                pass

    def diagnose(self, user_symptoms):
        """
        Matches user symptoms to known conditions using:
        1. Vector DB (Semantic Search) - BEST
        2. ML Model (Probabilistic Classification)
        3. Rule-based (Keyword Matching) - FALLBACK
        """
        user_symptoms_str = " ".join(user_symptoms)
        
        # 1. Try Vector DB
        if self.collection:
            try:
                results = self.collection.query(
                    query_texts=[user_symptoms_str],
                    n_results=1
                )
                
                if results["metadatas"] and results["metadatas"][0]:
                    # Format result to match expected output
                    best_match = results["metadatas"][0][0]
                    # Distance is a dissimilarity score (lower is better)
                    distance = results["distances"][0][0]
                    
                    # Threshold for valid match (heuristic)
                    if distance < 1.5: 
                         # We need to parse remedies back from string if we stored it as JSON string
                        import json # make sure json is available
                        remedies = best_match["remedies"]
                        if isinstance(remedies, str):
                            try:
                                remedies = json.loads(remedies)
                            except:
                                remedies = []

                        return [{
                            "name": best_match["name"],
                            "severity": best_match["severity"],
                            "remedies": remedies,
                            "source": "Vector AI"
                        }]
            except Exception as e:
                print(f"Vector search error: {e}")

        # 2. Try ML Model
        if self.ml_model:
            try:
                prediction_name = self.ml_model.predict([user_symptoms_str])[0]
                # Find details for predicted name
                for cond in self.conditions:
                    if cond["name"] == prediction_name:
                        return [{
                            "name": cond["name"],
                            "severity": cond.get("severity", "unknown"),
                            "remedies": cond.get("remedies", []),
                            "source": "ML Model"
                        }]
            except Exception as e:
                print(f"ML prediction error: {e}")

        # 3. Fallback to Rule-Based
        return self._diagnose_rule_based(user_symptoms)

    def _diagnose_rule_based(self, user_symptoms):
        potential_conditions = []
        user_symptoms_lower = [s.lower().strip() for s in user_symptoms]

        for condition in self.conditions:
            match_count = 0
            condition_symptoms = [s.lower() for s in condition.get("symptoms", [])]
            
            for user_symptom in user_symptoms_lower:
                for cond_symptom in condition_symptoms:
                    if cond_symptom in user_symptom or user_symptom in cond_symptom:
                         match_count += 1
                         break 
            
            if match_count > 0:
                potential_conditions.append({
                    "name": condition["name"],
                    "match_count": match_count,
                    "remedies": condition.get("remedies", []),
                    "severity": condition.get("severity", "unknown"),
                    "source": "Rule-Based"
                })
        
        potential_conditions.sort(key=lambda x: x["match_count"], reverse=True)
        return potential_conditions

