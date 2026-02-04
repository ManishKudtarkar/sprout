import json
import os
# Disable ChromaDB Telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_ANONYMIZED_TELEMETRY"] = "False"
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'symptoms.json')
REMEDIES_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'remedies.json')
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'chroma_db')

def ingest_data():
    print("Loading data...")
    conditions = []
    
    # 1. Load Original Dataset
    try:
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
            raw_conditions = data.get("disease_symptoms", {})
            
            # Load Validation/Remedy Map if available to cross-reference
            remedy_map = {}
            try:
                with open(REMEDIES_PATH, 'r') as rf:
                    rdata = json.load(rf)
                    remedy_map = rdata.get("disease_remedies", {})
                    additional = rdata.get("additional_conditions", [])
            except FileNotFoundError:
                additional = []

            # Process Original Diseases
            if raw_conditions:
                 for name, symptoms in raw_conditions.items():
                     # Fix name keys being capitalized or not matching perfectly
                     name_clean = name.lower().strip()
                     remedies = remedy_map.get(name_clean, ["Consult a doctor"])
                     
                     conditions.append({
                         "name": name, 
                         "symptoms": symptoms,
                         "remedies": remedies,
                         "severity": "Unknown"
                     })
            
            # 2. Add Additional Conditions (Nose Bleed, etc.)
            for item in additional:
                conditions.append(item)
                
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_PATH}")
        return
        print(f"Error: Data file not found at {DATA_PATH}")
        return

    print(f"Initializing ChromaDB at {DB_PATH}...")
    client = chromadb.PersistentClient(path=DB_PATH, settings=Settings(anonymized_telemetry=False))
    
    # Use a standard embedding model
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Create or get collection
    collection_name = "health_conditions"
    try:
        client.delete_collection(name=collection_name) # Clear existing for fresh ingest
        print(f"Deleted existing collection '{collection_name}'")
    except ValueError:
        pass
        
    collection = client.create_collection(
        name=collection_name, 
        embedding_function=sentence_transformer_ef
    )

    documents = []
    metadatas = []
    ids = []

    print(f"Processing {len(conditions)} conditions...")
    for idx, condition in enumerate(conditions):
        # We want to match based on symptoms, but retrieve the condition info.
        # So the 'document' we embed is the list of symptoms joined together.
        symptoms_text = ", ".join(condition["symptoms"])
        
        # Store full details in metadata so we don't need to look up JSON again
        meta = {
            "name": condition["name"],
            "remedies": json.dumps(condition["remedies"]), # Check if simple list stores ok, safer to stringify for some DBs
            "severity": condition["severity"],
            "symptoms_list": symptoms_text
        }
        
        documents.append(symptoms_text)
        metadatas.append(meta)
        ids.append(f"condition_{idx}")

    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Success! Data ingested into Vector DB.")
    else:
        print("No data found to ingest.")

if __name__ == "__main__":
    ingest_data()
