import xml.etree.ElementTree as ET
import requests
import arxiv
import fitz  # PyMuPDF
import os


def search_by_library(title):
    client = arxiv.Client()
    # Perform an exact title search
    search = arxiv.Search(
        query=f"ti:\"{title}\"",
        max_results=1
    )
    try:
        # Get the first result found
        article = next(client.results(search))
        print(f"Article found: {article.title}")

        # Extract metadata
        metadata = {
            "title": article.title,
            "authors": article.authors,
            "year": article.published.year,
            "summary": article.summary,
            "id": article.entry_id,
            "url": article.pdf_url
        }
        return metadata
    except StopIteration:
        print("Article not found.")
        return None



def download_by_library(article_id, filename="downloaded_article.pdf", directory="./"):
    # Remove o prefixo "http://arxiv.org/abs/" do ID, se presente
    if "http" in article_id:
        article_id = article_id.split("/")[-1]
    
    if article_id:
        # Define a busca pelo ID do artigo
        search = arxiv.Search(id_list=[article_id])
        try:
            article = next(arxiv.Client().results(search), None)
        except:
            article = None
        
        if article is None:
            print("Article not found.")
            return None
        
        # Define o caminho completo para o arquivo PDF
        pdf_path = os.path.join(directory, filename)
        
        # Baixa o PDF
        try:
            article.download_pdf(dirpath=directory, filename=filename)
            print(f"Article downloaded as '{filename}' in directory '{directory}'.")
        except:
            print("Error downloading the article.")
            return None
        # Extrai o texto do PDF
        with fitz.open(pdf_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()

        # Remove o PDF após a extração
        os.remove(pdf_path)
        print("PDF removed after text extraction.")
        return text
    else:
        print("No article ID provided.")
        return None






def arxivref(title, max_results=1):
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=ti:\"{title}\"&max_results={max_results}"
    try:
        response = requests.get(base_url + query)
    except:
        print("Error in the request.")
        return None
    
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
        if len(results) == 0:
            print("arXiv: Nenhum artigo encontrado.")
            return None
        return results[0]
    else:
        print(f"arXiv: Erro na requisição: {response.status_code}")
        return None

def download_pdf(pdf_url, filename="paper.pdf"):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"arXiv: PDF baixado com sucesso: {filename}")
        return filename
    else:
        print(f"arXiv: Erro ao baixar o PDF: {response.status_code}")
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
        print("arXiv: Artigo não encontrado.")
        return None
    
    article = articles  # Assume que o primeiro resultado é o correto
    
    # Passo 1: Obtenha o abstract via metadados
    paper_data = {
        "abstract": article["summary"]
    }
    
    # Passo 2: Obtenha o texto completo do paper via PDF
    pdf_url = article["pdf_url"]
    pdf_path = download_pdf(pdf_url, "downloaded_paper.pdf")
    if pdf_path:
        paper_data["full_text"] = extract_text_from_pdf(pdf_path)
        
        # Remove o PDF após a extração do texto
        os.remove(pdf_path)
        print(f"arXiv: PDF removido: {pdf_path}")
    
    return paper_data





if __name__ == "__main__":
    title = "Very deep convolutional networks for large-scale image recognition"
    paper_content = get_paper_content(title)
    if paper_content:
        print("Abstract:", paper_content["abstract"])
        print("Texto completo (primeiros 1000 caracteres):", paper_content["full_text"][:1000])

        print("Fim do programa")

