import xml.etree.ElementTree as ET
import requests
import fitz  # PyMuPDF
import os

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
