from langchain_groq import ChatGroq
from source.retreiver import get_retriever
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

    documents = retriever.invoke(question)
    print(len(documents))
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
You are a helpful assistant.
Answer the question only using the provided context.

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
