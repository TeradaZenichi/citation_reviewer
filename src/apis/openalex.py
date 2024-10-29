import requests

def openalex(title, max_results=1):
    base_url = "https://api.openalex.org/works"
    params = {
        "filter": f"title.search:{title}",  # Pesquisa pelo título
        "per_page": max_results
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()["results"]  # Retorna a lista de artigos encontrados
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None


