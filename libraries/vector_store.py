import langchain.vectorstores
import langchain.docstore.in_memory
from typing import NoReturn, Optional

import constants

_vector_store: Optional[langchain.vectorstores.FAISS] = None
_absolute_file_paths: Optional[list[str]] = None


def _load_vertex_store() -> NoReturn:
    global _vector_store
    _vector_store = langchain.vectorstores.FAISS.load_local(
        constants.STORE_FOLDER,
        langchain.embeddings.OpenAIEmbeddings()
    )


def get_vector_store() -> langchain.vectorstores.FAISS:
    if _vector_store is None:
        _load_vertex_store()
    return _vector_store


def _load_absolute_file_paths() -> NoReturn:
    global _absolute_file_paths
    store = get_vector_store()
    docstore: langchain.docstore.in_memory.InMemoryDocstore = store.docstore
    _absolute_file_paths = list(set(
        [doc.metadata[constants.METADATA_PROPERTY_SOURCE] for doc in docstore._dict.values()]))


def get_absolute_file_paths() -> list[str]:
    if _absolute_file_paths is None:
        _load_absolute_file_paths()
    return _absolute_file_paths
