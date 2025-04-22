import os
import sys
import pickle
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma  # MAKE SURE TO CHANGE THIS TO langchain_chroma
from langchain_openai import OpenAIEmbeddings
from db_config import fetch_all_data, update_embeddings_in_db


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def create_chroma_from_sql():
    data = fetch_all_data()
    print("DATA:") # ADD PRINT
    print(data) # ADD PRINT

    docs = []
    print("Raw SQL rows being processed:")
    for idx, row in enumerate(data):
        row_text = " | ".join([f"{key}: {value}" for key, value in row.items() if key != 'Embedding_Vector'])
        print(f"→ Row {idx + 1}: {row_text}")
        docs.append(Document(page_content=row_text))
    print("DOCS:") # ADD PRINT
    print(docs) # ADD PRINT

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(docs)
    print("SPLITS:") # ADD PRINT
    print(splits) # ADD PRINT
    print(f"🔹 Total splits created: {len(splits)}")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing from environment variables.")

    print("OpenAI API key loaded.")

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    contents = [doc.page_content for doc in splits]
    print("CONTENTS:") # ADD PRINT
    print(contents) # ADD PRINT
    embeddings_list = embeddings.embed_documents(contents)

    if not embeddings_list or all(e is None for e in embeddings_list):
        raise ValueError("Generated embeddings are empty. Check embedding model.")
    print(f"{len(embeddings_list)} embeddings generated.")

    update_embeddings_in_db(data, embeddings_list)  # EMBEDDINGS BEING UPDATED TO SQL DB

    persist_path = os.getenv("CHROMA_PERSIST_PATH", "./chroma_db")
    os.makedirs(persist_path, exist_ok=True)

    collection_name = "my_collection"
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_path,
        collection_name=collection_name
    )
    vectorstore.persist()
    print(f"Chroma vectorstore persisted under collection '{collection_name}'")

    return vectorstore
