import requests
import fitz  # PyMuPDF
import os

# Função para buscar metadados de um artigo no CORE usando o título
def search_by_core(title, max_results=1):
    api_key = os.getenv("CORE_API_KEY")  # Obtém a chave da API do ambiente
    if not api_key:
        print("Erro: A variável de ambiente 'CORE_API_KEY' não está definida.")
        return None

    url = f"https://api.core.ac.uk/v3/search/works"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "q": title,
        "fulltext": True,
        "page": 1,
        "pageSize": max_results
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            article = data["results"][0]
            metadata = {
                "title": article.get("title"),
                "authors": article.get("authors"),
                "year": article.get("datePublished", "").split("-")[0],
                "abstract": article.get("abstract"),
                "doi": article.get("doi"),
                "pdf_url": article.get("downloadUrl")
            }
            print(f"Artigo encontrado: {metadata['title']}")
            return metadata
        else:
            print("Nenhum artigo encontrado com esse título.")
            return None
    except requests.RequestException as e:
        print(f"Erro ao acessar a CORE API: {e}")
        return None

# Função para baixar o PDF do artigo
def download_pdf(pdf_url, filename="downloaded_article.pdf"):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"PDF baixado com sucesso: {filename}")
        return filename
    except requests.RequestException as e:
        print(f"Erro ao baixar o PDF: {e}")
        return None

# Função para extrair o texto do PDF usando PyMuPDF
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

# Função principal para obter o abstract e o texto completo do artigo
def get_paper_content(title):
    article = search_by_core(title)
    if not article:
        print("CORE: Artigo não encontrado.")
        return None
    
    paper_data = {
        "title": article["title"],
        "abstract": article["abstract"],
        "doi": article["doi"]
    }
    
    pdf_url = article.get("pdf_url")
    if pdf_url:
        pdf_path = download_pdf(pdf_url, "downloaded_paper.pdf")
        if pdf_path:
            paper_data["full_text"] = extract_text_from_pdf(pdf_path)
            os.remove(pdf_path)
            print(f"CORE: PDF removido após extração do texto: {pdf_path}")
        else:
            print("CORE: PDF não disponível para este artigo.")
    else:
        print("CORE: URL do PDF não disponível.")
    
    return paper_data


# Exemplo de uso
if __name__ == "__main__":
    title = "EV Charging Simulator for Public Infrastructure Considering Smart Charging and Price Policies"  # Substitua pelo título do artigo
    paper_content = get_paper_content(title)
    if paper_content:
        print("Abstract:", paper_content["abstract"])
        print("DOI:", paper_content["doi"])
        print("Texto completo (primeiros 1000 caracteres):", paper_content["full_text"][:1000])
        a = 1