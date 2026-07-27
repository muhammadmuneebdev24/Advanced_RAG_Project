def filter_chunks(results, margin=0.15,threshold = 1.7):
    """
    Filters retrieved chunks using the best-score + margin approach.

    Parameters:
        results : List of (Document, score) tuples returned by
                  similarity_search_with_score().
        margin  : How far from the best score a chunk can be and still be kept.

    Returns:
        List of Document objects.
    """

    if not results:
        return []

    results = sorted(results, key=lambda x: x[1])

    best_score = results[0][1]

    print(f"Best Score: {best_score}")

    if best_score > threshold:
     return []

    filtered_documents = []

    for doc, score in results:

        print(score)

        if score <= best_score + margin:
            filtered_documents.append(doc)


    return filtered_documents