import requests

def semantic_scholar(title, max_results=1):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "fields": "title,authors,year,abstract,doi",
        "limit": max_results
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()["data"]  # Retorna a lista de artigos encontrados
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None