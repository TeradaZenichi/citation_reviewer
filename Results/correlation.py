import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho para o arquivo JSON
file_path = 'Results/analisys.json'

# Carrega o arquivo JSON
with open(file_path, 'r') as f:
    data = json.load(f)

# Lista para armazenar os dados
data_rows = []

# Loop através de cada documento no JSON
for doc_id, metrics in data.items():
    row = {}
    
    # Extrai a média de cada métrica, substituindo valores ausentes por NaN
    row['faith'] = metrics['faithfulness']['mean'] if metrics['faithfulness']['mean'] is not None else np.nan
    row['prec'] = metrics['precision']['mean'] if metrics['precision']['mean'] is not None else np.nan
    row['rec'] = metrics['recall']['mean'] if metrics['recall']['mean'] is not None else np.nan
    row['sem_sim'] = metrics['semantic_similarity']['mean'] if metrics['semantic_similarity']['mean'] is not None else np.nan
    row['pdf_faith'] = metrics['pdf-faithfulness']['mean'] if metrics['pdf-faithfulness']['mean'] is not None else np.nan
    row['pdf_prec'] = metrics['pdf-precision']['mean'] if metrics['pdf-precision']['mean'] is not None else np.nan
    row['pdf_rec'] = metrics['pdf-recall']['mean'] if metrics['pdf-recall']['mean'] is not None else np.nan
    row['pdf_sem_sim'] = metrics['pdf-semantic_similarity']['mean'] if metrics['pdf-semantic_similarity']['mean'] is not None else np.nan

    # Converte o status para 1 para "accepted" e 0 para "rejected"
    row['status'] = 1 if metrics['status'] == "accepted" else 0

    # Adiciona a linha na lista de dados
    data_rows.append(row)

# Converte a lista de dados para um DataFrame
df = pd.DataFrame(data_rows)

# Calcula a matriz de correlação
correlation_matrix = df.corr()

# Plotando a matriz de correlação
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='viridis', vmin=-1, vmax=1, cbar=True)
plt.title("Matriz de Correlação das Métricas e Status")
plt.tight_layout()  # Ajusta o layout para uma visualização mais compacta
plt.savefig('Results/correlation_matrix.pdf')
