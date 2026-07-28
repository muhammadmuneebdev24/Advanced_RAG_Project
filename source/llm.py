from langchain_groq import ChatGroq
from source.retreiver import get_retriever
from dotenv import load_dotenv
from source.reranker import rerank_chunks
from source.filtering import filter_reranked_chunks
import os


load_dotenv()
retriever = get_retriever()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def get_answer(question: str):

    documents = retriever.invoke(question)
    print(f"Retrieved {len(documents)} chunks")
    
    ranked_results = rerank_chunks(question, documents)
    filtered_results = filter_reranked_chunks(ranked_results)
    print([(doc.metadata.get("heading"),doc.metadata.get("page"), score) for doc, score in ranked_results[:5]])


    if not filtered_results:
      return {
        "answer": "I couldn't find this information in the provided document.",
        "sources": []
    }

    documents = [doc for doc, score in filtered_results]

    sources = []

    for doc in documents:
     sources.append({
        "heading": doc.metadata.get("heading", "Untitled"),
        "source": doc.metadata.get("source"),
        "page": doc.metadata.get("page"),
        "total_pages": doc.metadata.get("total_pages")
    })

    context = "\n\n".join(
    f"## {doc.metadata.get('heading', 'Untitled')}\n{doc.page_content}"
    for doc in documents
    )
   


    prompt = f"""
You are an expert document question-answering assistant.

Answer ONLY using the provided context.

Rules:
1. Answer only the user's question.
2. Do not summarize the entire section.
3. Extract only the requested information.
4. If the answer is a specification, return only that specification.
5. Do not use outside knowledge.
6. If the information is missing, reply exactly:
"I couldn't find this information in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    print([(doc.metadata.get("heading"), score) for doc, score in ranked_results[:5]])

    return{
        "answer": response.content,
        "sources": sources     
    }
