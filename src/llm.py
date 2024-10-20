# Função para chamar a API do GPT passando o prompt e o contexto extraído do PDF
import openai
import os

def call_gpt(prompt, context):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Fazer a chamada para a API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Retornar a resposta gerada
    return completion.choices[0].message.content