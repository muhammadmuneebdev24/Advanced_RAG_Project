from langchain_groq import ChatGroq
from source.retreiver import get_retriever
from source.reranker import rerank_chunks
from dotenv import load_dotenv
import os

load_dotenv()

retriever = get_retriever()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


def get_answer(question: str):

    # -------------------------
    # Retrieve relevant chunks
    # -------------------------
    documents = retriever.invoke(question)

    # -------------------------
    # Rerank retrieved chunks
    # -------------------------
    ranked_results = rerank_chunks(question, documents)

    # Keep only the top 5 chunks
    documents = [doc for doc, score in ranked_results[:5]]

    # -------------------------
    # Build context
    # -------------------------
    context = "\n\n".join(
        f"## {doc.metadata.get('heading', 'Untitled')}\n{doc.page_content}"
        for doc in documents
    )

    # -------------------------
    # Build unique references
    # -------------------------
    sources = []
    seen = set()

    for doc in documents:

        heading = doc.metadata.get("heading", "Untitled")
        page = doc.metadata.get("page", 0)
      

        key = (heading, page)

        if key not in seen:
            seen.add(key)

            sources.append({
                "heading": heading,
                "page": page
            })

    # -------------------------
    # Prompt
    # -------------------------
    prompt = f"""
You are an expert document question-answering assistant.

Your task is to answer ONLY using the provided context.

Rules:

1. Answer ONLY the user's question.
2. Do NOT summarize the entire section.
3. Extract ONLY the specific information requested.
4. If the question asks for one specification (e.g., Image Sensor, Lens, Weight, Power Supply, Frame Rate),
   return only that specification and nothing else.
5. Do not include related specifications unless the user explicitly asks for them.
6. If multiple values exist, return all of them clearly.
7. If the answer is not present in the context, reply exactly:
   "I couldn't find this information in the provided document."
8. Never use outside knowledge.
9. Never guess.
10. Keep the answer concise and factual.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    # Debug (optional)
    print("\nRetrieved Chunks:")
    print("-" * 60)
    for doc in documents:
        print(doc.metadata)
        
    print([(doc.metadata.get("heading"), score) for doc, score in ranked_results[:5]])
    return {
        "answer": response.content,
        "sources": sources
    }