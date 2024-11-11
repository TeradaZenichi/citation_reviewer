# semantic_similarity.py

from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import os

# Inicialize o cliente da OpenAI com a chave de API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_text_embedding(text):
    # Gera embeddings usando `client.embeddings.create`
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
        encoding_format="float"
    )
    # Extrair o embedding do primeiro item na resposta
    embedding = response.data[0].embedding
    return embedding

def calculate_semantic_similarity(reference, response):
    # Gera embeddings para ambos os textos
    ref_embedding = get_text_embedding(reference)
    res_embedding = get_text_embedding(response)
    # Calcula a similaridade de cosseno entre os embeddings
    similarity = cosine_similarity([ref_embedding], [res_embedding])[0][0]
    return similarity

if __name__ == "__main__":
    reference_text = "Zeus is known as the god of the sky and thunder."
    response_text = "Zeus is the ruler of Mount Olympus and god of the sky and thunder."
    semantic_similarity = calculate_semantic_similarity(reference_text, response_text)
    print("Semantic Similarity:", semantic_similarity)

