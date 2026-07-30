from langchain_community.vectorstores import FAISS
from source.embeddings import get_embeddings


def get_retriever():

    embeddings = get_embeddings()

    vector_db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 20 
        }
    )

    return retriever