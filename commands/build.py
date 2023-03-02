"""
Parse files and build index.
"""
import langchain.embeddings
import langchain.text_splitter
import langchain.vectorstores
from typing import NoReturn
from pathlib import Path
from functools import reduce

import constants
import utilities


def run(arg: any) -> NoReturn:
    folder_path: str = arg.folder_path
    print(f"Building the vector store for folder {folder_path}")

    file_paths = list(Path(folder_path).glob("**/*.md"))

    if len(file_paths) == 0:
        raise Exception(f"No file found in {folder_path}")

    print(f"Found {len(file_paths)} files")

    files: list[str] = []
    for file_path in file_paths:
        with open(file_path, encoding="utf-8") as file:
            files.append(file.read())

    text_splitter = langchain.text_splitter.MarkdownTextSplitter()

    texts = []
    metadatas = []
    for i, file in enumerate(files):
        splits = text_splitter.split_text(file)
        texts.extend(splits)
        metadatas.extend(
            [{constants.METADATA_PROPERTY_SOURCE: file_paths[i].absolute()}] * len(splits))

    print(f"Total chunks after splitting the input files: {len(texts)}")

    total_tokens_for_embedding = reduce(
        lambda count, text: count + utilities.count_tokens_for_embedding(text),
        texts,
        0
    )
    print(f"Total tokens used for embedding: {total_tokens_for_embedding}")

    store = langchain.vectorstores.FAISS.from_texts(
        texts, langchain.embeddings.OpenAIEmbeddings(), metadatas
    )
    store.save_local(constants.STORE_FOLDER)

    print("Successfully built the vector store")
