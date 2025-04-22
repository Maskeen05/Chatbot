# RAG-based QnA Chatbot using FastAPI, LangChain, ChromaDB & OpenAI

This is a **Retrieval-Augmented Generation (RAG)** powered chatbot that enables users to ask natural language questions and receive intelligent responses based on structured data stored in a SQL Server database. It uses **FastAPI** for the backend, **Vue 3 with Quasar** for the frontend, and integrates **Langchain**, **ChromaDB**, and **OpenAI GPT** models for advanced language understanding and generation.

---

## Project Workflow Overview

### 1. Frontend (Vue 3 + Quasar + Axios)
- Built using [Quasar Framework](https://quasar.dev/) and Vue 3.
- Users type their questions in a clean and interactive chat UI.
- Axios sends POST requests to the FastAPI backend with the user's question.

### 2. Backend (FastAPI + LangChain)
- Accepts incoming requests from the frontend.
- Uses LangChain's RAG pipeline to perform similarity search and context enhancement.
- Connects to **ChromaDB** to fetch relevant vector-based data embeddings.
- Communicates with **OpenAI GPT API** to generate answers from relevant content.
- Returns the response back to the frontend.

### 3. ChromaDB (Vector Store)
- Stores embeddings of structured data originally stored in **SQL Server**.
- Performs similarity search using vector similarity (e.g., cosine similarity).
- Returns the most relevant chunks of data related to the user's question.

### 4. SQL Server Management Studio (SSMS)
- Stores the original structured data (e.g., employee records, customer data, etc.).
- Data is extracted and converted into embeddings using a Python script.

### 5. LLM (OpenAI GPT)
- Generates intelligent, human-like answers based on relevant context from ChromaDB.
- Optionally, Langchain Memory can be used to improve response quality through history-aware answers.

---

## Technologies Used

| Layer       | Technology/Tool                           |
|-------------|-------------------------------------------|
| Frontend    | Vue 3, Quasar, Axios                      |
| Backend     | FastAPI, Python, LangChain                |
| Vector DB   | ChromaDB                                  |
| Database    | SQL Server Management Studio (SSMS)       |
| LLM         | OpenAI GPT API                            |

---

## Folder Structure

project-root/
│
├── backend/
│   ├── db_config.py                        # DB connection configuration
│   ├── app/
│   │   ├── main.py                         # FastAPI entrypoint
│   │   ├── chromadb_setup.py              # ChromaDB initialization script
│   │   ├── services/
│   │   │   └── langchain_service.py        # Handles LangChain + Chroma + OpenAI logic
│   │   └── models/
│   │       └── question.py                 # Pydantic model for request
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatBox.vue                 # Main UI chatbox
│   │   ├── views/
│   │   │   └── ChatBox.vue                 # View for chat feature
│   │   └── services/
│   │       └── api.js                      # Axios config
│
├── chroma_db/
│   └── generate_embeddings             # Script to extract SQL data & store in Chroma
│
├── README.md
└── requirements.txt
---

## Installation & Setup

### Backend Setup (FastAPI)
```bash
# Create virtual environment
python -m venv venv
cd backend
source venv/bin/activate 
or 
venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn backend.app.main:app --reload
```

### Required Python Packages
Include in `requirements.txt`:
```txt
fastapi
uvicorn
langchain
langchain-community
google-generativeai
chromadb
pydantic
python-dotenv
sqlalchemy
pyodbc
jinja2
tqdm
httpx
aiofiles
tenacity
langchain-openai
langchain-community
```

### Frontend Setup (Quasar + Vue 3)
```bash
cd frontend
npm install axios
quasar dev
```

## API Endpoint

**POST /get-answer**

### Request:
```json
{
  "question": "What is the age of Bob?"
}
```

### Response:
```json
{
  "answer": "Bob is 25 years old."
}
```

---

## Features

-  Contextual understanding of structured data using RAG.
-  Natural language responses powered by OpenAI GPT.
-  Persistent embeddings with ChromaDB.
-  Seamless integration of Langchain, SQL Server, and LLM.
-  Beautiful frontend using Quasar UI and Vue 3.

---

## Testing the Backend
Test with curl:
```bash
curl -X POST "http://127.0.0.1:8000/get-answer" -H "Content-Type: application/json" -d "{"question":"What is the age of Bob?"}"
```

---

## Future Improvements

-  Add authentication (JWT).
-  Deploy to cloud (e.g., Azure/AWS/GCP).
-  Visual dashboard for query analytics.

---

## Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

---

## Known Issues

```txt
Error: '_type'
```

**Description:** This error commonly occurs after initializing the LLM in the `langchain_service.py` file, specifically during the construction of the `ConversationalRetrievalChain`. It may be due to incorrect memory or retriever type expected by LangChain components. Further debugging of `_type` in the LangChain modules may be needed.

---

## 📄 License

This project is licensed under the MIT License.
