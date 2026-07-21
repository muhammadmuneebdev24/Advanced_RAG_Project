from langchain_google_genai import ChatGoogleGenerativeAI
from source.retreiver import get_retriever
from dotenv import load_dotenv
import os


load_dotenv()


def get_answer(question: str):

    # Get FAISS retriever
    retriever = get_retriever()


    # Retrieve relevant documents
    documents = retriever.invoke(question)


    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )


    # Gemini API model
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
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


    return response.content[0]["text"]