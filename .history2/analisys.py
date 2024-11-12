import json
import pandas as pd
import os
import matplotlib.pyplot as plt

# Defina o número de artigos aceitos e rejeitados a serem selecionados
N = 15  # Modifique este valor conforme necessário

# Carregar o arquivo JSON do caminho especificado
with open('Results/analysis.json') as f:
    data = json.load(f)

# Converter dados JSON para um DataFrame
rows = []
for article, metrics in data.items():
    row = {'article': article, 'status': metrics.get('status')}
    for metric, values in metrics.items():
        if metric != 'status':
            for stat, value in values.items():
                row[f"{metric}_{stat}"] = value
    rows.append(row)

df = pd.DataFrame(rows)

# Remover linhas onde qualquer métrica é null
df.dropna(subset=[col for col in df.columns if any(m in col for m in ["faithfulness", "precision", "recall", "semantic_similarity"])], inplace=True)

# Balancear a amostra selecionando N artigos aceitos e N rejeitados
accepted = df[df['status'] == 'accepted'].sample(N, random_state=42)
rejected = df[df['status'] == 'rejected'].sample(N, random_state=42)
balanced_sample = pd.concat([accepted, rejected], ignore_index=True)

# Converter status para 0 e 1 (0 = rejeitado, 1 = aceito)
balanced_sample['status'] = balanced_sample['status'].map({'rejected': 0, 'accepted': 1})

# Converter colunas para numérico, ignorando colunas de texto
balanced_sample = balanced_sample.apply(pd.to_numeric, errors='ignore')

# Criar o diretório se não existir
output_dir = 'Results/correlation/'
os.makedirs(output_dir, exist_ok=True)

# Análise 1: Calcular médias das métricas para artigos aceitos vs. rejeitados e salvar
mean_metrics_by_status = balanced_sample.groupby('status').mean(numeric_only=True)
mean_metrics_by_status.to_csv(f'{output_dir}mean_metrics_by_status.csv')
print("Mean Metrics by Status (Balanced Sample):")
print(mean_metrics_by_status)

# Gráfico de barras para médias das métricas
mean_metrics_by_status.T.plot(kind='bar', figsize=(10, 6))
plt.title("Mean Metrics by Status (Balanced Sample)")
plt.ylabel("Mean Value")
plt.xlabel("Metrics")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_dir}mean_metrics_by_status.pdf')
plt.show()

# Análise 2: Matriz de correlação entre métricas e salvar
correlation_matrix = balanced_sample.corr(numeric_only=True)
correlation_matrix.to_csv(f'{output_dir}correlation_matrix.csv')
print("\nMetric Correlation Matrix (Balanced Sample):")
print(correlation_matrix)

# Heatmap para matriz de correlação, incluindo status como 0 e 1
plt.figure(figsize=(10, 8))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
plt.colorbar()
plt.title("Correlation Matrix Heatmap (Balanced Sample) with Status")
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45, ha="right")
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.tight_layout()
plt.savefig(f'{output_dir}correlation_matrix_heatmap.pdf')
plt.show()

# Análise 3: Distribuição de média e desvio padrão para cada métrica e salvar
metric_columns = [col for col in balanced_sample.columns if any(m in col for m in ["faithfulness", "precision", "recall", "semantic_similarity"])]
metric_distribution = balanced_sample[metric_columns].describe()
metric_distribution.to_csv(f'{output_dir}metric_distribution.csv')
print("\nMetric Distribution (Balanced Sample):")
print(metric_distribution)

# Boxplot para distribuição das métricas
balanced_sample[metric_columns].boxplot(figsize=(12, 6), rot=45)
plt.title("Metric Distribution (Balanced Sample)")
plt.ylabel("Value")
plt.savefig(f'{output_dir}metric_distribution_boxplot.pdf')
plt.show()

# Análise 4: Distribuição de `non_none_percentage` para aplicabilidade das métricas e salvar
non_none_columns = [col for col in metric_columns if "non_none_percentage" in col]
non_none_distribution = balanced_sample[non_none_columns].describe()
non_none_distribution.to_csv(f'{output_dir}non_none_percentage_distribution.csv')
print("\nNon-None Percentage Distribution (Balanced Sample):")
print(non_none_distribution)

# Gráfico de barras para non-none percentage
non_none_distribution.loc['mean'].plot(kind='bar', figsize=(10, 6))
plt.title("Average Non-None Percentage for Metrics (Balanced Sample)")
plt.ylabel("Percentage")
plt.xlabel("Metrics")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_dir}non_none_percentage_distribution.pdf')
plt.show()

# Nova Análise: Correlação entre mean, median, non_none_percentage e status para cada métrica
filtered_columns = [col for col in balanced_sample.columns if any(x in col for x in ["_mean", "_median", "non_none_percentage"])]
filtered_columns.append('status')  # Adicionar status

filtered_correlation_matrix = balanced_sample[filtered_columns].corr()

# Salvar a nova matriz de correlação
filtered_correlation_matrix.to_csv(f'{output_dir}filtered_correlation_matrix.csv')

# Exibir e salvar o heatmap da nova matriz de correlação
plt.figure(figsize=(10, 8))
plt.imshow(filtered_correlation_matrix, cmap='coolwarm', interpolation='nearest')
plt.colorbar()
plt.title("Correlation Matrix for Mean, Median, Non-None Percentage, and Status")
plt.xticks(range(len(filtered_correlation_matrix.columns)), filtered_correlation_matrix.columns, rotation=45, ha="right")
plt.yticks(range(len(filtered_correlation_matrix.columns)), filtered_correlation_matrix.columns)
plt.tight_layout()
plt.savefig(f'{output_dir}filtered_correlation_matrix_heatmap.pdf')
plt.show()
