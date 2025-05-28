# 🧑‍💼 Customer Semantic Search with Google AI & MongoDB Atlas 🚀

This project demonstrates a powerful semantic search application built using Google's Generative AI (Embedding & Gemini models) and MongoDB Atlas Vector Search. It provides a simple web interface, built with Streamlit, to search through a customer database using natural language queries.


Here's a quick look at the application interface:

![Application Demo Placeholder](https://github.com/ThinhHoang1/Customer-Semantic-Search-with-Google-AI-MongoDB-Atlas/blob/main/segmentic%20search%20demo.png)

## ✨ Key Features

* **Semantic Search:** Find customers based on the *meaning* of your query, not just keywords.
* **Google AI Integration:** Utilizes Google's state-of-the-art models for generating text embeddings.
* **MongoDB Atlas Vector Search:** Leverages MongoDB's efficient and scalable vector search capabilities for fast retrieval.
* **Interactive Web UI:** Uses Streamlit to provide an easy-to-use interface for searching.
* **Configuration Management:** Uses `.env` files for easy and secure management of credentials and settings.
* **(Optional) Gemini Summarization:** Can be extended to use Gemini for summarizing search results.

## 🛠️ Technology Stack

* **Database:** MongoDB Atlas (with Vector Search)
* **AI / Embeddings:** Google Generative AI (e.g., `text-embedding-004`)
* **Web Framework:** Streamlit
* **Programming Language:** Python
* **Key Libraries:** `pymongo`, `google-generativeai`, `streamlit`, `pandas`, `python-dotenv`

## ⚙️ Architecture Overview

1.  **Data Ingestion & Embedding:** A script (`generate_embeddings.py`) reads customer data from MongoDB, creates descriptive text, generates vector embeddings using Google AI, and stores them back in MongoDB.
2.  **Vector Indexing:** MongoDB Atlas creates and maintains a Vector Search index on the generated embeddings.
3.  **User Query:** The user enters a natural language query via the Streamlit interface (`app.py`).
4.  **Query Embedding:** The query text is converted into a vector using the same Google AI model.
5.  **Vector Search:** The query vector is sent to MongoDB Atlas, which performs a `$vectorSearch` to find the most similar customer profiles.
6.  **Display Results:** The Streamlit app displays the retrieved customer data.

## 🚀 Setup and Installation

### Prerequisites

* Python 3.8 or higher.
* A MongoDB Atlas account with a cluster set up (M0 free tier works).
* A Google AI API Key (obtainable from [Google AI Studio](https://aistudio.google.com/)).
* Git (for cloning).

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd customer-semantic-search
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up MongoDB Atlas:**
    * Create a database and a collection in your Atlas cluster.
    * Load your customer data into the collection.
    * Ensure "Network Access" in Atlas is configured to allow connections from your IP address (or `0.0.0.0/0` for testing, **use with caution**).
    * Go to your collection, click the "Search" tab, and create an "Atlas Vector Search" index. Use the JSON editor and configure it similar to this (adjust `numDimensions` and `path` if needed):
        ```json
        {
          "fields": [
            {
              "type": "vector",
              "path": "embedding_vector", // Must match the field you store embeddings in
              "numDimensions": 768,      // 768 for 'text-embedding-004'
              "similarity": "cosine"
            }
            // Add other filter fields if desired
          ]
        }
        ```
    * **Note down the exact name you give this index.**

5.  **Configure Environment Variables:**
    * Rename `.env.example` to `.env`.
    * Open the `.env` file and fill in your actual values for:
        * `MONGO_URI`
        * `DB_NAME`
        * `COLLECTION_NAME`
        * `GOOGLE_API_KEY`
        * `EMBEDDING_MODEL` (usually `models/text-embedding-004`)
        * `VECTOR_SEARCH_INDEX` (the name you gave your Atlas index)

## 🏃 Running the Application

1.  **Generate Embeddings (Run this first, and only once unless data changes):**
    * Ensure your customer data is already in MongoDB (without the `embedding_vector` field).
    * Run the script:
        ```bash
        python generate_embeddings.py
        ```
    * Verify in MongoDB Atlas that your documents now have an `embedding_vector` field populated.

2.  **Run the Streamlit Web App:**
    ```bash
    streamlit run app.py
    ```
    * This will open the application in your web browser.

## 🧑‍💻 Usage

1.  Open the web application in your browser.
2.  Type a description of the customers you are looking for into the search box (e.g., "elderly doctors living alone", "young professionals with high income", "artists with low spending habits").
3.  Click the "Search" button.
4.  The application will display the top matching customer profiles based on semantic similarity.

## 🔒 Security Note

* **Never commit your `.env` file to your Git repository.** The `.gitignore` file included should prevent this, but always be careful.
* Manage your API keys and database credentials securely.

---
