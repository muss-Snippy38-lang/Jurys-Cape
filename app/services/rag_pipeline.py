from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Setup local embeddings (This turns text into numbers)
embeddings = OllamaEmbeddings(model="llama3.2:1b")

# 2. Setup Vector Store (This stores the numbers locally in a folder)
# It will create a folder called 'vector_db' in your project
vector_db = Chroma(persist_directory="./data/vector_db", embedding_function=embeddings)

def add_documents_to_db(text: str):        
    """Splits text and adds it to the local vector database."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.create_documents([text])
    vector_db.add_documents(chunks)
    return "Successfully indexed document."

def search_legal_precedents(query: str):
    """Searches the database for the most relevant law/precedent."""
    results = vector_db.similarity_search(query, k=2)
    return [res.page_content for res in results]