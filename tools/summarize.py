import langchain
import langchain.agents
import langchain.callbacks
import langchain.chains
import langchain.embeddings
import langchain.vectorstores

import libraries.file_search
import libraries.vector_store


def get_tool() -> langchain.agents.Tool:
    return langchain.agents.Tool(
        name="Summarize a file by file path or file name",
        description="Useful when you need to summarize a file. Input should be the file's absolute path or name.",
        func=run
    )


def run(file_path: str) -> str:
    (actual_file_path, docs) = libraries.file_search.get_documents(file_path)
    if actual_file_path is None:
        return f"File with path {file_path} is not found among indexed files."

    llm = langchain.OpenAI(temperature=0)
    chain = langchain.chains.summarize.load_summarize_chain(
        llm,
        chain_type="map_reduce"
    )

    summary = chain.run(docs)
    return f"The summary of {actual_file_path} is: {summary}"
