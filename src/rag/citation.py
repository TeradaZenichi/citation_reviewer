# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
import faiss
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def batch_process_embeddings(texts, batch_size=64):
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=batch
        )
        all_embeddings.extend([item.embedding for item in response.data])
    return all_embeddings


def get_text_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    embedding = response.data[0].embedding
    return embedding


def paper_segmentation(pdf_text: str):

    text_splitter = RecursiveCharacterTextSplitter(
        # Default list of seperators
        separators=["\n\n", "\n", " ", ""],
        chunk_size=256,
        chunk_overlap=32,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(pdf_text)

    embed = batch_process_embeddings(chunks, batch_size=64)

    # Convert listo to numpy array
    embed = np.array(embed)

    # Create a faiss index
    index = faiss.IndexFlatIP(embed.shape[1])
    index.add(embed)

    return chunks, index


def retrieve_chunk(sentence, chunks, index, k=1):
    sentence_embedding = get_text_embedding(sentence)
    sentence_embedding = np.array([sentence_embedding])
    # Search for the most similar chunks
    _, idx = index.search(sentence_embedding, k)
    similar_chunks = [chunks[i] for i in idx[0]]

    return similar_chunks
