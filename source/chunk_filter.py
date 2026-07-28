def filter_chunks(question, documents):
    """
    Filters retrieved documents before sending them to the LLM.

    Currently returns all documents.
    """

    return documents