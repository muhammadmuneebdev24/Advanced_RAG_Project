from typing import List, Tuple
import statistics


LOW_CONFIDENCE_THRESHOLD = -7.0


def filter_reranked_chunks(
    ranked_results: List[Tuple],
    max_chunks: int = 5,
):
    """
    Filters reranked chunks using dynamic score-gap detection.

    Parameters:
        ranked_results:
            List of (Document, score) tuples sorted in
            descending order of score.

        max_chunks:
            Maximum number of chunks to return.

    Returns:
        Filtered list of (Document, score) tuples.
    """

    if not ranked_results:
        return []

    # Confidence check
    best_score = ranked_results[0][1]

    if best_score < LOW_CONFIDENCE_THRESHOLD:
        return []

    # Only one chunk
    if len(ranked_results) == 1:
        return ranked_results

    # Compute score gaps
    gaps = []

    for i in range(len(ranked_results) - 1):
        gap = ranked_results[i][1] - ranked_results[i + 1][1]
        gaps.append(gap)

    # Dynamic threshold
    mean_gap = statistics.mean(gaps)

    if len(gaps) > 1:
        std_gap = statistics.stdev(gaps)
    else:
        std_gap = 0.0

    threshold = mean_gap + std_gap

    # Find first significant gap
    split_index = None

    for i, gap in enumerate(gaps):
        if gap > threshold:
            split_index = i + 1
            break

    # Filter chunks
    if split_index is not None:
        filtered = ranked_results[:split_index]
    else:
        filtered = ranked_results

    return filtered[:max_chunks]