"""
Summarize the content of a file
"""
import langchain
import langchain.callbacks
import langchain.chains.summarize
import langchain.embeddings
import langchain.vectorstores
from typing import NoReturn

import libraries.file_search

def run(args) -> NoReturn:
    file_path: str = args.file_path

    (actual_file_path, docs) = libraries.file_search.get_documents(file_path)
    if actual_file_path is None:
        print(f"File with path {file_path} is not found among indexed files.")
        return

    llm = langchain.OpenAI(temperature=0)
    chain = langchain.chains.summarize.load_summarize_chain(
        llm,
        chain_type="map_reduce"
    )

    with langchain.callbacks.get_openai_callback() as openai_callback:
        print(f"Summarizing {actual_file_path}\n")
        summary = chain.run(docs)
        print(f"Summary: {summary.rstrip()}\n")
        print(f"Total tokens used for summarization: {openai_callback.total_tokens}")
