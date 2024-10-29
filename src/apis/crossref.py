import urllib.parse
import http.client
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
