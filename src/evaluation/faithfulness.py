# faithfulness.py

from openai import OpenAI
import os
import re

# Inicializa o cliente OpenAI com a chave da API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_chatgpt_4o(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def calculate_faithfulness(reference, response):
    prompt = (
        f"Consider the following context: {reference}. "
        f"Rate the faithfulness of this response to the context: {response}. "
        "Provide a score between 0 (not faithful) and 1 (completely faithful) as a numeric value only."
    )
    faithfulness_score_text = call_chatgpt_4o(prompt)
    
    # Usar regex para capturar o primeiro número entre 0 e 1 na resposta
    match = re.search(r"\b0(?:\.\d+)?|1\b", faithfulness_score_text)
    if match:
        score = float(match.group())
    else:
        score = 0.0  # Valor padrão caso a resposta não contenha um número válido

    return score

if __name__ == "__main__":
    reference_text = "Zeus is known as the god of the sky and thunder."
    response_text = "Abstract não disponível"
    faithfulness = calculate_faithfulness(reference_text, response_text)
    print("Faithfulness Score:", faithfulness)