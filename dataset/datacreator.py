import os
import json
import random

# Definindo o diretório principal e as subpastas
train_dir = "dataset/PeerRead/data/arxiv.cs.lg_2007-2017/train"
pdf_dir = os.path.join(train_dir, "parsed_pdfs")
review_dir = os.path.join(train_dir, "reviews")

# Listas para armazenar os dados
accepted_papers = []
rejected_papers = []

# Itera sobre os arquivos JSON em `parsed_pdfs`
for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith(".pdf.json"):
        # Carrega o conteúdo completo do JSON do paper
        with open(os.path.join(pdf_dir, pdf_file), 'r', encoding='utf-8') as f:
            paper_info = json.load(f)
        
        # Extrai o ID do paper
        paper_id = paper_info['name'].replace('.pdf', '')

        # Tenta encontrar o arquivo de revisão correspondente
        review_file_path = os.path.join(review_dir, f"{paper_id}.json")
        if os.path.exists(review_file_path):
            with open(review_file_path, 'r', encoding='utf-8') as f:
                review_data = json.load(f)
            
            # Verifica o status de aceitação e adiciona no dicionário de informações do paper
            if review_data.get("accepted", False):
                paper_info["status"] = "accepted"
                accepted_papers.append(paper_info)
            else:
                paper_info["status"] = "rejected"
                rejected_papers.append(paper_info)

# Define a semente para reprodutibilidade
random.seed(42)

# Seleciona uma quantidade aleatória de amostras de cada categoria
accepted_samples = random.sample(accepted_papers, random.randint(1, len(accepted_papers)))
rejected_samples = random.sample(rejected_papers, random.randint(1, len(rejected_papers)))

# Cria um dataset combinado com ambas as categorias e embaralha
combined_samples = accepted_samples + rejected_samples
random.shuffle(combined_samples)

# Define o diretório de destino para salvar os arquivos JSON
output_dir = "dataset"
os.makedirs(output_dir, exist_ok=True)

# Salva os datasets em arquivos JSON
with open(os.path.join(output_dir, "accepted_papers.json"), "w", encoding='utf-8') as f:
    json.dump(accepted_samples, f, ensure_ascii=False, indent=4)

with open(os.path.join(output_dir, "rejected_papers.json"), "w", encoding='utf-8', errors="backslashreplace") as f:
    json.dump(rejected_samples, f, ensure_ascii=False, indent=4)

with open(os.path.join(output_dir, "combined_papers.json"), "w", encoding='utf-8', errors="backslashreplace") as f:
    json.dump(combined_samples, f, ensure_ascii=False, indent=4)

print("Arquivos gerados com sucesso em 'dataset': 'accepted_papers.json', 'rejected_papers.json' e 'combined_papers.json'")
