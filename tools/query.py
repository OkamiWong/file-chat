import langchain
import langchain.agents
import langchain.callbacks
import langchain.chains
import langchain.embeddings
import langchain.vectorstores

import libraries.vector_store


def get_tool() -> langchain.agents.Tool:
    return langchain.agents.Tool(
        name="QA system about the files",
        description="Useful when you need to answer questions according to or related to the files. Input should be a fully formed question.",
        func=run
    )


def run(query: str) -> str:
    store = libraries.vector_store.get_vector_store()

    chain = langchain.chains.VectorDBQA.from_chain_type(
        llm=langchain.OpenAI(temperature=0),
        chain_type="stuff",
        vectorstore=store
    )

    answer = chain.run(query)

    return answer
