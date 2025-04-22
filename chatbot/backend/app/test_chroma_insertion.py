from chromadb import Client

def test_chroma_insertion():
    client = Client()
    collection_name = "my_collection"  # Use the actual collection name
    collection = client.get_collection(collection_name)

    # Try fetching a sample record
    data = collection.get_documents({"query": "Alice Johnson"})
    print("Fetched Data:", data)  # Should show Alice's details if inserted correctly

    # Run a query to check if data retrieval works
    query_result = collection.query(query_text="Alice Johnson", n_results=5)
    print("Query Result:", query_result)

if __name__ == "__main__":
    test_chroma_insertion()
