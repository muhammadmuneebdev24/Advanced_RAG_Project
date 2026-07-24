from langchain_community.vectorstores import FAISS
from source.embeddings import get_embeddings


def retrieve_chunks(question):

    embeddings = get_embeddings()

    vector_db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    results = vector_db.similarity_search_with_score(
    query=question,
    k=4
    )

    return results
