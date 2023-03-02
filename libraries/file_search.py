import thefuzz.process
import langchain.docstore.document
import langchain.docstore.in_memory
from typing import Optional

import constants
import libraries.vector_store

def search_file(file_path: str) -> Optional[str]:
    paths = libraries.vector_store.get_absolute_file_paths()
    file_search_result = thefuzz.process.extractOne(
        query=file_path,
        choices=paths,
        score_cutoff=10
    )

    if file_search_result is None:
        return None

    return file_search_result[0]


def get_documents(file_path: str) -> tuple[Optional[str], list[langchain.docstore.document.Document]]:
    actual_file_path = search_file(file_path)
    if actual_file_path is None:
        return (None, [])

    store = libraries.vector_store.get_vector_store()
    docstore: langchain.docstore.in_memory.InMemoryDocstore = store.docstore
    docs = docstore._dict.values()

    return (actual_file_path, list(filter(
        lambda doc: doc.metadata[constants.METADATA_PROPERTY_SOURCE] == actual_file_path,
        docs
    )))
