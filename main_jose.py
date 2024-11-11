from src.apis import check
from src.sentences.extract import *
from src.evaluation.metrics import *
import pandas as pd
import json
import src.sentences.get_dataset as dataset_sentences


filename = "dataset/combined_papers.json"
# filename = "dataset/accepted_papers.json"

# read data in dataset\combined_papers.json
with open(filename, "r", encoding="utf-8") as f:
    papers = json.load(f)

# extract the first paper
paper = papers[1]

# Texto completo do paper que vamos analisar
text = paper["metadata"]["sections"]
# dicionário de referências do paper
references = paper["metadata"]["references"]

references = dataset_sentences.extract(
    paper["metadata"]["referenceMentions"], references)

# extrair as sentenças que contêm a citação
# for refs in references:
#    refs["sentences"] = extract_sentences_with_citation(
#        text, refs['shortCiteRegEx'])

references, report = check.fill(references)

# Save the references to a file
# with open("references.json", "w", encoding="utf-8") as f:
#    json.dump(references, f, ensure_ascii=False, indent=4)

# Load the references from a file
# with open("references.json", "r", encoding="utf-8") as f:
#    references = json.load(f)


# convert report dict to DataFrame
report_df = pd.DataFrame(report)

# save the report to a csv file - transposed
report_df.T.to_csv("report.csv")

results = calculate_metrics(references)

# save the results to a csv file
results.to_csv("metrics.csv")

print("end of program")
