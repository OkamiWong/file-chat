"""
Ask one question to retrieve a factural information.
"""
import langchain
import langchain.callbacks
import langchain.chains
import langchain.embeddings
import langchain.vectorstores
from typing import NoReturn

import libraries.vector_store


def run(args) -> NoReturn:
    question: str = args.query

    print(f"Loading the vector store")
    store = libraries.vector_store.get_vector_store()
    print(f"Successfully loaded the vector store")

    chain = langchain.chains.VectorDBQAWithSourcesChain.from_llm(
        llm=langchain.OpenAI(temperature=0),
        vectorstore=store
    )

    with langchain.callbacks.get_openai_callback() as openai_callback:
        print(f"Question: {question}\n")
        result = chain({"question": question})
        print(f"Answer: {result['answer'].rstrip()}\n")
        print(f"Sources: {result['sources'].rstrip()}\n")
        print(
            f"Total tokens used for querying: {openai_callback.total_tokens}")
