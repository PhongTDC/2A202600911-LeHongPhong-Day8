import os
from dotenv import load_dotenv

load_dotenv()

def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    api_key = os.getenv("PAGEINDEX_API_KEY")
    if not api_key:
        return [{
            'content': "Kết quả dự phòng từ hệ thống PageIndex Vectorless cho truy vấn dữ liệu.",
            'score': 0.5,
            'metadata': {'source': 'pageindex_fallback'}
        }]
    return []
