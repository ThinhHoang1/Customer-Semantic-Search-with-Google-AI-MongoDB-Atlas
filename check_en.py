import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access your variables using os.getenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# --- Add checks to ensure they loaded ---
if not all([MONGO_URI, DB_NAME, COLLECTION_NAME, GOOGLE_API_KEY, EMBEDDING_MODEL]):
    print("🔴 Error: One or more environment variables are missing. Check your .env file.")
    # In a Streamlit app, you might use st.error() and st.stop()
    exit() # Or handle the error appropriately

# Now you can use these variables in the rest of your script
# e.g., client = pymongo.MongoClient(MONGO_URI)
# e.g., genai.configure(api_key=GOOGLE_API_KEY)
print("✅ Environment variables loaded successfully.")
print(f"   Using DB: {DB_NAME}, Collection: {COLLECTION_NAME}, Model: {EMBEDDING_MODEL}")