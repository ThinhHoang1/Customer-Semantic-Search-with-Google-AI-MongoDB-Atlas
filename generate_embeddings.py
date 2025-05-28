import pymongo
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() # This line loads variables from your .env file

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004") # Default if not set
VECTOR_SEARCH_INDEX = os.getenv("VECTOR_SEARCH_INDEX", "embedding_vector") # Default if not set
GEMINI_MODEL = "gemini-2.0-flash"
genai.configure(api_key=GOOGLE_API_KEY)
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# --- Function to create text representation ---
def create_customer_text(doc):
    # Combine relevant fields into a descriptive string
    return (f"Customer Profile: Gender is {doc.get('Gender', 'N/A')}, "
            f"Age is {doc.get('Age', 'N/A')}. "
            f"Annual income is ${doc.get('Annual Income ($)', 0)}. "
            f"Spending score is {doc.get('Spending Score (1-100)', 0)}. "
            f"Profession: {doc.get('Profession', 'N/A')}. "
            f"Work experience: {doc.get('Work Experience', 0)} years. "
            f"Family size: {doc.get('Family Size', 0)}.")

# --- Process and Update Documents ---
count = 0
for doc in collection.find({"embedding_vector": {"$exists": False}}): # Process only those without an embedding
    try:
        text_to_embed = create_customer_text(doc)
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text_to_embed,
            task_type="RETRIEVAL_DOCUMENT" # Important for retrieval tasks
        )
        embedding_vector = result['embedding']

        # Update the document in MongoDB
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding_vector": embedding_vector}}
        )
        count += 1
        print(f"Processed document {count}: {doc['_id']}")

    except Exception as e:
        print(f"Error processing document {doc['_id']}: {e}")

print(f"\nFinished processing. Added embeddings to {count} documents.")
client.close()