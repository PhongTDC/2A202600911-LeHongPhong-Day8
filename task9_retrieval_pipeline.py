from src.task5_semantic_search import semantic_search
from src.task6_lexical_search import lexical_search
from src.task7_reranking import rerank
from src.task8_pageindex_vectorless import pageindex_search

def retrieve(query: str, top_k: int = 5, score_threshold: float = 0.3) -> list[dict]:
    dense_results = semantic_search(query, top_k=10)
    lexical_results = lexical_search(query, top_k=10)
    
    max_lexical = max([x['score'] for x in lexical_results]) if lexical_results else 1
    for r in lexical_results:
        r['score'] = r['score'] / (max_lexical if max_lexical > 0 else 1)
        
    combined = dense_results + lexical_results
    final_results = rerank(query, combined, top_k=top_k)
    
    if not final_results or final_results[0]['score'] < score_threshold:
        print("⚠️ Hybrid search score dưới ngưỡng threshold! Đang kích hoạt Fallback...")
        final_results = pageindex_search(query, top_k=top_k)
    return final_results
