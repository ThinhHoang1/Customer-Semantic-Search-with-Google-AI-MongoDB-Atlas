import streamlit as st
import pymongo
import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv

# --- 1. Load Environment Variables ---
load_dotenv() # This line loads variables from your .env file

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004") # Default if not set
VECTOR_SEARCH_INDEX = os.getenv("VECTOR_SEARCH_INDEX", "embedding_vector") # Default if not set
GEMINI_MODEL = "gemini-2.0-flash"

# --- Initialize ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

embedding_service = genai.GenerativeModel(EMBEDDING_MODEL)
gemini_service = genai.GenerativeModel(GEMINI_MODEL) # Optional


# --- Function to get embedding ---
def get_embedding(text):
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="RETRIEVAL_QUERY" # Use QUERY type for searches
        )
        return result['embedding']
    except Exception as e:
        st.error(f"Embedding Error: {e}")
        return None

# --- Function to perform vector search ---
def vector_search(query_embedding, num_candidates=100, limit=5):
    if query_embedding is None:
        return []
    try:
        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "index": VECTOR_SEARCH_INDEX,
                    "path": "embedding_vector",
                    "queryVector": query_embedding,
                    "numCandidates": num_candidates,
                    "limit": limit
                }
            },
            {
                "$project": { # Project the fields you want to display
                    "score": {"$meta": "vectorSearchScore"},
                    "CustomerID": 1,
                    "Gender": 1,
                    "Age": 1,
                    "Annual Income ($)": 1,
                    "Spending Score (1-100)": 1,
                    "Profession": 1,
                    "Work Experience": 1,
                    "Family Size": 1,
                    "_id": 0 # Exclude the _id if not needed
                }
            }
        ])
        return list(results)
    except Exception as e:
        st.error(f"Vector Search Error: {e}")
        return []

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🧑‍💼 Customer Semantic Search with Gemini & MongoDB Atlas")
st.markdown("Enter a natural language description to find similar customer profiles.")

query_text = st.text_input("Search for customers:", placeholder="e.g., 'Young doctors with high income'")

if st.button("Search"):
    if not query_text:
        st.warning("Please enter a search query.")
    else:
        with st.spinner("Searching for similar customers..."):
            query_vec = get_embedding(query_text)
            if query_vec:
                search_results = vector_search(query_vec)

                if search_results:
                    st.subheader("Top Matching Customer Profiles:")
                    df = pd.DataFrame(search_results)
                    st.dataframe(df, use_container_width=True)

                    # --- Optional: Gemini Summary ---
                    # try:
                    #     prompt = (f"Based on the query '{query_text}', "
                    #               f"summarize these customer profiles:\n\n"
                    #               f"{df.to_string()}\n\n"
                    #               f"What are the key characteristics?")
                    #     response = gemini_service.generate_content(prompt)
                    #     st.subheader("Gemini's Summary:")
                    #     st.markdown(response.text)
                    # except Exception as e:
                    #     st.error(f"Gemini Summary Error: {e}")

                else:
                    st.info("No matching customers found.")

# --- Add instructions or other UI elements as needed ---
st.sidebar.header("About")
st.sidebar.info("This app uses Google AI and MongoDB Atlas Vector Search to find customers based on descriptions.")