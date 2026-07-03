import os
import chromadb
from rank_bm25 import BM25Okapi

chroma_client = chromadb.PersistentClient(path="data/chroma_db")

def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    try:
        collection = chroma_client.get_collection(name="drug_law_collection")
        all_docs = collection.get()
    except Exception:
        return []

    documents = all_docs.get('documents', [])
    metadatas = all_docs.get('metadatas', [])
    if not documents:
        return []
        
    tokenized_corpus = [doc.lower().split() for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    
    results = []
    for idx, score in enumerate(scores):
        results.append({
            'content': documents[idx],
            'score': float(score),
            'metadata': metadatas[idx] if metadatas else {}
        })
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]
