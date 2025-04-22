import pyodbc
import pickle
def fetch_all_data():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=your_server;"
        "DATABASE=your_db;"
        "Trusted_Connection=yes;"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")  
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]  
    data = [dict(zip(columns, row)) for row in rows]  
    return data


def update_embeddings_in_db(data, embeddings_list):
    
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=your_server;"
        "DATABASE=your_db;"
        "Trusted_Connection=yes;"
    )
    cursor = conn.cursor()

    
    for row, embedding in zip(data, embeddings_list):
        student_id = row['StudentID']
        
        embedding_bytes = pickle.dumps(embedding)

        
        cursor.execute("""
            UPDATE Students
            SET Embedding_Vector = ?
            WHERE StudentID = ?
        """, (embedding_bytes, student_id))
    
    
    conn.commit()
    print(f"Updated {len(embeddings_list)} embeddings in the database.")
    cursor.close()
    conn.close()
