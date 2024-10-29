import xml.etree.ElementTree as ET
import urllib.parse
import http.client
import requests
import fitz  # PyMuPDF
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


def opencitation(doi):
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




def arxiv(title, max_results=1):
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=ti:\"{title}\"&max_results={max_results}"
    response = requests.get(base_url + query)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        results = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            article = {
                "title": entry.find('{http://www.w3.org/2005/Atom}title').text,
                "summary": entry.find('{http://www.w3.org/2005/Atom}summary').text,
                "authors": [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                "published": entry.find('{http://www.w3.org/2005/Atom}published').text,
                "pdf_url": entry.find('{http://www.w3.org/2005/Atom}link[@title="pdf"]').attrib['href']
            }
            results.append(article)
        return results
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

def download_pdf(pdf_url, filename="paper.pdf"):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"PDF baixado com sucesso: {filename}")
        return filename
    else:
        print(f"Erro ao baixar o PDF: {response.status_code}")
        return None

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()
    return text

# Função principal para obter o abstract e o texto completo
def get_paper_content(title):
    articles = arxiv(title)
    if not articles:
        print("Artigo não encontrado.")
        return None
    
    article = articles[0]  # Assume que o primeiro resultado é o correto
    
    # Passo 1: Obtenha o abstract via metadados
    paper_data = {
        "abstract": article["summary"]
    }
    
    # Passo 2: Obtenha o texto completo do paper via PDF
    pdf_url = article["pdf_url"]
    pdf_path = download_pdf(pdf_url, "downloaded_paper.pdf")
    if pdf_path:
        paper_data["full_text"] = extract_text_from_pdf(pdf_path)
    
    return paper_data

# Exemplo de uso
title = "Supervised Feature Selection via Dependence Estimation"
paper_content = get_paper_content(title)
if paper_content:
    print("Abstract:", paper_content["abstract"])
    print("Texto completo (primeiros 1000 caracteres):", paper_content["full_text"][:1000])












def semantic_scholar(title):
    pass


def pubmed(title):
    pass

def fetch_pubmed_details(paper_id):
   pass


def google_scholar():
    pass

def microsoft_academic():
    pass

def dblp(title):
    pass


def springer(title, api_key):
    pass


def acm():
    pass

def ieee(title, api_key):
    pass

def elsevier():
    pass

def iet():
    pass

def mdpi():
    pass


def get_citations(doi):
    pass



