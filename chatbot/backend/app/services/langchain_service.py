import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

def get_vectorstore():
    persist_path = os.getenv("CHROMA_PERSIST_PATH", "./chroma_db")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    if not os.path.exists(persist_path) or not os.listdir(persist_path):
        print("Chroma DB is empty. Populating with sample documents...")
        sample_texts = [
            "Bob is 12 years old.",
            "Alice is 25 and works as a teacher."
        ]
        documents = [Document(page_content=txt, metadata={}) for txt in sample_texts]
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_path
        )
        vectorstore.persist()
    else:
        vectorstore = Chroma(persist_directory=persist_path, embedding_function=embeddings)
    return vectorstore

def create_rag_chain():
    llm = ChatOpenAI(
        temperature=0.3,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    retriever = get_vectorstore().as_retriever()

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question which might reference context in the chat history, "
        "formulate a standalone question which can be understood without the chat history. "
        "Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_system_prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\n\n{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(
        history_aware_retriever,
        question_answer_chain,
    )
    return rag_chain

# you can persist chat history per session/user if desired; for demo, we use a simple list.
chat_history = []

def get_answer(question: str) -> str:
    try:
        rag_chain = create_rag_chain()
        response = rag_chain.invoke({"input": question, "chat_history": chat_history})
        # Optionally update chat_history here if you want to keep history across turns
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": response.get("answer", "")})
        return response.get("answer", "Sorry, I couldn't generate a response.")
    except Exception as e:
        print(f"Error while getting answer: {e}")
        return f"Error: {str(e)}"
