from sentence_transformers import CrossEncoder


# Load reranker model once
reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


def rerank_chunks(question, documents):
    """
    Reranks retrieved documents according to their
    relevance to the user's question.

    Parameters:
        question: User's question.
        documents: List of LangChain Document objects.

    Returns:
        List of (Document, reranker_score) tuples,
        sorted from most relevant to least relevant.
    """

    if not documents:
        return []

    # Create question + document pairs
    pairs = [
        [question, doc.page_content]
        for doc in documents
    ]

    # Get reranker scores
    scores = reranker_model.predict(pairs)

    # Combine document + score
    ranked_results = list(zip(documents, scores))

    # Sort highest score first
    ranked_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_results