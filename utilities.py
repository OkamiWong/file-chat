import langchain.vectorstores
import tiktoken

import constants


def count_tokens_for_embedding(string: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def count_tokens_for_text_completion(string: str) -> int:
    encoding = tiktoken.get_encoding("p50k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens
