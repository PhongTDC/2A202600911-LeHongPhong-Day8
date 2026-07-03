def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c['content'] not in seen:
            seen.add(c['content'])
            unique_candidates.append(c)
    unique_candidates.sort(key=lambda x: x['score'], reverse=True)
    return unique_candidates[:top_k]
