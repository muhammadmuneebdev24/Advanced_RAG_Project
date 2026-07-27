from langchain_groq import ChatGroq
from source.retreiver import retrieve_chunks
from dotenv import load_dotenv
from source.chunk_filter import filter_chunks
import os


load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def get_answer(question: str):

    results = retrieve_chunks(question)
 #   print(results)

    documents = filter_chunks(results)
    print("After Filtering:", len(documents))

    sources = []

    for doc in documents:
     sources.append({
        "title": doc.metadata.get("chunk_title"),
        "source": doc.metadata.get("source"),
        "page": doc.metadata.get("page"),
        "total_pages": doc.metadata.get("total_pages")
    })


    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )


    prompt = f"""
You are an intelligent and accurate PDF Question Answering Assistant.

Your task is to answer the user's question using ONLY the information provided in the context below.

Instructions:
1. Read the context carefully before answering.
2. Do NOT use your own knowledge or make assumptions.
3. If the answer is not clearly present in the context, reply exactly:
   "The requested information is not available in the provided document."
4. If multiple pieces of context are relevant, combine them into a single clear answer.
5. Keep the answer concise, accurate, and well-structured.

Context:
{context}

Question:
{question}

Answer:
"""


    response = llm.invoke(prompt)


    return{
        "answer": response.content,
        "sources": sources     
    }
