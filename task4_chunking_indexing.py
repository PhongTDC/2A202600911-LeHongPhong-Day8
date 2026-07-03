import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

EMBED_FN = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-m3"
)

chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_or_create_collection(
    name="drug_law_collection", 
    embedding_function=EMBED_FN
)

def chunk_and_index():
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    standardized_dirs = ["data/standardized/legal", "data/standardized/news"]
    
    doc_id_counter = 0
    for s_dir in standardized_dirs:
        if not os.path.exists(s_dir):
            continue
        for file_name in os.listdir(s_dir):
            if not file_name.endswith(".md"):
                continue
            file_path = os.path.join(s_dir, file_name)
            
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                
            chunks = text_splitter.split_text(text)
            documents, metadatas, ids = [], [], []
            
            for chunk in chunks:
                documents.append(chunk)
                metadatas.append({"source": file_name, "category": s_dir.split("/")[-1]})
                ids.append(f"id_{doc_id_counter}")
                doc_id_counter += 1
                
            if documents:
                collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"✓ Indexed {doc_id_counter} chunks into Vector Store successfully.")

if __name__ == "__main__":
    chunk_and_index()
