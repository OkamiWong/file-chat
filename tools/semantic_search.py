import langchain
import langchain.agents
import langchain.callbacks
import langchain.chains
import langchain.embeddings
import langchain.vectorstores

import constants
import libraries.vector_store


def get_tool() -> langchain.agents.Tool:
    return langchain.agents.Tool(
        name="Search for files related to a topic",
        description="Useful when you need to find files related to a topic. Input should be the topic.",
        func=run
    )


def run(keyword: str) -> str:
    store = libraries.vector_store.get_vector_store()
    results = store.similarity_search_with_score(
        keyword, constants.SEARCH_TOP_K)
    visited = set()

    answer = f"Files related to {keyword} (ordered by similarity in descending order):\n"
    for i, result in enumerate(
            filter(
                lambda result: result[1] < constants.SEARCH_SIMILARITY_THRESHOLD,
                results
            )):
        source = result[0].metadata[constants.METADATA_PROPERTY_SOURCE]
        if source not in visited:
            visited.add(source)
            answer += f"{source}\n"
    return answer
