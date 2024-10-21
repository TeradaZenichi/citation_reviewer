import urllib.parse
import http.client
import requests
import json

def crossref(title):
    # Preparar o URL da API do CrossRef e os parâmetros da consulta
    url_base = "/works"
    query_params = urllib.parse.urlencode({'query.title': title, 'rows': 1})

    # Conectar-se à API do CrossRef
    connection = http.client.HTTPSConnection("api.crossref.org")
    
    try:
        # Fazer a requisição GET
        connection.request("GET", f"{url_base}?{query_params}")
        response = connection.getresponse()

        # Verificar se a requisição foi bem sucedida
        if response.status == 200:
            # Ler e converter a resposta JSON
            data = json.loads(response.read().decode())

            # Verificar se há resultados
            if data['message']['items']:
                # Extrair o primeiro resultado relevante
                paper_metadata = data['message']['items'][0]

                # Organizar as informações extraídas
                metadata = {
                    'title': paper_metadata.get('title', [''])[0],
                    'authors': [author.get('given', '') + ' ' + author.get('family', '') for author in paper_metadata.get('author', [])],
                    'doi': paper_metadata.get('DOI', 'N/A'),
                    'publisher': paper_metadata.get('publisher', 'N/A'),
                    'published_date': paper_metadata.get('created', {}).get('date-time', 'N/A'),
                    'abstract': paper_metadata.get('abstract', 'Abstract não disponível')  # Capturar o abstract
                }

                # Remover tags HTML do abstract, se houver
                if 'abstract' in metadata:
                    metadata['abstract'] = remove_html_tags(metadata['abstract'])
                
                return metadata
            else:
                return {"error": "Nenhum resultado encontrado para o título fornecido."}
        else:
            return {"error": f"Erro na requisição. Código de status: {response.status}"}
    except Exception as e:
        return {"error": f"Ocorreu um erro: {str(e)}"}
    finally:
        connection.close()

def extract_metadata(paper_metadata, source):
    # Organizar as informações extraídas
    metadata = {
        'title': paper_metadata.get('title', 'Título não disponível'),
        'authors': [author.get('given', '') + ' ' + author.get('family', '') for author in paper_metadata.get('author', [])] if 'author' in paper_metadata else [],
        'doi': paper_metadata.get('DOI', 'N/A'),
        'publisher': paper_metadata.get('publisher', 'N/A'),
        'published_date': paper_metadata.get('created', {}).get('date-time', 'N/A'),
        'abstract': paper_metadata.get('abstract', 'Abstract não disponível'),
        'source': source
    }

    # Remover tags HTML do abstract, se houver
    if 'abstract' in metadata:
        metadata['abstract'] = remove_html_tags(metadata['abstract'])
    
    return metadata

def remove_html_tags(text):
    import re
    # Remover tags HTML com expressões regulares
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)



def semantic_scholar(title):
    import requests
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}&fields=title,authors,abstract,year,doi,publisher"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            paper_metadata = data['data'][0]
            return extract_metadata(paper_metadata, "Semantic Scholar")
    return {"error": "Nenhum resultado encontrado ou erro na requisição."}


def semantic_scholar(title):
    import requests
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}&fields=title,authors,abstract,year,doi,publisher"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            paper_metadata = data['data'][0]
            return extract_metadata(paper_metadata, "Semantic Scholar")
    return {"error": "Nenhum resultado encontrado ou erro na requisição."}


def arxiv(title):
    import requests
    from xml.etree import ElementTree as ET
    
    url = "http://export.arxiv.org/api/query"
    params = {'search_query': f"ti:{title}", 'start': 0, 'max_results': 1}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            paper_metadata = {
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                'abstract': entry.find('{http://www.w3.org/2005/Atom}summary').text,
                'doi': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                'published_date': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'publisher': "arXiv"
            }
            return extract_metadata(paper_metadata, "arXiv")
    return {"error": "Nenhum resultado encontrado ou erro na requisição."}


