import chromadb
from src.task4_chunking_indexing import EMBED_FN

chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_collection(name="drug_law_collection", embedding_function=EMBED_FN)

def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    results = collection.query(query_texts=[query], n_results=top_k)
    formatted_results = []
    if results and results['documents']:
        for i in range(len(results['documents'][0])):
            distance = results['distances'][0][i] if 'distances' in results else 0
            score = 1 / (1 + distance) 
            formatted_results.append({
                'content': results['documents'][0][i],
                'score': float(score),
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
            })
    return formatted_results
