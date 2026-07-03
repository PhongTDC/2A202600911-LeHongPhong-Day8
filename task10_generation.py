import os
from openai import OpenAI
from dotenv import load_dotenv
from src.task9_retrieval_pipeline import retrieve

load_dotenv()

def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    sorted_chunks = sorted(chunks, key=lambda x: x['score'], reverse=True)
    reordered = [None] * len(sorted_chunks)
    left, right = 0, len(sorted_chunks) - 1
    for i, chunk in enumerate(sorted_chunks):
        if i % 2 == 0:
            reordered[left] = chunk
            left += 1
        else:
            reordered[right] = chunk
            right -= 1
    return reordered

SYSTEM_PROMPT = """Answer the following question comprehensively.
For every statement of fact or claim, immediately insert a citation
in brackets linking to the specific source..."""

def generate_with_citation(query: str, context_chunks: list[dict]) -> str:
    if not context_chunks:
        return "I cannot verify this information"
    ordered_chunks = reorder_for_llm(context_chunks)
    context_str = ""
    for idx, chunk in enumerate(ordered_chunks):
        source = chunk['metadata'].get('source', 'Unknown Source')
        context_str += f"--- Document {idx+1} (Source: {source}) ---\n{chunk['content']}\n\n"
        
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"}
            ],
            temperature=0.0,
            top_p=1.0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