def pubmed(title):
    import requests
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': title,
        'retmode': 'json',
        'retmax': 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['esearchresult']['idlist']:
            paper_id = data['esearchresult']['idlist'][0]
            return fetch_pubmed_details(paper_id)
    return {"error": "Nenhum resultado encontrado ou erro na requisição."}

def fetch_pubmed_details(paper_id):
    import requests
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        'db': 'pubmed',
        'id': paper_id,
        'retmode': 'json'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        paper_metadata = response.json()['result'][paper_id]
        return extract_metadata(paper_metadata, "PubMed")
    return {"error": "Nenhum resultado encontrado."}


def google_scholar():
    pass

def microsoft_academic():
    pass

def dblp(title):
    import requests
    url = f"https://dblp.org/search/publ/api?q={title}&format=json"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['result']['hits']['hit']:
            paper_metadata = data['result']['hits']['hit'][0]['info']
            return extract_metadata(paper_metadata, "DBLP")
    return {"error": "Nenhum resultado encontrado ou erro na requisição."}


def springer(title, api_key):
    import requests
    url = "http://api.springernature.com/meta/v2/json"
    params = {'q': title, 'api_key': api_key}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['records']:
            paper_metadata = data['records'][0]
            return extract_metadata(paper_metadata, "Springer")
    return {"error": "Nenhum resultado encontrado ou erro na requisição."}


def acm():
    pass

def ieee(title, api_key):
    import requests
    url = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    params = {'apikey': api_key, 'querytext': title}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['articles']:
            paper_metadata = data['articles'][0]
            return extract_metadata(paper_metadata, "IEEE Xplore")
    return {"error": "Nenhum resultado encontrado ou erro na requisição."}

def elsevier():
    pass

def iet():
    pass

def mdpi():
    pass


def get_citations(doi):
    """
    Busca as citações recebidas por um artigo com base no DOI usando a OpenCitations API.
    """
    url = f"https://opencitations.net/index/coci/api/v1/citations/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        citations = response.json()
        if citations:
            print(f"Encontradas {len(citations)} citações para o DOI {doi}:")
            for citation in citations:
                print(f"- DOI da citação: {citation['citing']} | Data da citação: {citation['creation']}")
        else:
            print(f"Nenhuma citação encontrada para o DOI {doi}.")
    else:
        print(f"Erro: não foi possível buscar as citações para o DOI {doi}. Status: {response.status_code}")

def get_article_metadata(doi):
    """
    Busca os metadados de um artigo com base no DOI usando a OpenCitations API.
    """
    url = f"https://opencitations.net/index/coci/api/v1/metadata/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        metadata = response.json()
        if metadata:
            article = metadata[0]  # OpenCitations retorna uma lista, normalmente com um item
            print(f"\nMetadados do artigo para o DOI {doi}:")
            print(f"Título: {article.get('title', 'Título não disponível')}")
            print(f"Autores: {', '.join(article.get('author', ['Autores não disponíveis']))}")
            print(f"Data de publicação: {article.get('issued', 'Data não disponível')}")
            print(f"Editor: {article.get('publisher', 'Editor não disponível')}")
        else:
            print(f"Nenhum metadado encontrado para o DOI {doi}.")
    else:
        print(f"Erro: não foi possível buscar os metadados para o DOI {doi}. Status: {response.status_code}")

if __name__ == "__main__":
    # Exemplo de uso
    doi = "10.1038/s41586-020-2649-2"  # DOI de exemplo
    
    # Buscar citações recebidas pelo artigo
    get_citations(doi)
    
    # Buscar os metadados do artigo
    get_article_metadata(doi)



if __name__ == "__main__":
    # Exemplo de uso
    titulo_paper = "The Influence of ChatGPT on Student Learning and Academic Performance"
    metadados = crossref(titulo_paper)

    # Exibir os metadados
    print(metadados)


