from src.sentences import extractPDF
from src.evaluation import calculate
from src.apis import check
import pandas as pd
import json

pdf = "journal.pdf"
path_pdf = f"dataset/{pdf}"

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

print(f"Processing {pdf}")
references = extractPDF.extract_references_metadata(path_pdf)
print(f"Number of citations: {len(references)}\n")
for ref in references:
    print(f"ID: {ref['id']}\nTitle: {ref['title']}\nAuthor: {ref['author']}\nYear: {ref['year']}\nDOI: {ref['doi']}\nIn-text citation: {ref['in_text_citation']}\nSentences: {ref['sentence']}\n\n")

for ref in references:
    #join all sentences in a single string
    ref['sentence'] = " ".join(ref['sentence'])

refefences, report = check.fill(references)
results = calculate.fill(references, report)

#save references in a json file
with open(f"Results/{pdf}_references.json", "w", encoding="utf-8") as f:
    json.dump(references, f, indent=4)

#convert results dict to DataFrame trasposed
final_df = pd.DataFrame(results).T
final_df.to_csv(f"Results/{pdf}.csv")


statistics = {}

# Calcula estatísticas para cada coluna relevante
columns_to_analyze = ['faithfulness', 'precision', 'recall', 'semantic_similarity', 'pdf-faithfulness', 'pdf-precision', 'pdf-recall', 'pdf-semantic_similarity']
statistics = {col: calculate_statistics(final_df, col) for col in columns_to_analyze}
# for col in columns_to_analyze:
#     try:
#         statistics[col]["non_none_percentage"] = statistics[col]["non_none_percentage"]
#     except:
#         statistics[col]["non_none_percentage"] = None



# Salva as estatísticas em um arquivo JSON
with open(f"Results/statistics_{pdf}.json", "w", encoding="utf-8") as f:
    json.dump(statistics, f, indent=4)



print("End of program")

print('fim do programa')