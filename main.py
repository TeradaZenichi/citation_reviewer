import src.evaluation.evaluation as evaluation
import src.sentences.get_dataset as dataset_sentences
import src.sentences.dataset as sentences
import src.sentences.get_llm as llm_sentences
from src.evaluation import calculate
from src.apis import check
import pandas as pd
import json

# Função para calcular estatísticas
def calculate_statistics(df, column_name):
    try:
        column = df[column_name].dropna()  # Remove valores None/NaN para os cálculos
        mean_val = column.mean()
        median_val = column.median()
        std_dev = column.std()
        non_none_percentage = (len(column) / len(df)) * 100  # Percentual de elementos não None
        
        return {
            "mean": mean_val,
            "median": median_val,
            "std_dev": std_dev,
            "non_none_percentage": non_none_percentage
        }
    except:
        return {
            "mean": None,
            "median": None,
            "std_dev": None,
            "non_none_percentage": None
        }

filename = "dataset/combined_papers.json"

analisys = {}

#read data in dataset\combined_papers.json
with open(filename, "r", encoding="utf-8") as f:
    papers = json.load(f)


for n, paper in enumerate(papers):
    print(f"Paper {n + 1} of {len(papers)}")
    statistics = {}
    text = paper["metadata"]["sections"]           # Texto completo do paper que vamos analisar
    references = paper["metadata"]["references"]   # dicionário de referências do paper
    refefences, report = check.fill(references)
    references = dataset_sentences.extract(paper["metadata"]["referenceMentions"], references)
    results = calculate.fill(references, report)

    #save references in a json file
    with open(f"Results/{paper['name']}_references.json", "w", encoding="utf-8") as f:
        json.dump(references, f, indent=4)

    #convert results dict to DataFrame trasposed
    final_df = pd.DataFrame(results).T
    final_df.to_csv(f"Results/{paper['name']}.csv")

    # Calcula estatísticas para cada coluna relevante
    columns_to_analyze = ['faithfulness', 'precision', 'recall', 'semantic_similarity']
    statistics = {col: calculate_statistics(final_df, col) for col in columns_to_analyze}
    for col in columns_to_analyze:
        try:
            statistics[col]["non_none_percentage"] = statistics[col]["non_none_percentage"]
        except:
            statistics[col]["non_none_percentage"] = None
    statistics["status"] = paper["status"]
    analisys[paper["name"]] = statistics

    # Salva as estatísticas em um arquivo JSON
    with open(f"Results/statistics_{paper['name']}.json", "w", encoding="utf-8") as f:
        json.dump(statistics, f, indent=4)

    # save analisys in a json file
    with open(f"Results/analisys.json", "w", encoding="utf-8") as f:
        json.dump(analisys, f, indent=4)


print("end of program")