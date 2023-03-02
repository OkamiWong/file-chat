"""
A conversation agent with the ability to:
1. Semantically search for files
2. Read file content
"""
import langchain
import langchain.agents
import langchain.callbacks
import langchain.chains.conversation.memory
from typing import Any, NoReturn

import prompts.agent
import tools.query
import tools.semantic_search
import tools.summarize


def get_tools() -> list[langchain.agents.Tool]:
    return [
        tools.semantic_search.get_tool(),
        tools.query.get_tool(),
        tools.summarize.get_tool()
    ]


def run(*args: Any) -> NoReturn:
    memory = langchain.chains.conversation.memory.ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=3
    )
    llm = langchain.OpenAI(temperature=0.1)
    tools = get_tools()
    agent = langchain.agents.initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        verbose=True,
        memory=memory,
        agent_kwargs={"prefix": prompts.agent.PREFIX}
    )

    with langchain.callbacks.get_openai_callback() as openai_callback:
        try:
            print(f"AI: Hi, I am your assistant to help you understand your files.")
            print(
                f"    FYI, you can say \"restart\" to clear my memory or say \"bye\" to end the conversaion.")
            print(f"    How can I help you?")
            while True:
                human_input = input("Human: ")
                if human_input.lower() == "restart":
                    memory.clear()
                    print(f"AI: Succssfully cleared my memory.")
                    continue
                elif human_input.lower() == "bye":
                    break
                agent.run(input=human_input)
        finally:
            print("AI: Have a nice day.")
            print(
                f"Total tokens used for chatting: {openai_callback.total_tokens}")
