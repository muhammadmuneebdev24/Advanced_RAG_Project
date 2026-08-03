from langchain_community.vectorstores import FAISS


def create_vector_db(chunks, embeddings):

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    vector_store.save_local(
        "faiss_index"
    )

    return vector_store



def load_vector_db(embeddings):

    db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db
    

