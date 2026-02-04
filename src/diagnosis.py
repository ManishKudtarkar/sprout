import json
import os
import sys

# Disable ChromaDB Telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_ANONYMIZED_TELEMETRY"] = "False"

# Try imports for advanced features, handle failure gracefully
try:
    import chromadb
    from chromadb.utils import embedding_functions
    from chromadb.config import Settings
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
                    self.vector_client = chromadb.PersistentClient(path=self.db_path, settings=Settings(anonymized_telemetry=False))
                    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
                    self.collection = self.vector_client.get_collection(name="health_conditions", embedding_function=ef)
                    print("Debug: Vector DB loaded successfully.")
            except Exception as e:
                print(f"Debug: Vector DB init failed: {e}")
                # pass

    def _init_ml_model(self):
        if ML_MODEL_AVAILABLE:
            try:
                if os.path.exists(self.model_path):
                    self.ml_model = joblib.load(self.model_path)
                    print("Debug: ML Model loaded successfully.")
            except Exception as e:
                # print(f"Debug: ML Model init failed: {e}")
                pass

    def diagnose(self, user_symptoms, user_profile=None):
        """
        Production-Grade Diagnosis Pipeline:
        1. Contextual Vector Search (Filter by Metadata if possible)
        2. Semantic Similarity Re-ranking
        3. Business Logic / Safety Layer
        """
        user_symptoms_str = " ".join(user_symptoms)
        
        # 1. Advanced Vector Search
        if self.collection:
            try:
                # Query more results to allow for re-ranking/filtering
                results = self.collection.query(
                    query_texts=[user_symptoms_str],
                    n_results=5 
                )
                
                if results['metadatas'] and results['metadatas'][0]:
                    candidates = []
                    for i, meta in enumerate(results['metadatas'][0]):
                        dist = results['distances'][0][i]
                        
                        # Parse complex fields
                        import json
                        try:
                            remedies = json.loads(meta.get('remedies', '[]'))
                        except:
                            remedies = []
                            
                        candidate = {
                            "name": meta['name'],
                            "severity": meta['severity'],
                            "remedies": remedies,
                            "source": "Vector AI",
                            "score": 1 - dist # Convert distance to similarity score
                        }
                        candidates.append(candidate)
                    
                    # Rerank / Filter candidates based on profile (Faang-style logic)
                    best_match = self._rerank_candidates(candidates, user_profile)
                    if best_match:
                        return [best_match]

            except Exception as e:
                print(f"Vector search error: {e}")

        # 2. Try ML Model (Fall back if Vector fails)
        if self.ml_model:
            try:
                prediction_name = self.ml_model.predict([user_symptoms_str])[0]
                for cond in self.conditions:
                    if cond["name"] == prediction_name:
                        return [{
                            "name": cond["name"],
                            "severity": cond.get("severity", "unknown"),
                            "remedies": cond.get("remedies", []),
                            "source": "ML Model"
                        }]
            except Exception as e:
                pass

        # 3. Fallback
        return self._diagnose_rule_based(user_symptoms)

    def _rerank_candidates(self, candidates, profile):
        """
        Reranks potential diagnoses based on specific rules or profile data.
        """
        if not candidates:
            return None
            
        # For now, just return the highest score, but this is where
        # you would add logic like "If age < 10, de-prioritize 'Adult Onset Diabetes'"
        # or specific confidence thresholds.
        
        # Filter out low confidence
        high_conf = [c for c in candidates if c['score'] > 0.2] # Adjust threshold
        
        if not high_conf:
            return None
            
        return max(high_conf, key=lambda x: x['score'])


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

