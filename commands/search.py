"""
Semantically search for files
"""
from typing import NoReturn

import constants
import libraries.vector_store
import utilities


def run(args) -> NoReturn:
    keyword: str = args.keyword

    print(f"Loading the vector store")
    store = libraries.vector_store.get_vector_store()
    print(f"Successfully loaded the vector store")

    print(f"Searching for files related to \"{keyword}\"")
    results = store.similarity_search_with_score(
        keyword, constants.SEARCH_TOP_K)
    visited = set()
    print(f"Results in the descending order of similarity:")
    for result in filter(
        lambda result: result[1] < constants.SEARCH_SIMILARITY_THRESHOLD,
        results
    ):
        source = result[0].metadata[constants.METADATA_PROPERTY_SOURCE]
        if source not in visited:
            visited.add(source)
            print(source)
    print(
        f"Total tokens used for embedding: {utilities.count_tokens_for_embedding(keyword)}"
    )
